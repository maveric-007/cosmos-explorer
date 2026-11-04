#!/usr/bin/env node
import assert from 'node:assert/strict';
import {planetNineScenarioAU,PLANET_NINE_SCENARIO as P} from './planet-nine-scenario.mjs';
assert.match(P.status,/UNCONFIRMED/);
assert.match(P.positionStatus,/unknown/);
const peri=P.semimajorAxisAU*(1-P.eccentricity),aph=P.semimajorAxisAU*(1+P.eccentricity);
for(const y of [-1e6,0,1e4,1e6]){
 const p=planetNineScenarioAU(y),r=Math.hypot(...p);
 assert.ok(p.every(Number.isFinite));
 assert.ok(r>=peri-1e-7&&r<=aph+1e-7,'representative orbit remains bound');
}
const a=planetNineScenarioAU(12.34),b=planetNineScenarioAU(12.34+P.periodYears);
assert.ok(Math.hypot(...a.map((v,i)=>v-b[i]))<1e-6,'scenario orbital phase cycles');
console.log('Unconfirmed Planet Nine scenario checks PASS');
