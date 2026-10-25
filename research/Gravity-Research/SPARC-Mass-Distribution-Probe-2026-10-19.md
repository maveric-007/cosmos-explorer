# SPARC — Matched-Galaxy Matter-Distribution Probe

**Research date:** 2026-10-19  
**Question:** O-01 — Are galaxy rotation anomalies explained simply by incorrectly treating very differently distributed ordinary matter as if it had the same gravitational field?  
**Status:** Completed **exploratory matched-pair diagnostic**, **NOT resolution of Question 1** and **NOT a new gravity theory**.  
**Reproduction:** [Python script](sparc_mass_distribution_2026-10-19.py), stdlib only; prints individual pairs and sensitivity analyses.  
**Previous:** [Radius-versus-acceleration diagnostic](SPARC-Distance-vs-Acceleration-Probe-2026-10-19.md).

## Physical distinction: mass total versus mass distribution

Newtonian gravity is **not** exclusively a function of the total galaxy mass. It depends on **where that mass is located**. A flattened stellar/gas disk, bulge, and extended halo produce a field by summing their spatial contributions. Galaxies of comparable total baryonic mass but different disk scale lengths can have different predicted ordinary-matter rotation curves **without changing Newton's law**.

At a circular-equivalent radius $R$, the observed acceleration is $g_{obs}=V_{obs}^2/R$. We use the published SPARC gas/disk/bulge *distributed* mass-model velocity terms to compute baryonic acceleration $g_{bar}=V_{bar}^2/R$, rather than using the inappropriate spherical point-mass $GM/R^2$ for flattened disks. This is already an explicit test of the effect of mass distribution.

**Caution:** Galactocentric **physical radius**, disk **scale length**, baryonic acceleration, stellar surface density, and dynamical environment are related but not interchangeable. A comparison at 2.2 stellar disk scale lengths for each galaxy is at the **same relative location, not the same number of kiloparsecs**.

## Data and quality rules

