# Gravity Research — Open Questions and Test Plan

> **Status:** Idea / research notebook v0.1 • **Opened:** 2026-10-14 • **Domain:** HOME (personal side project)  
> **Owner:** Sean • **Purpose:** Investigate whether observed gravitational discrepancies expose unmodeled matter, incomplete gravitational laws, systematic error, or combinations of these.  
> **Ground rule:** Seek disconfirmation as actively as confirmation. Nothing here is a discovery claim.


**Home / Obsidian location:** `Projects/Gravity-Research/`  

**Equations, supporting derivations, and explained variables:** [Gravity Equations and Variable Reference](Gravity-Equations-and-Variable-Reference.md) — project-wide, beginner-friendly mathematical reference with assumptions, units, worked examples, and links to observational tests.

## The question we actually want to answer

**Is our current description of gravity complete across the Solar System, galaxies, galaxy clusters, and cosmological scales? If not, what measurable prediction distinguishes a better model from existing ones?**

This began with a concern that dark matter might be a label for something missing in gravitational calculations. Treat that as a **question**, not proof of a missing force. Dark matter has strong, independent indirect evidence, but its microscopic identity is unknown. Modified-gravity proposals exist and need to confront the *entire* evidence set, not merely galaxy rotation curves.

### Historical precedent: who has asked these questions? (verified 2026-10-19)

**This is an active, established scientific debate, not a novel either/or framing.** The project contribution must be a precise, independently testable prediction or a better-controlled comparison, not simply raising the dark-matter-versus-gravity possibility.

