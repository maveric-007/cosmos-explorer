# Cosmos Explorer — Research Hub

**Canonical location:** `maveric-007/cosmos-explorer/research/` · **Consolidated:** 2026-10-24  
**Status:** Personal astronomy and gravitational-physics investigation; **not a confirmed new gravity theory**. Use `Cosmos Explorer` as a visualization and research workbench; do not confuse an illustrative display with independent physical validation.

## Begin here

1. **[Working gravity hypothesis and falsification strategy](WORKING_HYPOTHESIS.md)** — central research statement, null/comparator hypotheses, field equations, constraints, and rejection tests.
2. [Original Gravity Research charter and eleven open questions](Gravity-Research/Gravity-Research.md) — original evidence-led plan, now retained verbatim from Home.
3. [Gravity Equations and Variable Reference](Gravity-Research/Gravity-Equations-and-Variable-Reference.md) — formulas, terminology, units, assumptions and worked examples.
4. [Original dated research index / handoff](Gravity-Research/README.md) — October 19 execution checkpoint; **historical references to Home are source-date context, not current repository ownership**.
5. [JWST and dark matter evidence assessment](JWST_DARK_MATTER_EVIDENCE.md) — what new observations challenge, what they do not establish, and independent constraints.
6. [Astronomical dataset inventory](../data/ASTRONOMICAL_DATASETS.md) — catalogued authoritative sources, currently an inventory rather than bulk-ingested data.
7. [Constellation data provenance](../data/CONSTELLATION_CREDITS.md) — Hipparcos-indexed display sample and visualization limitations.
8. [Data release / refresh protocol](DATA_REFRESH_PROTOCOL.md) — last checked vs publisher released vs imported, provenance and failure gates.
9. [Migration manifest](MIGRATION_MANIFEST.md) — precise original Home paths and matching Git blob checksums.

## Archived laboratory studies (source copies intact)

### Earth controls — `research/Gravity-Research/`

- [Earth mass 91-point latitude study](Gravity-Research/Earth-Latitude-Apparent-Mass-Sweep-2026-10-15.md) and [CSV](Gravity-Research/Earth-Latitude-Apparent-Mass-Sweep-2026-10-15.csv).
- [WGS 84 Gauss flux 1-degree model consistency experiment](Gravity-Research/Earth-Mass-Gauss-Flux-1-Degree-Grid-2026-10-15.md), [180-band CSV](Gravity-Research/Earth-Mass-Gauss-Flux-Latitude-Bands-2026-10-15.csv), and [reproduction script](Gravity-Research/earth_mass_gauss_flux.py). **Not independent measurements of Earth mass**.

### Galaxy tests — `research/Gravity-Research/`

- [SPARC radius versus acceleration diagnostic](Gravity-Research/SPARC-Distance-vs-Acceleration-Probe-2026-10-19.md) and [script](Gravity-Research/sparc_distance_acceleration_2026-10-19.py).
- [SPARC distributed-mass matched galaxy diagnostic](Gravity-Research/SPARC-Mass-Distribution-Probe-2026-10-19.md) and [script](Gravity-Research/sparc_mass_distribution_2026-10-19.py).
- [Cross-survey fiducial-radius exploratory comparison](Gravity-Research/Cross-Survey-Fiducial-Probe-2026-10-19.md) and [script](Gravity-Research/cross_survey_fiducial_2026-10-19.py): **reported comparisons not yet reproduced with exact pinned 160-row catalog by running the committed script**.

## Scientific interpretation and standing decisions

- Treat measurement, derived quantity, inferred physical model and speculation as distinct data types. Preserve raw source, publication version, observation epoch, uncertainties, coordinate frame and calculation code. Never silently turn unknown mass or velocity into zero.
- Model all relevant matter, not only luminous stars, but quantify its gravitational impact and plausible upper bound before treating it as the source of a discrepancy. A sky catalog is not an exhaustive baryonic mass census.
- For Galactic analysis use Sagittarius A* / Galactocentric origin for reference. This **does not** imply all galactic gravity arises from the central black hole; the Milky Way's distributed mass dominates the Solar orbit. Do not treat constellations as gravitationally bound systems.
- Compare constrained baryonic-only, baryons+dark halos, and published modified-gravity/dynamics calculations using consistent input and held-out tests. Galaxy curves alone are not sufficient; preserve lensing, cluster, CMB, BBN and Solar System constraints.
- Do not claim new gravitational law, evidence of universal gravity shielding, or disproven dark matter without independent reproducible discriminating measurements.
- The Solar System JPL data and cosmology source catalogs are distinct from the **mixed-fidelity, illustrative** layers in [the viewer](../index.html). Do not infer that a catalogue listed here has been ingested or revalidated merely because it is named.
- **NASA exoplanet hosts are now an ingested searchable dataset**: 6,451 confirmed planets, 4,847 systems on 2026-10-25, with an active daily validated import. See [data status](../data/exoplanet-sync-status.json), [all-star inclusion requirement](../docs/STAR_SYSTEM_SCOPE.md), and [refresh protocol](DATA_REFRESH_PROTOCOL.md). All other source-inventory items require separately verified extraction/check schedules; Gaia-scale all-star catalog is not yet implemented.

## Next scientifically meaningful step

**O-01 remains open.** Reproduce and pin the exact SPARC and cross-survey inputs, then build a quality-filtered Gaia 6D sample in the Sagittarius A*-centered frame with released-distance posterior/covariance, supplemented by gas, dust and small-body catalogs where relevant. Fit reference gravitational models and report out-of-sample uncertainties.

## Ownership and historical copies

This research originated in [Home/Projects/Gravity-Research](https://github.com/maveric-007/Home/tree/main/Projects/Gravity-Research) in October 2026 and had earlier historical copies in `software-projects/projects/`. **This Cosmos repository is the new authoritative working home.** Dated original files are reproduced *byte-for-byte*; their old HOME ownership statements are historical. The software-projects repository should keep a portfolio pointer only. GitHub history retains the older context.
