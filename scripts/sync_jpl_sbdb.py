#!/usr/bin/env python3
"""Import a bounded JPL SBDB Query snapshot of asteroid orbital elements.

The elements are osculating orbital elements at a stated epoch (JPL SBDB
ecliptic/equinox convention), not present-day 3D positions or measured masses.
No API calls from the GitHub Pages browser. Python standard library only.
"""
import argparse
import datetime as dt
import hashlib
import json
import math
import os
from pathlib import Path
import tempfile
import urllib.parse
import urllib.request

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "data/jpl-sbdb-sample.json"
STATUS = ROOT / "data/jpl-sbdb-sync-status.json"
FIELDS = ["spkid", "pdes", "full_name", "kind", "orbit_id", "epoch",
          "e", "a", "i", "om", "w", "diameter", "GM"]
BASE = "https://ssd-api.jpl.nasa.gov/sbdb_query.api"
PARAMS = {"fields": ",".join(FIELDS), "sb-kind": "a",
          "sort": "spkid", "limit": "200"}
QUERY_URL = BASE + "?" + urllib.parse.urlencode(PARAMS)


def utc_now():
    return dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")


def number(value, minimum=None, maximum=None):
    if value is None or str(value).strip() in ("", "--", "null"):
        return None
    n = float(value)
    if not math.isfinite(n):
        raise ValueError("Non-finite SBDB numeric field")
    if minimum is not None and n < minimum or maximum is not None and n > maximum:
        raise ValueError("Out-of-range SBDB orbital field")
    return n


def normalize(raw, minimum=10):
    doc = json.loads(raw)
    signature = doc.get("signature") or {}
    if not str(signature.get("version", "")).startswith("1."):
        raise ValueError("Unknown JPL SBDB Query API format/version")
    columns = doc.get("fields")
    if not isinstance(columns, list) or len(columns) != len(set(columns)):
        raise ValueError("Invalid SBDB source columns")
    if set(FIELDS) - set(columns):
        raise ValueError("Missing expected SBDB source columns")
    rows = doc.get("data")
    if not isinstance(rows, list) or not minimum <= len(rows) <= 200:
        raise ValueError("Missing, oversized, or unexpectedly short JPL sample")
    entries, seen = [], set()
    for row in rows:
        if not isinstance(row, list) or len(row) != len(columns):
            raise ValueError("SBDB column/row mismatch")
        values = dict(zip(columns, row))
        spkid = str(values.get("spkid") or "").strip()
        pdes = str(values.get("pdes") or "").strip()
        if not spkid.isdecimal() or not pdes or spkid in seen:
            raise ValueError("Invalid/duplicate JPL stable object ID")
        seen.add(spkid)
        kind = values.get("kind")
        if kind not in ("an", "au"):
            raise ValueError("Non-asteroid in asteroid sample")
        a = number(values.get("a"), 0)
        ecc = number(values.get("e"), 0)
        epoch = number(values.get("epoch"), 2000000, 3000000)
        if epoch is None or ecc is None:
            raise ValueError("Missing orbital epoch/eccentricity")
        entries.append({
            "spkid": spkid, "primary_designation": pdes,
            "full_name": str(values.get("full_name") or "").strip() or None,
            "kind": kind, "orbit_solution_id": values.get("orbit_id"),
            "epoch_jd_tdb": epoch, "eccentricity": ecc,
            "semimajor_axis_au": a,
            "inclination_deg": number(values.get("i"), 0, 180),
            "ascending_node_deg": number(values.get("om"), 0, 360),
            "argument_of_perihelion_deg": number(values.get("w"), 0, 360),
            "diameter_km_catalog": number(values.get("diameter"), 0),
            "gm_km3_s2_catalog": number(values.get("GM"), 0)
        })
    entries.sort(key=lambda x: int(x["spkid"]))
    return {
        "schema": "cosmos-explorer-jpl-sbdb-sample-v1",
        "source": "NASA JPL Small-Body Database Query API",
        "source_release": None,
        "query_url": QUERY_URL,
        "reference": "https://ssd-api.jpl.nasa.gov/doc/sbdb_query.html",
        "sample_only": True,
        "scope": "At most 200 asteroid records in SPK-ID order; not a full population census.",
        "units": {"orbit_epoch": "JD TDB", "a": "AU", "angles": "degrees",
                  "diameter": "km", "GM": "km^3/s^2"},
        "limitations": "Osculating orbit elements at source epoch, not an ephemeris. Missing diameter or GM is unknown; no inferred body mass or 3D instantaneous location.",
        "count": len(entries), "objects": entries
    }