- **Observed galaxy rotations / inferred mass:** Vera Rubin and W. Kent Ford (1970), [*Rotation of the Andromeda Nebula*](https://doi.org/10.1086/150317), mapped galaxy rotation and the inferred radial mass distribution.
- **Hidden mass versus gravity itself:** Mordehai Milgrom (1983), [*A modification of the Newtonian dynamics as a possible alternative to the hidden mass hypothesis*](https://doi.org/10.1086/161130), posed almost precisely our central fork and proposed a low-acceleration modification (MOND).
- **Similar mass, different surface-brightness/matter distribution:** Stacy McGaugh and Erwin de Blok (1998), [*Testing the Dark Matter Hypothesis with Low Surface Brightness Galaxies and Other Evidence*](https://doi.org/10.1086/305612), found stronger apparent mass discrepancies in diffuse galaxies. This is closely related to our matched-SPARC size/density experiment; it is prior art, not a finding unique to us.
- **Mass-model acceleration relationship:** McGaugh, Lelli and Schombert (2016), [*Radial Acceleration Relation in Rotationally Supported Galaxies*](https://doi.org/10.1103/PhysRevLett.117.201101), studied 2,693 points in 153 galaxies, showing a tight observed versus ordinary-matter acceleration correlation. Our separately defined exploratory 3,166-point dataset is **not** their exact analysis sample.
- **Tests designed to separate the hypotheses:** [2024 *Hooks & Bends in the radial acceleration relation*](https://doi.org/10.1093/mnras/stae819) explores potentially discriminating features in simulations; [2025 *The radial acceleration relation at the EDGE of galaxy formation*](https://doi.org/10.1051/0004-6361/202557106) studies very low-mass dwarf galaxies that challenge simple universal extrapolations.
- **Missing ordinary matter / boundary accounting:** Joel Bregman (2007), [*The Search for the Missing Baryons at Low Redshift*](https://doi.org/10.1146/annurev.astro.45.051806.110619), documents the distinct baryon-inventory problem. Missing baryons in intergalactic reservoirs do not automatically provide the **radially located mass** required by any particular galaxy's rotation curve.

**Our next contribution:** Keep the existing [matched galaxy mass-distribution result](SPARC-Mass-Distribution-Probe-2026-10-19.md) separate from the above literature; quantitatively bound missing baryonic reservoirs/inflows/outflows, compare physically constrained dark-halo and published modified-dynamics models, and seek held-out predictions that actually differ. Avoid treating published MOND/RAR relationships or surface-brightness trends as original discoveries.

### Central competing-explanations hypothesis (agreed 2026-10-19)

**Plain-language question:** *Is dark matter the real missing link, or is our understanding of gravity incomplete?*

**Scientific formulation:** Can ordinary matter plus an independently specified modified-gravity theory predict galaxy rotation curves, gravitational lensing, galaxy clusters, cosmic structure and precision Solar System observations **at least as well as** conventional gravity plus a dark-matter component, while using comparably justified assumptions and not introducing more unconstrained parameters?

- **H1 — Additional gravitating matter:** Conventional Newtonian/GR gravity remains effective, and a nonluminous matter component contributes to the field. Specify and test a conventional halo model rather than taking the unexplained rotation residual as proof of a particle.
- **H2 — Modified gravity:** A specific published alternative gravitational law or relativistic theory explains the discrepancy with no, or less, additional matter. Distinguish galaxy-scale empirical MOND/RAR fits from a complete gravity theory.
- **H3 — Incomplete ordinary-matter inventory and astrophysical systematics:** Missing baryons, distances, inclinations, gas flows, mass-to-light assumptions or noncircular motions contribute. Bound these corrections with independent observations; do not add arbitrary invisible baryons.
- **H4 — Combination:** Additional matter, changes to gravitational physics and/or systematics could coexist; do not force a false binary.

**Decision standard:** Compare H1–H4 on the **same** high-quality data, common error/selection rules, matched complexity/priors and predeclared held-out predictions. Seek observations where models predict *different* outcomes, then test independent constraints (especially lensing, merging clusters, cosmology and Solar System). A tight rotation fit alone cannot determine the cause.

**What our 2026-10-19 probes show so far:** [Radius versus weak acceleration](SPARC-Distance-vs-Acceleration-Probe-2026-10-19.md) favors the weak-acceleration statistical predictor over absolute radius but **does not identify a physical cause**. [Matched galaxy matter distributions](SPARC-Mass-Distribution-Probe-2026-10-19.md) confirm that ordinary-matter geometry affects the predicted field and that observed discrepancies remain in selected comparisons; this too **does not distinguish H1 from H2**. **O-01 stays open.**

**Next decisive work in O-01:** Quantify baryonic inventory/systematics, fit conventional dark-halo models and published MOND prescriptions on matched galaxy-held-out samples, and formulate out-of-sample observational predictions before making a conclusion. Do not claim the proposed alternative has been verified or that dark matter has been disproved.


### What would distinguish dark matter from modified gravity?

A **rotation discrepancy alone is not a discriminator**: a conventional Newtonian/GR baryon+dark-halo model and a specific modified-gravity prescription can both fit many of the same measured velocities. Make **quantitative, different predictions before testing the held-out observations**.

1. **Radial rotation-curve details at fixed baryonic mass distribution:** Published MOND-like prescriptions use a characteristic acceleration scale and tightly link expected rotation to observed stellar/gas geometry, subject to their explicit external-field treatment; conventional dark-matter halo models add a spatially distributed halo whose allowed mass/concentration/core shape must satisfy astrophysical priors. Test *where* their predicted velocities differ, not just total fit quality. Fit ordinary-matter M/L, distance, inclination and velocity uncertainties consistently, and penalize extra degrees of freedom. No generic assertion that one explanation has no freedom: both have nuisance choices.
2. **External gravitational environment:** MOND theories such as AQUAL/QUMOND predict an intrinsic **external field effect**, which can modify internal dynamics even in a free-falling system. Standard GR/CDM does not yield that same fundamental uniform-field effect, but nearby halos, tides and environmentally correlated galaxy properties can **mimic a statistical signal**. Look for the *theory-specific sign and size*, after controlling for tides/environment; current galaxy detections remain contested. [AQUAL/QUMOND numerical test, Physical Review D (2022)](https://doi.org/10.1103/PhysRevD.106.103025); [CDM counterexample, MNRAS (2022)](https://academic.oup.com/mnras/article/517/1/130/6713954).
3. **Mass inferred from gravitational lensing vs observed baryons:** In merging clusters the principal lensing peaks can be separated from hot X-ray gas containing most observed baryons (e.g. Bullet Cluster). A collisionless gravitating component explains this naturally; any gravity-only replacement must quantitatively predict the *positions and strengths* of lensing signals, not merely fit a disk rotation curve. A nonrelativistic MOND interpolation is not a lensing theory by itself; different **relativistic modified-gravity theories** make different lensing predictions. [NASA Webb Bullet Cluster (2025)](https://science.nasa.gov/missions/webb/nasa-webb-pierces-bullet-cluster-refines-its-mass/).
4. **Early Universe and structure growth:** The ΛCDM framework simultaneously predicts CMB acoustic-peak patterns, cosmic matter abundances and growth of galaxies/clusters. A replacement must supply a specified relativistic cosmology reproducing those *same independent observations*, not only galaxy rotation. [ESA Planck overview](https://www.esa.int/Science_Exploration/Space_Science/Planck/Planck_science_highlights); [Planck 2018 legacy assessment](https://doi.org/10.1051/0004-6361/201833880).
5. **Ordinary matter missing from an inventory:** A physically measured or defensibly bounded gas component must have **sufficient mass at the required radii** to alter predicted rotation, without violating gas emission/absorption, lensing and baryon constraints. Matter merely crossing a galaxy-disk boundary may remain in the halo; it cannot be added twice. This is a third competing hypothesis, not itself a test of modified gravity.

**Connection to our completed matched-distribution diagnostic:** [22 selected independent matched galaxy pairs](SPARC-Mass-Distribution-Probe-2026-10-19.md) include **20** in which the more extended disk has the larger observed-to-baryon acceleration ratio. This confirms *a descriptive trend in our selected sample*, **not** which underlying model causes it. The matched galaxies must be retested with physical predictions and uncertainties.

**Prioritized Question O-01 test:** At the same SPARC radii, compare (a) published distributed-baryon prediction, (b) constrained NFW/cored halo velocity models, and (c) one explicitly named published MOND model. Predefine stellar M/L, distance, inclination, gas, external field and halo priors; retain full rotation-curve geometry; assess fit quality **plus complexity** and withheld-galaxy or withheld-radius generalization without leaking fitted galaxy-specific parameters. Next, stress-test with independent environment and lensing evidence. Only a robust failure or distinctive successful prediction changes the preferred explanation.

**Current conclusion:** Independent cluster lensing and cosmological evidence favor the conventional dark-matter framework overall; galaxy-level acceleration regularities motivate further tests of its small-scale predictions and of modified dynamics. Neither an observed mass discrepancy nor a compelling galaxy fit identifies a dark-matter particle or proves gravity is complete. **O-01 remains OPEN.**

### Vocabulary / foundations

- **Newtonian gravity:** Masses attract with magnitude $F=Gm_1m_2/r^2$ for point masses or spherically symmetric bodies, with appropriate integration over extended mass distributions. It accurately describes many everyday and orbital situations.
- **Newtonian orbital test:** For a circular orbit around a *spherical* mass distribution, $g=v^2/r=GM(<r)/r^2$. For a real flattened galaxy disk, calculate the distributed gravitational field instead of blindly using the spherical enclosed-mass formula.
- **General relativity (GR):** Gravity is described through spacetime geometry; the Newtonian law is an excellent weak-field, low-speed approximation.
- **Baryons / ordinary matter:** Stars, gas, dust, and related conventional matter; some is not luminous but is still ordinary matter.
- **Dark matter:** An inferred gravitating component in the standard cosmological framework, not a directly confirmed particle species.
- **Dark energy:** The name given to the component/phenomenology driving cosmic acceleration; a different problem from galactic dark matter.
- **MOND / modified gravity:** Families of alternative ideas; simple low-acceleration prescriptions alone are not complete cosmological theories.
- **Not a force:** Inertia is not an additional fundamental interaction. A residual in a calculation does not itself establish a new force.

## Annotated open seams / scientific uncertainty register

**O-01 — Galaxy rotation curves and acceleration relation**  
**What is observed:** Many outer galaxy rotation curves remain relatively flat; the relationship between observed acceleration and acceleration predicted by baryons is tight in observational studies. The 2016 radial-acceleration paper reported 2,693 measurements across 153 galaxies.  
**What is unresolved:** What underlying physical mechanism produces this relation? Particle dark matter with galaxy formation, modifications of gravity, or other explanations may reproduce parts of it.  
**Competing hypotheses:** Baryons + a dark halo; MOND-like laws; more general relativistic modified-gravity models; systematic astrophysical effects.  
**Test:** Reproduce galaxy-by-galaxy acceleration residuals from SPARC; compare held-out predictive performance, uncertainty, parameter count, and residual correlations.  
**2026-10-19 first radius/acceleration diagnostic:** [Results and remaining tests](SPARC-Distance-vs-Acceleration-Probe-2026-10-19.md) and [reproducible code](sparc_distance_acceleration_2026-10-19.py). The 153-galaxy exploratory held-out analysis finds low acceleration substantially more predictive than galactocentric radius; radius's small extra signal disappears among the 93 highest-quality galaxies. This **does not settle Question O-01** or distinguish dark matter from new gravitational dynamics.  
**Caution:** Stellar mass-to-light ratios, disk inclination, distance, asymmetric drift and noncircular motion affect the inference. A fit is not automatically an explanation.  
**New sub-question (19 Oct 2026) — dynamic mass inventory and boundaries:** When studying a planet, Solar System, galaxy disk, or entire galactic halo, how much matter crosses the chosen boundary over time, how much remains gravitationally bound inside a larger system, and could an incomplete mass inventory or changing mass distribution materially affect the gravitational predictions we compare with observations? Are inflow/outflow rates large enough *over the relevant orbital timescale* to matter, rather than merely being nonzero?  
**Clarifications:** Matter leaving Earth's atmosphere is not automatically lost from the Solar System; gas leaving a galaxy's visible disk may remain in its halo and later return. Breathing and other ordinary chemical reactions rearrange atoms and transfer mass between reservoirs; they do not create net mass. An object's gravitational motion near a galaxy depends on the full matter distribution, its position and velocity—not only the galaxy's total mass.  
**Falsifiable test:** Explicitly specify the boundary, timespan, ordinary-matter reservoirs (stars, atomic/molecular gas, dust, hot/ionized gas and circumgalactic material when applicable), inflow/outflow estimates, and uncertainties. Evaluate how plausible extremes in the **spatially distributed** baryonic mass budget change the predicted rotation curve, and test whether those changes can account for observed SPARC residuals without double-counting matter or contradicting independent lensing and other constraints. If the maximum physically supported effect is much smaller than the discrepancy, reject missing boundary-crossing mass as a sufficient explanation. This is a testable accounting question, **not evidence that gravity is wrong**.  
**Sources:** [SPARC](https://astroweb.case.edu/SPARC/); [Lelli et al. 2016](https://arxiv.org/abs/1606.09251); [McGaugh et al. 2016](https://doi.org/10.1103/PhysRevLett.117.201101).

**O-02 — Nature and distribution of dark matter**  
**Observed:** Rotation, lensing, cluster dynamics and cosmic microwave background constraints jointly support gravitating mass beyond observed baryons within standard models.  
**Unknown:** Particle identity, mass, non-gravitational interactions, and detailed small-scale behavior. The hypothesis of dark matter is not equivalent to proving a particular particle.  
**Test:** Compare predictions for galaxy dynamics, clusters and cosmology; do not infer particle mass from a galaxy mass deficit.  
**Source:** [NASA dark matter overview](https://science.nasa.gov/dark-matter/).

**O-03 — Gravitational lensing and colliding clusters**  
**Observed:** Lensing maps in the Bullet Cluster and other mergers show mass distributions offset from much of the hot baryonic gas.  
**Open issue:** Can a proposed gravitational theory reproduce both the dynamics of ordinary matter and the observed deflection of light, across these systems, using one consistent framework?  
**Test:** Assess published lensing-map likelihoods and consistency with mass components in each model. Rotation curves by themselves are insufficient.  
**Sources:** [NASA Hubble dark matter](https://science.nasa.gov/mission/hubble/science/science-behind-the-discoveries/hubble-dark-matter/); [NASA colliding-cluster comparison](https://science.nasa.gov/missions/chandra/a-clash-of-clusters/).

**O-04 — Solar System and local gravitational constraints**  
**Observed:** Precise planetary ephemerides and spacecraft tracking are tightly consistent with conventional gravitational predictions within measured uncertainty.  
**Open issue:** Any proposed extra force must be weak enough locally (or have a justified, testable mechanism making it weak), not silently switched off. Smooth background galactic gravity largely accelerates the Sun and Earth together; relative tidal effects can be much smaller.  
**Test:** Compare modeled Earth–Sun relative acceleration and outer-Solar-System trajectories to NASA/JPL reference ephemerides with explicit uncertainties.  
**Illustration, *not a measurement*:** Assuming a smooth local density of roughly $0.3$ GeV/cm³ ($\sim5.3\times10^{-22}$ kg/m³), the amount within a Sun-centered sphere of radius 1 AU is about $7.5\times10^{12}$ kg, versus the Sun's $1.99\times10^{30}$ kg. This order-of-magnitude example explains how an effect can exist yet be tiny in Earth's relative orbit; it does **not** determine the actual local halo structure.  
**Sources:** [JPL Horizons](https://ssd.jpl.nasa.gov/horizons/); [NASA Solar System dark matter discussion](https://www.nasa.gov/universe/dark-matter/how-dark-matter-could-be-measured-in-the-solar-system/).

**O-05 — Milky Way kinematics / local mass budget**  
**Open issue:** How well do stellar motions reveal the local gravitational potential when distance errors, non-equilibrium motion, dust extinction and population selection are included?  
**Test:** Cross-check separate stellar-population and radial-distance bins using publicly released Gaia astrometry and velocities.  
**Source:** [ESA Gaia archive](https://gea.esac.esa.int/archive/).

**O-06 — Cosmological initial conditions and background anisotropies**  
**Observed:** Cosmic microwave background power spectra, large-scale structure and primordial element abundances constrain how matter gravitated as the universe evolved.  
**Open issue:** Can a revised gravity model match those observables *and* galaxy kinematics without contradictory parameter settings?  
**Test:** Compare predictions for angular power spectra and matter growth with Planck and DESI summaries or likelihoods. This is a later-stage model-comparison task, not a simple spreadsheet exercise.  
**Sources:** [ESA Planck Legacy Archive](https://pla.esac.esa.int/); [DESI public release documentation](https://data.desi.lbl.gov/doc/releases/dr1/).

**O-07 — Dark energy and large-scale cosmic acceleration**  
**Open issue:** Is late-time acceleration described by a cosmological constant, evolving dark energy, or modified gravitational dynamics? This must not be conflated with dark matter in galaxies.  
**Test:** Evaluate competing expansion histories using supernova/BAO/CMB observational constraints.  
**Source:** [NASA dark energy program](https://science.nasa.gov/astrophysics/programs/physics-of-the-cosmos/expand-our-knowledge-of-dark-energy/).

**O-08 — Quantum gravity and extreme regimes**  
**Open issue:** General relativity is a classical theory; no experimentally established, complete quantum theory of gravity exists. This is a genuine foundational gap but does **not** by itself explain galaxy rotation curves.  
**Test:** Document proposed quantum-gravity predictions separately from phenomenological galaxy fits; favor claims with specific testable observables.  
**Source:** [NASA quantum-gravity experiment concept](https://www.nasa.gov/directorates/stmd/niac/supreme-qg-space-borne-ultra-precise-measurement-of-the-equivalence-principle-signature-of-quantum-gravity/).

**O-09 — Strong-field gravity and gravitational-wave propagation**  
**Observed:** LIGO/Virgo gravitational-wave events enable tests of compact-object gravity and wave propagation, and so constrain alternative theories.  
**Open issue:** Do proposed modifications violate limits from waveform measurements or propagation constraints?  
**Test:** Treat relevant gravitational-wave bounds as independent exclusion tests for any future theory.  
**Source:** [LIGO GW170817 relativity tests](https://ligo.org/science-summaries/gw170817tgr/).

**O-10 — Measurement assumptions, inference and bias**  
**Open issue:** Misestimated distances, mass-to-light ratios, gas distributions, velocity-field geometry, selection effects, fit flexibility and overlooked systematics can masquerade as theoretical problems or hide real ones.  
**Test:** Track original data provenance; publish calculation units, uncertainties, quality exclusions and preregistered comparison criteria; use withheld galaxies and bootstrap/sensitivity checks.  
**Principle:** Do not redefine every unexplained residual as dark matter, or every residual as new physics.

**O-11 — Understanding gravity versus manipulating gravity**  
**Distinction:** Gravitational theory predicts the field and motion; practical levitation can be achieved with aerodynamic or electromagnetic forces without controlling gravity. No verified general-purpose gravity shield or antigravity propulsion technology is established.  
**Open question:** Whether a future theory yields independently controllable gravitational phenomena is unknown; lack of flying cars is not evidence the current equations are wrong.  
**Test standard:** Require a quantitative, repeatable physical prediction and reproducible experiment rather than a technological aspiration.

## Our falsifiable working proposition (not a new theory yet)

**Research question:** Is there a universal acceleration or environmental dependence that predicts galaxy kinematics more accurately than established models *without breaking* Solar System, lensing, gravitational-wave and cosmological constraints?

- Null/reference explanation: established Newtonian/GR gravity with conventional baryons and an independently parameterized halo, within an explicit galaxy model.
- Comparator: published empirical radial acceleration relation / MOND-style prescription (acknowledged prior art).
- Exploratory alternative: model the residual dependence on measurable galaxy properties or environment, **only after reproducing the baselines**.
- Rejection conditions: worse out-of-sample performance, unrealistic stellar populations, prediction failures in high-acceleration systems, failure to account for light deflection or cosmological constraints, or unmotivated additional free parameters.
- Honest conclusion allowed: existing explanation remains preferred; no novel effect detected.

## Dataset catalog — public, independent, and purpose-specific

| Dataset | What we can test | Authoritative entry point | Starting priority |
| --- | --- | --- | --- |
| SPARC (175 disk galaxies) | Rotation curves, baryonic mass models, galaxy acceleration residuals | [SPARC data/downloads](https://astroweb.case.edu/SPARC/) | 1 — first reproducible analysis |
| JPL Horizons | Planetary positions, velocities and ephemerides; high-precision local checks | [Horizons](https://ssd.jpl.nasa.gov/horizons/) | 1 — Solar System control |
| ESA Gaia DR3 archive | Milky Way stellar kinematics and Galactic mass inference | [Gaia archive](https://gea.esac.esa.int/archive/) | 2 |
| ESA Planck Legacy Archive | CMB-based constraints on cosmic matter and gravity | [Planck archive](https://pla.esac.esa.int/) | 3 |
| DESI DR1 and published DR2 cosmology products | Galaxy redshifts, clustering and cosmic expansion/growth tests | [DESI public data](https://data.desi.lbl.gov/doc/) | 3 |
| Published cluster lensing + X-ray studies | Cluster mass geometry and mergers | [NASA Bullet Cluster overview](https://science.nasa.gov/mission/hubble/science/science-behind-the-discoveries/hubble-dark-matter/) | 2 — choose a quantitative, reusable dataset later |

**Data handling:** Keep provenance URLs, survey/data-release IDs, retrieval date, citations, coordinate conventions, units, filter decisions, model assumptions, and checksums alongside downloaded data. Do not commit multi-gigabyte data dumps to Git. Different astronomical datasets have different selection effects; they are not automatically row-joinable.

## First reproducible experiment — baseline before speculation

1. [ ] Read the [SPARC master paper](https://arxiv.org/abs/1606.09251) and [2016 radial-acceleration paper](https://doi.org/10.1103/PhysRevLett.117.201101); record assumptions and their possible failure modes.
2. [ ] Download a small SPARC sample and preserve the unaltered source files and metadata. Inspect actual column names, data dictionaries, and units.
3. [ ] Select one well-measured galaxy plus at least one contrasting low-surface-brightness galaxy. Do not cherry-pick only favorable systems.
4. [ ] Calculate $g_{obs}=V_{obs}^2/R$ and $g_{bar}$ from the *published flattened-disk/bulge/gas mass model* with correct mass-to-light assumptions and signed gas contributions where applicable.
5. [ ] Reproduce the published observed-vs-baryonic acceleration figure within tolerances and documented error bars.
6. [ ] Compare Newtonian baryon-only, conventional dark-halo fits, and an established MOND/RAR fitting relation using consistent fit/holdout rules.
7. [ ] Compute residuals and uncertainties; test whether radius, surface brightness, gas fraction, or environment explains held-out discrepancies after controlling for data errors.
8. [ ] Build a separate approximate Earth–Sun calculation, then compare to JPL ephemerides. Do not claim an approximate two-body orbit reproduces full relativistic multi-body ephemerides.
9. [ ] Record negative findings and reasons for model rejection with equal prominence.
10. [ ] Advance to lensing, clusters and cosmology only after baseline reproducibility and model validation.

### Definition of evidence

**Observed measurement** ≠ **derived quantity** ≠ **model inference** ≠ **working speculation**. Keep these labels explicit. No claim of a discovered force, new particle, disproved dark matter, or demonstrated antigravity without independently validated predictions.

## Research workflow / durable continuity

- This file is the **initial research charter and annotated open-questions index**. Until executable analysis exists, keep this as the canonical project note in the [software-projects portfolio](https://github.com/maveric-007/software-projects/blob/main/README.md).
- **When coding starts:** establish a dedicated personal research repository for scripts, tests, data manifests, methods, notebook outputs and change history; link it from this portfolio, and leave only project-level context here. Follow [Project Standards](https://github.com/maveric-007/software-projects/blob/main/PROJECT-STANDARDS.md).
- Home-computer work only; do not mix PeopleTec/DoD environments, ADO, or customer data with this personal experiment.
- No calendar events, background jobs, or ChatGPT automations are authorized by this note.
- Future conversations can resume from the unchecked steps and references here. Update factual status only after confirmed work, not on intent.

## Session decisions (2026-10-14)

- Proceed as an informal evidence-led personal side project, with beginner-friendly explanations and annotated math.
- Compare known predictions at Solar System and galaxy scales; if something acts gravitationally everywhere, explain differences in magnitude, distribution, and differential/tidal effects rather than asserting it is absent.
- Include competing explanations and design tests capable of proving the working suspicion wrong.
- Use multiple public astronomical datasets, beginning with SPARC and NASA JPL Horizons.
- User requested a committed Markdown source of truth that can be revisited on a future drive; no scheduled reminders.
