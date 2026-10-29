#!/usr/bin/env python3
"""Bounded VizieR TAP extraction: GALAH DR4 derived table, then APOGEE DR17.

The GALAH VizieR source is a *detrended derivative* of DR4, not the original
Data Central allStar release. APOGEE III/286 represents DR17 allStar.
Never confuse these source views with full source catalog coverage.
"""
import argparse,csv,datetime as dt,hashlib,io,json,math,os,pathlib,tempfile
import urllib.parse,urllib.request,xml.etree.ElementTree as ET
ROOT=pathlib.Path(__file__).resolve().parents[1]
BASE="https://tapvizier.cds.unistra.fr/TAPVizieR/tap/sync"
TABLES={
 "galah_dr4":{"table":'"J/A+A/703/A104/catalog"',
      "columns":("recno","GALAH","GaiaDR3","RAJ2000","DEJ2000"),
      "identifier":"GALAH","release_label":"GALAH DR4 detrended catalogue (derived, Kos et al. 2025)",
      "reference":"https://vizier.cds.unistra.fr/viz-bin/VizieR?-source=J/A+A/703/A104"},
 "apogee_dr17":{"table":'"III/286/catalog"',
      "columns":("recno","APOGEE","RAJ2000","DEJ2000"),
      "identifier":"APOGEE","release_label":"SDSS APOGEE-2 DR17 allStar (VizieR III/286)",
      "reference":"https://vizier.cds.unistra.fr/viz-bin/VizieR?-source=III/286"}
}
def now():
    return dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds").replace("+00:00","Z")
def query(source):
    config=TABLES[source]
    return "SELECT TOP 200 "+",".join(config["columns"])+" FROM "+config["table"]
def source_url(source):
    return BASE+"?"+urllib.parse.urlencode({"REQUEST":"doQuery","LANG":"ADQL","FORMAT":"csv","QUERY":query(source)})
def from_votable(raw):
    root=ET.fromstring(raw)
    for s in root.iter():
        if s.tag.split("}")[-1]=="INFO" and s.get("name")=="QUERY_STATUS" and s.get("value") not in ("OK","OVERFLOW"):
            raise ValueError("VizieR rejected query: "+str(s.get("value"))+" "+str(s.text or "")[:120])
    table=next((t for t in root.iter() if t.tag.split("}")[-1]=="TABLE"),None)
    if table is None:raise ValueError("VizieR did not supply a TABLE")
    fields=[f.get("name") for f in table if f.tag.split("}")[-1]=="FIELD"]
    if not fields:raise ValueError("No VizieR VOTable fields")
    buffer=io.StringIO();writer=csv.writer(buffer);writer.writerow(fields)
    for tr in table.iter():
        if tr.tag.split("}")[-1]!="TR":continue
        cells=["".join(v.itertext()).strip() for v in tr if v.tag.split("}")[-1]=="TD"]
        if len(cells)!=len(fields):raise ValueError("VizieR VOTable field count mismatch")
        writer.writerow(cells)
    return buffer.getvalue()
def normalize(source,raw,minimum=10):
    cfg=TABLES[source]
    if raw.lstrip().startswith("<"):raw=from_votable(raw)
    rd=csv.DictReader(io.StringIO(raw.lstrip("\ufeff")))
    if set(cfg["columns"])-set(rd.fieldnames or []):
        raise ValueError("Missing published VizieR source columns: "+str(sorted(set(cfg["columns"])-set(rd.fieldnames or []))))
    result=[];seen=set()
    for row in rd:
        if len(result)>=200:raise ValueError("Sample exceeds configured cap")
        recno=str(row["recno"]).strip()
        obj=(row.get(cfg["identifier"]) or "").strip()
        if not recno.isdecimal() or recno in seen:raise ValueError("Bad/duplicate source record number")
        seen.add(recno)
        ra=float(row["RAJ2000"]);dec=float(row["DEJ2000"])
        if not math.isfinite(ra) or not math.isfinite(dec) or not 0<=ra<360 or not -90<=dec<=90:
            raise ValueError("Invalid equatorial coordinates")
        info={"source_row_id":recno,"catalog_object_id":obj or None,"ra_deg":ra,"dec_deg":dec}
        if source=="galah_dr4":
            gaia=(row.get("GaiaDR3") or "").strip()
            if gaia and not gaia.isdecimal():raise ValueError("Invalid Gaia cross-reference")
            info["gaia_dr3_source_id"]=gaia or None
        result.append(info)
    if not minimum<=len(result)<=200:raise ValueError("VizieR result missing or truncated")
    result.sort(key=lambda x:int(x["source_row_id"]))
    return {"schema":"cosmos-explorer-vizier-survey-sample-v1","source_id":source,
       "source_release":cfg["release_label"],"upstream_vizier_table":cfg["table"],
       "source_reference":cfg["reference"],"query_url":source_url(source),
       "units":{"ra_dec":"J2000 equatorial degrees"},
       "scope":"Up to 200 published sample rows. Not all catalog stars. No coordinates-to-distance inference.",
       "license_notice":"Preserve original survey and derived-source citation; check upstream terms before bulk redistribution.",
       "counts":{"sample_rows":len(result)},"records":result}
