/**
 * Render-only presentation of Solar System motion across Galactic scales.
 *
 * Physical AU state vectors are never altered. This radial, monotonic map
 * improves visibility of inner orbits on a phone; use only for scene geometry.
 * A body marker is a visual glyph, not a metrically sized sphere.
 */
export const MOTION_ORBIT_VISUAL_SCALE = 22; // scene units per ln(1 + radius / AU)

export const MOTION_MARKER_SPECS = Object.freeze({
  Sun:       { minPx:3.6, maxPx:9.0, baseWorldRadius:0.70, maxWorldRadius:2.15 },
  Mercury:   { minPx:2.0, maxPx:3.5, baseWorldRadius:0.09, maxWorldRadius:0.75 },
  Venus:     { minPx:2.2, maxPx:3.8, baseWorldRadius:0.11, maxWorldRadius:0.85 },
  Earth:     { minPx:2.4, maxPx:4.0, baseWorldRadius:0.12, maxWorldRadius:0.85 },
  Mars:      { minPx:2.1, maxPx:3.6, baseWorldRadius:0.10, maxWorldRadius:0.75 },
  Jupiter:   { minPx:3.0, maxPx:5.5, baseWorldRadius:0.22, maxWorldRadius:1.25 },
  Saturn:    { minPx:2.9, maxPx:5.0, baseWorldRadius:0.20, maxWorldRadius:1.15 },
  Uranus:    { minPx:2.5, maxPx:4.5, baseWorldRadius:0.16, maxWorldRadius:1.00 },
  Neptune:   { minPx:2.5, maxPx:4.5, baseWorldRadius:0.16, maxWorldRadius:1.00 },
  'Planet Nine (hypothesis)': { minPx:2.5, maxPx:4.5, baseWorldRadius:0.14, maxWorldRadius:1.0 }
});
const DEFAULT_SPEC = Object.freeze({ minPx:2, maxPx:4, baseWorldRadius:0.10, maxWorldRadius:0.75 });

export function visualOrbitOffsetAU({ alongAU, verticalAU, radialAU }) {
  const length = Math.hypot(alongAU, verticalAU, radialAU);
  if(!(length > 0))return { x:0, y:0, z:0 };
  const ratio = MOTION_ORBIT_VISUAL_SCALE * Math.log1p(length) / length;
  return { x: alongAU * ratio, y:verticalAU * ratio, z:radialAU * ratio };
}

/**
 * Returns a radius in SCENE units with projected minimum and maximum
 * glyph radii in CSS px, limited by orbital clearance in world units.
 *
 * On a far-away view, the maxWorldRadius cap takes precedence over minPx;
 * it is better to show a small dot/label than blot out nearby orbits.
 */
export function projectedMotionMarker(name, distance, viewportHeight, verticalFovDegrees) {
  const spec = MOTION_MARKER_SPECS[name] || DEFAULT_SPEC;
  const d = Math.max(0.01, distance);
  const height = Math.max(1, viewportHeight);
  const halfFov = Math.max(1, Math.min(89, verticalFovDegrees / 2)) * Math.PI / 180;
  const pxPerUnit = height / (2 * Math.tan(halfFov) * d);
  // minPx/maxPx are RADII, not diameters.
  const naturalPx = spec.baseWorldRadius * pxPerUnit;
  const desiredPx = Math.max(spec.minPx, Math.min(spec.maxPx, naturalPx));
  const worldRadius = Math.min(spec.maxWorldRadius, desiredPx / pxPerUnit);
  return { worldRadius, projectedRadiusPx: worldRadius * pxPerUnit, minPx:spec.minPx, maxPx:spec.maxPx };
}
