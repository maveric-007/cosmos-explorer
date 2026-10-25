#!/usr/bin/env python3
"""Download all *confirmed* exoplanets from NASA Exoplanet Archive PSCompPars.

PSCompPars is one composite (mixed-publication) row per planet; it is NOT a
precision self-consistent ephemeris. Never invent missing orbits, masses or 3D
distances. This is not an all-Gaia-stars ingestion. Python >=3.9, stdlib only.

Usage:
  python scripts/sync_exoplanets.py --self-test
  python scripts/sync_exoplanets.py --input local.csv --output data/exoplanet-systems.json
  python scripts/sync_exoplanets.py --output data/exoplanet-systems.json
"""
import argparse
import csv
import datetime as dt
import hashlib
import io
import json
import math
import os
import pathlib
import sys
import tempfile
import urllib.parse
import urllib.request
from collections import defaultdict

SOURCE = "https://exoplanetarchive.ipac.caltech.edu/TAP/sync"
COLUMNS = (
    "hostname", "pl_name", "hip_name", "gaia_dr2_id", "gaia_dr3_id",
    "ra", "dec", "sy_dist", "st_mass", "st_rad", "sy_snum", "sy_pnum",
    "pl_orbper", "pl_orbsmax", "pl_orbeccen", "pl_orbincl", "pl_bmasse",
    "pl_rade", "pl_controv_flag", "discoverymethod", "disc_year"
)
QUERY = "select " + ",".join(COLUMNS) + " from pscomppars"
QUERY_URL = SOURCE + "?" + urllib.parse.urlencode({"query": QUERY, "format": "csv"})
REFERENCE = "https://exoplanetarchive.ipac.caltech.edu/docs/API_PS_columns.html"
MIN_PLANETS = 4000  # fail closed on a truncated / unexpectedly filtered archive
MAX_PLANETS = 30000

def numeric(v):
    if v in (None, "", "null", "NULL", "--"):
        return None
    try:
        value = float(v)
    except (ValueError, TypeError):
        return None
    return round(value, 9) if math.isfinite(value) else None

def text_or_null(v):
    return str(v).strip() if v is not None and str(v).strip() else None

def first_not_null(rows, key):
    for r in rows:
        if r.get(key) not in (None, ""):
            return r[key]
    return None

def normalize(csv_text, min_count=MIN_PLANETS):
    reader = csv.DictReader(io.StringIO(csv_text.lstrip("\ufeff")))
    cols = set(reader.fieldnames or ())
    if set(COLUMNS) - cols:
        raise ValueError("Missing archive columns: " + str(sorted(set(COLUMNS) - cols)))
    by_host = defaultdict(list)
    seen_planets = set()
    source_rows = 0
    for row in reader:
        source_rows += 1
        host = text_or_null(row["hostname"])
        name = text_or_null(row["pl_name"])
        if not host or not name:
            raise ValueError("Missing hostname or planet name in row " + str(source_rows))
        if name in seen_planets:
            raise ValueError("Duplicate confirmed planet: " + name)
        seen_planets.add(name)
        by_host[host].append(row)
    if not (min_count <= source_rows <= MAX_PLANETS):
        raise ValueError("Unexpected archive row count " + str(source_rows) + " (expected " + str(min_count) + "–" + str(MAX_PLANETS) + ")")
    systems = []
    for host, rows in sorted(by_host.items(), key=lambda x:x[0].casefold()):
        ra = numeric(first_not_null(rows, "ra"))
        dec = numeric(first_not_null(rows, "dec"))
        dist = numeric(first_not_null(rows, "sy_dist"))
        if (ra is not None and not 0 <= ra < 360) or (dec is not None and not -90 <= dec <= 90):
            raise ValueError("Invalid sky coordinates: " + host)
        if dist is not None and dist <= 0:
            dist = None
        planets = []
        for row in sorted(rows, key=lambda x:x["pl_name"].casefold()):
            a = numeric(row["pl_orbsmax"])
            period = numeric(row["pl_orbper"])
            radius = numeric(row["pl_rade"])
            mass = numeric(row["pl_bmasse"])
            eccentricity = numeric(row["pl_orbeccen"])
            if a is not None and a <= 0:
                a = None
            if period is not None and period <= 0:
                period = None
            if radius is not None and radius <= 0:
                radius = None
            if mass is not None and mass <= 0:
                mass = None
            if eccentricity is not None and not 0 <= eccentricity < 1:
                eccentricity = None
            planets.append({
                "name": row["pl_name"].strip(),
                "a_au": a,
                "period_days": period,
                "radius_earth": radius,
                "mass_earth": mass,
                "eccentricity": eccentricity,
                "inclination_deg": numeric(row["pl_orbincl"]),
                "controversial": str(row["pl_controv_flag"]).strip() == "1",
                "discovery_method": text_or_null(row["discoverymethod"]),
                "discovery_year": numeric(row["disc_year"]),
            })
        system = {
            "name": host,
            "hip_name": text_or_null(first_not_null(rows, "hip_name")),
            "gaia_dr2_id": text_or_null(first_not_null(rows, "gaia_dr2_id")),
            "gaia_dr3_id": text_or_null(first_not_null(rows, "gaia_dr3_id")),
            "ra_deg": ra,
            "dec_deg": dec,
            "distance_pc": dist,
            "stellar_mass_solar": numeric(first_not_null(rows, "st_mass")),
            "stellar_radius_solar": numeric(first_not_null(rows, "st_rad")),
            "number_of_stars": numeric(first_not_null(rows, "sy_snum")),
            "reported_planet_count": numeric(first_not_null(rows, "sy_pnum")),
            "planets": planets
        }
        systems.append(system)
    with_position = sum(1 for s in systems if s["ra_deg"] is not None and s["dec_deg"] is not None and s["distance_pc"] is not None)
    with_orbit = sum(1 for s in systems for p in s["planets"] if p["a_au"] is not None)
    return {
        "schema": "cosmos-explorer-exoplanets-v1",
        "source": "NASA Exoplanet Archive PSCompPars (confirmed exoplanets, mixed-reference composite)",
        "query": QUERY,
        "documentation": REFERENCE,
        "distance_units": "pc", "ra_dec_units": "degrees (ICRS)",
        "orbit_units": "AU", "period_units": "days",
        "scope_note": "One composite row per confirmed planet; does not include unconfirmed candidates, every Gaia star, moons, or an accurate orbital phase/ephemeris.",
        "counts": {
            "confirmed_planets": source_rows,
            "host_systems": len(systems),
            "located_hosts_3d": with_position,
            "planets_with_semimajor_axis": with_orbit
        },
        "systems": systems
    }

