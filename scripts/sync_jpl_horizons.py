#!/usr/bin/env python3
"""Verified, bounded JPL Horizons barycentric vector snapshots for 11 Solar bodies.

Fixed epoch, ICRF axes, Solar System barycenter, geometric state in km and
km/s. No browser API requests. This is not a continuous-time integration,
a gravitational mass inventory or an instantaneous observed sky appearance.
"""
import argparse
import csv
import datetime as dt
import hashlib
import io
import json
import math
import os
from pathlib import Path
import re
import tempfile
import time
import urllib.parse
import urllib.request

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data/jpl-horizons-sample.json"
STATUS = ROOT / "data/jpl-horizons-sync-status.json"
BASE = "https://ssd.jpl.nasa.gov/api/horizons.api"
TARGETS = {
    "10": "Sun", "199": "Mercury", "299": "Venus", "399": "Earth",
    "301": "Moon", "499": "Mars", "599": "Jupiter", "699": "Saturn",
    "799": "Uranus", "899": "Neptune", "999": "Pluto",
}
EPOCH = "2026-10-29 00:00"
EXPECTED_JD_TDB = 2461342.5  # check, not an independent observation


def timestamp():
    return dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")


def query_url(target):
    if target not in TARGETS:
        raise ValueError("Unknown JPL target ID")
    settings = {
        "format": "json", "COMMAND": "'" + target + "'",
        "OBJ_DATA": "NO", "MAKE_EPHEM": "YES", "EPHEM_TYPE": "VECTORS",
        "CENTER": "'500@0'", "REF_PLANE": "FRAME", "REF_SYSTEM": "ICRF",
        "VEC_TABLE": "2", "VEC_LABELS": "NO", "CSV_FORMAT": "YES",
        "OUT_UNITS": "KM-S", "VEC_CORR": "NONE", "TIME_TYPE": "TDB",
        "START_TIME": "'2026-10-29 00:00'",
        "STOP_TIME": "'2026-10-30 00:00'", "STEP_SIZE": "'1 d'",
    }
    return BASE + "?" + urllib.parse.urlencode(settings)


def finite(value):
    val = float(value)
    if not math.isfinite(val):
        raise ValueError("Nonfinite Horizons state vector field")
    return val


def parse_reply(target, raw):
    if target not in TARGETS:
        raise ValueError("Invalid JPL target")
    payload = json.loads(raw)
    signature = payload.get("signature") or {}
    if not str(signature.get("version", "")).startswith("1.") or "Horizons" not in str(signature.get("source", "")):
        raise ValueError("Unexpected JPL Horizons API signature/version")
    if payload.get("error"):
        raise ValueError("Horizons query error: " + str(payload["error"])[:300])
    result = payload.get("result") or ""
    match = re.search(r"\$\$SOE\s*(.*?)\s*\$\$EOE", result, re.DOTALL)
    if not match:
        raise ValueError("Missing Horizons ephemeris data markers")
    parsed = list(csv.reader(io.StringIO(match.group(1))))
    if not 1 <= len(parsed) <= 2:
        raise ValueError("Expected one/two daily vector records, got " + str(len(parsed)))
    record = [c.strip() for c in parsed[0]]
    if len(record) < 8 or any(x for x in record[8:]):
        raise ValueError("Unexpected Horizons CSV vector columns")
    jd = finite(record[0])
    if abs(jd - EXPECTED_JD_TDB) > 0.002:
        raise ValueError("Unexpected Horizons vector epoch")
    vals = [finite(v) for v in record[2:8]]
    x, y, z, vx, vy, vz = vals
    norm = math.sqrt(x*x+y*y+z*z)
    speed = math.sqrt(vx*vx+vy*vy+vz*vz)
    if norm > 1e11 or speed > 100:
        raise ValueError("Implausible barycentric vector magnitude or velocity")
    return {
        "target_id": target, "target_name": TARGETS[target],
        "epoch_jd_tdb": jd,
        "position_km_icrf_ssb": [x, y, z],
        "velocity_km_s_icrf_ssb": [vx, vy, vz]
    }


def digest(obj):
    return hashlib.sha256(json.dumps(obj, ensure_ascii=False, sort_keys=True,
                                      separators=(",", ":")).encode("utf-8")).hexdigest()


def atomic(path, data):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(mode="w", encoding="utf-8", dir=path.parent, delete=False) as f:
        json.dump(data, f, ensure_ascii=False, separators=(",", ":"))
        f.write("\n")
        name = f.name
    os.replace(name, path)


