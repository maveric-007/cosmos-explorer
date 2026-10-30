#!/usr/bin/env python3
"""Import a bounded, source-attributed NEOWISE small-body physical-property sample.

This is not a full IRSA/PDS census or a measurement of mass. A diameter may
be fitted or fixed; fit_code and provenance must remain available.
"""
import argparse
import csv
import datetime as dt
import hashlib
import io
import json
import math
import pathlib
import tempfile
import os
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET

ROOT = pathlib.Path(__file__).resolve().parents[1]
BASE = "https://irsa.ipac.caltech.edu/TAP/sync"
TABLE = "neowisesbpropv2"
FIELDS = ("asteroid_number", "prov_desig", "mean_jd", "fit_code",
          "diameter", "diameter_err", "v_albedo", "v_albedo_err", "pds_ref_code")
SCHEMA = "cosmos-explorer-neowise-properties-sample-v1"
STATUS_SCHEMA = "cosmos-explorer-neowise-sync-status-v1"
COUNT = 200
DATA = ROOT / "data/neowise-sample.json"
STATUS = ROOT / "data/neowise-sync-status.json"

def utc():
    return dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")

def source_url():
    query = "SELECT TOP 200 " + ",".join(FIELDS) + " FROM " + TABLE + " ORDER BY asteroid_number"
    return BASE + "?" + urllib.parse.urlencode({"QUERY":query,"LANG":"ADQL","FORMAT":"CSV"})

def num(value, lower=None, upper=None):
    if value is None or str(value).strip() in ("","null","NaN"):
        return None
    f = float(value)
    if not math.isfinite(f) or lower is not None and f < lower or upper is not None and f > upper:
        raise ValueError("Invalid physical/epoch quantity")
    return f

def from_votable(raw):
    root=ET.fromstring(raw)
    for node in root.iter():
        if node.tag.split("}")[-1] == "INFO" and node.attrib.get("name") == "QUERY_STATUS":
            if node.attrib.get("value") not in ("OK","OVERFLOW"):
                raise ValueError("IRSA TAP query rejected: " + repr("".join(node.itertext()).strip())[:550])
    table=next((n for n in root.iter() if n.tag.split("}")[-1]=="TABLE"),None)
    if table is None:
        raise ValueError("IRSA TAP VOTable has no data table: " + raw[:600])
    fields=[n.attrib.get("name") for n in table if n.tag.split("}")[-1]=="FIELD"]
    if not fields:raise ValueError("Missing IRSA VOTable column names")
    stream=io.StringIO();writer=csv.writer(stream);writer.writerow(fields)
    for tr in table.iter():
        if tr.tag.split("}")[-1]!="TR":continue
        vals=["".join(td.itertext()).strip() for td in tr if td.tag.split("}")[-1]=="TD"]
        if len(vals)!=len(fields):raise ValueError("IRSA VOTable inconsistent row width")
        writer.writerow(vals)
    return stream.getvalue()

def normalize(raw, min_count=20):
    if raw.lstrip().startswith("<?xml") or raw.lstrip().startswith("<VOTABLE"):
        raw=from_votable(raw)
    reader = csv.DictReader(io.StringIO(raw.lstrip("\ufeff")))
    if not reader.fieldnames:
        raise ValueError("Missing IRSA CSV headers")
    # IRSA returns catalog column aliases in the requested schema.
    columns = {key.strip().lower():key for key in reader.fieldnames}
    if set(FIELDS) - columns.keys():
        raise ValueError("Unexpected IRSA NEOWISE columns: " + repr(sorted(set(FIELDS)-columns.keys())) + "; returned header=" + repr(reader.fieldnames)[:450] + "; payload prefix=" + repr(raw[:180]))
    records = []
    ids = set()
    for row in reader:
        if len(records) >= COUNT:
            raise ValueError("NEOWISE response exceeds bounded cap")
        val = {k:(row[columns[k]] or "").strip() for k in FIELDS}
        number = val["asteroid_number"]
        designation = val["prov_desig"]
        if number and not number.isdecimal():
            raise ValueError("NEOWISE asteroid number not integral")
        if not number and not designation:
            raise ValueError("Missing minor-body ID")
        jd = num(val["mean_jd"], 2000000, 3000000)
        diameter = num(val["diameter"],0)
        diameter_err = num(val["diameter_err"],0)
        visible_albedo = num(val["v_albedo"],0,2)
        albedo_err = num(val["v_albedo_err"],0)
        if diameter is None and visible_albedo is None:
            raise ValueError("Physical-property sample contains neither diameter nor albedo")
        # Different observations/fits may exist for the same asteroid.
        uid = "|".join([number,designation,str(jd),val["pds_ref_code"],val["fit_code"]])
        if uid in ids:
            raise ValueError("Repeated NEOWISE property-fit identifier")
        ids.add(uid)
        records.append({
            "source_row_id":uid,"asteroid_number":number or None,
            "provisional_designation":designation or None,
            "mean_julian_day":jd,"diameter_km":diameter,
            "diameter_uncertainty_km":diameter_err,
            "visible_geometric_albedo":visible_albedo,
            "visible_albedo_uncertainty":albedo_err,
            "fit_code":val["fit_code"] or None,
            "diameter_was_fitted":"D" in val["fit_code"] if val["fit_code"] else None,
            "pds_publication_reference":val["pds_ref_code"] or None})
    if not min_count <= len(records) <= COUNT:
        raise ValueError("NEOWISE sample unexpectedly empty or truncated")
    return {
        "schema":SCHEMA,"source_id":"neowise","source_release":"NEOWISE diameter/albedo properties V2",
        "catalog_table":TABLE,"query_url":source_url(),"sample_only":True,
        "scope":"First 200 catalog entries; repeat asteroid fits may exist. Not full NEOWISE.",
        "caveat":"Diameter may be fitted or fixed. Neither diameter nor albedo is an asteroid mass.",
        "units":{"diameter":"km","mean_julian_day":"JD","albedo":"dimensionless"},
        "row_count":len(records),"records":records}

