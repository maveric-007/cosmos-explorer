# Cross-survey galaxy comparison — fiducial-radius exploratory probe (2026-10-19)

**Research question:** O-01 (dark matter vs incomplete gravity). **Status:** One newly calculated **cross-survey, single-radius** check; NOT replication of full SPARC radial diagnostics and NOT model discrimination.

## Observations and exact provenance

- Primary scientific paper: Santos-Santos et al. (2020), [Baryonic clues to the puzzling diversity of dwarf galaxy rotation curves](https://doi.org/10.1093/mnras/staa1072).
- Official catalog: CDS/VizieR [J/MNRAS/495/58, Table A1](https://cdsarc.cds.unistra.fr/viz-bin/cat/J/MNRAS/495/58) (160 original catalog rows). [CDS byte specification](https://cdsarc.cds.unistra.fr/viz-bin/ReadMe/J/MNRAS/495/58?format=html).
- Input actually retrieved through connected GitHub: [original fixed-width table mirror, pinned revision](https://github.com/dp-web4/Synchronism/blob/1fe4a0f1193b563ed02796460b986256fc390650/data/little_things/tablea1.dat), Git blob SHA `3d8839e658c84002387273755e21237191fd7d48`. **Source fidelity relative to the live official CDS download not independently byte-verified.**
- Parsed **160 distinct listed galaxies**, with source flags: **141 SPARC (S), 11 LITTLE THINGS (LT), 2 THINGS (TH), 2 Adams et al. (A), 4 Relatores et al. (R)**. The **19 non-SPARC rows** supply additional catalog-lineage evidence; they are NOT 160 independent new galaxies. Published compilation resolves survey duplication by preferring SPARC when a galaxy appears in multiple surveys.
- Unlike the earlier [3,166-radius SPARC run](SPARC-Distance-vs-Acceleration-Probe-2026-10-19.md), the catalog has **one specified fiducial rotation measurement per galaxy** and **no full radial gas/disk/bulge component curves or gas fractions**. Do not imply a point-by-point replication of the earlier SPARC method.

**Executable reproduction:** [cross_survey_fiducial_2026-10-19.py](cross_survey_fiducial_2026-10-19.py) was committed to `main` on 2026-10-19 (commit `5b6888aa07c5734dcf55bf4ee02224ee3ddb754f`). It accepts the original fixed-width `tablea1.dat` from the pinned source, verifies its Git blob hash, and calculates the four catalog splits, prediction errors, fixed benchmarks, and coarse matched pairs. **The exact committed script has not yet been run end-to-end against the catalog in the execution environment.** The numerical results below were independently computed during the interactive analysis. Do not call the script reproduction validated until its results match the table.

## Reproduction equations, units and analysis

For each fixed-width row, use `Vmax`, `Vfid`, `Vbfid`, `Mbar`, `rbhalf`, `Sample` according to CDS ReadMe. Radius in kpc, velocity in km/s:
```
r_fid = 2 * (Vmax/70)    [kpc]
g_obs = Vfid^2 / r_fid  [km^2 s^-2 kpc^-1] * 1e6 / 3.085677581491367e19 [m^-1 kpc]
g_bar = Vbfid^2 / r_fid [same conversion]
y = log10(g_obs/g_bar)
x_radius = log10(r_fid/kpc)
x_accel = log10((1e-10 m/s^2)/g_bar)
```
Fit least-squares models `y ~ 1`, `y ~ 1+x_radius`, `y ~ 1+x_accel` and `y ~ 1+x_radius+x_accel`. Entire galaxies are held out: sort identifiers using JavaScript `localeCompare`, assign five deterministic folds by sorted index mod 5, report root mean square test residual in log10 gravity ratio (dex) across galaxies, each with one point. Separately report fixed baryon-only `y_pred=0` and the **published-form illustration** `g_pred=g_bar/(1-exp(-sqrt(g_bar/a0)))` with `a0=1.2e-10 m/s^2` (not fitted). These are exploratory statistics, not physically fitted dark-halo-versus-MOND likelihood models. No measurement uncertainty / correlated covariance propagation applied.

## Actual first-pass calculations (2026-10-19)

**Five-fold held-out error; lower is better (dex):**

| Source subset | Galaxies | Constant | Radius | Acceleration | Both | Baryons-only fixed | Published-form RAR fixed |
|---|---:|---:|---:|---:|---:|---:|---:|
| Full 2020 compilation | 160 | 0.32018 | 0.30411 | 0.23549 | 0.17522 | 0.54747 | 0.24126 |
| Compilation SPARC-labeled only | 141 | 0.30202 | 0.28812 | 0.22450 | 0.17368 | 0.51394 | 0.22830 |
| **Non-SPARC source flags combined** | **19** | **0.38419** | **0.40533** | **0.34266** | **0.22544** | **0.75089** | **0.32155** |
| LITTLE THINGS flag only | 11 | 0.43538 | 0.40211 | 0.38368 | 0.28347 | 0.79761 | 0.39272 |

**Interpretation:** In the 19 non-SPARC galaxies, weak baryonic acceleration predicts the gravity discrepancy better than radius alone, while adding radius reduces error further. **This contrasts with our strict 93-galaxy SPARC test where adding radius worsened held-out prediction.** These cannot be directly compared as a physical radius effect: the small 19-galaxy sample is heterogeneous, its `r_fid` is defined by `Vmax`, and its single-radius calculation differs from the earlier full radial tests. A two-predictor fit on only 19 galaxies is unstable; changing fold assignments or survey composition may alter the result. This is a **flag for additional validation**, not proof of new physics.

**Coarse matched distribution diagnostic** (NOT a repeat of original matched-SPARC protocol): match mass within 0.10 dex, baryonic half-mass radius factor >=2, no reuse of galaxies; pair priority closest total mass then greatest half-mass-radius difference. **No gas-fraction control is possible.** At each galaxy's own `r_fid` (not same absolute/relative radius):

| Sample | Nonoverlapping pairs | Larger half-mass radius gives lower baryonic acceleration | Larger half-mass radius gives larger mismatch |
|---|---:|---:|---:|
| All 160 | 44 | 42 | 29 |
| SPARC-flagged 141 | 38 | 37 | 22 |
| Non-SPARC 19 | 1 | 0 | 1 |
| LITTLE THINGS 11 | 1 | 0 | 1 |

**Caution:** These pairs lack matched gas fraction and directly comparable radial sampling. They cannot substitute for [our original 22 strict SPARC disk-scale pair results](SPARC-Mass-Distribution-Probe-2026-10-19.md), much less establish a physical cause. No p-value or uncertainty propagation claimed.

## Multi-source inventory and work status

| Dataset | Observations required | Verified availability | Current analysis status |
|---|---|---|---|
| SPARC | Full observed and modeled baryonic radial curves, galaxy metadata | Existing pinned mirror, 175 parent sample | **Full radial distance test and 22-pair distribution test completed previously**, reproducible notes/code linked above |
| Santos-Santos 2020 mixed catalog | One `Vfid`, `Vbfid`, `Mbar`, `rbhalf` per galaxy | 160 rows; 19 non-SPARC | **Single-fiducial cross-survey check calculated here**, not full replication |
| LITTLE THINGS (Oh et al. 2015) | Full dwarf rotation curves plus baryon component profiles | [CDS J/AJ/149/180](https://vizier.cds.unistra.fr/viz-bin/VizieR?-source=J/AJ/149/180): 26 galaxies; `rotdmbar` 1,716 rows includes plotted *Data/Model* and should not be misread as individual gas/star velocity terms | **11 single-point rows above; full radial baryonic profile check outstanding** |
| THINGS (de Blok et al. 2008) | 19 high-resolution galaxy rotation/mass models | [Publication](https://doi.org/10.1088/0004-6256/136/6/2648) | **2 single-point non-overlap rows above; full radial replication outstanding** |
| GHASP | H-alpha galaxy rotation profiles plus gas/star mass assumptions | Needs confirmed machine-readable component profiles and harmonization | **Not calculated** |
| WALLABY Pilot DR2 | H I rotation curves, surface density and matched stellar photometry | [WALLABY public DR2](https://wallaby-survey.org/data/data-pilot-survey-dr2/): 126 resolved kinematic models, but **not automatically full stellar/gas mass models** | **Not calculated** |
| Gaia, lensing clusters, Planck, DESI, JPL Horizons | Independent gravity tests at other scales | Refer to [research charter](Gravity-Research.md) | **Not covered by galaxy-only calculations; separate observables/models required** |

## Remaining verification before O-01 conclusion

- [ ] Cross-check mirrored 160-row input against official CDS byte-for-byte and pin its SHA-256.
- [ ] Run the same complete per-radius equations on original LITTLE THINGS / THINGS / GHASP / WALLABY **only after establishing suitable baryonic component profiles**, survey-specific quality cuts, errors and non-overlapping galaxy IDs. Avoid artificially inflating sample sizes.
- [ ] Fit physical NFW/cored-halo versus published MOND models using common nuisance parameters and meaningful independent holdouts, then assess independent lensing, cosmology and Solar System constraints.
- [ ] Correctly quantify missing molecular/hot/ionized/circumgalactic matter before concluding incomplete mass accounting can or cannot explain discrepancies.
- [ ] Propagate errors and repeat robustness checks using alternate folds and source classifications.

**Scientific status: O-01 remains OPEN.** No new force or conclusion about the identity of dark matter is established. No automated task or schedule created.
