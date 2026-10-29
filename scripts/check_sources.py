#!/usr/bin/env python3
"""Per-provider astronomy catalog monitoring. Network availability != new data release.

NASA PSCompPars has its own validated ingest workflow. For all other sources,
this checks the provider's documented metadata/documentation entrypoint with a
bounded request. It does NOT download, claim to validate, or replace massive
survey catalogs. Unknown release/import timestamps remain null.
"""
import argparse
import datetime as dt
import json
import pathlib
import urllib.error
import urllib.request

BASE = pathlib.Path(__file__).resolve().parents[1]
REGISTRY = BASE / "data/source-registry.json"
STATUS = BASE / "data/source-refresh-status.json"
NASA = BASE / "data/exoplanet-sync-status.json"
USER_AGENT = "CosmosExplorerCatalogAudit/1.0 (noncommercial catalog status check)"

def now_utc():
    return dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")

def probe(url, timeout=9):
    headers = {"User-Agent": USER_AGENT, "Accept": "*/*"}
    # HEAD checks only reachability and response metadata. Dynamic HTML and
    # Last-Modified are NOT publisher/catalog release information.
    for method in ("HEAD", "GET"):
        request_headers = dict(headers)
        if method == "GET":
            request_headers["Range"] = "bytes=0-0"
        req = urllib.request.Request(url, method=method, headers=request_headers)
        try:
            with urllib.request.urlopen(req, timeout=timeout) as reply:
                if method == "GET":
                    reply.read(1)
                return {"ok": True, "http_status": reply.status,
                        "remote_etag": reply.headers.get("ETag"),
                        "remote_last_modified": reply.headers.get("Last-Modified"),
                        "method": method, "error": None}
        except urllib.error.HTTPError as exc:
            if method == "HEAD" and exc.code in (405, 501):
                continue
            return {"ok": False, "http_status": exc.code, "method": method,
                    "error": "HTTP " + str(exc.code)}
        except (urllib.error.URLError, TimeoutError, OSError, ValueError) as exc:
            return {"ok": False, "http_status": None, "method": method,
                    "error": str(exc)[:180]}
    return {"ok": False, "http_status": 405, "method": "HEAD/GET",
            "error": "No supported metadata request"}

