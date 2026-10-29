#!/usr/bin/env python3
"""Build a bounded unified OBSERVATION index from existing validated Cosmos catalogs.

Every row remains a source-scoped observation or system, not an assertion that
nearby coordinates represent the same object. Only explicit published Gaia DR3
and HIP identifiers create cross-catalog associations. Source JSON is preserved.
No inferred stellar mass, missing radial velocity, or galaxy distance is added.
"""
import argparse
import hashlib
import json
import math
import os
from pathlib import Path
import re
import tempfile

ROOT = Path(__file__).resolve().parents[1]
SOURCES = {
    "nasa_pscomppars": ("exoplanet-systems.json", "systems", True),
    "gaia_dr3": ("gaia-sample.json", "stars", True),
    "hyg": ("constellations-catalog.json", "stars", True),
    "allwise": ("allwise-sample.json", "records", True),
    "twomass": ("twomass-sample.json", "records", True),
    "lamost_dr12": ("lamost_dr12-sample.json", "records", True),
    "desi_dr1": ("desi_dr1-sample.json", "records", True),
    "galah_dr4": ("galah_dr4-sample.json", "records", False),
    "apogee_dr17": ("apogee_dr17-sample.json", "records", False),
    "jpl_sbdb": ("jpl-sbdb-sample.json", "objects", True),
    "jpl_horizons": ("jpl-horizons-sample.json", "bodies", True),
}
SCHEMA = "cosmos-explorer-unified-observation-index-v1"


def number(value, low=None, high=None):
    if value is None or value == "":
        return None
    if isinstance(value, bool):
        raise ValueError("Boolean where number required")
    result = float(value)
    if not math.isfinite(result):
        raise ValueError("Non-finite coordinate or distance")
    if low is not None and result < low or high is not None and result > high:
        raise ValueError("Out-of-range coordinate or distance")
    return result


def pair(ra, dec):
    a = number(ra, 0, 360)
    d = number(dec, -90, 90)
    if (a is None) != (d is None) or a == 360:
        raise ValueError("Missing/inconsistent sky coordinates")
    return a, d


def numeric_id(value, prefix):
    if value is None:
        return None
    value = str(value).strip()
    if not value:
        return None
    match = re.fullmatch(r"(?:" + prefix + r"\s+)?([0-9]+)", value, re.IGNORECASE)
    return str(int(match.group(1))) if match else None


