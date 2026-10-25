# Star and planetary-system coverage — authoritative product requirement

**Accepted:** 2026-10-25 · **Version:** 1.0 · **Owner:** Cosmos Explorer
**Principle:** Astronomical observations, **not membership in any constellation**, define the eligible stars and systems.

## Inclusion rule

**Include every star or gravitationally associated star system with usable published astronomical records in the supported source releases.** When its planets, stellar companions, moons or small bodies have confirmed or otherwise suitably classified published data, associate each body with the proper host and preserve what is known. Do not restrict the search/render database to the IAU 88 constellation patterns, the Hipparcos bright-star subset or manually chosen nearby stars.

The user must be able to search the entire ingested index and drill down from sky/Galactic scale → host system → specific planets and observed companions. Use level-of-detail rendering and scoped queries; billions of stars need not be rendered as billions of simultaneous markers on a phone.

## Current implementation — checked 2026-10-25

- **NASA Exoplanet Archive PSCompPars:** actual imported **6,451 confirmed exoplanets in 4,847 host systems**; 4,819 hosts had sky position plus distance sufficient for 3D placement; 5,956 planets had an archive semimajor-axis value. This is the complete current **confirmed composite table**, not all Gaia objects or suspected candidate exoplanets.
- [Ingested all-host dataset](../data/exoplanet-systems.json), [audit/status](../data/exoplanet-sync-status.json), [Python standard-library importer](../scripts/sync_exoplanets.py), [daily GitHub Actions workflow](../.github/workflows/exoplanets.yml). The importer checks one row per planet, source counts, no duplicate planet names, coordinate range and non-negative distances; failed checks don't replace the existing catalog.
- [7,922-star HYG-based sample](../data/constellations-catalog.json), separate from NASA's full confirmed host index. Its 88 Western figures are **optional annotations**, not a filter. A Hipparcos crossmatch may link to a NASA host; host search remains comprehensive even without a Hipparcos ID.
- **Host search:** full loaded index matches host or planet name, not limited to the currently visible slice. **3D host markers:** only when source RA/Dec and distance exist; the Nearby stars and Milky Way views cull physically distant points at their appropriate level of detail. Unplottable systems remain findable by search.
- **Planetary system view:** catalogued planets appear as labelled planets with an orbit when semimajor axis exists, or an explicitly derived Kepler estimate when period and stellar mass exist. Planets lacking either remain in the selectable system details but do not acquire invented orbits. **Positions/orientation/phases are illustrated** unless a future source provides a consistent precise 6D epoch ephemeris.
- The Solar System is separately represented by the bundled Swiss Ephemeris 2026–2031 (not JPL Horizons).

## Critical limitations (scientific and engineering)

1. **All known planet-host systems ≠ all known stars.** Gaia has a vastly larger astrometric catalog. The HYG subset and all-host NASA exoplanets do not yet span Gaia DR3 full stars or every independently discovered star lacking known planets.
2. **No planets confirmed ≠ no planets exist.** Non-detection and catalog incompleteness are not evidence of a planet-free system.
3. NASA PSCompPars **composite fields may mix publications and parameter sets**. A reported `pl_orbsmax` can represent projected separation for directly imaged / microlensing planets; reported inclination is not enough to know the 3D orbital node. Do not describe display orbit as a measured instantaneous position.
4. **Multiple star systems:** NASA reports host-system `sy_snum` and some circumbinary status, but detailed component astrometry or true multiple-star orbits are not generated from an aggregate host entry. Do not render invented companions or gravitating masses.
5. **Dynamical modeling:** A 3D location, estimated stellar mass and schematic planet orbit do not furnish initial conditions for a full N-body integration. Orbital velocities, uncertainties, crossmatches, epoch standards and each body mass must come from appropriate sources.
6. **Scale and performance:** overlay large star catalogs by tiles, magnitude and distance culls or spatial indices. Preserve all searchable source records separately from point-render subsets. Gaia-scale ingestion requires a separate indexed backend or precomputed tile pipeline and provider-conscious access policy.
7. **Metadata timestamps:** `last_checked_utc` is a fetch log; the actual source release or observation dates may differ or not be published in a machine-readable form. Preserve `last_imported_utc` and the exact source SHA separately.
8. **Archive scope:** NASA Exoplanet Archive confirmed planets are the first planetary-system provider. The search does not yet integrate unconfirmed candidates, non-NASA catalogs of binary companions, full stellar spectroscopy, moon ephemerides, or the distribution of exoplanet comets/asteroids. Future sources must be individually provenance-tagged and deduplicated.

## Next expansion sequence

1. Query Gaia (and supplementary Hipparcos/GALAH/APOGEE/LAMOST) using **source_id**, sky tiles and quality flags; build a scalable *all-available-star* index, including those with no known exoplanets. Respect source epoch and 5D/6D availability.
2. Crossmatch star Gaia DR3 / DR2 ID, HIP, HD, aliases and carefully reviewed positional matches to existing exoplanet hosts. Avoid duplicate stars or accidental merging of binary components. Preserve mismatches for review.
3. Enrich every known host with stellar radius/mass/spectroscopy where source-supported; maintain direct, model-derived and absent values distinctly, including uncertainties.
4. Add independently verified multiple-star orbits, moons and planetary satellites when data allow. Import planet candidates separately with **candidate/unconfirmed** labels; never silently present them as confirmed.
5. For sufficiently constrained systems, integrate physical trajectories with correct initial state vectors, gravitational masses and observation epochs; compare to published ephemerides and clearly mark simulated future and past movement.
6. Include the mass budget and non-detections only as **bounded evidence** in the broader [gravity hypothesis research](../research/WORKING_HYPOTHESIS.md); no arbitrary planetary population to fix galactic gravitational residuals.

## Data authorities

- [NASA Exoplanet Archive TAP / PSCompPars](https://exoplanetarchive.ipac.caltech.edu/docs/TAP/usingTAP.html)
- [Planetary-system field definitions](https://exoplanetarchive.ipac.caltech.edu/docs/API_PS_columns.html)
- [ESA Gaia Archive](https://gea.esac.esa.int/archive/)
- [NASA JPL Horizons](https://ssd.jpl.nasa.gov/horizons/)
- [CDS SIMBAD](https://simbad.cds.unistra.fr/simbad/)