Original: [Lelli et al., SPARC (2016)](https://astroweb.case.edu/SPARC/) and [2016 paper](https://arxiv.org/abs/1606.09251). Public mirror of original-format tables: [mass-model rows](https://github.com/JustinSchneider/baryonic-omega-analysis/blob/main/data/raw/MassModels_Lelli2016c.mrt) (Git blob SHA `3f0ea8e3577ec9e0226e4f6a65f1019d45f1aec6`) and [galaxy sample metadata](https://github.com/JustinSchneider/baryonic-omega-analysis/blob/main/data/raw/SPARC_Lelli2016c.mrt) (SHA `8cdfb503c58bf5f4fc6321e976f7caec6e353bf3`). Script verifies downloaded Git blob hashes and rejects changed source bytes; third-party raw files are not copied into Home.

- Starting source: **175 galaxies**, **3,391 observed radial rows**.
- Primary sample: SPARC quality flag **1 or 2**, inclination **>= 30 degrees**, positive disk scale length, valid estimated mass. **153 galaxies eligible.**
- For each, interpolate **squared** observed and baryonic rotation speeds to **R = 2.2 stellar disk scale lengths (2.2 Rd)** using the two *bracketing observed radii* only; no extrapolation. **148 galaxies** have eligible interpolation and positive model/observed speed-squared at that relative radius.
- SPARC modeled baryonic rotation field:
  $$V_{bar}^2=V_{gas}|V_{gas}|+0.5 V_{disk}^2+0.7 V_{bulge}^2,$$
  using *illustrative fixed* 3.6-micron disk and bulge mass-to-light ratios, respectively. Gas component velocity may be signed. Do **not** interpret the 0.5/0.7 stellar M/L choices as measured values for every galaxy.
- Matching estimate of total baryonic mass:
  $$M_{bar,est}\approx 0.5 L_{3.6}\,[M_\odot/L_\odot] + 1.33 M_{HI},$$
  expressed in solar masses. The first term is photometric stellar mass at assumed M/L and the second corrects observed neutral hydrogen for helium. **It is not a complete inventory:** molecular/hot/ionized/circumgalactic gas, mass inference systematics, and outflows are not fully accounted for.
- Each matched pair must have $|\log_{10}(M_a/M_b)|\leq0.10$ dex (up to ~26% mass ratio); absolute estimated neutral-gas mass-fraction difference <= **0.10** (10 percentage points); disk scale length ratio **>=2.0**.
- Choose **non-overlapping** pairs by sorting all qualifying pairs by smallest gas-fraction difference, then closest mass, then largest size ratio, then IDs; greedily accept only pairs with neither member used before. **This selection is deterministic but not unique/optimal**, and its statistics are not a random or independent population estimate. Each galaxy is in at most one selected pair.

## Primary results — same estimated baryonic mass, different distribution

Of 148 interpolable quality-filtered galaxies, the matching yielded **40 candidate pairs** and **22 non-overlapping selected pairs** (44 distinct galaxies).

| Direction at each galaxy's own 2.2 Rd | Count | What it means |
|---|---:|---|
| **More extended galaxy has weaker baryon-predicted gravitational acceleration** | **21 / 22 pairs** | Distribution is important even in conventional gravity. |
| More extended galaxy has lower baryon-predicted circular **speed** | 18 / 22 pairs | Distribution affects speed as well, but spatial gas and bulge profiles complicate simple size scaling. |
| **More extended galaxy has larger observed/baryonic acceleration ratio** | **20 / 22 pairs** | The discrepancy remains—and is usually larger—in these more spread-out galaxies. |
| More extended galaxy has higher **observed** circular speed | 15 / 22 pairs | Observed speed is not simply determined by modeled ordinary-matter distribution. |

The "discrepancy" is $g_{obs}/g_{bar}=V_{obs}^2/V_{bar}^2$, not the physical density of dark matter or a measured correction to Newton's gravitational constant.

**Interpretation:** The shape of the observed ordinary-matter distribution explains meaningful variation in the *predicted ordinary-matter gravitational field*. However, the same ordinary-matter model does **not** by itself explain observed rotations across this selected matched sample. This pattern is compatible with already published low-acceleration/RAR behavior; it is **not** unique evidence for modified gravity or for particle dark matter.

### Worked real-galaxy pair — NGC 2403 and NGC 4183

Both galaxies pass the stricter SPARC **quality flag 1** filter. Their neutral gas fractions are similar (~45.9% and 46.3% under the chosen coarse mass estimator).

| Quantity | NGC 2403 (compact) | NGC 4183 (extended) |
|---|---:|---:|
| Coarse baryonic mass (solar masses) | **9.28 billion** | **10.08 billion** |
| Stellar disk scale length, Rd | **1.39 kpc** | **2.79 kpc** |
| Analysis radius = 2.2 Rd | **3.06 kpc** | **6.14 kpc** |
| Baryons-only modeled circular speed | **73.6 km/s** | **57.2 km/s** |
| Observed circular speed | **101.6 km/s** | **103.1 km/s** |
| Observed/baryon predicted gravitational-acceleration ratio | **1.90** | **3.25** |

**Plain-language takeaway:** Roughly the same estimated ordinary-matter mass is spread over about twice the stellar disk scale length. Conventional distributed-matter modeling predicts the more extended galaxy has **lower** circular speed contributed by baryons at its own 2.2 Rd. Yet their observed speeds are close, leaving a larger unexplained discrepancy for the extended galaxy. **This does not show that Newton's gravity changes over distance:** the different radii, gas/stellar spatial profiles, dark-halo possibilities, and errors must all be assessed.

## Robustness cases

| Analysis restriction | Disjoint pairs | Extended galaxy has weaker modeled baryonic acceleration | Extended galaxy has larger observed/baryonic discrepancy |
|---|---:|---:|---:|
| Primary: Q1+Q2, mass <=0.10 dex, gas fraction <=0.10, size >=2x | **22** | **21** | **20** |
| **Only highest-quality Q1 galaxies** | **9** | **9** | **9** |
| Gas-fraction mismatch tightened to <=0.05 | **17** | **17** | **15** |
| Mass mismatch tightened to <=0.05 dex | **14** | **12** | **12** |
| Disk-size factor increased to >=3x | **6** | **5** | **6** |

The sign of the pattern persists across these *selected* matches, but matched-pair thresholds and pairing order affect sample composition. **No uncertainty propagation, p-value, independent cross-validation, or causal identification is claimed.** A selection on galaxy disk size, plus the inverse relationship between mass density and acceleration, can itself produce strong apparent associations.

## What this probe resolves — and doesn't

**Resolved in a limited sense:** Different ordinary-matter mass **distributions do produce different Newtonian baryonic gravitational fields**. Treating galaxies as point masses or comparing total masses alone can be misleading; the published SPARC component models already account for the flattened disk's geometry.

**Not resolved:** The *full measured* galaxy rotation curves still differ from simple stars+gas predictions in these examples. This matched comparison cannot adjudicate standard baryons+dark halo against MOND-like laws; it does not independently measure all material crossing boundaries; it doesn't account for distance/inclination correlated uncertainty or molecular and circumgalactic gas. These limitations are not "tiny numbers to ignore"—they are part of the hypothesis testing.

### Mandatory next experiments before finishing Question 1

- [ ] **Baryonic inventory limits:** quantify measured/unmeasured molecular, ionized and circumgalactic gas and their spatial distribution; compute physically defensible maximum corrections to rotation curves without treating arbitrary hidden gas as free fitting mass.
- [ ] **Competing physical fits:** dark halo models (e.g. NFW and cored halo) versus published MOND prescriptions; use identical galaxies, measurement uncertainties, prior constraints, withheld targets and penalty for adjustable parameters.
- [ ] **Geometry and systematic sensitivities:** interpolate at several relative and fixed physical radii; vary stellar M/L, distances, inclinations, and gas profiles, with propagated covariance/measurement errors.
- [ ] **External constraints:** compare galaxy-scale model implications with lensing, clusters and precision Solar-System gravity; local galaxy rotation patterns alone cannot establish universal modified gravity.

**Status:** Question 1 remains OPEN. This was an exploratory observation+published-mass-model comparison, not proof of a new law. No automatic reminders or scheduled jobs created.