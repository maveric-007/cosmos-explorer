# Cosmos Explorer — constellation data and interpretation

**Integrated:** 2026-10-24. The catalogue is a **frozen J2000 reference sample**, not the newest astronomical survey or a full six-dimensional dynamics solution.

## Sources and licensing

- **Star sky coordinates, approximate apparent magnitudes, B–V and HIP identifiers:** [HYG-based bright-star extract in Star Finder](https://github.com/mien-bot/Star-Finder/blob/main/public/data/hyg-bright.json). Original [HYG v4.1 archive by David Nash / Astronexus](https://github.com/astronexus/HYG-Database/tree/main/hyg/CURRENT), a compilation of Hipparcos, Yale Bright Star and Gliese data. **CC BY-SA 4.0**; see upstream license.
- **Distances in parsecs** from [starmap's versioned bright-star metadata](https://github.com/shaunak3000/starmap/blob/main/public/catalog/t0.meta.json), drawn from its HYG / AT-HYG compilation. Join is by numeric Hipparcos identifier, not star name. These are estimated distances and may differ by version and solution.
- **88 Western constellation line figures** from [Stellarium's Western sky culture](https://github.com/Stellarium/stellarium-skycultures/blob/master/western/index.json). Figure lines are **CC BY-SA** per [Stellarium Western sky-culture credits](https://github.com/Stellarium/stellarium-skycultures/blob/master/western/description.md). Copyright and cultural credit to the Stellarium team.
- **No constellation drawing is official IAU geometry.** The IAU defines 88 sky regions; the line-stick figures are a culturally selected projection from near Earth.

The combined data file `constellations-catalog.json` is a compact transformation/compilation of the above, provided with attribution and the upstream share-alike terms. This file does not change the independent software license of original Cosmos Explorer code.

## Columns and fidelity

Each star: `[HIP, RA_hours, Dec_degrees, distance_parsecs, apparent_visual_magnitude, B-V, proper_name_or_null]`. J2000 heliocentric positions computed as radial unit vectors from RA/Dec times distance; Galactic-local coordinates transform through the conventional ICRS-to-Galactic rotation and assume a Sun-to-center baseline of 26 kly as the **visualization's approximate scale**, not a precision Sagittarius A* reference frame.

**7,922** HIP-matched stars with positions and nonzero distance estimates. **88** Western constellation figures, involving 691 numerical HIP IDs; **690** have matching position-and-distance rows. One HIP star (89341) is missing from the combined set and its segment is omitted rather than assigned a fictitious location.

- **Sky pattern view:** projects stars onto a common observer-centered visual sphere; projected line figures are recognizable from the solar viewpoint, but apparent depth is deliberately removed.
- **True 3D view:** uses the supplied distance estimates; lines are visual links between physically separated stars, **not** gravitational connections, orbits or material filaments.
- The catalogue layer remains at **J2000** for both views; current animation does **not** propagate all these stars over time because proper motion and radial velocity are not present in this prepared subset. The existing separate three-star astrometric demonstration has limited straight-line motion.
- Sky orientation assumes the Sun/observer at the origin (Earth-vs-Sun parallax ignored on parsec scales). In the Milky Way scene, star positions are shown in an approximate Sagittarius A*-centered visual frame. These positions are not a mass census.
- Star-point radius and brightness are screen-legibility effects, not physical stellar diameters. `distance_parsecs` is a source estimate, not directly measured mass.

## Verify / next research steps

Match full Gaia source identifiers, epoch, parallax, radial velocity, covariance, appropriate distance posterior and stellar parameter tables before promoting these points into a 6D dynamics catalog. Preserve original versions, source refresh checks and transformation parameters. Hold out stars from fitting for kinematic validation; do not equate stable constellation shape with an orbit.