def run(registry_path=REGISTRY, status_path=STATUS, nasa_path=NASA):
    manifest = json.loads(registry_path.read_text(encoding="utf-8"))
    current = json.loads(status_path.read_text(encoding="utf-8"))
    assert manifest["schema"] == "cosmos-explorer-source-registry-v1"
    assert current["schema"] == "cosmos-explorer-source-refresh-status-v1"
    sources = manifest["sources"]
    ids = [source["id"] for source in sources]
    if len(ids) != len(set(ids)) or len(ids) < 15:
        raise ValueError("Invalid / incomplete catalog registry")
    results = current["sources"]
    for source in sources:
        key = source["id"]
        old = results.get(key, {})
        entry = dict(old)
        entry["import_state"] = source["import_state"]
        entry["method"] = source["check_method"]
        if source["check_method"] == "nasa":
            # NASA timestamps come from the independent, actually validated ingest.
            official = json.loads(nasa_path.read_text(encoding="utf-8"))
            entry.update({
                "last_checked_utc": official.get("last_checked_utc"),
                "last_successful_check_utc": official.get("last_checked_utc") if official.get("check_status") in ("unchanged", "updated") else old.get("last_successful_check_utc"),
                "last_imported_utc": official.get("last_imported_utc"),
                "publisher_release_utc": official.get("publisher_release_utc"),
                "check_status": official.get("check_status"),
                "counts": official.get("counts"),
                "error": None,
                "method": "NASA PSCompPars validated full import",
            })
        elif source["check_method"] == "gaia":
            gaia_path = BASE / "data/gaia-sync-status.json"
            if gaia_path.exists():
                official = json.loads(gaia_path.read_text(encoding="utf-8"))
                if official.get("schema") != "cosmos-explorer-gaia-sync-status-v1":
                    raise ValueError("Invalid Gaia import audit schema")
                entry.update({
                    "last_checked_utc": official.get("last_checked_utc"),
                    "last_successful_check_utc": official.get("last_checked_utc"),
                    "last_imported_utc": official.get("last_imported_utc"),
                    "publisher_release_utc": official.get("publisher_release_utc"),
                    "check_status": official.get("check_status"),
                    "count": official.get("count"),
                    "method": "ESA Gaia DR3 bounded validated sample import",
                    "import_state": "bounded_sample_ingested",
                    "error": None
                })
            else:
                entry["check_status"] = "adapter_configured_not_checked"
                entry["method"] = "Gaia bounded importer configured but not yet verified"
        elif source["check_method"] == "irsa":
            audit_file = BASE / ("data/" + key + "-sync-status.json")
            if audit_file.exists():
                official = json.loads(audit_file.read_text(encoding="utf-8"))
                if official.get("schema") != "cosmos-explorer-irsa-sync-status-v1" or official.get("source_id") != key:
                    raise ValueError("Invalid source-specific IRSA status for " + key)
                entry.update({
                    "last_checked_utc": official.get("last_checked_utc"),
                    "last_successful_check_utc": official.get("last_checked_utc"),
                    "last_imported_utc": official.get("last_imported_utc"),
                    "publisher_release_utc": official.get("publisher_release_utc"),
                    "check_status": official.get("check_status"),
                    "counts": official.get("counts"),
                    "method": "IRSA TAP bounded validated sample import",
                    "import_state": "bounded_sample_ingested",
                    "error": None
                })
            else:
                entry["check_status"] = "adapter_configured_not_imported"
                entry["method"] = "IRSA TAP adapter pending successful import"
        elif source["check_method"] in ("lamost", "desi"):
            audit_name = "lamost_dr12" if source["check_method"] == "lamost" else "desi_dr1"
            audit_path = BASE / ("data/" + audit_name + "-sync-status.json")
            expected = "cosmos-explorer-lamost-sync-status-v1" if source["check_method"] == "lamost" else "cosmos-explorer-desi-sync-status-v1"
            if audit_path.exists():
                official = json.loads(audit_path.read_text(encoding="utf-8"))
                if official.get("schema") != expected:
                    raise ValueError("Invalid catalog import status for " + audit_name)
                entry.update({
                    "last_checked_utc": official.get("last_checked_utc"),
                    "last_successful_check_utc": official.get("last_checked_utc"),
                    "last_imported_utc": official.get("last_imported_utc"),
                    "publisher_release_utc": official.get("publisher_release_utc"),
                    "check_status": official.get("check_status"),
                    "counts": official.get("counts"),
                    "method": "Verified bounded catalog import (not full survey)",
                    "import_state": "bounded_sample_ingested",
                    "error": None
                })
            else:
                entry["check_status"] = "adapter_configured_not_imported"
                entry["method"] = "Bounded importer configured; no verified data yet"
        else:
            checked = now_utc()
            outcome = probe(source["official_url"])
            entry["last_checked_utc"] = checked
            entry["check_status"] = "endpoint_reachable_release_unverified" if outcome["ok"] else "endpoint_check_failed"
            entry["last_http_status"] = outcome["http_status"]
            entry["method"] = outcome["method"] + " endpoint metadata only"
            entry["error"] = outcome["error"]
            if outcome["ok"]:
                entry["last_successful_check_utc"] = checked
                entry["remote_etag"] = outcome.get("remote_etag")
                entry["remote_last_modified"] = outcome.get("remote_last_modified")
            # Neither URL reachability nor changed HTTP metadata proves a new
            # provider scientific release. Do not fill publisher_release_utc.
            # Only an actual validated ingestion may set last_imported_utc.
        results[key] = entry
        print(key, entry["check_status"], entry.get("last_checked_utc"))
    current["generated_at_utc"] = now_utc()
    current["sources"] = {source["id"]: results[source["id"]] for source in sources}
    temporary = status_path.with_name(status_path.name + ".tmp")
    temporary.write_text(json.dumps(current, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    temporary.replace(status_path)

def self_test():
    registry = json.loads(REGISTRY.read_text(encoding="utf-8"))
    status = json.loads(STATUS.read_text(encoding="utf-8"))
    ids = [s["id"] for s in registry["sources"]]
    assert len(ids) == len(set(ids)) >= 15
    assert all(s["official_url"].startswith("https://") for s in registry["sources"])
    assert set(status["sources"]) == set(ids)
    assert all("last_checked_utc" in status["sources"][key] for key in ids)
    assert all("last_imported_utc" in status["sources"][key] for key in ids)
    assert all("publisher_release_utc" in status["sources"][key] for key in ids)
    assert status["sources"]["nasa_exoplanets"]["method"].startswith("NASA")
    print("Source registry and timestamp schema validated:", len(ids), "sources")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    if args.self_test:
        self_test()
    else:
        run()
