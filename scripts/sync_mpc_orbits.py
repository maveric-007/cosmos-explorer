#!/usr/bin/env python3
"""Bounded MPC orbital-solution snapshots using its published JSON GET-body API.

This is a four-target source verification, NOT the full MPC catalog. MPC orbit
solutions are not heliocentric measured positions at the viewer's current date.
"""
import argparse
import datetime as dt
import hashlib
import json
import pathlib
import tempfile
import os
import urllib.request

ROOT=pathlib.Path(__file__).resolve().parents[1]
URL="https://data.minorplanetcenter.net/api/get-orb"
TARGETS=("Ceres","Vesta","Bennu","Apophis")
SCHEMA="cosmos-explorer-mpc-orbits-sample-v1"
DATA=ROOT/"data/mpc-orbits-sample.json"
AUDIT=ROOT/"data/mpc-orbits-sync-status.json"

def utc():
    return dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds").replace("+00:00","Z")

def normalized(raw):
    if len(raw)!=len(TARGETS):raise ValueError("MPC response count does not match target list")
    out=[];seen=set()
    for designation, value in zip(TARGETS,raw):
        if not isinstance(value,list) or not value or not isinstance(value[0],dict):
            raise ValueError("Invalid MPC response for "+designation)
        entries=value[0].get("mpc_orb")
        if not isinstance(entries,list) or not entries or not isinstance(entries[0],dict):
            raise ValueError("MPC supplied no orbit for "+designation)
        orbit=entries[0]
        if "COM" not in orbit and "KEP" not in orbit and "CAR" not in orbit:
            raise ValueError("MPC orbit missing published orbital representation for "+designation)
        # Preserve raw publisher fields in the snapshot, do not invent frame,
        # epoch or convert different orbital-element conventions.
        key=designation.lower()
        if key in seen:raise ValueError("Repeated designation")
        seen.add(key)
        out.append({"designation_queried":designation,"source_row_id":key,
                    "mpc_orb":orbit})
    return {"schema":SCHEMA,"source_id":"mpc",
            "source":"Minor Planet Center Orbits API",
            "source_url":URL,
            "request":"HTTP GET with JSON body {'desig': '<one object>'} per call",
            "sample_only":True,"scope":"Four individually queried selected named objects; not all MPC orbits",
            "caveat":"MPC orbit representation and epoch must be interpreted from source fields; not current 3D positions.",
            "row_count":len(out),"records":out}

def write(path,obj):
    path.parent.mkdir(parents=True,exist_ok=True)
    with tempfile.NamedTemporaryFile("w",encoding="utf-8",dir=path.parent,delete=False) as tmp:
        json.dump(obj,tmp,separators=(",",":"),ensure_ascii=False);tmp.write("\n")
        x=tmp.name
    os.replace(x,path)

def fingerprint(obj):
    return hashlib.sha256(json.dumps(obj,sort_keys=True,separators=(",",":"),ensure_ascii=False).encode()).hexdigest()

def sync(raw,data=DATA,audit=AUDIT):
    doc=normalized(raw)
    data=pathlib.Path(data);audit=pathlib.Path(audit)
    previous=json.loads(audit.read_text()) if audit.exists() else {}
    hash=fingerprint(doc)
    unchanged=data.exists() and fingerprint(json.loads(data.read_text()))==hash
    now=utc()
    if not unchanged:write(data,doc)
    status={"schema":"cosmos-explorer-mpc-orbits-sync-status-v1","source_id":"mpc",
            "check_status":"unchanged" if unchanged else "updated",
            "last_checked_utc":now,"last_imported_utc":previous.get("last_imported_utc") if unchanged else now,
            "publisher_release_utc":None,"normalized_sha256":hash,
            "source_row_count":doc["row_count"],"sample_only":True,"source_url":URL}
    write(audit,status);return status

def fetch_one(designation):
    # API explicitly documents GET with JSON request body, unusual but supported.
    payload=json.dumps({"desig":designation}).encode()
    req=urllib.request.Request(URL,data=payload,method="GET",headers={
        "Content-Type":"application/json","Accept":"application/json",
        "User-Agent":"CosmosExplorer/1.0 (bounded MPC research samples)"})
    with urllib.request.urlopen(req,timeout=22) as response:
        raw=response.read(260001)
        if len(raw)>260000:raise ValueError("MPC response exceeds cap for "+designation)
    return json.loads(raw)

def self_test():
    fixture=[[{"mpc_orb":[{"COM":{"coefficient_names":["e"],"coefficient_values":[.1]}}]}] for _ in TARGETS]
    doc=normalized(fixture)
    assert doc["row_count"]==4 and doc["records"][2]["designation_queried"]=="Bennu"
    with tempfile.TemporaryDirectory() as d:
        p=pathlib.Path(d)
        assert sync(fixture,p/"m.json",p/"s.json")["check_status"]=="updated"
        assert sync(fixture,p/"m.json",p/"s.json")["check_status"]=="unchanged"
    try:normalized(fixture[:-1])
    except ValueError:pass
    else:raise AssertionError("Incomplete MPC source did not fail closed")
    print("MPC parser, target list, fail-closed semantics, idempotency OK")

def main():
    a=argparse.ArgumentParser();a.add_argument("--self-test",action="store_true");args=a.parse_args()
    if args.self_test:return self_test()
    rows=[]
    for name in TARGETS:
        rows.append(fetch_one(name))
        print("Fetched MPC orbit for",name)
    print(json.dumps(sync(rows),indent=2))
if __name__=="__main__":
    main()
