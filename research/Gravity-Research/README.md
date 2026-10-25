# Gravity Research

**Personal project** · Owner: HOME · Stage: Research idea, not a validated theory.

We are investigating whether observational gravitational discrepancies are best explained by additional mass, changes to gravitational laws, measurement/systematic errors, or some combination. We deliberately try to **prove our hypotheses wrong** as well as right.

## Research execution notes — avoid repeating known blockers (2026-10-19)

**Read this before acquiring data, writing a script, or claiming that a test has been reproduced.** These notes document problems we encountered, how we worked around them, and what remains unverified.

- **Known environment constraint:** The ChatGPT Python execution environment used during the October 19, 2026 session does **not permit ordinary outbound internet downloads**. This is an environment limitation, **not** evidence that an astronomical dataset, website, or GitHub is unavailable. Access capabilities can differ across sessions/tools, so verify the actual environment rather than assuming direct internet access or an outage.
- **Preferred workaround:** Retrieve source files via an available authorized web or connected GitHub tool; use a current conversation attachment or a supported materialization/export mechanism to get bytes into the execution environment. Use Python/container tools for **local** calculations. If bytes cannot be transferred into that runtime, use an actually available execution path or explicitly record that end-to-end reproduction is pending. Do **not** waste time repeatedly attempting the same blocked direct Python download.
- **Provenance and reproducibility:** Pin the release, source URL, file format, schema, units, sample cuts, and a verifiable hash. Treat an independently retrieved mirror as a mirror until checked against the original scientific catalog. Deduplicate cross-survey galaxies; don't confuse a single fiducial point with a complete rotation curve.
- **Honest status gates:** Distinguish (1) calculations performed interactively, (2) code committed to GitHub, (3) exact committed code **actually executed** on original/pinned inputs, and (4) independent source verification. A syntax check, GitHub commit, or remote file read is **not** a successful end-to-end reproduction. Confirm output values and sample counts before labeling it validated.
- **Record new friction here:** Whenever a retrieval, permission, execution, data-format, or validation obstacle is encountered, record the error, affected tool/environment, reliable workaround, and remaining follow-up in this README or the linked study report. Review these notes at the beginning of later sessions so the same obstacle is not rediscovered.

**Specific open validation:** The [cross-survey fiducial-radius report](Cross-Survey-Fiducial-Probe-2026-10-19.md) and [committed Python analysis script](cross_survey_fiducial_2026-10-19.py) are in the repository, but the report records that the **exact committed script has not yet been executed end-to-end against the 160-row pinned catalog**. Preserve that distinction until tested. **Question O-01 remains open.**

## Session checkpoint — paused October 19, 2026

**Status: Research paused for today by user request; O-01 remains OPEN.** The gravity question is not settled. Resume from this verified checkpoint rather than restarting completed tests:

- **Committed and verified on GitHub:** the full SPARC radius/acceleration and matched-distribution reports and scripts; the [cross-survey fiducial analysis report](Cross-Survey-Fiducial-Probe-2026-10-19.md) and [Python analysis script](cross_survey_fiducial_2026-10-19.py). The latest cross-survey results use one point per galaxy in a 160-galaxy compilation, including 19 non-SPARC source flags; these do not replace full rotation-curve work.
- **New permanent lesson:** use this README's data-access notes at the beginning of the next session. Do not try direct Python internet downloads repeatedly. Fetch catalog bytes through an available authorized retrieval route, verify the pinned input hash, and use a local execution environment.
- **First outstanding verification:** execute the **exact committed** cross-survey script against the pinned 160-row original fixed-width catalog and compare all four splits and matched-pair counts with the report. A committed file or syntax check alone is insufficient. If unavailable, preserve the unverified status; do not invent results.
- **Then continue O-01:** retrieve suitable full radial baryonic mass/rotation models from other independent surveys, deduplicate shared galaxies, perform physical halo-versus-modified-gravity fits, propagate uncertainties, and test independent non-galaxy constraints. Nothing about Question 2 is authorized by this pause.
- **No new reminder, calendar event, automated run, or ChatGPT task is authorized.** This is a durable Markdown handoff only.

## Start here

1. [Gravity Research — Open Questions and Test Plan](Gravity-Research.md) — our original questions, 11 annotated open problems, scientific datasets, experiment roadmap, and checklist.
2. [Gravity Equations and Variable Reference](Gravity-Equations-and-Variable-Reference.md) — equations, definition of each symbol, sub-equations, units, assumptions, numerical examples, and experimental tests.

## Public astronomical data starting points

- [SPARC galaxy rotation curves](https://astroweb.case.edu/SPARC/) — our starting galaxy analysis.
- [NASA/JPL Horizons](https://ssd.jpl.nasa.gov/horizons/) — Earth–Sun and planetary dynamics control.
- [Gaia](https://gea.esac.esa.int/archive/), [Planck](https://pla.esac.esa.int/), and [DESI](https://data.desi.lbl.gov/doc/) — independent follow-up datasets.

## Recent experiments

- [**Earth Mass — 1° gravitational-flux audit (2026-10-15)**](Earth-Mass-Gauss-Flux-1-Degree-Grid-2026-10-15.md) — contrasts traditional NGA WGS 84 and JPL Earth-mass estimates with our original 91-latitude mean and corrected 180-band flux; annotated equations, constants, 90 north/south latitude-pair ledger, and CSV. **WGS 84 model verification, not independent mass observation.**

- [Earth apparent-mass sweep by latitude — 2026-10-15](Earth-Latitude-Apparent-Mass-Sweep-2026-10-15.md) — full 91-row 0°–90° WGS 84 model table, equations, unweighted apparent-mass mean, and reference-mass comparison. **This is a simplified model diagnostic, not an independently measured Earth mass.**

## Galaxy rotation: first distance-versus-acceleration diagnostic (2026-10-19)

- [SPARC radius versus weak-acceleration probe — methods, results, uncertainty, and follow-up tests](SPARC-Distance-vs-Acceleration-Probe-2026-10-19.md): evaluated 3,166 observed radial points across 153 quality-filtered galaxies. Weak baryonic acceleration predicts the mismatch much better than radius alone; radius's small extra contribution disappears on a stricter high-quality subset. **Preliminary result only: Question O-01 remains OPEN.**
- [Reproduction script (Python 3 standard library)](sparc_distance_acceleration_2026-10-19.py): refetch original SPARC mass-model and galaxy-sample tables from a version-documented public mirror; no large third-party raw files committed. Execute on home/personal equipment.

## Next action

Reproduce published SPARC galaxy calculations and a transparent Earth–Sun baseline **before proposing a new force**. Keep any future code and large raw datasets in a dedicated personal repository or local data workspace; keep the canonical explanatory notes here for Obsidian.

There is **no scheduled task or automation** associated with this project.

**GitHub notes location:** `maveric-007/Home/Projects/Gravity-Research/`. If this folder does not appear in Obsidian on your phone, the Home vault has not yet received these new GitHub commits; sync/pull the vault through your established sync workflow.
