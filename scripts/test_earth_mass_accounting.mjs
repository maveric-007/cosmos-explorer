#!/usr/bin/env node
import assert from 'node:assert/strict';
import {EARTH_MASS_LEDGER as data, earthMassLedgerHTML} from './earth-mass-accounting.mjs';

// Gravitational inference is known, but a complete incoming/outgoing mass budget is not.
assert.equal(data.schema, 'cosmos-earth-mass-ledger-v1');
assert.equal(data.earthGM.value, 398600.435507);
assert.equal(data.earthGM.units, 'km³/s²');
assert.equal(data.earthMass.value, 5.9722e24);
assert.equal(data.atmosphereMass.value, 5.1e18);
assert.equal(data.micrometeoritesAtSurface.value, 5200);
assert.equal(data.micrometeoritesAtSurface.units, 'metric tonnes/year');
assert.match(data.micrometeoritesAtSurface.scope, /not total material/);
assert.match(data.atmosphericLoss.units, /not specified/);
assert.equal(data.totalIncoming, null);
assert.equal(data.totalOutgoing, null);
assert.equal(data.netAnnualChange, null);
assert.equal(data.earthGM.uncertainty, null); // no falsely exact uncertainty
const html = earthMassLedgerHTML();
for (const label of ['ORBITALLY INFERRED','DERIVED / INFERRED','OBSERVATION-BASED ESTIMATE','UNKNOWN / UNRESOLVED']) {
  assert.ok(html.includes(label), 'missing evidence level ' + label);
}
assert.match(html, /do not add it a second time/);
assert.match(html, /not live daily measurements/);
assert.match(html, /net annual ΔM: not established/);
assert.match(html, /rel="noopener noreferrer"/);
console.log('Earth mass accounting evidence tests PASS');
