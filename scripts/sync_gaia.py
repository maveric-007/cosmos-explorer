#!/usr/bin/env python3
"""Bounded Gaia DR3 TAP importer; NASA-style checks, hashes and atomic writes.
This is a quality-filtered sample, NOT all Gaia stars or a 6D dynamical model.
"""
import argparse,csv,datetime as dt,hashlib,io,json,math,os,pathlib,tempfile,urllib.parse,urllib.request
ROOT=pathlib.Path(__file__).resolve().parents[1]
OUT=ROOT/"data/gaia-sample.json"
STATUS=ROOT/"data/gaia-sync-status.json"
COLS="source_id random_index ref_epoch ra dec parallax parallax_error parallax_over_error pmra pmdec radial_velocity phot_g_mean_mag ruwe".split()
QUERY=("SELECT TOP 1000 "+",".join(COLS)+" FROM gaiadr3.gaia_source "
       "WHERE random_index BETWEEN 0 AND 300000 AND parallax > 0 "
       "AND parallax_over_error >= 10 AND ruwe > 0 AND ruwe < 1.4 "
       "AND phot_g_mean_mag < 17 ORDER BY random_index")
URL="https://gea.esac.esa.int/tap-server/tap/sync?"+urllib.parse.urlencode(
 {"REQUEST":"doQuery","LANG":"ADQL","FORMAT":"csv","QUERY":QUERY})
def num(v):
    if v is None or str(v).strip().lower() in ("","null","nan"):return None
    n=float(v)
    if not math.isfinite(n):raise ValueError("Non-finite numeric field")
    return n
def normalize(raw,minimum=25):
    reader=csv.DictReader(io.StringIO(raw.lstrip("\ufeff")))
    if set(COLS)-set(reader.fieldnames or ()):raise ValueError("Missing Gaia source columns")
    stars=[];seen=set()
    for row in reader:
        if len(stars)==1000:raise ValueError("Result exceeds the 1000-row sample cap")
        sid=str(row["source_id"]).strip()
        if not sid.isdecimal() or sid in seen:raise ValueError("Missing/duplicate source_id")
        seen.add(sid)
        a,d,p=num(row["ra"]),num(row["dec"]),num(row["parallax"])
        pe,snr,rw,mag=num(row["parallax_error"]),num(row["parallax_over_error"]),num(row["ruwe"]),num(row["phot_g_mean_mag"])
        ri=int(row["random_index"])
        if not (a is not None and 0<=a<360 and d is not None and -90<=d<=90 and
                p is not None and p>0 and pe is not None and pe>0 and
                snr is not None and snr>=10 and rw is not None and 0<rw<1.4 and
                mag is not None and mag<17 and 0<=ri<=300000):raise ValueError("Gaia quality gate failed")
        stars.append({"source_id":sid,"random_index":ri,"epoch_year":num(row["ref_epoch"]),
          "ra_deg":a,"dec_deg":d,"parallax_mas":p,"parallax_error_mas":pe,
          "parallax_snr":snr,"distance_pc_approx":round(1000/p,6),
          "pmra_mas_yr":num(row["pmra"]),"pmdec_mas_yr":num(row["pmdec"]),
          "radial_velocity_km_s":num(row["radial_velocity"]),
          "phot_g_mean_mag":mag,"ruwe":rw})
    if not minimum<=len(stars)<=1000:raise ValueError("Gaia result unexpectedly empty or truncated")
    if any(s["epoch_year"] is None for s in stars):raise ValueError("Missing astrometric reference epoch")
    stars.sort(key=lambda s:(s["random_index"],s["source_id"]))
    return {"schema":"cosmos-explorer-gaia-sample-v1","source":"ESA Gaia DR3 gaiadr3.gaia_source",
      "query":QUERY,"query_url":URL,"reference_frame":"ICRS",
      "scope":"Fixed small random_index window, high-quality astrometric subset; NOT all stars or a representative volume census.",
      "distance_caveat":"1000/parallax mas is a high-SNR approximate distance, NOT a calibrated posterior; missing RV remains null.",
      "count":len(stars),"stars":stars}
def sha(obj):
    return hashlib.sha256(json.dumps(obj,sort_keys=True,separators=(",",":")).encode()).hexdigest()
def atomic(path,obj):
    path.parent.mkdir(parents=True,exist_ok=True)
    with tempfile.NamedTemporaryFile(mode="w",encoding="utf-8",dir=path.parent,delete=False) as t:
        json.dump(obj,t,separators=(",",":"));t.write("\n");name=t.name
    os.replace(name,path)
def sync(raw,out=OUT,status=STATUS):
    obj=normalize(raw);digest=sha(obj);old=json.loads(status.read_text()) if status.exists() else {}
    same=out.exists() and sha(json.loads(out.read_text()))==digest
    now=dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds").replace("+00:00","Z")
    if not same:atomic(out,obj)
    record={"schema":"cosmos-explorer-gaia-sync-status-v1","source_release_id":"Gaia DR3",
      "last_checked_utc":now,"last_imported_utc":old.get("last_imported_utc") if same else now,
      "publisher_release_utc":None,"check_status":"unchanged" if same else "updated",
      "count":obj["count"],"query_url":URL,"source_csv_sha256":hashlib.sha256(raw.encode()).hexdigest(),
      "normalized_sha256":digest,"sample_only":True}
    atomic(status,record);return record
def test():
    def row(i,rv=""):
        vals=dict(zip(COLS,["123","1","2016.0","20","-10","10",".2","50","1","2",rv,"12","1.1"]))
        vals["source_id"]=str(i);vals["random_index"]=str(i)
        return ",".join(vals[c] for c in COLS)
    raw=",".join(COLS)+"\n"+row(1)+"\n"+row(2,"20")+"\n"
    assert normalize(raw,2)["stars"][0]["radial_velocity_km_s"] is None
    with tempfile.TemporaryDirectory() as d:
        o=pathlib.Path(d)/"sample.json";s=pathlib.Path(d)/"status.json"
        assert sync(raw,o,s)["check_status"]=="updated"
        assert sync(raw,o,s)["check_status"]=="unchanged"
    print("Gaia self-test passed")
def main():
    p=argparse.ArgumentParser();p.add_argument("--self-test",action="store_true");p.add_argument("--input");a=p.parse_args()
    if a.self_test:return test()
    if a.input:raw=pathlib.Path(a.input).read_text()
    else:
        request=urllib.request.Request(URL,headers={"User-Agent":"CosmosExplorer/0.5","Accept":"text/csv"})
        with urllib.request.urlopen(request,timeout=110) as r:
            data=r.read(2000001)
            if len(data)>2000000:raise ValueError("Oversized TAP response")
            raw=data.decode()
    if raw.lstrip().startswith("<"):raise ValueError("TAP returned error markup, not CSV")
    print(json.dumps(sync(raw),indent=2))
if __name__=="__main__":main()
