// Earth mass accounting: provenance-labeled reference values, not a live mass-balance measurement.
// Source URLs and units are retained verbatim where the publisher did not define "ton".
export const EARTH_MASS_LEDGER = Object.freeze({
  schema: 'cosmos-earth-mass-ledger-v1',
  reviewedDate: '2026-11-10',
  earthGM: Object.freeze({
    value: 398600.435507, units: 'km³/s²',
    classification: 'ORBITALLY INFERRED',
    method: 'JPL DE440 planetary ephemeris gravitational parameter',
    source: 'https://ssd.jpl.nasa.gov/astro_par.html',
    uncertainty: null
  }),
  earthMass: Object.freeze({
    value: 5.9722e24, units: 'kg',
    classification: 'DERIVED / INFERRED',
    method: 'NASA rounded mass reference; mass in kilograms depends on independent G',
    source: 'https://nssdc.gsfc.nasa.gov/planetary/factsheet/earthfact.html',
    uncertainty: null
  }),
  atmosphereMass: Object.freeze({
    value: 5.1e18, units: 'kg',
    classification: 'MODEL ESTIMATE',
    method: 'NASA terrestrial atmosphere reference; already included in the Earth system mass',
    source: 'https://nssdc.gsfc.nasa.gov/planetary/factsheet/earthfact.html',
    uncertainty: null
  }),
  micrometeoritesAtSurface: Object.freeze({
    value: 5200, units: 'metric tonnes/year',
    classification: 'OBSERVATION-BASED ESTIMATE',
    scope: 'Micrometeorites reaching the ground, extrapolated from Antarctic samples; not total material arriving at the atmosphere',
    source: 'https://doi.org/10.1016/j.epsl.2021.116794',
    uncertainty: null
  }),
  atmosphericLoss: Object.freeze({
    hydrogen: 95000, helium: 1500, oxygen: 100,
    units: 'tons/year (NASA educational slide; ton convention not specified)',
    classification: 'PUBLISHED APPROXIMATIONS',
    scope: 'Selected escaping gases, not a complete Earth-system outgoing mass ledger',
    source: 'https://assets.science.nasa.gov/content/dam/science/hpd/heat/heat-pdfs/hby-and-math-slide-decks/HBY%20and%20Math%2017_%20Atmosphere%20Loss%20Through%20Solar%20Wind.pdf?emrc=68d6c6d716c3f',
    uncertainty: null
  }),
  totalIncoming: null,
  totalOutgoing: null,
  netAnnualChange: null
});

export function earthMassLedgerHTML() {
  const d = EARTH_MASS_LEDGER;
  const link = (url, label) => `<a href="${url}" target="_blank" rel="noopener noreferrer">${label}</a>`;
  return `<details class="mass-budget-detail" open>
    <summary>Earth mass accounting · evidence levels</summary>
    <div class="mass-budget-row"><span class="mass-budget-level">ORBITALLY INFERRED</span>
      <strong>GM = ${d.earthGM.value.toFixed(6)} km³/s²</strong>
      <p>JPL DE440 fitted gravitational parameter. This is more directly constrained by orbital motion than kilograms of mass. ${link(d.earthGM.source, 'JPL source')}</p></div>
    <div class="mass-budget-row"><span class="mass-budget-level">DERIVED / INFERRED</span>
      <strong>Earth mass ≈ 5.9722 × 10²⁴ kg</strong>
      <p>Rounded NASA reference, dependent on the independently determined gravitational constant G. Not a direct count of Earth's matter. ${link(d.earthMass.source, 'NASA Earth fact sheet')}</p></div>
    <div class="mass-budget-row"><span class="mass-budget-level">MODEL ESTIMATE</span>
      <strong>Atmosphere ≈ 5.1 × 10¹⁸ kg</strong>
      <p>Included in Earth's overall mass — do not add it a second time. ${link(d.atmosphereMass.source, 'NASA')}</p></div>
    <div class="mass-budget-row"><span class="mass-budget-level">OBSERVATION-BASED ESTIMATE</span>
      <strong>Surface micrometeorites ≈ ${d.micrometeoritesAtSurface.value.toLocaleString('en-US')} metric tonnes/year</strong>
      <p>Material that reaches the ground, <em>not</em> all incoming space material. ${link(d.micrometeoritesAtSurface.source, 'Rojas et al. 2021')}</p></div>
    <div class="mass-budget-row"><span class="mass-budget-level">PUBLISHED APPROXIMATIONS</span>
      <strong>Atmospheric escape: H ≈ 95,000; He ≈ 1,500; O ≈ 100 tons/year</strong>
      <p>NASA education estimates. The source says “tons” without establishing a metric-tonne convention; these are not comparable totals until units, period and scope are reconciled. ${link(d.atmosphericLoss.source, 'NASA HEAT')}</p></div>
    <div class="mass-budget-row mass-budget-unknown"><span class="mass-budget-level">UNKNOWN / UNRESOLVED</span>
      <strong>Full incoming mass, full outgoing mass, net annual ΔM: not established</strong>
      <p>No invented zero or falsely precise net. Surface deposition alone omits atmospheric entry/ablation; selected gas escape estimates omit other flows. No measured annual total can be derived by simply subtracting the rows above.</p></div>
    <p class="mass-budget-footnote">Reference estimates are <strong>not live daily measurements</strong>; cited source methods have different dates and uncertainty coverage. This ledger does not yet drive the 3D gravitational solver. <a href="./research/EARTH_MASS_BUDGET.md">Read scope, provenance and validation plan</a>.</p>
  </details>`;
}
