#!/usr/bin/env python3
"""Discover and import a bounded LAMOST DR12 v2.0 public TAP sample.

The primary aim is fail-closed source schema discovery, then a validated
catalog subset. It does NOT represent every LAMOST spectrum or claim to
measure masses/distances. Run independently of existing NASA/Gaia/IRSA jobs.
"""
import argparse,csv,datetime as dt,hashlib,io,json,math,os,pathlib,re,tempfile
import urllib.parse,urllib.request
ROOT=pathlib.Path(__file__).resolve().parents[1]
ENDPOINT="https://www.lamost.org/dr12/v2.0/voservice/tap/sync"
OUTPUT=ROOT/"data/lamost_dr12-sample.json"
STATUS=ROOT/"data/lamost_dr12-sync-status.json"
def stamp():
    return dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds").replace("+00:00","Z")
def tap(sql):
    url=ENDPOINT+"?"+urllib.parse.urlencode({"REQUEST":"doQuery","LANG":"ADQL","FORMAT":"csv","QUERY":sql})
    req=urllib.request.Request(url,headers={"User-Agent":"CosmosExplorer/0.6 (bounded public academic astronomy catalog import)","Accept":"text/csv"})
    with urllib.request.urlopen(req,timeout=100) as r:
        if r.status!=200:raise ValueError("LAMOST TAP HTTP "+str(r.status))
        data=r.read(650001)
        if len(data)>650000:raise ValueError("LAMOST response exceeds bounded sample size")
        txt=data.decode("utf-8-sig")
    if txt.lstrip().startswith("<"):raise ValueError("LAMOST TAP returned XML/error, not CSV: "+txt[:800].replace("\n"," "))
    return txt,url
def parse_csv(raw):
    reader=csv.DictReader(io.StringIO(raw))
    if not reader.fieldnames:raise ValueError("missing response header")
    return list(reader)
def pick_table(names):
    valid=[x for x in names if re.fullmatch(r"[A-Za-z_][A-Za-z_0-9.]*",x)]
    matches=[x for x in valid if x.split(".")[-1].lower()=="catalogue"]
    if not matches:matches=[x for x in valid if "catalogue" in x.lower() and "med_" not in x.lower()]
    if not matches:raise ValueError("LAMOST TAP_SCHEMA has no identifiable LRS catalogue table")
    return sorted(matches,key=lambda x:(len(x),x))[0]
def pick_columns(columns):
    lower={x.lower():x for x in columns}
    id_name=next((lower[x] for x in ("obsid","obs_id","designation","specid") if x in lower),None)
    ra=next((lower[x] for x in ("ra","ra_obs","ra_deg") if x in lower),None)
    dec=next((lower[x] for x in ("dec","dec_obs","dec_deg") if x in lower),None)
    if not (id_name and ra and dec):raise ValueError("catalogue lacks verified obsid/RA/Dec columns")
    return (id_name,ra,dec)
def normalize(rows,table,cols,query_url):
    id_name,ra_col,dec_col=cols
    out=[];seen=set()
    for r in rows:
        sid=str(r.get(id_name) or "").strip()
        if not sid or sid in seen:raise ValueError("missing or repeated LAMOST identifier")
        seen.add(sid)
        ra,dec=float(r[ra_col]),float(r[dec_col])
        if not math.isfinite(ra) or not math.isfinite(dec) or not 0<=ra<360 or not -90<=dec<=90:
            raise ValueError("invalid LAMOST sky coordinates")
        out.append({"source_observation_id":sid,"ra_deg":ra,"dec_deg":dec})
    if not 5<=len(out)<=200:raise ValueError("unexpected number of LAMOST sample rows")
    out.sort(key=lambda x:x["source_observation_id"])
    return {"schema":"cosmos-explorer-lamost-sample-v1",
     "provider":"LAMOST DR12 v2.0, China-VO public TAP","table":table,
     "query_url":query_url,"source_id_column":id_name,
     "units":{"ra_dec":"degrees (equatorial sky coordinates)"},
     "sample_only":True,"limits":"First at most 200 source observations; no stellar distances, masses, epoch-integrated tracks or 6D velocity inference. Multiple spectra of one star may exist; no cross-survey source matching here.",
     "counts":{"sample_observations":len(out)},"records":out}
def atomic(path,obj):
    path.parent.mkdir(parents=True,exist_ok=True)
    with tempfile.NamedTemporaryFile(mode="w",encoding="utf-8",dir=path.parent,delete=False) as f:
        json.dump(obj,f,separators=(",",":"));f.write("\n");tmp=f.name
    os.replace(tmp,path)
def sha(obj):
    return hashlib.sha256(json.dumps(obj,sort_keys=True,separators=(",",":")).encode("utf-8")).hexdigest()
def save(data,raw,output=OUTPUT,status=STATUS):
    h=sha(data)
    old=json.loads(status.read_text()) if status.exists() else {}
    same=output.exists() and sha(json.loads(output.read_text()))==h
    if not same:atomic(output,data)
    checked=stamp()
    audit={"schema":"cosmos-explorer-lamost-sync-status-v1","provider":"LAMOST DR12 v2.0",
      "last_checked_utc":checked,"last_imported_utc":old.get("last_imported_utc") if same else checked,
      "publisher_release_utc":None,"source_release":"DR12 v2.0 (public 2026)",
      "check_status":"unchanged" if same else "updated",
      "counts":data["counts"],"source_csv_sha256":hashlib.sha256(raw.encode()).hexdigest(),
      "normalized_sha256":h,"source_query_url":data["query_url"],"sample_only":True}
    atomic(status,audit)
    return audit
def sync():
    listing,_=tap("SELECT TOP 200 table_name FROM TAP_SCHEMA.tables")
    t=pick_table([r.get("table_name","") for r in parse_csv(listing)])
    def escaped(x):return x.replace("'","''")
    cols_raw,_=tap("SELECT TOP 400 column_name FROM TAP_SCHEMA.columns WHERE table_name='"+escaped(t)+"'")
    cols=pick_columns([r.get("column_name","") for r in parse_csv(cols_raw)])
    raw,url=tap("SELECT TOP 200 "+",".join(cols)+" FROM "+t)
    data=normalize(parse_csv(raw),t,cols,url)
    return save(data,raw)
def test():
    assert pick_table(["TAP_SCHEMA.tables","catalogue","med_catalogue"])=="catalogue"
    cols=pick_columns(["obsid","ra","dec","mag","z"])
    rows=[{"obsid":str(i),"ra":"66.7","dec":"26.1"} for i in range(1,12)]
    parsed=normalize(rows,"catalogue",cols,"fixture")
    assert parsed["counts"]["sample_observations"]==11
    with tempfile.TemporaryDirectory() as d:
        a=pathlib.Path(d)/"cat.json";b=pathlib.Path(d)/"status.json"
        r1=save(parsed,"fixture",a,b);r2=save(parsed,"fixture",a,b)
        assert r1["check_status"]=="updated" and r2["check_status"]=="unchanged"
    print("LAMOST schema discovery and importer self-test passed")
if __name__=="__main__":
    a=argparse.ArgumentParser();a.add_argument("--self-test",action="store_true")
    opts=a.parse_args()
    if opts.self_test:test()
    else:print(json.dumps(sync(),indent=2))
