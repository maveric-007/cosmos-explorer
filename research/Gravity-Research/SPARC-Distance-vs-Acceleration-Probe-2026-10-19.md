# SPARC Galaxy Rotation — Does Distance Explain the Discrepancy?

**Experiment date:** 2026-10-19  
**Research item:** O-01, galaxy rotation curves / acceleration relation  
**Status:** Exploratory diagnostic; **NOT a new-gravity discovery or a comprehensive physical model comparison**.  
**Code:** [Reproduce the diagnostic](sparc_distance_acceleration_2026-10-19.py) (Python 3, standard library).  
**Source-of-truth question:** Does galactocentric radius predict the rotation discrepancy independently of ordinary-matter-predicted gravitational acceleration?

## Clarifying the "distance" question

This experiment's **distance** is orbital radius **from the galaxy center** (kpc). It is *not* the distance from Earth to a distant galaxy, nor an object simply "falling into" a galaxy. Whether an object is bound depends on the gravitational potential **and** initial velocity; a galaxy's total mass alone cannot predict its trajectory.

For an ideal exterior circular orbit around a fixed **spherical** mass, Newtonian gravity gives $v=\sqrt{GM/r}$: if distance doubles, circular speed falls by $1/\sqrt2$. But galaxy stars and gas orbit a **spatially extended, often flattened mass distribution**. Disk, gas, and any halo must be modeled with the appropriate geometry; treating a galaxy's mass as one central point is an invalid general test. Neither a galactic radius nor a low acceleration is a new force.

### Precisely stated competing hypotheses

- **H-distance:** Residuals after the modeled ordinary-matter gravity are meaningfully predicted by galactocentric radius, even after conditioning on the baryonic acceleration.
- **H-low-acceleration:** The discrepancy is better predicted by **how weak** the local baryonic gravitational acceleration becomes.
- **H-combined:** Both give stable additional held-out predictive information.
- **Null conclusion permitted:** Neither predictor identifies the physical mechanism; dark matter, modified gravity, baryonic mass systematics, and selection effects remain candidates. The inputs are not independent: $g_{bar}=v_{bar}^{2}/r$, so acceleration already contains radius mathematically.

## Original observed data and provenance

