# Working Gravity Hypothesis — Incomplete Mass Inventory and Model Discrimination

**Research ID:** CE-GR-01 | **Established:** 2026-10-24 | **Scientific status:** **TESTABLE RESEARCH HYPOTHESIS, NOT A VALIDATED THEORY OR DISCOVERY**  
**Project:** Cosmos Explorer / Gravity Research | **Origin:** Home/Projects/Gravity-Research (started 2026-10-14)  
**Owner:** Independent personal science research; no connection to PeopleTec/DoD work.

## Plain-language theory statement

> **Our working hypothesis is that some apparent discrepancies between observed gravitational behavior and predictions calculated from known matter may be reduced by a more complete, spatially resolved, time-aware inventory of *ordinary matter* and by explicitly accounting for measurement uncertainty and observational selection.** We will test the gravitational effect of both luminous and nonluminous baryonic material—stars and stellar remnants, planets and small bodies, molecular and atomic gas, dust, and other independently constrained matter—using its measured or inference-qualified spatial distribution. **We do not assume this correction eliminates the need for nonbaryonic dark matter or new gravity.** We will compare its predictions, without tuning the answer in advance, against conventional dark-matter models and published modified-gravity alternatives across galaxies, gravitational lensing, galaxy clusters, the Solar System, and cosmological data.

This is **a hypothesis about the adequacy of mass inventories and gravitational modeling**, not a claim that dark matter has been disproved, general relativity is wrong, or that a new force has been observed.

## Core investigative question

**After accounting for the best independently constrained distribution of ordinary matter and measurement uncertainties, is there statistically significant, reproducible unexplained gravitational behavior? If so, which competing physical explanation predicts independent observations best?**

A star's apparent location and velocity alone do not uniquely tell us the complete local mass distribution or its orbit. The gravitational field depends on the distribution of mass-energy **throughout the relevant environment**; the many mass components, distances, velocities, and correlations must be handled with uncertainty. In the weak-field, nonrelativistic regime this reduces to distributed-mass gravitational potential and acceleration; relativistic lensing, black holes and cosmology require appropriate spacetime models.

## Physical formulation — known rules before speculation

For a distributed ordinary-matter density \(\rho_b(\mathbf{x},t)\), in the Newtonian/weak-field limit,

\[
\nabla^2 \Phi_b(\mathbf{x},t)=4\pi G \rho_b(\mathbf{x},t),
\qquad
\mathbf g_b(\mathbf{x},t)=-\nabla \Phi_b(\mathbf{x},t).
\]

For a circular-equivalent test point in a galaxy, define \(g_{\rm obs}(R)=V_{\rm obs}^2(R)/R\) with the required caveat that noncircular motions, inclination, asymmetric drift and disequilibrium can invalidate that simplification. Compare to \(g_b(R)\) computed from **distributed** gas, stellar disk and bulge models—not the inaccurate replacement of an entire disk by a single central point mass.

A reference \(\Lambda\)CDM comparison computes a total field with a baryonic term and an independently constrained dark-halo term. A published MOND / radial-acceleration-relation alternative predicts motion using its own dynamical prescription. A gravity modification is a **competing model**, not an arbitrary residual term added after fitting a dark halo. For lensing, structure formation and compact objects, use the relevant relativistic field treatment; a Newtonian orbit formula alone is not sufficient.

**Our proposed novelty must be empirical, if any:** an independently reproduced, observation-backed improvement in mass completeness and uncertainty propagation that changes held-out predictions and survives independent-scale tests. It is **not** novel to suggest missing baryons or a special acceleration scale: these are existing research questions with extensive prior work.

## Competing hypotheses — no preselected winner

| ID | Explanation | What would support it | What would count against it |
|---|---|---|---|
| H0 — observational/model improvements | Better distances, inclination, surface brightness, gas, stellar mass-to-light assumptions, and spatial distribution reduce some reported residuals, but do **not** necessarily solve the full discrepancy. | Stable partial improvement that stays within independently measured matter bounds; reproducible across surveys. | Improvements vanish on held-out samples or require unphysical parameter changes. |
| H1 — baryonic-completeness sufficiency **(exploratory strong form)** | Ordinary mass currently missed or misallocated explains the full target discrepancy within standard dynamics. | **Independent** detection or bounded inference of enough ordinary mass in the right 3D locations, giving accurate galaxy kinematics **and** lensing, cluster, BBN/CMB and other tests with a common parameter set. | Required unseen baryon mass exceeds independent baryon constraints or has disallowed distribution; lensing/clusters/cosmology fail. |
| H2 — nonbaryonic dark component | Standard dynamics and independently constrained dark matter halos remain necessary beyond any bounded baryonic correction. | Predictive wins across held-out rotation, lensing, clusters, growth of structure and CMB. | Repeatable failures under reasonable halo/baryon priors and source corrections, or competing models predict independent datasets better with fewer effective freedoms. |
| H3 — modified dynamics / modified gravity | Published alternatives produce correct low-acceleration behavior without the same additional mass assumptions. | Consistent predictions for rotation, lensing, clusters, gravitational waves and the cosmological expansion/structure history. | Failure at any of these scales, excessive tuning, or conflict with high-precision Solar System/relativity measurements. |

