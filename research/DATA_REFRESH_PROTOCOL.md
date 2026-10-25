# Astronomical Data Refresh and Provenance Protocol

**Designed 2026-10-24. Implementation status: DOCUMENTED, NOT SCHEDULED OR RUNNING.** No claim of complete source ingestion, automated polling, data verification, or new publication until logs and runs exist.

## Why a daily check, not a daily full re-download

A publisher website update is not necessarily a data release; likewise observations can be reprocessed without a new paper. The aim is a daily source *change check* where supported, followed by scoped, reproducible downloads **only when independently verified release metadata or hashes change**. Not every publisher provides a machine-readable version, ETag, DOI release timestamp, or file checksum. Record the absence explicitly.

## Source registry record — required fields

| Field | Description |
|---|---|
| `source_id, official_url, data_license, category` | Official provider identity, authoritative endpoint, reuse limits |
| `release_id, published_at, observation_epoch` | **Different** facts: release/version, source release date, observation date or interval |
| `last_checked_at, check_status, check_method` | Actual network check timestamp, success/no change/changed/failure/unsupported, API/ETag/manifest/HEAD/hash/manual |
| `remote_digest, remote_etag, last_modified_header` | Evidence of external changes where supported; not universal proof content changed |
| `last_retrieved_at, imported_release, imported_at` | Exact staged bytes and last successfully validated import |
| `source_sha256, row_count, unit_schema, query, quality_filter` | Immutable input provenance and quality gate |
| `derived_output_sha256, code_commit, transform_params, model_version` | Trace back to every rendered or studied result |
| `health, failure_reason, regression_check` | Fallback conditions and verification trail |

Keep **three dates visibly separate**: `last_checked_at`, `published_at` for the underlying publisher release, and `imported_at` for successful Cosmos ingestion. A “no changes” result refers only to the scope checked, not all records at the source.

## Refresh lifecycle

1. Register authoritative catalog endpoint and appropriate rate/terms, plus exact scoped query. Current candidates: ESA Gaia, NASA Exoplanet Archive, JPL Horizons/small-body databases, MPC, NEOWISE, HI4PI gas, Planck, DESI, GALAH, APOGEE, LAMOST, CDS, etc. See [source inventory](../data/ASTRONOMICAL_DATASETS.md). Not every source will be polled with the same method.
2. Daily scheduled check when/if separately implemented: fetch published release metadata, relevant manifest or stable file hash using polite retries, caching and API request limits. Record timestamp, method, remote version and success/failure.
3. When a release changes, stage **new** files separately, check checksum, archive source URI and method. Do not replace current rendering data yet.
4. Validate schema/column names, units, data frame and epoch; unique IDs; coordinates/velocities and covariance; row counts and joins; missing radial velocities; source license. Rebuild only affected bounded subsets, keeping previous prepared data.
5. Recompute dependent scientific outputs with versioned code; run cross-survey regression / holdout / invariants (e.g., Galactic origin, epoch transformation, no negative distances). Publish a new immutable product only when validation succeeds.
6. Promote output to GitHub Pages only after scientific and browser QA. On error or unresolved discrepancy, **continue serving prior validated version** and log the failure with exact source.
7. Produce append-only run manifest and preserve release history; do not label “up to date” merely because the polling request succeeded.

## Operational controls

- **No enormous catalogs in the Pages repository:** leave raw Gaia/SPARC/Planck data in an external versioned data workspace or publish a bounded curated derivative as needed with licenses and proper citations.
- **Avoid conflating “last checked” with “last published”:** a 2026-10-24 ping cannot make a Gaia 2022/2023 released data record into a 2026 observation.
- **No overwriting successful data on a transient upstream error.** Log monitoring failures distinctly from unchanged sources.
- **No bare network claims:** store response metadata, access time, source location, checksum or version ID; note service without accessible automated metadata.
- **No scheduled job exists in this repository as of 2026-10-24.** Designing this flow does not create or authorize ChatGPT scheduled reminders or other service triggers; explicitly choose GitHub Actions / external ingestion job and its secrets/data footprint before enabling.

## Status table template (NOT actual completed checks)

| Source | Last checked | Publisher release | Latest imported release | Status |
|---|---|---|---|---|
| Gaia DR3 | **Not yet checked by automated job** | DR3 published June 2022; focused update Oct 2023 | Not ingested | Await automation |
| JPL Horizons | **Not yet checked by automated job** | Ephemerides change by object/solution | App uses Swiss Ephemeris, not Horizons | Await curated extraction |
| SPARC | **Not yet checked by automated job** | Original 2016 galaxy data; source-pin hashes in archived scripts | Script-dependent studies; no standardized managed import | Reproduction outstanding |
| Other inventory sources | **Not yet checked by automated job** | Source-specific; see official provider | Not ingested wholesale | Catalog and ingestion design |

**Important:** These table cells are not proof of a 2026 live provider check.