- Published SPARC mass models: Lelli, McGaugh & Schombert 2016, [original SPARC archive](https://astroweb.case.edu/SPARC/), [2016 paper](https://arxiv.org/abs/1606.09251).
- Accessed public mirror (original table format): [MassModels_Lelli2016c.mrt](https://github.com/JustinSchneider/baryonic-omega-analysis/blob/main/data/raw/MassModels_Lelli2016c.mrt), Git blob SHA `3f0ea8e3577ec9e0226e4f6a65f1019d45f1aec6`.
- Galaxy metadata and quality flags: [SPARC_Lelli2016c.mrt](https://github.com/JustinSchneider/baryonic-omega-analysis/blob/main/data/raw/SPARC_Lelli2016c.mrt), Git blob SHA `8cdfb503c58bf5f4fc6321e976f7caec6e353bf3`.
- Source inventory: 175 galaxies, 3,391 radial data rows. The primary filter retains galaxies with quality flag 1 or 2 and disk inclination >=30 degrees; positive radius, observed speed and calculated baryonic speed-squared are also required. It yields **153 distinct galaxies and 3,166 radial observations** (two invalid nonpositive baryonic model rows excluded from retained galaxies).
- These selection criteria are **not identical** to the 153-galaxy/2,693-point subset used in the published 2016 RAR paper. Do not equate our 3,166 points to that published count or imply we have reproduced all of its selection and uncertainty treatment.
- The code fetches tables from the public mirror at execution time. For rigorous future replication, preserve a vetted local copy and its byte-level checksum, confirm it matches the SPARC publication, and pin a permanent source revision; Git blob SHAs above record the versions analyzed here. No raw multi-megabyte datasets committed into Home.

## Reproducible calculation (original file column definitions)

For each observed galaxy radius $r$ (kpc), SPARC gives observed circular velocity $V_{obs}$ and modeled component circular velocities for gas, disk and bulge. With **fixed illustrative** 3.6-micron stellar mass-to-light ratios $\Upsilon_{disk}=0.5$, $\Upsilon_{bulge}=0.7$ (solar units):

$$
V_{bar}^{2} = V_{gas}|V_{gas}| + 0.5 V_{disk}^{2} + 0.7 V_{bulge}^{2}.
$$

The signed gas term is intentional: SPARC may report *negative* gas component circular-velocity contributions. The baryonic components are for mass-to-light ratio 1 and are rescaled, not independently refitted per galaxy. **Exclude** invalid nonpositive modeled $V_{bar}^2$ rather than pretending to take their logarithm.

$$
g_{obs} = V_{obs}^{2}/r,\qquad g_{bar} = V_{bar}^{2}/r,
\qquad y = \log_{10}(g_{obs}/g_{bar}).
$$

Use SI units for accelerations (1 [km/s]²/kpc = $10^6/3.085677581491367\times10^{19}$ m/s²). Predict $y$ using one or two simple linear diagnostics:

- **Radius only:** $y=a+b\log_{10}(r/\mathrm{kpc})$.
- **Weak acceleration only:** $y=a+c\log_{10}[(10^{-10}\,\mathrm{m/s}^2)/g_{bar}]$.
- **Both:** $y=a+b\log_{10}(r/\mathrm{kpc})+c\log_{10}[(10^{-10}\,\mathrm{m/s}^2)/g_{bar}]$.

A constant-only model is another reference. Fit weighted least squares with each galaxy's observations totaling one weight unit. Assign **whole galaxies**, not individual radial points, to five deterministic test folds sorted alphabetically by galaxy ID (fold = index mod 5); train on four folds and evaluate the other. Score is root-mean-squared held-out prediction error in dex, **first averaged inside each galaxy, then across galaxies equally**. This is exploratory cross-validation, not an error-distribution likelihood fit. The code also prints fixed no-dark-matter baryon-only and published-form RAR benchmarks. RAR benchmark uses $g_{pred}=g_{bar}/(1-e^{-\sqrt{g_{bar}/a_0}})$ with fixed illustrative $a_0=1.2\times10^{-10}$ m/s², *not fitted for this data*.

## Results: primary selection (153 galaxies, 3,166 points)

| Predictor of the observed/baryonic gravity ratio | Galaxy-held-out RMS error (dex) |
|---|---:|
| Constant adjustment only | 0.30235 |
| **Galactocentric radius only** | **0.30003** |
| **Weak baryonic acceleration only** | **0.20358** |
| **Acceleration + radius** | **0.20113** |

**Interpretation:** Radius alone is much less predictive than low baryonic acceleration. Adding radius reduces held-out error from 0.20358 to 0.20113 dex: about **1.2%** relative. The fitted *in-sample* radius coefficient when acceleration is included is about **+0.0676 dex per decade in radius**, corresponding to about 17% in the $g_{obs}/g_{bar}$ ratio per tenfold radius **under the specified linear model**. The slope is *not* a force law or proof of a distance-driven physical change.

**Separate physical benchmarks, same primary sample:** fixed baryon-only gravity predicts $y=0$ and scores **0.56256 dex**; the fixed published-form RAR benchmark described above scores **0.20897 dex**. These scores should not be confused with fitted out-of-galaxy halo-model predictions. The RAR scale was taken from prior published analyses, so this is not a blind independent discovery.

## Critical robustness / disconfirmation checks

| Sensitivity case | Galaxies / radii | Radius only | Acceleration only | Both | Interpretation |
|---|---:|---:|---:|---:|---|
| Main case: Q1+Q2, inclination >=30°, disk M/L 0.5 | 153 / 3,166 | 0.30003 | 0.20358 | 0.20113 | Small incremental radius gain |
| **Strict high quality: Q1 only**, inclination >=30° | **93 / 2,060** | **0.29722** | **0.16817** | **0.16885** | **Adding radius gets slightly worse** |
| Q1+Q2, no inclination cutoff | 163 / 3,269 | 0.30289 | 0.21064 | 0.20878 | Small radius gain persists |
| Q1+Q2, disk M/L 0.2 | 153 / 3,164 | 0.30111 | 0.21241 | 0.21188 | Radius gain very small |
| Q1+Q2, disk M/L 0.4 | 153 / 3,166 | 0.29740 | 0.20304 | 0.20113 | Radius gain small |
| Q1+Q2, disk M/L 0.6 | 153 / 3,166 | 0.30422 | 0.20538 | 0.20259 | Radius gain small |
| Q1+Q2, disk M/L 0.8 | 153 / 3,166 | 0.31330 | 0.20994 | 0.20679 | Radius gain small |

In the stricter Q1-only sample, the radius coefficient after controlling for acceleration is approximately **0.0000103 dex per decade**, essentially zero within this diagnostic, and CV error increases slightly (0.16817 -> 0.16885 dex). Since the samples differ, **do not compare absolute error levels across Q1 and Q1+Q2 as an isolated causal test**. Compare model differences *within* each sample.

In the main case, out-of-fold residuals of the acceleration-only predictor are also **nonmonotonic across five radius bins**: mean weighted residuals approximately -0.084, +0.031, +0.050, +0.002, +0.015 dex, from smallest to largest radii. This weakens an interpretation of one simple universal radius-driven correction.

## Evidence-based verdict **for this limited distance test**

1. **Supported:** Measured stellar/gas orbital discrepancies are much more systematically predictable from weak baryonic acceleration than absolute galactocentric radius in this experiment.
2. **Not established:** Any *independent* causal modification of gravity triggered by radial distance. The small radius signal does not hold robustly in the strictest quality subset.
3. **Not decided:** Particle dark matter versus modified gravity, whether observational baryon inventory is incomplete, or whether any distinct new physical theory is needed. A tight RAR-like pattern can arise in different theoretical frameworks.
4. **Not a complete answer to O-01:** This analysis is a statistical predictor comparison, **not** a conventional halo fit, full physical modified-gravity fit, lensing test, galaxy-environment test, or a time-dependent matter inflow/outflow simulation.

### Outstanding O-01 validation before we call Question 1 complete

- [ ] Check source fidelity against official SPARC releases; preserve SHA-256 of locally vetted originals and recorded retrieval date.
- [ ] Fit physically motivated Newtonian baryon-plus-dark-halo profiles and published MOND prescriptions on matched train/test splits, including parameter-count penalties and astrophysical priors.
- [ ] Vary bulge/disk stellar M/L, inclinations, distances, correlated errors and baryonic gas accounting; propagate uncertainties and model covariance.
- [ ] Test apparent distance effects **within galaxies** at matched low acceleration, and across galaxy size/scale-length bins; guard against dependence because $g_{bar}$ itself contains $1/r$.
- [ ] Explicitly define mass-system boundaries (galaxy disk versus halo), account for gas inflow/outflow and missing ordinary-matter reservoirs with plausible measured bounds, then test if their maximal effect closes the discrepancy.
- [ ] Compare predictions with independent gravitational lensing/cluster/Solar-System/cosmological constraints before advancing a theory claim.

**No new gravitational law, new mass component, or complete resolution is claimed.** Continue Question 1; do not jump to O-02.