**Do not collapse the alternatives:** missing baryonic mass, nonbaryonic dark matter, systematic error, dark energy and modified gravitational dynamics describe different possible mechanisms and observables. A more complete *star catalog* is not itself a measured mass budget: stellar luminosity, estimated stellar mass and actual gravitational mass are distinct.

## Study design / rejection gates

1. **Freeze observables.** Record release, raw source, epoch, units, sky reference frame, measurement method, error/covariance, sample selection and unique source IDs. Separate observation from inferred stellar mass, distance, gas conversion factor, model assumptions, and synthetic visualization.
2. **Replicate baselines first.** Reproduce peer-reviewed SPARC galaxy kinematics and the radial acceleration relation from pinned input bytes; compare with a Solar System JPL Horizons control. Re-run the already committed Home gravity-study scripts on the exact pinned datasets before upgrading their validation status.
3. **Build a source-constrained baryon inventory**, including luminous and dark remnants, neutral/molecular/ionized gas, dust and small bodies where relevant. Quantify completeness limits and **upper bounds** on missing components. Mass not seen is **unknown**, not automatically zero and not automatically large.
4. **Calculate the gravitational potential properly.** Integrate the spatial distribution of mass, keeping Sgr A* as a Galactocentric coordinate origin **without pretending its black-hole mass accounts for the Milky Way's total gravity**. Where 6D astrometry is missing, propagate uncertainties instead of assuming zero radial velocity.
5. **Match fit degrees of freedom.** Fit standard baryons, baryons+physical halos, and published modified-gravity relations using comparable independent quality cuts, nuisance priors and training/held-out partitions. No per-galaxy arbitrary invisible-mass dial that simply forces agreement.
6. **Require independent validation.** Check predictive held-out rotation curves and separately withheld galaxy populations; test lensing/cluster maps, gas inventories, BBN/CMB baryon abundance, structure growth, compact-object/gravitational-wave and Solar System bounds. Appropriate relativistic calculations are mandatory for strong-field and lensing tests.
7. **Try to falsify the hypothesis.** Pre-register thresholds **after** baseline reproduction but **before** evaluating a held-out test set. Publish complete residuals, uncertainty bands, selection sensitivity, bootstrap intervals, negative results, reproducibility instructions, and alternative-model fits. A large catalog alone is not proof.
8. **Preserve publication versions.** A new observation/release may alter estimates; do not silently retroactively relabel old derived results. Link every model result to exact source versions and a reproducible run.

## Current evidence and limits (as of 2026-10-24)

- Prior work in [the original gravity research](Gravity-Research/Gravity-Research.md) catalogued eleven unresolved questions. Its experiments include Earth WGS 84 theoretical consistency checks (not independent Earth gravity measurements) and exploratory SPARC rotation studies.
- The [SPARC radius vs acceleration diagnostic](Gravity-Research/SPARC-Distance-vs-Acceleration-Probe-2026-10-19.md) records 3,166 radial records from 153 galaxies. It found low predicted baryonic acceleration more informative than galactocentric radius alone. This **does not identify the correct physical mechanism**.
- The [SPARC distribution comparison](Gravity-Research/SPARC-Mass-Distribution-Probe-2026-10-19.md) and [cross-survey single-radius probe](Gravity-Research/Cross-Survey-Fiducial-Probe-2026-10-19.md) are exploratory. In particular, the source research README explicitly says the exact cross-survey script has **not yet been executed end-to-end against its 160-row pinned source input**. Keep O-01 **OPEN**.
- The expanded astronomical [dataset source inventory](../data/ASTRONOMICAL_DATASETS.md) and [7,922-star positional visualization catalog](../data/CONSTELLATION_CREDITS.md) are **not** a complete measured galaxy mass census.
- JWST has revealed unexpected early-galaxy populations and also enabled finer **lensing-derived** mass maps. Neither an unexpected galaxy count nor a lensing map by itself is direct laboratory detection of a dark-matter particle or proof of its nonexistence. See [Evidence assessment](JWST_DARK_MATTER_EVIDENCE.md).

## Prior art / external sources to reproduce

- [SPARC — original rotation-curve and distributed baryonic mass-model tables](https://astroweb.cwru.edu/SPARC/)
- [McGaugh, Lelli & Schombert (2016), radial acceleration relation](https://doi.org/10.1103/PhysRevLett.117.201101)
- [Planck 2018 VI, CMB / baryon and dark-matter density constraints](https://www.aanda.org/articles/aa/abs/2020/09/aa33910-18/aa33910-18.html)
- [NASA 2026 Webb lensing / dark matter mapping summary](https://www.nasa.gov/missions/webb/nasa-reveals-new-details-about-dark-matters-influence-on-universe/)
- [ESA Gaia archive](https://gea.esac.esa.int/archive/) and [NASA/JPL Horizons](https://ssd.jpl.nasa.gov/horizons/)

## What would constitute a theory (not yet reached)

A **physical theory** requires a complete mathematically consistent set of governing equations with specified domain, physical degrees of freedom, boundary/initial conditions, independent parameters, and **new quantitative, falsifiable predictions**. The working hypothesis above is a program for testing existing models and observational incompleteness. It should not be promoted to a novel gravity law merely because an observation/model discrepancy exists.