def normalize(raw_by_target):
    if set(raw_by_target) != set(TARGETS):
        raise ValueError("Missing or extra Horizons target response")
    items = [parse_reply(key, raw_by_target[key]) for key in TARGETS]
    jds = [r["epoch_jd_tdb"] for r in items]
    if max(jds) - min(jds) > 0.00001:
        raise ValueError("Mismatched simultaneous Horizons state-vector epochs")
    return {
        "schema": "cosmos-explorer-jpl-horizons-snapshot-v1",
        "source": "NASA JPL Horizons API",
        "reference": "https://ssd-api.jpl.nasa.gov/doc/horizons.html",
        "epoch_calendar_tdb": EPOCH, "epoch_jd_tdb": jds[0],
        "reference_frame": "ICRF", "reference_plane": "FRAME (ICRF equator)",
        "origin": "Solar System Barycenter (500@0)",
        "correction": "NONE (geometric)", "units": {"position": "km", "velocity": "km/s"},
        "scope": "Eleven selected major Solar System targets at one fixed epoch; not a complete astronomical body catalog.",
        "warning": "Barycentric vectors are model-derived ephemerides, not telescope observations. Future states and orbital phases are not physically integrated by the website.",
        "query_urls": {key: query_url(key) for key in TARGETS},
        "count": len(items), "bodies": items,
    }


def sync(raw_by_target, output=OUT, status=STATUS):
    doc = normalize(raw_by_target)
    output, status = Path(output), Path(status)
    fingerprint = digest(doc)
    prior = json.loads(status.read_text(encoding="utf-8")) if status.exists() else {}
    same = output.exists() and digest(json.loads(output.read_text(encoding="utf-8"))) == fingerprint
    now = timestamp()
    if not same:
        atomic(output, doc)
    source_digests = {k: hashlib.sha256(raw_by_target[k].encode("utf-8")).hexdigest()
                      for k in TARGETS}
    audit = {"schema": "cosmos-explorer-jpl-horizons-sync-status-v1",
             "last_checked_utc": now, "last_imported_utc": prior.get("last_imported_utc") if same else now,
             "publisher_release_utc": None, "ephemeris_epoch_tdb": EPOCH,
             "check_status": "unchanged" if same else "updated",
             "count": len(doc["bodies"]), "source_json_sha256": source_digests,
             "normalized_sha256": fingerprint, "snapshot_only": True}
    atomic(status, audit)
    return audit


def offline_test():
    def fixture(key):
        vec = [1e6, 2e6, 3e6, 4.5, 6.7, 8.9]
        row = "2461342.500000000, A.D. 2026-Oct-29 00:00:00.0000, " + ", ".join(str(n) for n in vec) + ", "
        return json.dumps({"signature": {"source": "NASA/JPL Horizons API", "version": "1.3"},
                           "result": "sample\n$$SOE\n" + row + "\n$$EOE\n"})
    source = {k: fixture(k) for k in TARGETS}
    out = normalize(source)
    assert len(out["bodies"]) == 11
    assert out["bodies"][0]["position_km_icrf_ssb"] == [1e6, 2e6, 3e6]
    with tempfile.TemporaryDirectory() as d:
        p = Path(d)
        assert sync(source, p / "sample.json", p / "status.json")["check_status"] == "updated"
        assert sync(source, p / "sample.json", p / "status.json")["check_status"] == "unchanged"
    bad = dict(source)
    bad["399"] = json.dumps({"signature": {"source": "NASA/JPL Horizons API", "version": "1.3"},
                              "error": "unavailable"})
    try:
        normalize(bad)
        raise AssertionError("Unsuccessful target not rejected")
    except ValueError:
        pass
    bad = dict(source)
    bad.pop("301")
    try:
        normalize(bad)
        raise AssertionError("Missing target not rejected")
    except ValueError:
        pass
    print("JPL Horizons offline tests passed: epoch, frame metadata, units, required targets, atomic no-op, API failures")


def download(key):
    req = urllib.request.Request(query_url(key), headers={
        "User-Agent": "CosmosExplorer/1.0 (public bounded scientific ephemeris snapshot)",
        "Accept": "application/json"})
    with urllib.request.urlopen(req, timeout=40) as response:
        if response.status != 200:
            raise ValueError("Horizons API HTTP " + str(response.status))
        blob = response.read(220001)
        if len(blob) > 220000:
            raise ValueError("Oversized JPL Horizons response")
    return blob.decode("utf-8")


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--self-test", action="store_true")
    p.add_argument("--input-dir", help="Offline pinned API JSON responses named <target_id>.json")
    args = p.parse_args()
    if args.self_test:
        return offline_test()
    if args.input_dir:
        raw = {key: (Path(args.input_dir) / (key + ".json")).read_text(encoding="utf-8")
               for key in TARGETS}
    else:
        raw = {}
        for key in TARGETS:
            raw[key] = download(key)
            parse_reply(key, raw[key])  # fail before publication on malformed response
            time.sleep(0.25)
    print(json.dumps(sync(raw), indent=2))


if __name__ == "__main__":
    main()