def build(data_dir):
    data_dir = Path(data_dir)
    rows, links, manifest, seen = [], [], [], set()
    gaia_ids, hip_ids = set(), set()
    system_refs, galah_refs = [], []

    def emit(source, source_row_id, kind, ra, dec, **attrs):
        key = source + ":" + str(source_row_id)
        if not str(source_row_id) or key in seen:
            raise ValueError("Missing or repeated source-scoped ID: " + key)
        a, d = pair(ra, dec)
        row = {"id": key, "source": source, "source_row_id": str(source_row_id),
               "kind": kind, "ra_deg": a, "dec_deg": d}
        row.update({k: v for k, v in attrs.items() if v is not None})
        rows.append(row)
        seen.add(key)
        return key

    for source, (filename, collection, required) in SOURCES.items():
        path = data_dir / filename
        if not path.exists():
            if required:
                raise ValueError("Missing required validated snapshot: " + filename)
            continue
        raw = path.read_bytes()
        obj = json.loads(raw)
        items = obj.get(collection)
        if not isinstance(items, list) or not items:
            raise ValueError("Empty/malformed source " + filename + " / " + collection)
        if source == "nasa_pscomppars":
            if obj.get("schema") != "cosmos-explorer-exoplanets-v1":
                raise ValueError("NASA source schema mismatch")
        elif source == "gaia_dr3":
            if obj.get("schema") != "cosmos-explorer-gaia-sample-v1":
                raise ValueError("Gaia source schema mismatch")
        elif source == "hyg":
            if obj.get("schema") != "cosmos-explorer-star-catalog-v1":
                raise ValueError("HYG source schema mismatch")
        elif source in ("allwise", "twomass"):
            if obj.get("schema") != "cosmos-explorer-irsa-sample-v1":
                raise ValueError("IRSA source schema mismatch")
        elif source == "lamost_dr12":
            if obj.get("schema") != "cosmos-explorer-lamost-sample-v1":
                raise ValueError("LAMOST source schema mismatch")
        elif source == "desi_dr1":
            if obj.get("schema") != "cosmos-explorer-desi-dr1-sample-v1":
                raise ValueError("DESI source schema mismatch")
        elif source in ("galah_dr4", "apogee_dr17"):
            if obj.get("schema") != "cosmos-explorer-vizier-survey-sample-v1":
                raise ValueError("VizieR source schema mismatch")
        elif source == "jpl_sbdb":
            if obj.get("schema") != "cosmos-explorer-jpl-sbdb-sample-v1":
                raise ValueError("JPL SBDB schema mismatch")
        elif source == "jpl_horizons":
            if (obj.get("schema") != "cosmos-explorer-jpl-horizons-snapshot-v1"
                    or obj.get("reference_frame") != "ICRF"
                    or obj.get("origin") != "Solar System Barycenter (500@0)"
                    or obj.get("correction") != "NONE (geometric)"):
                raise ValueError("JPL Horizons schema/frame/origin mismatch")
        manifest.append({"source": source, "file": "data/" + filename,
                         "sha256": hashlib.sha256(raw).hexdigest(),
                         "schema": obj.get("schema"), "rows": len(items),
                         "scope": "source snapshot, not complete sky census"})
        for item in items:
            if source == "nasa_pscomppars":
                name = str(item["name"]).strip()
                key = emit(source, name, "planetary_host_system",
                           item.get("ra_deg"), item.get("dec_deg"),
                           name=name, distance_pc_catalog=number(item.get("distance_pc"), 0),
                           confirmed_planets=len(item["planets"]))
                system_refs.append((key, numeric_id(item.get("gaia_dr3_id"), r"Gaia\s+DR3"),
                                    numeric_id(item.get("hip_name"), "HIP")))
            elif source == "gaia_dr3":
                sid = str(item["source_id"])
                key = emit(source, sid, "stellar_source",
                           item.get("ra_deg"), item.get("dec_deg"),
                           name=None, epoch_year=number(item.get("epoch_year")),
                           distance_pc_inverse_parallax_approx=number(item.get("distance_pc_approx"), 0),
                           radial_velocity_km_s=number(item.get("radial_velocity_km_s")))
                gaia_ids.add(sid)
            elif source == "hyg":
                if not isinstance(item, list) or len(item) < 4:
                    raise ValueError("Malformed HYG packed star")
                hip = str(int(item[0]))
                key = emit(source, hip, "bright_star",
                           number(item[1], 0, 24) * 15, item[2],
                           name=item[6] if len(item) > 6 and item[6] else None,
                           distance_pc_catalog=number(item[3], 0))
                hip_ids.add(hip)
            elif source in ("allwise", "twomass"):
                emit(source, item["designation"], "infrared_detection",
                     item.get("ra_deg"), item.get("dec_deg"))
            elif source == "lamost_dr12":
                emit(source, item["source_observation_id"], "spectral_observation",
                     item.get("ra_deg"), item.get("dec_deg"))
            elif source == "desi_dr1":
                emit(source, item["targetid"], "galaxy_redshift_entry",
                     item.get("ra_deg"), item.get("dec_deg"),
                     redshift=number(item.get("redshift"), 0))
            elif source == "galah_dr4":
                key = emit(source, item["source_row_id"], "spectral_catalog_entry",
                           item.get("ra_deg"), item.get("dec_deg"))
                galah_refs.append((key, str(item.get("gaia_dr3_source_id") or "")))
            elif source == "apogee_dr17":
                emit(source, item["source_row_id"], "spectral_catalog_entry",
                     item.get("ra_deg"), item.get("dec_deg"))
            elif source == "jpl_sbdb":
                # Orbital elements do not imply a fixed equatorial sky position.
                emit(source, item["spkid"], "small_body_orbit_solution", None, None,
                     name=item.get("full_name"),
                     primary_designation=item.get("primary_designation"),
                     orbit_solution_id=item.get("orbit_solution_id"),
                     orbit_epoch_jd_tdb=number(item.get("epoch_jd_tdb"), 2000000, 3000000),
                     semimajor_axis_au=number(item.get("semimajor_axis_au"), 0),
                     eccentricity=number(item.get("eccentricity"), 0),
                     inclination_deg=number(item.get("inclination_deg"), 0, 180),
                     diameter_km_catalog=number(item.get("diameter_km_catalog"), 0),
                     gm_km3_s2_catalog=number(item.get("gm_km3_s2_catalog"), 0))
            elif source == "jpl_horizons":
                # ICRF barycentric vectors are not RA/Dec sky positions.
                position = item.get("position_km_icrf_ssb")
                velocity = item.get("velocity_km_s_icrf_ssb")
                if (not isinstance(position, list) or len(position) != 3
                        or not isinstance(velocity, list) or len(velocity) != 3):
                    raise ValueError("Invalid JPL Horizons state-vector dimensions")
                position = [number(v) for v in position]
                velocity = [number(v) for v in velocity]
                if any(v is None for v in position + velocity):
                    raise ValueError("Missing JPL Horizons state vector components")
                epoch = number(item.get("epoch_jd_tdb"), 2000000, 3000000)
                if epoch is None or epoch != number(obj.get("epoch_jd_tdb"), 2000000, 3000000):
                    raise ValueError("JPL Horizons target snapshot epoch mismatch")
                emit(source, item["target_id"], "solar_system_ephemeris_state", None, None,
                     name=item.get("target_name"), epoch_jd_tdb=epoch,
                     position_km_icrf_ssb=position, velocity_km_s_icrf_ssb=velocity,
                     reference_frame="ICRF",
                     origin="Solar System Barycenter (500@0)",
                     correction="NONE (geometric)")
    for source_key, gaia, hip in system_refs:
        if gaia is not None and gaia in gaia_ids:
            links.append({"from": source_key, "to": "gaia_dr3:" + gaia,
                          "basis": "published_gaia_dr3_id", "relation": "source_identifier_association"})
        if hip is not None and hip in hip_ids:
            links.append({"from": source_key, "to": "hyg:" + hip,
                          "basis": "published_hip_id", "relation": "source_identifier_association"})
    for source_key, gaia in galah_refs:
        if gaia and gaia in gaia_ids:
            links.append({"from": source_key, "to": "gaia_dr3:" + gaia,
                          "basis": "published_gaia_dr3_id", "relation": "source_identifier_association"})
    rows.sort(key=lambda x: x["id"])
    links.sort(key=lambda x: (x["from"], x["to"]))
    counts = {s: sum(r["source"] == s for r in rows) for s in SOURCES
              if any(r["source"] == s for r in rows)}
    return {"schema": SCHEMA,
            "scope": "Source-scoped, searchable observation index. Links are ID associations, not automatic physical-object merges.",
            "caveats": ["Samples are not full catalogs or a mass census.",
                        "Nearby sky coordinates alone never establish an identity.",
                        "Unknown radial velocities, ages, masses and distances stay unknown.",
                        "Infrared detections can be nonstellar; DESI redshift is not a Euclidean distance.",
                        "NASA composite host identifier may represent a multiple-star system.",
                        "JPL Horizons vectors are model-derived barycentric ephemerides only at their stated epoch.",
                        "JPL SBDB asteroid elements do not specify instantaneous sky positions or unknown masses."],
            "input_manifest": manifest,
            "counts": {"indexed_records": len(rows), "by_source": counts,
                       "published_id_links": len(links), "unresolved_records": len(rows) - len({v["from"] for v in links})},
            "records": rows, "links": links}


