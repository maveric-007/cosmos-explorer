#!/usr/bin/env python3
"""Validated, bounded IRSA TAP imports in descending official source-count order.

NASA/Gaia pattern: fixed queries, schema and unit checks, source hashes,
atomic replace, distinct checked/imported timestamps, and never fabricate
distance or source classification. These are small spatial samples, not
complete AllWISE or 2MASS. Full archives require external partitioned storage.
"""
import argparse,csv,datetime as dt,hashlib,io,json,math,os,pathlib,tempfile
import urllib.parse,urllib.request

ROOT=pathlib.Path(__file__).resolve().parents[1]
ENDPOINT="https://irsa.ipac.caltech.edu/TAP/sync"
CENTER_RA,CENTER_DEC,RADIUS_DEG=66.76957,26.10453,0.12
MAX_ROWS=500
CATALOGS={
 "allwise":{"table":"allwise_p3as_psd",
   "columns":("designation","ra","dec","w1mpro","w1sigmpro","w2mpro","w2sigmpro","ph_qual"),
   "photometry":("w1mpro","w2mpro"),"errors":("w1sigmpro","w2sigmpro"),
   "bands":"W1 / W2 (Vega magnitudes)","published_entries":747634026,
   "reference":"https://irsa.ipac.caltech.edu/data/WISE/docs/release/AllWISE/expsup/sec1_3.html"},
 "twomass":{"table":"fp_psc",
   "columns":("designation","ra","dec","j_m","h_m","k_m","ph_qual"),
   "photometry":("j_m","h_m","k_m"),"errors":(),
   "bands":"J / H / Ks (Vega magnitudes)","published_entries":470992970,
   "reference":"https://irsa.ipac.caltech.edu/data/2MASS/docs/releases/allsky/doc/sec2_2.html"}
}
def now():
    return dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds").replace("+00:00","Z")
def numeric(x):
    if x is None or str(x).strip().lower() in ("","null","nan","--"):return None
    n=float(x)
    if not math.isfinite(n):raise ValueError("non-finite numeric value")
    return n
def query(source):
    c=CATALOGS[source]
    # Official IRSA TAP docs support small-area geometry, TOP and selected fields.
    return ("SELECT TOP "+str(MAX_ROWS)+" "+",".join(c["columns"])+" FROM "+c["table"]+
      " WHERE CONTAINS(POINT('ICRS',ra,dec),CIRCLE('ICRS',"+
      str(CENTER_RA)+","+str(CENTER_DEC)+","+str(RADIUS_DEG)+"))=1 ORDER BY designation")
def url(source):
    return ENDPOINT+"?"+urllib.parse.urlencode({"QUERY":query(source),"FORMAT":"csv"})
def separation(ra,dec):
    a,b,c,d=map(math.radians,(ra,dec,CENTER_RA,CENTER_DEC))
    cosine=math.sin(b)*math.sin(d)+math.cos(b)*math.cos(d)*math.cos(a-c)
    return math.degrees(math.acos(max(-1.0,min(1.0,cosine))))
def normalize(source,raw,minimum=10):
    p=CATALOGS[source];reader=csv.DictReader(io.StringIO(raw.lstrip("\ufeff")))
    if set(p["columns"])-set(reader.fieldnames or ()):raise ValueError("TAP missing expected columns")
    rows=[];seen=set()
    for record in reader:
        if len(rows)>=MAX_ROWS:raise ValueError("too many sample rows")
        designation=(record.get("designation") or "").strip()
        if not designation or designation in seen:raise ValueError("duplicate or absent source designation")
        seen.add(designation)
        ra,dec=numeric(record["ra"]),numeric(record["dec"])
        if ra is None or dec is None or not 0<=ra<360 or not -90<=dec<=90:raise ValueError("invalid coordinates")
        if separation(ra,dec)>RADIUS_DEG+0.0002:raise ValueError("source outside fixed sample cone")
        mags={x:numeric(record.get(x)) for x in p["photometry"]}
        errors={x:numeric(record.get(x)) for x in p["errors"]}
        if any(v is not None and v<0 for v in errors.values()):raise ValueError("negative photometry uncertainty")
        rows.append({"designation":designation,"ra_deg":ra,"dec_deg":dec,
                     "magnitudes":mags,"magnitude_uncertainties":errors,
                     "photometric_quality":(record.get("ph_qual") or "").strip() or None})
    if not minimum<=len(rows)<=MAX_ROWS:raise ValueError("unexpected sample row count: "+str(len(rows)))
    rows.sort(key=lambda x:x["designation"])
    return {"schema":"cosmos-explorer-irsa-sample-v1",
       "provider":"NASA/IPAC IRSA","source_id":source,"table":p["table"],
       "official_query_url":url(source),"source_reference":p["reference"],
       "published_full_catalog_entries":p["published_entries"],
       "selection":{"ra_center_deg":CENTER_RA,"dec_center_deg":CENTER_DEC,
                    "cone_radius_deg":RADIUS_DEG,"max_records":MAX_ROWS,
                    "not_whole_catalog":True},
       "units":{"ra_dec":"ICRS J2000 degrees","magnitudes":p["bands"]},
       "limitations":"Small region and TOP limit; catalog detections may include stars/galaxies/other objects. No source crossmatch, distances, masses or 6D velocities supplied. Null means unknown.",
       "counts":{"sample_records":len(rows)},
       "records":rows}
