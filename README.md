# Cosmos Explorer — GitHub Pages

An interactive 3D astronomy exploration application for Safari and desktop browsers.

## Research program — canonical home (2026-10-24)

**[Open the complete research hub](research/README.md)** — personal gravity research, astronomical data sources, original Earth and SPARC studies and executable scripts, migrated from `Home/Projects/Gravity-Research` with **14 matching original Git blob SHAs**.

**[Working Gravity Hypothesis](research/WORKING_HYPOTHESIS.md)** — a clearly labeled **testable, unvalidated hypothesis**: evaluate whether fuller independent inventories of ordinary matter and correctly modeled mass distribution reduce gravitational discrepancies, with head-to-head reference halo and modified-gravity comparisons and explicit falsification criteria.

[Original eleven open questions](research/Gravity-Research/Gravity-Research.md) · [current open questions O-12–O-15](research/OPEN_QUESTIONS.md) · [annotated equations](research/Gravity-Research/Gravity-Equations-and-Variable-Reference.md) · [SPARC experiments](research/Gravity-Research/README.md) · [JWST evidence assessment](research/JWST_DARK_MATTER_EVIDENCE.md) · [dataset inventory](data/ASTRONOMICAL_DATASETS.md) · [refresh protocol](research/DATA_REFRESH_PROTOCOL.md) · [migration audit](research/MIGRATION_MANIFEST.md).

**Integrity note:** Previous SPARC calculations are exploratory; the pinned 160-row cross-survey script has an open end-to-end reproduction requirement. The NASA exoplanet-source daily check is active; a general refresh job for the remaining astronomical sources is **not yet running**. Dark matter has **not** been disproved by this research, and the visualization is not a complete 6D gravitational simulation.


## Publish with GitHub Pages

1. Create a **public** GitHub repository named `cosmos-explorer` under `maveric-007`. Initialize it with a README so that the `main` branch exists.
2. The published root `index.html` is Cosmos Explorer **v3.2** with scale/time controls, a calculated cosmological light cone, a 7,922-star bright-sky layer, and a **searchable complete NASA confirmed planetary-system index** independent of constellations.
3. In the repository open **Settings → Pages** and select **Source: Deploy from a branch**, **Branch: main**, **Folder: /(root)**; click **Save**.
4. After GitHub reports publication, open `https://maveric-007.github.io/cosmos-explorer/` in Safari.

No build process or server is required. Internet access is needed to load Three.js from the jsDelivr CDN.

## All known planetary systems — v3.2

- The entire ingested [NASA Exoplanet Archive PSCompPars confirmed-planet catalog](data/exoplanet-systems.json) includes **6,451 confirmed planets grouped into 4,847 host systems** as checked **2026-10-25** (4,819 with 3D host positions; 5,956 with supplied semimajor axis). This is **not** a subset of constellation stars. All loaded host systems and planet names can be searched from the *Planetary-system search* control anywhere in the app, and explored in the separate **Planetary systems** 3D view.
- Plotted markers in Nearby stars/Milky Way are distance-capped for screen legibility, **but search covers every host**, including stars outside those views and hosts missing a 3D distance. The 88 Western constellation outlines are optional; they no longer turn the base 7,922-star map on/off.
- Orbital semimajor axes and masses/radii are NASA composite **observations and model estimates**; an orbit inferred from period + host-star mass is labelled **derived**. Planet positions and orbit-plane orientation are illustrative because most systems lack full epoch-matched 6D orbit ephemerides. Missing orbital distances result in a listed planet without a fictitious orbital path. Multi-star host systems are not inaccurately expanded into separately animated companions.
- The first successful GitHub Actions import generated [catalog refresh status](data/exoplanet-sync-status.json): **last checked** and **last imported** are separate fields; source's publication epoch is unknown from this extraction. A [daily GitHub Action](.github/workflows/exoplanets.yml) now checks *NASA only* using [the validated importer](scripts/sync_exoplanets.py); other astronomical sources do not yet refresh automatically.
- The full **all-star/catalog-coverage requirement** and next Gaia-scale ingestion phases are in [STAR_SYSTEM_SCOPE.md](docs/STAR_SYSTEM_SCOPE.md). The application is **not yet a full Gaia stellar database**. Catalogued ≠ all stars physically existing, and “no confirmed planets” ≠ no planets exist.

## v3.2 navigation and status