def atomic(path, obj):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile("w", encoding="utf-8", dir=path.parent, delete=False) as tmp:
        json.dump(obj, tmp, separators=(",", ":"), ensure_ascii=False)
        tmp.write("\n")
        staged = tmp.name
    os.replace(staged, path)


def self_test():
    with tempfile.TemporaryDirectory() as d:
        p = Path(d)
        fixtures = {
            "exoplanet-systems.json": {"schema": "cosmos-explorer-exoplanets-v1", "systems": [
                {"name": "Host A", "ra_deg": 12, "dec_deg": 1, "distance_pc": 30,
                 "gaia_dr3_id": "Gaia DR3 42", "hip_name": "HIP 9", "planets": [{"name": "Host A b"}]},
                {"name": "Host B", "ra_deg": None, "dec_deg": None, "gaia_dr3_id": None, "planets": []}]},
            "gaia-sample.json": {"schema": "cosmos-explorer-gaia-sample-v1", "stars": [
                {"source_id": "42", "ra_deg": 12, "dec_deg": 1, "distance_pc_approx": 28.2},
                {"source_id": "43", "ra_deg": 12, "dec_deg": 1, "radial_velocity_km_s": None}]},
            "constellations-catalog.json": {"schema": "cosmos-explorer-star-catalog-v1",
                                            "stars": [[9, 0.8, 1, 30, 5, 0, "Example"]]},
            "allwise-sample.json": {"schema": "cosmos-explorer-irsa-sample-v1",
                                    "records": [{"designation": "IR", "ra_deg": 12, "dec_deg": 1}]},
            "twomass-sample.json": {"schema": "cosmos-explorer-irsa-sample-v1",
                                    "records": [{"designation": "IR", "ra_deg": 12, "dec_deg": 1}]},
            "lamost_dr12-sample.json": {"schema": "cosmos-explorer-lamost-sample-v1",
                                        "records": [{"source_observation_id": "L1", "ra_deg": 12, "dec_deg": 1}]},
            "desi_dr1-sample.json": {"schema": "cosmos-explorer-desi-dr1-sample-v1",
                                     "records": [{"targetid": "D1", "ra_deg": 12, "dec_deg": 1, "redshift": 1.2}]},
            "jpl-sbdb-sample.json": {"schema": "cosmos-explorer-jpl-sbdb-sample-v1",
                                     "objects": [{"spkid": "20000001", "full_name": "1 Ceres",
                                                  "primary_designation": "1", "epoch_jd_tdb": 2461200.5,
                                                  "semimajor_axis_au": 2.7, "eccentricity": 0.08,
                                                  "gm_km3_s2_catalog": None}]},
            "jpl-horizons-sample.json": {"schema": "cosmos-explorer-jpl-horizons-snapshot-v1",
                                        "reference_frame": "ICRF",
                                        "origin": "Solar System Barycenter (500@0)",
                                        "correction": "NONE (geometric)",
                                        "epoch_jd_tdb": 2461342.5,
                                        "bodies": [{"target_id": "10", "target_name": "Sun",
                                                    "epoch_jd_tdb": 2461342.5,
                                                    "position_km_icrf_ssb": [1., 2., 3.],
                                                    "velocity_km_s_icrf_ssb": [0.01, 0.02, 0.03]}]}}
        for filename, fixture in fixtures.items():
            (p / filename).write_text(json.dumps(fixture), encoding="utf-8")
        index = build(p)
        assert index["counts"]["indexed_records"] == 11
        assert index["counts"]["published_id_links"] == 2
        assert index["counts"]["by_source"]["jpl_sbdb"] == 1
        assert index["counts"]["by_source"]["jpl_horizons"] == 1
        assert next(r for r in index["records"] if r["id"] == "jpl_sbdb:20000001")["ra_deg"] is None
        assert "gm_km3_s2_catalog" not in next(r for r in index["records"] if r["id"] == "jpl_sbdb:20000001")
        assert next(r for r in index["records"] if r["id"] == "jpl_horizons:10")["velocity_km_s_icrf_ssb"] == [0.01, 0.02, 0.03]
        assert "gaia_dr3:43" in {r["id"] for r in index["records"]}
        assert not any(x["to"] == "gaia_dr3:43" for x in index["links"])
        assert index == build(p)
        assert next(r for r in index["records"] if r["id"] == "gaia_dr3:43").get("radial_velocity_km_s") is None
        (p / "gaia-sample.json").write_text(json.dumps({"schema": "bad", "stars": []}))
        try:
            build(p)
            raise AssertionError("Malformed source did not fail closed")
        except ValueError:
            pass
    print("Unified index self-tests passed: published IDs, distinct asteroid/ephemeris types, no proximity merges, nulls, deterministic output, schema rejection")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--self-test", action="store_true")
    parser.add_argument("--data-dir", default=str(ROOT / "data"))
    parser.add_argument("--output", default=str(ROOT / "data/unified-observation-index.json"))
    args = parser.parse_args()
    if args.self_test:
        self_test()
        return
    index = build(args.data_dir)
    if index["counts"]["indexed_records"] < 10000:
        raise ValueError("Snapshot unexpectedly small: refusing to replace prior unified index")
    out = Path(args.output)
    old = out.read_bytes() if out.exists() else None
    serialized = (json.dumps(index, separators=(",", ":"), ensure_ascii=False) + "\n").encode("utf-8")
    if len(serialized) > 6_000_000:
        raise ValueError("Index exceeds lightweight GitHub Pages output limit")
    if old != serialized:
        atomic(out, index)
    print(json.dumps(index["counts"], indent=2))


if __name__ == "__main__":
    main()