def fingerprint(obj):
    return hashlib.sha256(json.dumps(obj,sort_keys=True,separators=(",",":"),ensure_ascii=False).encode()).hexdigest()

def atomic(path,obj):
    path.parent.mkdir(parents=True,exist_ok=True)
    with tempfile.NamedTemporaryFile("w",encoding="utf-8",dir=path.parent,delete=False) as f:
        json.dump(obj,f,separators=(",",":"),ensure_ascii=False)
        f.write("\n")
        tmp=f.name
    os.replace(tmp,path)

def sync(raw,data=DATA,status=STATUS):
    doc=normalize(raw)
    data=pathlib.Path(data);status=pathlib.Path(status)
    prev=json.loads(status.read_text()) if status.exists() else {}
    h=fingerprint(doc)
    old=data.exists() and fingerprint(json.loads(data.read_text()))==h
    now=utc()
    if not old:atomic(data,doc)
    audit={"schema":STATUS_SCHEMA,"source_id":"neowise",
           "check_status":"unchanged" if old else "updated",
           "last_checked_utc":now,
           "last_imported_utc":prev.get("last_imported_utc") if old else now,
           "publisher_release_utc":None,
           "source_sha256":hashlib.sha256(raw.encode()).hexdigest(),
           "normalized_sha256":h,"count":doc["row_count"],
           "sample_only":True,"query_url":source_url()}
    atomic(status,audit)
    return audit

def self_test():
    with tempfile.TemporaryDirectory() as d:
        buf=io.StringIO();w=csv.writer(buf);w.writerow(FIELDS)
        for i in range(20):
            w.writerow([str(i+1),"",2459000+i,"DV--",1.1+i*.01,.1,.12,.01,"PaperXYZ"])
        raw=buf.getvalue()
        a=normalize(raw);assert a["row_count"]==20
        assert a["records"][0]["diameter_was_fitted"] is True
        p=pathlib.Path(d)
        assert sync(raw,p/"v.json",p/"s.json")["check_status"]=="updated"
        assert sync(raw,p/"v.json",p/"s.json")["check_status"]=="unchanged"
        try:
            normalize(raw+raw.splitlines()[1]+"\n")
        except ValueError:pass
        else:raise AssertionError("Duplicate physical fit not caught")
    # TAP returns VOTables by default even when CSV was requested.
    xml='<VOTABLE><RESOURCE><INFO name="QUERY_STATUS" value="ERROR">Unknown table</INFO></RESOURCE></VOTABLE>'
    try:normalize(xml)
    except ValueError as ex:assert "Unknown table" in str(ex)
    else:raise AssertionError("IRSA query error disguised as source records")
    print("NEOWISE schema, units, identifiers, completeness and idempotency OK")

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--self-test",action="store_true")
    args=parser.parse_args()
    if args.self_test:return self_test()
    req=urllib.request.Request(source_url(),headers={"User-Agent":"CosmosExplorer/1.0 (bounded research catalog)","Accept":"text/csv"})
    with urllib.request.urlopen(req,timeout=65) as result:
        raw=result.read(750001)
        if len(raw)>750000:raise ValueError("Unexpected oversized NEOWISE response")
    print(json.dumps(sync(raw.decode("utf-8-sig")),indent=2))

if __name__=="__main__":
    main()
