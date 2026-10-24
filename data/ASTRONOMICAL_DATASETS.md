# Cosmos Explorer — astronomical data-source inventory

**As-of:** 2026-10-24 (America/Chicago)  
**Scope:** sources for observable positions, velocities, physical size, mass estimates, planets, small bodies, diffuse matter, Galactic-center kinematics, and a later gravity-model comparison.  
**Status:** This is a **source inventory**, not evidence that any full catalog has been ingested. Published v3 still contains a small manually entered sample plus illustrative data. URLs point to source authorities and documentation checked on 2026-10-24.

## Research standard

1. **Observation** (angles, brightness, spectra, Doppler shift, proper motion, angular separation) is separate from **inference** (distance from parallax, stellar radius, estimated stellar mass, modeled galactic matter).
2. A catalog does not know every body. **Never replace missing mass with zero**; represent unmeasured contributions as uncertainty or an unresolved component. Avoid assuming missing matter necessarily explains galactic rotation.
3. Record **source name/release, exact column, original units, observed epoch, coordinate frame, measurement/derivation method, quality flag, uncertainty and source reference** for every value used. Crossmatch objects before summing mass or counting stars.
4. Many stars have 5D astrometry (angles, parallax and two proper motions) but **no radial velocity**. Full 6D phase space needs radial velocity; missing radial velocity cannot be silently treated as zero.
5. A measured size or luminosity is **not a direct mass measurement**. Stellar masses from fitting evolutionary models and asteroid masses from assumed density must be tagged inferred. Small bodies and dust may contribute gravity, but their importance must be calculated at the scale studied.
6. Do not publish gigabytes of source catalogs in GitHub Pages. Query only a bounded quality-controlled sample, save raw inputs/checksums separately, publish downsampled visualization products and source links.

## Verified catalog entry points

Each entry below is **source identified and documentation inspected; bulk catalog not yet downloaded**.