def hash_object(doc):
    return hashlib.sha256(json.dumps(doc,sort_keys=True,separators=(",",":"),ensure_ascii=False).encode("utf-8")).hexdigest()
def write(path,obj):
    path.parent.mkdir(parents=True,exist_ok=True)
    with tempfile.NamedTemporaryFile("w",encoding="utf-8",dir=path.parent,delete=False) as f:
        json.dump(obj,f,ensure_ascii=False,separators=(",",":"));f.write("\n");temp=f.name
    os.replace(temp,path)
def sync(source,raw,data=None,status=None):
    doc=normalize(source,raw)
    data=pathlib.Path(data) if data else ROOT/("data/"+source+"-sample.json")
    status=pathlib.Path(status) if status else ROOT/("data/"+source+"-sync-status.json")
    new_hash=hash_object(doc)
    unchanged=data.exists() and hash_object(json.loads(data.read_text(encoding="utf-8")))==new_hash
    previous=json.loads(status.read_text(encoding="utf-8")) if status.exists() else {}
    timestamp=now()
    if not unchanged:write(data,doc)
    audit={"schema":"cosmos-explorer-vizier-survey-status-v1","source_id":source,
       "source_release":TABLES[source]["release_label"],"check_status":"unchanged" if unchanged else "updated",
       "last_checked_utc":timestamp,"last_imported_utc":previous.get("last_imported_utc") if unchanged else timestamp,
       "publisher_release_utc":None,"sample_only":True,"counts":doc["counts"],
       "source_sha256":hashlib.sha256(raw.encode("utf-8")).hexdigest(),
       "normalized_sha256":new_hash,"official_query_url":source_url(source)}
    write(status,audit);return audit
def fetch(source):
    req=urllib.request.Request(source_url(source),headers={
      "User-Agent":"CosmosExplorer/0.8 (bounded VizieR research sample)","Accept":"text/csv,application/xml"})
    with urllib.request.urlopen(req,timeout=100) as res:
        if res.status!=200:raise ValueError("VizieR TAP HTTP "+str(res.status))
        data=res.read(1300001)
        if len(data)>1300000:raise ValueError("Oversized VizieR response")
    return data.decode("utf-8-sig")
def self_test():
    for name,cfg in TABLES.items():
        row=dict(zip(cfg["columns"],[""]*len(cfg["columns"])))
        lines=[",".join(cfg["columns"])]
        for i in range(1,21):
            row.update({"recno":str(i),cfg["identifier"]:str(100+i),"RAJ2000":"217.4","DEJ2000":"-62.7"})
            if name=="galah_dr4":row["GaiaDR3"]=str(800000+i)
            lines.append(",".join(row[x] for x in cfg["columns"]))
        raw="\n".join(lines)+"\n"
        normalized=normalize(name,raw)
        assert normalized["counts"]["sample_rows"]==20
        with tempfile.TemporaryDirectory() as d:
            p=pathlib.Path(d)
            a=sync(name,raw,p/"data.json",p/"status.json")
            b=sync(name,raw,p/"data.json",p/"status.json")
            assert a["check_status"]=="updated" and b["check_status"]=="unchanged"
        try:
            normalize(name,raw+lines[1]+"\n")
            raise AssertionError("duplicate not detected")
        except ValueError:pass
    print("VizieR GALAH and APOGEE adapters passed offline invariants")
def main():
    p=argparse.ArgumentParser();p.add_argument("--source",choices=TABLES);p.add_argument("--self-test",action="store_true")
    a=p.parse_args()
    if a.self_test:return self_test()
    if not a.source:p.error("--source required")
    print(json.dumps(sync(a.source,fetch(a.source)),indent=2))
if __name__=="__main__":main()