def checksum_content(data):
    return hashlib.sha256(json.dumps(data, sort_keys=True, separators=(",",":"),ensure_ascii=False).encode("utf-8")).hexdigest()

def write_atomic(path, data):
    path = pathlib.Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(mode="w", encoding="utf-8", dir=path.parent, delete=False) as tmp:
        tmp.write(json.dumps(data, ensure_ascii=False, separators=(",",":")) + "\n")
        temp = tmp.name
    os.replace(temp, path)

def test():
    columns = list(COLUMNS)
    def row(host, planet, **kw):
        o = {c:"" for c in columns}
        o.update({"hostname":host, "pl_name":planet, "ra":"17.5","dec":"-22.1","sy_dist":"11.2"})
        o.update(kw)
        return o
    buf = io.StringIO()
    w=csv.DictWriter(buf, fieldnames=columns)
    w.writeheader()
    w.writerow(row("System A","System A b",pl_orbsmax="0.1",pl_orbper="12",st_mass="0.8",sy_snum="2"))
    w.writerow(row("System A","System A c",pl_orbsmax="",pl_orbper="",pl_controv_flag="1"))
    w.writerow(row("Other Host","Other Host b",sy_dist="",pl_rade="1.2"))
    data=normalize(buf.getvalue(),min_count=3)
    assert data["counts"]=={"confirmed_planets":3,"host_systems":2,"located_hosts_3d":1,"planets_with_semimajor_axis":1}
    assert data["systems"][0]["planets"][1]["a_au"] is None
    assert data["systems"][1]["distance_pc"] is None
    try:
        normalize(buf.getvalue(),min_count=5)
        raise AssertionError("minimum-row guard did not reject source")
    except ValueError:
        pass
    print("Self-test passed: grouping, missing fields, controversial flag, counts, truncated-source rejection.")

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--output", default="data/exoplanet-systems.json")
    parser.add_argument("--status", default="data/exoplanet-sync-status.json")
    parser.add_argument("--input", help="Use an existing CSV for offline verification")
    parser.add_argument("--self-test", action="store_true")
    args=parser.parse_args()
    if args.self_test:
        test()
        return
    now=dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds").replace("+00:00","Z")
    if args.input:
        source_csv=pathlib.Path(args.input).read_text(encoding="utf-8")
    else:
        req=urllib.request.Request(QUERY_URL,headers={"User-Agent":"CosmosExplorer/0.4 (research catalog indexing; public NASA archive)", "Accept":"text/csv"})
        with urllib.request.urlopen(req,timeout=100) as response:
            if response.status != 200:
                raise ValueError("Archive responded " + str(response.status))
            raw=response.read(MAX_PLANETS*1100)
            if len(raw)>=MAX_PLANETS*1100:
                raise ValueError("Unexpectedly large TAP export")
            source_csv=raw.decode("utf-8")
    catalog=normalize(source_csv)
    fingerprint=checksum_content(catalog)
    target=pathlib.Path(args.output)
    prior=None
    if target.exists():
        old=json.loads(target.read_text(encoding="utf-8"))
        prior=checksum_content(old)
    status_path=pathlib.Path(args.status)
    past={}
    if status_path.exists():
        past=json.loads(status_path.read_text(encoding="utf-8"))
    modified=fingerprint!=prior
    if modified:
        write_atomic(target,catalog)
    status={
        "schema":"cosmos-explorer-catalog-refresh-status-v1",
        "provider":"NASA Exoplanet Archive",
        "catalog":"pscomppars",
        "official_query_url":QUERY_URL,
        "last_checked_utc":now,
        "check_status":"updated" if modified else "unchanged",
        "last_imported_utc":now if modified else past.get("last_imported_utc"),
        "publisher_release_utc":None,
        "publisher_release_status":"Not supplied by TAP export; do not confuse check time with observation or release date",
        "source_file_sha256":hashlib.sha256(source_csv.encode("utf-8")).hexdigest(),
        "normalized_sha256":fingerprint,
        "counts":catalog["counts"]
    }
    write_atomic(status_path,status)
    print(json.dumps({"updated":modified,"sha256":fingerprint,"counts":catalog["counts"],"last_checked":now},indent=2))
if __name__=="__main__":
    main()