| Domain | Catalog / authoritative access | Scientific fields useful to us | Caveat and first use |
|---|---|---|---|
| Stellar 5D/6D | [ESA Gaia DR3 archive](https://gea.esac.esa.int/archive/) · [TAP API](https://www.cosmos.esa.int/web/gaia-users/archive/programmatic-access) | ICRS RA/Dec, parallax, PMRA/PMDEC, radial velocity subset, errors, source_id, RUWE | Some distances/velocities missing; selection functions and binary stars; first **bounded 6D sample** |
| Stellar radius/mass | [Gaia DR3 data release](https://www.cosmos.esa.int/web/gaia/dr3), astrophysical_parameters | photometric/spectroscopic stellar parameters; estimated radius/mass for subsets | Model-dependent radius/mass, not direct dynamical measurement |
| Stellar chemistry/mass | [GALAH DR4](https://www.galah-survey.org/dr4/the_catalogues/) | 917,588 stars; radial velocity, parameters, Bayesian mass, radius value-added catalog, Gaia DR3 IDs | Use quality flags and published uncertainty; crossmatch by Gaia ID |
| Spectroscopic velocity | [SDSS APOGEE DR17](https://www.sdss4.org/dr17/irspec/spectro_data/) | RVs, abundance, temperature, surface gravity; infrared penetrates dust | Selection/crowding and stellar model assumptions |
| Spectroscopic velocity | [LAMOST public DR12 v2.0](https://www.lamost.org/dr12/) · [release table](https://www.lamost.org/lmusers/) | spectra, stellar classifications, velocity/atmospheric parameters | DR13/DR14 identified as **internal**, not presumed publicly usable as of this date |
| Stellar + distant structure | [DESI DR1](https://data.desi.lbl.gov/doc/releases/dr1/) | large redshift sample; stellar spectra, galaxy redshifts | Extragalactic redshift-to-distance requires cosmology; not a 3D instantaneous snapshot |
| Near-infrared survey | [NASA/IPAC 2MASS](https://data.nasa.gov/dataset/2mass-all-sky-point-source-catalog) | near-IR point sources; crossmatches, obscured regions | Photometric detection is not direct mass or guaranteed 3D distance |
| Mid-infrared survey | [NASA/IPAC AllWISE](https://data.nasa.gov/dataset/allwise-source-catalog) | IR positions, fluxes, apparent motion, source identification | Mixed stars/galaxies/dust: careful source classification |
| Crossmatching/metadata | [CDS SIMBAD](https://simbad.cds.unistra.fr/simbad/) and [CDS VizieR](https://vizier.cds.unistra.fr/cgi-bin/VizieR) | alias resolution, source identifiers, vetted published catalogs | Aggregators; keep original observation paper and source release |
| Exoplanets/host stars | [NASA Exoplanet Archive TAP](https://exoplanetarchive.ipac.caltech.edu/docs/TAP/usingTAP.html) | planets, period, semimajor axis, planet radius/mass, host-star radius/mass, uncertainties | Many values null, estimated, or drawn from different references; `ps` vs `pscomppars` distinction |
| Solar system ephemerides | [JPL Horizons API](https://ssd-api.jpl.nasa.gov/doc/horizons.html) | planets, moons, barycentric vectors, time-tagged trajectories | **JPL's API must not be embedded in the website**; create precomputed versioned data extracts |
| Asteroids and comets | [JPL Small-Body Database](https://ssd-api.jpl.nasa.gov/doc/sbdb.html) | named small-body orbital elements, covariance, select diameter/rotation properties | Most objects lack directly measured mass/density; orbit solution changes with observations |
| Minor planet observations | [IAU Minor Planet Center data services](https://data.minorplanetcenter.net/) | observed positions, orbit solutions, designations, MPCORB | Detection incomplete, especially faint/distant bodies |
| Small-body archive | [NASA PDS Small Bodies Node](https://pds.nasa.gov/home/about/node-descriptions.shtml) | asteroid/comet, Kuiper Belt objects, interplanetary dust, mission/ground physical datasets | Archive of studies, not all small bodies or total belt mass |
| Small-body sizes | [NEOWISE diameters/albedos v2](https://www.ipac.caltech.edu/doi/10.26131/IRSA631) · [column definitions](https://irsa.ipac.caltech.edu/data/WISE/NEOWISE_SB/gator_docs/neowisesbprop_colDescriptions.html) | thermal-model diameter, error, albedo and assumed/fitted flags | **Diameter does not fix mass without density**; not complete Kuiper Belt |
| Atomic gas | [HI4PI full-sky neutral-hydrogen survey](https://arxiv.org/abs/1610.06175) | 21-cm brightness, column density, line-of-sight velocity | Converting signal to 3D gas distribution/mass requires temperature, distance and velocity modeling |
| Dust in 3D | [Bayestar 2019 dust map](https://dustmaps.readthedocs.io/en/latest/modules.html) | estimated reddening vs distance along sightlines | Dust extinction traces dust, not directly total gas or gravitational mass |
| Far-IR dust maps | [ESA Planck Legacy Archive](https://pla.esac.esa.int/) | microwave/submillimeter maps and modeled dust emission | Model-dependent foreground separation and dust-to-mass conversion |
| Galactic-center gravitational constraints | [ESO/MPE GRAVITY research](https://www.mpg.de/26915272/a-star-with-an-extreme-orbit-s301-feels-the-rotation-of-the-milky-way-s-central-black-hole) | directly followed S-star orbits near Sagittarius A*, including 2026 S301 finding | Near-center black-hole-dominated regime; not equivalent to Milky Way-wide potential |
| Galactic coordinates | [Astropy Galactocentric documentation](https://docs.astropy.org/en/stable/coordinates/example_gallery_plot_galactocentric_frame.html) | reference-frame conversion of ICRS positions + velocities to Galactic-center origin | **Not a dataset.** Transformation requires assumed Sun-GC distance, solar height/velocity, epoch conventions |

## Sagittarius A*–centered coordinate standard (planned processing)

Adopt **Galactocentric origin near Sagittarius A*** rather than Earth's position for all Galactic motion analyses. The standard right-handed Cartesian axes and velocities follow Astropy `Galactocentric` (no homemade subtraction of RA, Dec, or parallax). Reference-frame settings are **parameters**, not immutable truths.

Suggested **first-run sensitivity baseline**: Sun-to-center distance `R0=8.277 kpc` (published orbit-based literature value); Sun above plane `z_sun=20.8 pc`; solar Galactocentric Cartesian velocity `(11.1, 245.6, 7.78) km/s` (Astropy example baseline, not perfectly known). Store the adopted parameter values and citations with every derived row, then vary them in robustness tests. A Sagittarius A*-centered frame is an origin **choice**: it does **not** make the entire Galactic potential equal to a single point mass or magically measure missing motions.

The input ideally contains `source_id, ra_deg, dec_deg, distance_pc, pmra_mas_yr, pmdec_mas_yr, rv_km_s, epoch, uncertainties`; output contains `x_kpc,y_kpc,z_kpc,vx_km_s,vy_km_s,vz_km_s` and provenance. For credible 6D kinematics, use appropriate posterior distance estimates and preserve covariance. Simple inversion `distance_pc = 1000/parallax_mas` is only a **high-S/N initial smoke test**, not the production method.

## Ingestion order / honest progress

- **Inventory documented**: all sources listed above identified from official documentation or linked publications.
- **Not yet completed**: the bulk source downloads, catalog crossmatches, large-scale 3D position catalogs, full mass census, integrated Milky Way dynamics, or a measured missing-mass conclusion.
- **First implement**: a capped Gaia DR3 6D query; transform to Galactocentric positions and velocities with recorded settings; separately query NASA Exoplanet Archive for host/planet physical parameters.
- **Next**: GALAH/APOGEE/LAMOST RV/radius/mass crossmatch; gas/dust maps with distance uncertainty; JPL/MPC/NEOWISE physical bodies; gravity model comparison using the same immutable observational input.
- **Browser**: load a curated compressed subset (not raw Gaia's ~10 TB). Keep massive research/catalog extraction as an offline pipeline.

## Data quality gates

No fabricated star masses or body sizes. No default zero for missing radial velocities, density, or hidden-mass estimates. Every catalog row has a source ID and epoch, the exact measurement/inference label, units and quality flags. Cross-catalog duplicates removed by documented matching logic; propagate uncertainty in velocities, stellar distance, solar reference-frame choice and selection effects. Test predicted kinematics against **held-out** observational data and compare Newtonian ordinary matter vs dark-matter potentials vs alternative laws without fitting and evaluating on identical samples.
