#!/usr/bin/env python3
"""Bounded DESI DR1 galaxy redshift adapter using NASA/Gaia fail-closed pattern.

Fetch NOIRLab public TAP zpix rows with validated measurement/provenance,
without claiming redshift is a measured metric distance. Does not ingest the
complete 23 million-plus DR1 zpix table. Missing fields stay null.
"""
import argparse,csv,datetime as dt,hashlib,io,json,math,os,pathlib,tempfile
import urllib.parse,urllib.request
ROOT=pathlib.Path(__file__).resolve().parents[1]
DATA=ROOT/"data/desi_dr1-sample.json"
STATUS=ROOT/"data/desi_dr1-sync-status.json"
ENDPOINT="https://datalab.noirlab.edu/tap/sync"
HEALPIX=None
QUERY=("SELECT TOP 200 targetid,survey,program,mean_fiber_ra,mean_fiber_dec,"
       "z,zerr,zwarn,spectype,healpix FROM desi_dr1.zpix "
       "WHERE zwarn=0 AND spectype='GALAXY' AND z>0")
URL=ENDPOINT+"?"+urllib.parse.urlencode({"REQUEST":"doQuery","LANG":"ADQL","FORMAT":"csv","QUERY":QUERY})
FIELDS=("targetid","survey","program","mean_fiber_ra","mean_fiber_dec","z","zerr","zwarn","spectype","healpix")
def utc():
    return dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds").replace("+00:00","Z")
def as_float(v):
    if v is None or str(v).strip().lower() in ("","nan","null","--"):return None
    n=float(v)
    if not math.isfinite(n):raise ValueError("nonfinite DESI measurement")
    return n
def normalize(raw,minimum=10):
    reader=csv.DictReader(io.StringIO(raw.lstrip("\ufeff")))
    if set(FIELDS)-set(reader.fieldnames or ()):raise ValueError("DESI zpix response missing required columns")
    records=[];seen=set()
    for item in reader:
        if len(records)>=200:raise ValueError("DESI TAP exceeded sample cap")
        targetid=str(item["targetid"]).strip()
        survey=(item["survey"] or "").strip()
        program=(item["program"] or "").strip()
        if not targetid.isdecimal() or not survey or not program:
            raise ValueError("invalid DESI target key")
        key=(targetid,survey,program)
        if key in seen:raise ValueError("duplicate DESI zpix target-survey-program key")
        seen.add(key)
        ra,dec=as_float(item["mean_fiber_ra"]),as_float(item["mean_fiber_dec"])
        z,zerr=as_float(item["z"]),as_float(item["zerr"])
        flag=(item["zwarn"] or "").strip()
        pixel=(item["healpix"] or "").strip()
        if (ra is None or not 0<=ra<360 or dec is None or not -90<=dec<=90 or
           z is None or z<=0 or zerr is None or zerr<0 or flag!="0" or
           (item["spectype"] or "").strip()!="GALAXY" or not pixel.isdecimal()):
            raise ValueError("DESI sky/redshift/quality gates failed")
        records.append({"targetid":targetid,"survey":survey,"program":program,
           "ra_deg":ra,"dec_deg":dec,"redshift":z,"redshift_error":zerr,
           "zwarn":0,"spectype":"GALAXY","healpix_nside64_nested":int(pixel)})
    if not minimum<=len(records)<=200:raise ValueError("DESI sample unexpectedly empty/truncated")
    records.sort(key=lambda r:(r["targetid"],r["survey"],r["program"]))
    return {"schema":"cosmos-explorer-desi-dr1-sample-v1",
       "provider":"DESI DR1 through NOIRLab Astro Data Lab public TAP",
       "source_table":"desi_dr1.zpix","source_release":"DR1 / iron",
       "query":QUERY,"query_url":URL,
       "reference":"https://data.desi.lbl.gov/doc/access/database/",
       "license":"DESI DR1 CC BY 4.0; cite official DESI Collaboration and acknowledgments",
       "sample_scope":"Up to 200 quality-filtered zpix galaxy entries from public TAP; not the full DR1 or statistically representative survey.",
       "scientific_caveat":"Measured spectroscopic redshifts, not measured Euclidean distances; no cosmological distance inversion or physical motion inferred here.",
       "units":{"sky":"ICRS degrees (mean fiber position)","z":"dimensionless spectroscopic redshift"},
       "counts":{"sample_entries":len(records)},"records":records}