def digest(obj):
    return hashlib.sha256(json.dumps(obj, sort_keys=True, separators=(",", ":")).encode("utf-8")).hexdigest()


def atomic(path, obj):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile("w", encoding="utf-8", dir=path.parent, delete=False) as f:
        json.dump(obj, f, ensure_ascii=False, separators=(",", ":"))
        f.write("\n")
        name = f.name
    os.replace(name, path)


def sync(raw, out=OUTPUT, status=STATUS):
    obj = normalize(raw)
    changed = not out.exists() or digest(json.loads(out.read_text(encoding="utf-8"))) != digest(obj)
    old = json.loads(status.read_text(encoding="utf-8")) if status.exists() else {}
    time = utc_now()
    if changed:
        atomic(out, obj)
    state = {"schema": "cosmos-explorer-jpl-sbdb-sync-status-v1",
             "last_checked_utc": time,
             "last_imported_utc": time if changed else old.get("last_imported_utc"),
             "publisher_release_utc": None,
             "check_status": "updated" if changed else "unchanged",
             "sample_only": True, "count": obj["count"],
             "query_url": QUERY_URL,
             "source_json_sha256": hashlib.sha256(raw.encode("utf-8")).hexdigest(),
             "normalized_sha256": digest(obj)}
    atomic(status, state)
    return state


def test():
    fields = FIELDS
    data = []
    for i in range(1, 21):
        obj = dict.fromkeys(fields)
        obj.update({"spkid": str(2000000 + i), "pdes": str(i),
                    "kind": "an", "epoch": "2460000.5",
                    "e": "0.15", "a": "2.7",
                    "i": "6.5", "om": "190", "w": "110"})
        data.append([obj[x] for x in fields])
    raw = json.dumps({"signature": {"version": "1.0"},
                      "fields": fields, "data": data})
    assert normalize(raw)["count"] == 20
    with tempfile.TemporaryDirectory() as d:
        p = Path(d)
        assert sync(raw, p/"d.json", p/"s.json")["check_status"] == "updated"
        assert sync(raw, p/"d.json", p/"s.json")["check_status"] == "unchanged"
    bad = json.loads(raw)
    bad["data"].append(bad["data"][0])
    try:
        normalize(json.dumps(bad))
        raise AssertionError("duplicate detection failed")
    except ValueError:
        pass
    bad = json.loads(raw)
    bad["data"][0][fields.index("kind")] = "cn"
    try:
        normalize(json.dumps(bad))
        raise AssertionError("nonasteroid detection failed")
    except ValueError:
        pass
    print("JPL SBDB offline tests passed: source IDs, units, nulls, duplicates, asteroid-only, idempotency")


def fetch():
    request = urllib.request.Request(QUERY_URL, headers={
        "User-Agent": "CosmosExplorer/0.9 (bounded public JPL asteroid catalog research)",
        "Accept": "application/json"})
    with urllib.request.urlopen(request, timeout=45) as response:
        if response.status != 200:
            raise ValueError("JPL SBDB query HTTP " + str(response.status))
        blob = response.read(600001)
        if len(blob) > 600000:
            raise ValueError("Oversized JPL sample")
    return blob.decode("utf-8")


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--self-test", action="store_true")
    p.add_argument("--input")
    args = p.parse_args()
    if args.self_test:
        return test()
    raw = Path(args.input).read_text(encoding="utf-8") if args.input else fetch()
    print(json.dumps(sync(raw), indent=2))


if __name__ == "__main__":
    main()
