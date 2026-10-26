# Cosmos Explorer — Project Instructions

## Ownership and purpose

Dedicated personal research/code repository for the **Cosmos Explorer 3D astronomy visualization** and the **Gravity Research** evidence-testing program. Its research originated in `maveric-007/Home/Projects/Gravity-Research/`, was transferred with matching SHA on 2026-10-24, and is now **canonical here**. Home and software-projects hold only links, not independent research edits.

## Canonical scientific entrypoints

- [Research hub](research/README.md)
- [Current falsifiable gravity hypothesis](research/WORKING_HYPOTHESIS.md)
- [Original eleven open research questions](research/Gravity-Research/Gravity-Research.md)
- [Current open questions O-12–O-15](research/OPEN_QUESTIONS.md) — quantum energy, conservation-law domain, Newtonian limits, mass-energy accounting, and black-hole radiation/information, all unvalidated.
- [Equations reference](research/Gravity-Research/Gravity-Equations-and-Variable-Reference.md)
- [Original session/validation blockers](research/Gravity-Research/README.md) — dated historical baseline
- [Source catalog](data/ASTRONOMICAL_DATASETS.md) and [data-refresh protocol](research/DATA_REFRESH_PROTOCOL.md)
- [Migration manifest / exact SHA origins](research/MIGRATION_MANIFEST.md)

## Scientific claims — hard gates

1. Never label a **research hypothesis** a validated new gravitational theory. Retain and actively test competing baryonic, nonbaryonic dark-matter, systematic-error and modified-dynamics explanations. Gravitational potentials depend on 3D mass distributions; Sagittarius A* is an adopted Galactocentric origin, not the exclusive mass source.
2. Distinguish **directly measured observables**, estimates/inferences, physical-model predictions and illustrative rendered placements. Preserve epoch, instrument, units, uncertainties/covariance, dataset release, source ID, quality flags, license, original input hash, code version and derived output hash.
3. No missing value silently becomes zero or fact. Unknown faint bodies, stellar companions, molecular/ionized gas and dust may add gravity but must be bounded by independent data before being assigned a free mass. Stellar radius is not gravitating mass by itself.
4. The original SPARC Earth/Gauss and galaxy reports remain dated study artifacts. Retain O-01 **OPEN**; the cross-survey 160-row pinned reproducibility gap in the original README remains until the **exact committed script and pinned bytes** are executed and verified. GitHub commit and syntax review are not runtime scientific validation.
5. Tests must compare the already published SPARC and JPL baselines before constructing any new force law. Use holdout galaxies and independent Solar System, cluster lensing, CMB/BBN and other relativistic constraints. Never treat unexpected JWST discoveries as proof of a dark-matter retraction without an actual identified formal retraction.
6. Don't silently rewrite previous dated findings or scripts to match a future preferred theory; new versions need documented comparison results and reproducibility checks.

## Data architecture, rendering and updates

- `index.html` and curated `data/` products are a lightweight iPhone/Safari GitHub Pages application; massive raw Gaia/other astronomy surveys should not be uploaded into this public repo. Existing JS astronomical simulation uses mixed measured, approximate and schematic layers. No claim of general-relativistic N-body integration.
- Data changes require a source/provenance manifest; check if a provider has actually published a new **underlying release**, not only altered a webpage. Record three distinct dates: last checked, last provider release, last successful import. Stage+validate changes; keep the last known good visualization on failure.
- **As of 2026-10-25**, `.github/workflows/exoplanets.yml` is active: daily NASA Exoplanet Archive PSCompPars fetch/validation via `scripts/sync_exoplanets.py`, with compact verified output and separated `last_checked_utc` and `last_imported_utc`. Other astronomy source refreshes are **not** running; see `research/DATA_REFRESH_PROTOCOL.md`. A completed Action validates a data ingestion, not the browser's end-to-end scientific rendering.
- Static projection of constellation sky figures is separate from their depth-resolved J2000 positions. Do not infer gravitational linkage or future star trajectories from projected shape.
- **Mandatory star/system coverage**: include every star or stellar system with available source-backed records in the supported catalogs, not just selected bright stars or those forming constellations. All NASA-confirmed planetary hosts are searchable independently of local scene distance or constellation figure. Planet candidates and no-detection cases require explicit status; unknown orbital elements, masses, ages or unmeasured companions must never be invented. [Authoritative inclusion standard](docs/STAR_SYSTEM_SCOPE.md). The 7,922-star HYG sample is **not** exhaustive Gaia-scale coverage.
- Verify desktop/mobile 3D interactions, URLs, data fetches, astronomy units and labels after changes; separate successful Pages deployment from actual iPhone/Safari testing.
- Use full source repositories/instructions before changes and preserve original Git history when relocating references.

## Security and scope

This is a public personal research repository. No PeopleTec/DoD/source customer data, personal medical/financial information, private home details, access tokens or copyrighted bulk datasets with incompatible licenses. Keep globally applicable instructions in the canonical general operating-instructions repository; this file owns Cosmos-only scientific and implementation standards.