def digest(obj):
    return hashlib.sha256(json.dumps(obj,sort_keys=True,separators=(",",":"),ensure_ascii=False).encode()).hexdigest()
def atomic(path,obj):
    path.parent.mkdir(parents=True,exist_ok=True)
    with tempfile.NamedTemporaryFile("w",dir=path.parent,encoding="utf-8",delete=False) as f:
        json.dump(obj,f,ensure_ascii=False,separators=(",",":"));f.write("\n");tmp=f.name
    os.replace(tmp,path)
def paths(source):
    return ROOT/("data/"+source+"-sample.json"),ROOT/("data/"+source+"-sync-status.json")
def sync(source,raw,output=None,status=None):
    if source not in CATALOGS:raise ValueError("unknown catalog")
    output_default,status_default=paths(source)
    output=pathlib.Path(output) if output is not None else output_default
    status=pathlib.Path(status) if status is not None else status_default
    normalized=normalize(source,raw)
    fingerprint=digest(normalized)
    old_record=json.loads(status.read_text(encoding="utf-8")) if status.exists() else {}
    unchanged=output.exists() and digest(json.loads(output.read_text(encoding="utf-8")))==fingerprint
    checked=now()
    if not unchanged:atomic(output,normalized)
    audit={"schema":"cosmos-explorer-irsa-sync-status-v1","source_id":source,
           "source_table":CATALOGS[source]["table"],"official_query_url":url(source),
           "last_checked_utc":checked,"last_imported_utc":old_record.get("last_imported_utc") if unchanged else checked,
           "publisher_release_utc":None,"publisher_release_status":"Not asserted from TAP response; release metadata must be verified separately",
           "check_status":"unchanged" if unchanged else "updated",
           "source_csv_sha256":hashlib.sha256(raw.encode()).hexdigest(),
           "normalized_sha256":fingerprint,"counts":normalized["counts"],
           "sample_only":True}
    atomic(status,audit)
    return audit
def fetch(source):
    req=urllib.request.Request(url(source),headers={
       "User-Agent":"CosmosExplorer/0.6 (public astronomy research; bounded API query)",
       "Accept":"text/csv"})
    with urllib.request.urlopen(req,timeout=140) as response:
        if response.status!=200:raise ValueError("IRSA TAP HTTP "+str(response.status))
        raw=response.read(900001)
        if len(raw)>900000:raise ValueError("unexpectedly large catalog response")
        raw=raw.decode("utf-8")
    if raw.lstrip().startswith("<"):raise ValueError("IRSA returned XML/VOTable error, expected CSV")
    return raw
def self_test():
    for source,p in CATALOGS.items():
        lines=[",".join(p["columns"])]
        for i in range(1,12):
            d={c:"" for c in p["columns"]}
            d.update({"designation":source.upper()+str(i),"ra":str(CENTER_RA+.00003*i),
                      "dec":str(CENTER_DEC+.00001*i),"ph_qual":"AA"})
            for c in p["photometry"]:d[c]="12.1"
            for c in p["errors"]:d[c]="0.05"
            lines.append(",".join(d[c] for c in p["columns"]))
        raw="\n".join(lines)+"\n"
        result=normalize(source,raw)
        assert result["counts"]["sample_records"]==11
        with tempfile.TemporaryDirectory() as folder:
            a,b=pathlib.Path(folder)/"sample.json",pathlib.Path(folder)/"status.json"
            one=sync(source,raw,a,b);two=sync(source,raw,a,b)
            assert one["check_status"]=="updated" and two["check_status"]=="unchanged"
            assert one["last_imported_utc"]==two["last_imported_utc"]
        try:
            normalize(source,raw+lines[1]+"\n")
            raise AssertionError("duplicate not detected")
        except ValueError:pass
    print("IRSA AllWISE and 2MASS self-tests passed (query schema, coordinates, duplicates, hashes, safe no-op).")
def main():
    p=argparse.ArgumentParser()
    p.add_argument("--source",choices=list(CATALOGS))
    p.add_argument("--self-test",action="store_true")
    p.add_argument("--input",help="Local CSV fixture for reproducibility")
    args=p.parse_args()
    if args.self_test:return self_test()
    if not args.source:p.error("--source required except for --self-test")
    raw=pathlib.Path(args.input).read_text(encoding="utf-8") if args.input else fetch(args.source)
    record=sync(args.source,raw)
    print(json.dumps({"source":args.source,"status":record["check_status"],
       "count":record["counts"]["sample_records"],"checked":record["last_checked_utc"],
       "imported":record["last_imported_utc"]},indent=2))
if __name__=="__main__":main()
