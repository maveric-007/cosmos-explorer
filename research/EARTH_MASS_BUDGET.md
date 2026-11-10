# Earth mass accounting — evidence, scope, and validation

**Research topic:** CE-GR-01 / Solar System matter completeness · **As-reviewed:** 2026-11-10  
**Status:** Reference evidence ledger in the Cosmos Explorer object inspector; **not** a measured, closed daily/annual Earth mass balance and **not** a dynamic Earth-mass/gravity solver.

## Question

What do we actually know about Earth's total mass, the rate of matter entering and leaving the Earth system, and the unresolved difference (ΔM)?

Define a system boundary before computing any net flow. Atmospheric entry, atmospheric deposition, reentry, leaving the exosphere, and escaping Earth's gravitational influence are **not interchangeable boundaries**.

## Evidence taxonomy and current inputs

The **single numeric source for the viewer** is [`scripts/earth-mass-accounting.mjs`](../scripts/earth-mass-accounting.mjs). Each term retains status, units, source, scope, and explicit null uncertainty where an extract did not establish one; `null` is **unknown**, never zero.

| Term | Classification | What it establishes | What it does *not* establish |
|---|---|---|---|
| Earth GM from JPL DE440 | Orbitally inferred / ephemeris fit | Gravitational parameter from orbital dynamics, in km³/s² | A census of individual mass constituents or directly measured annual mass changes |
| Earth mass, NASA fact sheet | Derived/inferred rounded reference in kg | Approximate total gravitational mass using externally determined G | An exact kilogram value independent of laboratory uncertainty in G |
| Earth's atmospheric mass, NASA fact sheet | Model estimate | Approximate atmospheric contribution to the whole-Earth mass | Additional mass to add to Earth GM; atmosphere is already part of the system |
| Ground-reaching micrometeorites, Rojas et al. (2021) | Observation-based extrapolation | Annual material deposited on Earth's surface, in metric tonnes/year | All extraterrestrial material arriving at the top of the atmosphere or captured elsewhere |
| Hydrogen/helium/oxygen loss, NASA HEAT teaching slides | Published approximate atmospheric escape | Species-specific loss rates, reported by NASA in “tons/year” | All outgoing flux; the slides do not specify a metric-versus-US ton convention |
| Full incoming, full outgoing, and net annual ΔM | **Unknown/unresolved** | Missing terms and boundary definitions needing independent measurement | A legitimate number to set to 0 or to derive by subtracting incompatible partial figures |

**Scientific distinction:** NASA's mass and JPL's GM are not two independent direct measurements of Earth's mass. The kilogram value also depends on independently measured Newtonian G. No zero uncertainty is asserted.

### Why the simple subtraction is invalid

The 2021 5,200-metric-tonne estimate is material **reaching the ground**, not the complete incoming Earth-system flux. NASA's educational gas-escape figures cover selected species and preserve the original unspecified “tons” convention. Missing terms include airborne ablated extraterrestrial material that remains Earth-bound, other atmospheric escape processes and species, and non-atmospheric transfers. Their epochs, units, methods, and boundaries must be harmonized before any defensible net balance:

```text
ΔM_earth / Δt = Σ(mass crossing chosen boundary inward per unit time)
              − Σ(mass crossing chosen boundary outward per unit time)
              + explicitly modeled mass-energy terms where relevant
```

Do not count internal atmosphere/ocean/crust exchanges as gains or losses for the whole Earth system. Earth can change its local gravity harmonics through **redistribution** without appreciably changing total mass; gravitational measurements can constrain the system without identifying every particle.

### External sources and provenance

1. **JPL Solar System Dynamics**, [Astrodynamic Parameters](https://ssd.jpl.nasa.gov/astro_par.html): Earth `GM = 398600.435507 km³/s²`, planetary ephemeris DE440 context (Park et al., 2021).
2. **NASA NSSDCA**, [Earth Fact Sheet](https://nssdc.gsfc.nasa.gov/planetary/factsheet/earthfact.html): rounded Earth mass `5.9722 × 10²⁴ kg` and atmosphere `5.1 × 10¹⁸ kg`.
3. **Rojas et al. (2021)**, [The micrometeorite flux at Dome C (Antarctica)](https://doi.org/10.1016/j.epsl.2021.116794), *Earth and Planetary Science Letters*, 560:116794: approximately `5,200 metric tonnes/year` reaching the surface; extrapolation from a sample.
4. **NASA HEAT**, [Atmosphere Loss Through Solar Wind (educational slide deck)](https://assets.science.nasa.gov/content/dam/science/hpd/heat/heat-pdfs/hby-and-math-slide-decks/HBY%20and%20Math%2017_%20Atmosphere%20Loss%20Through%20Solar%20Wind.pdf): approximate annual atmospheric losses for hydrogen, helium and oxygen. Retain raw “tons” as stated and do not falsely assign its unit system.

**Source check, not a source release claim:** Linked source material was reviewed for this 2026-11-10 ledger. It is a versioned, cited reference summary, not a daily automated measurement or new mission observation. Confidence intervals are not supplied in this bounded extraction, so `uncertainty: null` remains explicit. Source publication and data-epoch distinctions are not silently inferred.

## Acceptance and future scientific validation

- [x] Show classification, units, cited source, methodological boundary and unknown values in Earth selection inspector
- [x] Separate atmospheric mass from extra additive mass; keep totals from double counting
- [x] Guard against a fabricated net change, exactness, or false day-by-day measurement with a deterministic test
- [ ] Retrieve comparable species-specific physical influx/escape measurements with defined Earth-system boundary and aligned units/epochs
- [ ] Attach reported uncertainties or credible bounds for each input and propagate to a net-rate interval; **unknown ≠ 0**
- [ ] Establish measured Earth-system rate and compare it with orbital GM constraints where achievable
- [ ] Expand source-qualified mass accounting to other planets, moons, small-body populations and unresolved diffuse material
- [ ] Build and validate a **time-evolving** gravitational potential from independently supported 3D mass/trajectory data; current visualization does **not** implement this

The [working hypothesis](WORKING_HYPOTHESIS.md) remains unvalidated. No claimed discovery or missing-mass explanation follows from incomplete bookkeeping alone.