- **Space scale**: A logarithmic-style, level-of-detail slider steps through solar system → nearby stars → Milky Way → nearby galaxies → observable universe. Camera zoom varies smoothly **within** each band, but crossing a band boundary switches representations; it is **not** a mathematically seamless single-coordinate-scale universe yet. Black-hole spacetime remains a **separate physics mode** reached with its button.
- **Time/epoch**: Solar system 2026-10-24 through 2031-10-24 from bundled Swiss Ephemeris; three nearby stars ±20,000 years with linear propagation; Milky Way ±230 million years with a schematic circular solar orbit; nearby galaxies ±1 billion years with a radial-only Andromeda scenario. Observable universe now shows a numerically integrated, model-dependent flat ΛCDM **past light cone** for 0 to ~13.791 Gyr lookback; the shell radius is **comoving distance**, not a linear time fraction, and is not a time-evolving 3D universe survey. Black-hole spacetime is a stationary idealized physics view.
- **Star catalog and constellations (new)**: [data/constellations-catalog.json](data/constellations-catalog.json) holds **7,922 HIP-matched bright stars**, J2000 RA/Dec and approximate distance estimates, with **88** Western sky-culture figures (690 of 691 figure stars matched). In Nearby stars or Milky Way, toggle **Constellations** and choose a figure. **True 3D star distances** in Nearby stars restores each star's estimated depth; unchecked uses the familiar sky projection. These are **static J2000 sample coordinates**; they are not a 6D time-integrated Milky Way catalog. Only the previously existing three manually entered stellar samples have approximate propagated proper motions. [Attribution, licensing and caveats](data/CONSTELLATION_CREDITS.md).
- **Selected galaxy directions**: Andromeda (M31), Triangulum (M33), and M87 use J2000 ICRS pointing directions from SIMBAD and approximate distance estimates. Other galaxies, the Milky Way spiral and cosmic-web points retain illustrative/schematic positions.
- **Cosmological horizon (new)**: Planck-style base ΛCDM parameters, H₀=67.4 km/s/Mpc, Ωₘ=0.315, with approximate Ωᵣ=9.2×10⁻⁵ and flatness, are integrated over log(scale factor). Model results: **~13.791 Gyr age** and **~46.13 billion ly present-day comoving particle horizon**. The time control displays lookback, model redshift, scale factor, comoving and emission-epoch proper distance. Cosmic-web points remain **synthetic** (not observed galaxies). The model horizon is not the optical CMB surface; early-universe radiation/neutrino treatment is approximate. Sources: [Planck 2018](https://www.aanda.org/articles/aa/abs/2020/09/aa33910-18/aa33910-18.html), [Astropy FLRW conventions](https://docs.astropy.org/en/stable/api/astropy.cosmology.FLRW.html).

## Scientific interpretation

The planetary positions in this version are Swiss Ephemeris 2.10.03 / Moshier computations, sampled every two days and interpolated for 2026-10-24 through 2031-10-24. This is **not JPL Horizons** or a directly integrated general-relativistic n-body simulation. Black-hole gravity-well surfaces are mathematical visualizations of idealized relativistic geometries, not literal surfaces. Local stars, galaxies, and visual distance compressions include schematic elements, as labeled in the application. For high-precision or research use, provenance, uncertainties, and object-specific ephemerides should be reviewed separately.

### Responsive viewport layout (2026-10-29)

Desktop uses a viewport-fitting scene with independently scrollable sidebars; intermediate widths place the details panel below the scene; phone and narrow-tablet layouts stack the scene, navigation, search, playback controls and panels vertically. The layout assigns every direct frame child its own grid area so constellation and planetary-system tools cannot displace the canvas. Three.js resizes to the stage bounds, adjusts camera field of view to maintain horizontal framing on narrow screens, and responds to orientation and visual viewport changes without resetting navigation.

**Regression matrix:** Inspect widths of 320, 375, 390, 768, 1024, 1366 and 1920 CSS pixels, with portrait/landscape where applicable. Verify no horizontal scrolling or overlapping toolbars, a correctly fitted canvas, readable labels, and usable scale/time sliders, search, view changes, and touch zoom/orbit. Check actual iPhone Safari separately; source-level review and a successful Pages deploy do not prove real-device behavior.

## Rendering notes

Solar-system positions and velocities are calculated from the bundled ephemerides in physical AU. The 3D **rendering** uses a monotonic logarithmic distance transform (`9 × ln(1 + r/AU)` scene units) to separate inner planets on small screens; this does not alter measured positions in the object details. Orbital trajectories and moving planets use the same transform. Sun/planet radii remain illustrative, not physically to scale. Nearby-star labels are prioritized and hidden when they collide; some labels may not appear until the camera changes. On iPhone, playback controls sit immediately beneath the scene. The v3.2 scale and time sliders are implemented as a first usable, explicitly mixed-fidelity prototype; a fully continuous all-scale metric transform, full Gaia ingestion, validated physical stellar orbits, a measured cosmic-web map, and all-scale metric transitions remain future work.

## Deployment check

- [ ] Open the Planetary-system search, enter a NASA host such as TRAPPIST-1 and also a host **not** in the 88 figures, and select Explore system. All NASA systems must remain searchable even when not shown in the current zoomed scene.
- [ ] Verify the importer output totals against `data/exoplanet-sync-status.json` and check an unknown orbit stays unplotted, with the planet retained in detail lists.
- [ ] In Nearby stars and Milky Way, click catalogued host markers to enter their systems; constellation outlines should be independently toggleable without losing the base star points.
- [ ] Verify the three-dimensional planetary geometry is flagged illustrative rather than a measured 2026 ephemeris.

- For Nearby stars, verify the figure selector lists 88 constellation names; sky projection shows recognizable outlines and True 3D toggles line segments to physically estimated stellar depths.
- For Milky Way, catalogued stars should cluster near the Sun rather than forming an artificial outer galactic shell.
- For Observable universe, move time from 0 to 5, 10 and maximum lookback Gyr. Check the radius grows according to calculated **comoving light-cone distance** rather than linearly; point cloud remains labeled synthetic.
- Confirm GitHub Pages serves the separate star-catalog JSON. A failed data fetch must leave the solar-system and other views usable.

- Confirm the site loads and renders on desktop and iPhone Safari.
- Test all seven views (including the observable universe), move both sliders, change time range/playback, select objects, and toggle gravity-well slices.
- At the observable-universe scale, verify the lookback shell responds to time; in the nearby-star scale, verify Proxima Centauri, Barnard's Star, and Sirius move while schematic stars are stationary.
- On iPhone Safari, check controls fit, the timeline remains below the scene, and the scale switch from galaxies to observable universe does not throw a camera error.
- Confirm Pages is serving the latest `main` commit, and that the browser has network access to jsDelivr.