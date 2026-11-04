/**
 * Shared, time-dependent reference model for Cosmos Explorer.
 *
 * Coordinates: Sun at (8.2 kpc, +0.0208 kpc, 0) at 2026-10-24;
 * x/z in the Galactic disk, y perpendicular to the disk. Sagittarius A* is
 * the coordinate origin, NOT the sole gravitational source.
 *
 * This is an explicit axisymmetric epicyclic SCENARIO, not an integrated orbit
 * from a fitted Galactic gravitational potential. Radial/vertical amplitudes,
 * phases and periods are illustrative. Do not classify these as observations.
 */
export const GALACTIC_MODEL = Object.freeze({
  epoch: '2026-10-24T00:00:00Z',
  radiusKpc: 8.2,
  sunHeightKpc: 0.0208,
  azimuthalSpeedKmS: 230,
  radialAmplitudeKpc: 0.35,
  radialPeriodYears: 155e6,
  verticalAmplitudeKpc: 0.09,
  verticalPeriodYears: 85e6,
  model: 'approximate epicyclic, non-circular, not N-body'
});
export const AU_KM = 149597870.7;
const KPC_KM = 3.085677581491367e16;
const YEAR_SECONDS = 365.25 * 86400;
const KPC_TO_AU = KPC_KM / AU_KM;
const T = Math.PI * 2;
const radialFrequency = T / GALACTIC_MODEL.radialPeriodYears;
const verticalFrequency = T / GALACTIC_MODEL.verticalPeriodYears;
const angularFrequency = GALACTIC_MODEL.azimuthalSpeedKmS * YEAR_SECONDS /
  (KPC_KM * GALACTIC_MODEL.radiusKpc);

export function galacticSunKpc(yearsSinceEpoch) {
  if (!Number.isFinite(yearsSinceEpoch)) throw new RangeError('Nonfinite epoch');
  const rPhase = 0.37, vPhase = 0.23, t = yearsSinceEpoch;
  const r = GALACTIC_MODEL.radiusKpc + GALACTIC_MODEL.radialAmplitudeKpc *
    (Math.sin(radialFrequency * t + rPhase) - Math.sin(rPhase));
  const phi = angularFrequency * t +
    (2 * angularFrequency / radialFrequency) *
    (GALACTIC_MODEL.radialAmplitudeKpc / GALACTIC_MODEL.radiusKpc) *
    (Math.cos(radialFrequency * t + rPhase) - Math.cos(rPhase));
  const y = GALACTIC_MODEL.sunHeightKpc + GALACTIC_MODEL.verticalAmplitudeKpc *
    (Math.sin(verticalFrequency * t + vPhase) - Math.sin(vPhase));
  return { x: r * Math.cos(phi), y, z: r * Math.sin(phi), radiusKpc: r, azimuthRad: phi };
}

export function galacticOffsetAU(yearsSinceEpoch, originYears = 0) {
  const p = galacticSunKpc(yearsSinceEpoch), a = galacticSunKpc(originYears);
  const dx = p.x - a.x, dz = p.z - a.z, angle = a.azimuthRad;
  const radialAU = (dx * Math.cos(angle) + dz * Math.sin(angle)) * KPC_TO_AU;
  const alongAU = (-dx * Math.sin(angle) + dz * Math.cos(angle)) * KPC_TO_AU;
  const verticalAU = (p.y - a.y) * KPC_TO_AU;
  return { alongAU, radialAU, verticalAU, displacementAU: Math.hypot(alongAU, radialAU, verticalAU) };
}

// J2000 heliocentric ecliptic AU -> Galactocentric local scene basis.
// Return (along-track, vertical, outward radial) AU relative to Sun.
// Rotations account for mean J2000 obliquity and ICRS -> Galactic orientation;
// the approximation lies in the adopted orientation/epoch and dynamical model.
export function eclipticToGalacticTangentAU(au, tangentOriginYears = 0) {
  const eps = 23.439291111 * Math.PI / 180;
  const [x, eY, eZ] = au;
  const y = Math.cos(eps) * eY - Math.sin(eps) * eZ;
  const z = Math.sin(eps) * eY + Math.cos(eps) * eZ;
  const gx = -0.0548755604*x - 0.8734370902*y - 0.4838350155*z;
  const gy =  0.4941094279*x - 0.4448296300*y + 0.7469822445*z;
  const gz = -0.8676661490*x - 0.1980763734*y + 0.4559837762*z;
  const phi = galacticSunKpc(tangentOriginYears).azimuthRad;
  const rx = -gx, rz = gy;
  return { alongAU: -rx*Math.sin(phi)+rz*Math.cos(phi), radialAU: rx*Math.cos(phi)+rz*Math.sin(phi), verticalAU: gz };
}

// Two-body Kepler fallback from sampled heliocentric (position, velocity)
// at the start of the 2026-2031 source ephemeris. Ignores perturbations and
// long-term secular changes; NEVER label long-range output as an ephemeris.
export function propagateKeplerAU(position, velocity, elapsedDays) {
  const mu = 0.0002959122082855911; // Solar GM (AU^3/day^2)
  const dot = (a,b) => a[0]*b[0]+a[1]*b[1]+a[2]*b[2];
  const cross = (a,b) => [a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0]];
  const norm = a => Math.hypot(...a);
  const scale = (a,f) => a.map(v=>v*f);
  const r = norm(position), v2 = dot(velocity,velocity), a = 1 / (2/r-v2/mu);
  if (!(a > 0) || !Number.isFinite(elapsedDays)) throw new RangeError('Unsupported Kepler orbit');
  const h = cross(position,velocity), hHat = scale(h,1/norm(h));
  const eVec = cross(velocity,h).map((q,i)=>q/mu-position[i]/r);
  const e = norm(eVec);
  if (e >= 1) throw new RangeError('Unbound Kepler orbit');
  const P = e > 1e-8 ? scale(eVec,1/e) : scale(position,1/r);
  const Q = cross(hHat,P);
  const beta = Math.sqrt(1-e*e);
  const E0 = Math.atan2(dot(position,Q)/(a*beta),dot(position,P)/a+e);
  const M0 = E0-e*Math.sin(E0), period = T*Math.sqrt(a*a*a/mu);
  let M = ((M0 + (elapsedDays%period)*(T/period)) % T + T) % T;
  if(M > Math.PI) M -= T;
  let E = M;
  for(let i=0;i<12;i++){const step=(E-e*Math.sin(E)-M)/(1-e*Math.cos(E));E-=step;if(Math.abs(step)<1e-13)break;}
  const c=a*(Math.cos(E)-e),s=a*beta*Math.sin(E);
  const point = P.map((v,i)=>c*v+s*Q[i]);
  const dEdt=Math.sqrt(mu/(a*a*a))/(1-e*Math.cos(E));
  const velocityResult=P.map((v,i)=>(-a*Math.sin(E)*v+a*beta*Math.cos(E)*Q[i])*dEdt);
  return { pos: point, vel:velocityResult, type:'estimated Kepler two-body' };
}