def sha(obj):
    return hashlib.sha256(json.dumps(obj,sort_keys=True,ensure_ascii=False,separators=(",",":")).encode()).hexdigest()
def atomic(path,obj):
    path.parent.mkdir(parents=True,exist_ok=True)
    with tempfile.NamedTemporaryFile(mode="w",encoding="utf-8",dir=path.parent,delete=False) as f:
        json.dump(obj,f,ensure_ascii=False,separators=(",",":"));f.write("\n");name=f.name
    os.replace(name,path)
def sync(raw,out=DATA,status=STATUS):
    normalized=normalize(raw)
    digest=sha(normalized)
    prior=json.loads(status.read_text(encoding="utf-8")) if status.exists() else {}
    same=out.exists() and sha(json.loads(out.read_text(encoding="utf-8")))==digest
    when=utc()
    if not same:atomic(out,normalized)
    audit={"schema":"cosmos-explorer-desi-sync-status-v1","source_id":"desi_dr1",
      "last_checked_utc":when,"last_imported_utc":prior.get("last_imported_utc") if same else when,
      "publisher_release_utc":None,"source_release":"DESI DR1 iron",
      "check_status":"unchanged" if same else "updated","sample_only":True,
      "counts":normalized["counts"],"official_query_url":URL,
      "source_csv_sha256":hashlib.sha256(raw.encode("utf-8")).hexdigest(),
      "normalized_sha256":digest}
    atomic(status,audit);return audit
def fetch():
    req=urllib.request.Request(URL,headers={
        "Accept":"text/csv","User-Agent":"CosmosExplorer/0.7 (bounded public astronomical research)"})
    with urllib.request.urlopen(req,timeout=120) as res:
        if res.status!=200:raise ValueError("NOIRLab TAP returned HTTP "+str(res.status))
        payload=res.read(600001)
        if len(payload)>600000:raise ValueError("NOIRLab TAP response exceeded fixed bound")
    raw=payload.decode("utf-8-sig")
    if raw.lstrip().startswith("<") or raw.startswith("Error"):
        raise ValueError("NOIRLab TAP returned structured error, not CSV: "+raw[:350].replace("\n"," "))
    return raw
def test():
    def row(i):
        return ",".join([str(1000+i),"main","DARK","155.32","24.12","0.541","0.0004","0","GALAXY","500"])
    raw=",".join(FIELDS)+"\n"+"\n".join(row(i) for i in range(20))+"\n"
    a=normalize(raw);assert a["counts"]["sample_entries"]==20
    with tempfile.TemporaryDirectory() as folder:
        p=pathlib.Path(folder)
        x=sync(raw,p/"data.json",p/"status.json")
        y=sync(raw,p/"data.json",p/"status.json")
        assert x["check_status"]=="updated" and y["check_status"]=="unchanged"
        assert y["last_imported_utc"]==x["last_imported_utc"]
    for bad in [raw+row(1)+"\n",raw.replace("0.541","-1.0",1),raw.replace("GALAXY","STAR",1)]:
        try:normalize(bad);raise AssertionError("invalid sample passed")
        except ValueError:pass
    print("DESI offline importer self-tests passed")
def main():
    p=argparse.ArgumentParser();p.add_argument("--self-test",action="store_true");p.add_argument("--input")
    args=p.parse_args()
    if args.self_test:return test()
    raw=pathlib.Path(args.input).read_text(encoding="utf-8") if args.input else fetch()
    print(json.dumps(sync(raw),indent=2))
if __name__=="__main__":main()
