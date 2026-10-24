# Cosmos Explorer — GitHub Pages

An interactive 3D astronomy exploration application for Safari and desktop browsers.

## Publish with GitHub Pages

1. Create a **public** GitHub repository named `cosmos-explorer` under `maveric-007`. Initialize it with a README so that the `main` branch exists.
2. Add the contents of this package (`index.html`, `.nojekyll`) to the root of the `main` branch. The index file is the existing Cosmos Explorer v2 application, unchanged.
3. In the repository open **Settings → Pages** and select **Source: Deploy from a branch**, **Branch: main**, **Folder: /(root)**; click **Save**.
4. After GitHub reports publication, open `https://maveric-007.github.io/cosmos-explorer/` in Safari.

No build process or server is required. Internet access is needed to load Three.js from the jsDelivr CDN.

## Scientific interpretation

The planetary positions in this version are Swiss Ephemeris 2.10.03 / Moshier computations, sampled every two days and interpolated for 2026-10-24 through 2031-10-24. This is **not JPL Horizons** or a directly integrated general-relativistic n-body simulation. Black-hole gravity-well surfaces are mathematical visualizations of idealized relativistic geometries, not literal surfaces. Local stars, galaxies, and visual distance compressions include schematic elements, as labeled in the application. For high-precision or research use, provenance, uncertainties, and object-specific ephemerides should be reviewed separately.

## Deployment check

- Confirm the site loads and renders on desktop and iPhone Safari.
- Drag the view, select objects, change scales, and toggle gravity-well slices.
- Confirm Pages is serving the latest `main` commit, and that the browser has network access to jsDelivr.