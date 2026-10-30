# Astronomical Data Refresh and Provenance Protocol

**Designed 2026-10-24; partially operational 2026-10-25.** NASA Exoplanet Archive PSCompPars is now checked on a **daily GitHub Actions schedule**, using a validated source fetch and versioned compact snapshot. **All other listed surveys remain inventory-only unless individually verified otherwise.** No claim of full Gaia, stellar/ISM/galaxy ingestion, or scientifically validated gravity simulation.

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
- **Active NASA schedule from 2026-10-25**: `.github/workflows/exoplanets.yml`, daily at 06:17 UTC with manual dispatch. It fetches all confirmed PSCompPars planet rows, tests invariant checks, keeps failed fetches from replacing previous data, and records SHA256 and timestamps separately. The NASA TAP export does not provide an authoritative publisher release date in the current query, so it remains **not supplied**. Other inventory sources still have **no enabled polling**. A GitHub Actions bot commit may not retrigger Pages; the viewer loads the latest raw GitHub catalog first, then falls back to the Pages-local snapshot.

## Verified first run — NASA only (2026-10-25)

The actual [GitHub Actions run](https://github.com/maveric-007/cosmos-explorer/actions/runs/40211923343) succeeded; archived status is [data/exoplanet-sync-status.json](../data/exoplanet-sync-status.json).

| Field | Recorded value |
|---|---|
| Check/import UTC | **2026-10-25T16:29:39Z** |
| Dataset | NASA Exoplanet Archive `pscomppars` confirmed composite |
| Confirmed planet rows | **6,451** |
| Host systems | **4,847** |
| Host systems with usable 3D sky position and distance | **4,819** |
| Planets with archive semimajor-axis value | **5,956** |
| Publisher release time | **Unknown from TAP export** |
| Source CSV SHA256 | `08cd41275386ba350d63ffc7586e278e59ac1797c9d73b962b2282bd858d604a` |
| Normalized output SHA256 | `765b2ddba581f0639a945194ee68d23cfc6fc7cef8b3ce23c5da68a621df2b3f` |

This is one real successful provider check and does not imply historical observations were taken in 2026.

## Other sources (not yet automatically checked)

| Source | Last checked | Publisher release | Latest imported release | Status |
|---|---|---|---|---|
| Gaia DR3 | **Not yet checked by automated job** | DR3 published June 2022; focused update Oct 2023 | Not ingested | Await automation |
| JPL Horizons | **Not yet checked by automated job** | Ephemerides change by object/solution | App uses Swiss Ephemeris, not Horizons | Await curated extraction |
| SPARC | **Not yet checked by automated job** | Original 2016 galaxy data; source-pin hashes in archived scripts | Script-dependent studies; no standardized managed import | Reproduction outstanding |
| Other inventory sources | **Not yet checked by automated job** | Source-specific; see official provider | Not ingested wholesale | Catalog and ingestion design |

**Important:** These table cells are not proof of a 2026 live provider check.

## Verified import and coverage update — 2026-10-30

**Source of truth for live timestamps:** [data/source-refresh-status.json](../data/source-refresh-status.json), generated by [scripts/check_sources.py](../scripts/check_sources.py) through [the metadata/import reconciliation workflow](../.github/workflows/sources.yml). **Do not copy the dates in this document forward as current**. Last checked, last successful import, and publisher release are separate values. An endpoint returning HTTP 200 has *not* imported any astronomy records.

### Verified new imports

- **NEOWISE V2:** [data/neowise-sample.json](../data/neowise-sample.json) contains **200** source-backed asteroid physical-property fits, with measured/fixed diameter treatment and albedo/error fields; [run 41063730698](https://github.com/maveric-007/cosmos-explorer/actions/runs/41063730698) succeeded on 2026-10-30, import recorded at **13:30:13 UTC**. [Audit](../data/neowise-sync-status.json), [ingester](../scripts/sync_neowise.py), [weekly workflow](../.github/workflows/neowise.yml). No body mass inferred from diameter.
- **Minor Planet Center:** [data/mpc-orbits-sample.json](../data/mpc-orbits-sample.json) records **four** actual MPC orbit responses for Ceres, Vesta, Bennu, and Apophis; [run 41063854649](https://github.com/maveric-007/cosmos-explorer/actions/runs/41063854649) succeeded and recorded import at **13:30:53 UTC**. [Audit](../data/mpc-orbits-sync-status.json), [ingester](../scripts/sync_mpc_orbits.py), [weekly workflow](../.github/workflows/mpc_orbits.yml). These are orbital model/fit solutions with their own epoch/conventions, **not** observed instantaneous sky coordinates or a complete MPCORB extract.
- The [unified observation index](../data/unified-observation-index.json) was rebuilt with both new kinds in distinct source-scoped categories, without artificial source-object merges or unknown physical masses. [Builder run 41064021307](https://github.com/maveric-007/cosmos-explorer/actions/runs/41064021307) succeeded with **15,285 indexed source records** and **137 published-ID association links**. The count is **not** 15,285 unique astrophysical bodies. The index is **not yet the primary WebGL render input**.
- The [source metadata audit run 41064190918](https://github.com/maveric-007/cosmos-explorer/actions/runs/41064190918) passed after adding actual imported timestamps from MPC, NEOWISE, JPL, and optional VizieR manifests. Source status is derived from on-disk validated data, not just importer existence.

### Remaining sources are not all the same type

As of this update, the 23-source registry comprises **1 full confirmed-planet composite import** (NASA; *not* all candidate stars), **9 validated bounded survey/ephemeris imports**, **4 bundled/static source derivatives**, **2 configured but failed GALAH/APOGEE imports**, **6 not ingested services or maps** (SIMBAD, VizieR, PDS, HI4PI, Bayestar, Planck), and **1 SPARC research-only source**. The appropriate next operations are:

| Sources | Current boundary | Required next implementation |
|---|---|---|
| **GALAH DR4 derivative; APOGEE DR17** | Their VizieR TAP hostname **and three independent ASU mirrors timed out from GitHub Actions** on 2026-10-30; [run 41062870538](https://github.com/maveric-007/cosmos-explorer/actions/runs/41062870538). Importer local parser tests passed; there is **no committed validated GALAH/APOGEE snapshot**. | Use authenticated/accessible **Data Central's GALAH original allStar release** or **SDSS DR17 SkyServer** directly, select a bounded quality-controlled set, verify IDs/units, re-run and commit; do not mark ingested until result is verified. |
| **SIMBAD and VizieR** | These are name/crossmatch/catalog aggregation services, not one finite single release to download wholesale. | Query target identifiers against registered surveys, preserve per-result original catalog and alias basis; no proximity-only merging. |
| **NASA PDS Small Bodies Node** | Federation of distinct archived products; no single uniform planetary dataset. | Choose versioned PDS bundle(s), enforce usage/licensing and sample/format validation; link to JPL/MPC by published identifiers. |
| **HI4PI hydrogen survey, Bayestar dust, Planck legacy maps** | Multidimensional maps (velocity channels, distance/posteriors, multi-frequency HEALPix/FITS), not stellar position rows. | Retrieve official versioned maps to an external science-data workspace; preserve frames, units, uncertainty, beams, and survey model assumptions. Produce small map tiles/pyramids for the viewer **only after** scientific QC. |
| **SPARC** | Existing research code/links, but a reproducible pinned source-plus-transform run remains open. | Validate original 175-galaxy and rotation-curve products with license/provenance, reproduce the pinned 160-row experiment, then publish independent derived summary products. No new-gravity conclusion implied. |
| **AllWISE, 2MASS, Gaia, LAMOST, DESI** | Bounded snapshots are imported; published surveys are vastly larger than their browser subsets. | Build partitioned, checkpointed full-source processing in external storage; publish only quality-controlled compact search indexes and progressive visible regions. |

**Scaling requirement:** *All catalog records with source-backed identifiers* remains the research coverage objective, but hosting all physical raw survey files in GitHub Pages is not tenable. A full-census claim requires external partitioned storage, a measured ingestion manifest, licensing review, durable checkpoints and checksums, and source-specific success/failure accounting. **Do not count configured jobs, source webpage probes, or single 200-row samples as whole-catalog coverage.** This document is a progress/architecture checkpoint, **not acceptance that all sources have been imported or displayed**.
