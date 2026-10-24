# Cosmos Explorer — GitHub Pages

An interactive 3D astronomy exploration application for Safari and desktop browsers.

## Publish with GitHub Pages

1. Create a **public** GitHub repository named `cosmos-explorer` under `maveric-007`. Initialize it with a README so that the `main` branch exists.
2. The published root `index.html` is Cosmos Explorer **v3** with independent space and time sliders, responsive layouts, sampled astrometric motion, and an observable-universe overview. `.nojekyll` preserves direct static serving.
3. In the repository open **Settings → Pages** and select **Source: Deploy from a branch**, **Branch: main**, **Folder: /(root)**; click **Save**.
4. After GitHub reports publication, open `https://maveric-007.github.io/cosmos-explorer/` in Safari.

No build process or server is required. Internet access is needed to load Three.js from the jsDelivr CDN.

## v3 navigation and status

- **Space scale**: A logarithmic-style, level-of-detail slider steps through solar system → nearby stars → Milky Way → nearby galaxies → observable universe. Camera zoom varies smoothly **within** each band, but crossing a band boundary switches representations; it is **not** a mathematically seamless single-coordinate-scale universe yet. Black-hole spacetime remains a **separate physics mode** reached with its button.
- **Time/epoch**: Solar system 2026-10-24 through 2031-10-24 from the bundled Swiss Ephemeris; nearby stars ±20,000 years using straight-line propagation for three sampled astrometric objects; Milky Way ±230 million years using a schematic circular solar orbit; nearby galaxies ±1 billion years using a radial-only Andromeda scenario; observable universe 0–13.8 billion years lookback using an illustrative shell (not a measured light cone). Time sliders and playback controls change range and units by mode. Black-hole spacetime has no claimed time-evolution model.
- **Selected star positions**: Proxima Centauri, Barnard's Star, and Sirius have manually entered, approximately published J2000 sky directions, distances, proper motions, and radial velocities. Their propagated locations assume constant velocity and do **not** account for binary orbits, solar motion, or full Galactic dynamics. Source records are linked in the application. Other displayed stars still have schematic directions.
- **Selected galaxy directions**: Andromeda (M31), Triangulum (M33), and M87 use J2000 ICRS pointing directions from SIMBAD and approximate distance estimates. Other galaxies, the Milky Way spiral and cosmic-web points retain illustrative/schematic positions.
- **Observed vs modeled**: The application labels ephemeris calculations, approximate astrometry, simplified extrapolations and purely illustrative scenes separately. It does not load Gaia DR3 wholesale, integrate general-relativistic N-body trajectories, or reconstruct cosmic evolution.

## Scientific interpretation

The planetary positions in this version are Swiss Ephemeris 2.10.03 / Moshier computations, sampled every two days and interpolated for 2026-10-24 through 2031-10-24. This is **not JPL Horizons** or a directly integrated general-relativistic n-body simulation. Black-hole gravity-well surfaces are mathematical visualizations of idealized relativistic geometries, not literal surfaces. Local stars, galaxies, and visual distance compressions include schematic elements, as labeled in the application. For high-precision or research use, provenance, uncertainties, and object-specific ephemerides should be reviewed separately.

## Rendering notes

Solar-system positions and velocities are calculated from the bundled ephemerides in physical AU. The 3D **rendering** uses a monotonic logarithmic distance transform (`9 × ln(1 + r/AU)` scene units) to separate inner planets on small screens; this does not alter measured positions in the object details. Orbital trajectories and moving planets use the same transform. Sun/planet radii remain illustrative, not physically to scale. Nearby-star labels are prioritized and hidden when they collide; some labels may not appear until the camera changes. On iPhone, playback controls sit immediately beneath the scene. The v3 scale and time sliders are implemented as a first usable, explicitly mixed-fidelity prototype; a fully continuous all-scale metric transform, large catalog ingestion, and validated physical evolution models remain future work.

## Deployment check

- Confirm the site loads and renders on desktop and iPhone Safari.
- Test all six views (including the observable universe), move both sliders, change time range/playback, select objects, and toggle gravity-well slices.
- At the observable-universe scale, verify the lookback shell responds to time; in the nearby-star scale, verify Proxima Centauri, Barnard's Star, and Sirius move while schematic stars are stationary.
- On iPhone Safari, check controls fit, the timeline remains below the scene, and the scale switch from galaxies to observable universe does not throw a camera error.
- Confirm Pages is serving the latest `main` commit, and that the browser has network access to jsDelivr.