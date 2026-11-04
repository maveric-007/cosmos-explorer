#!/usr/bin/env node
import assert from 'node:assert/strict';
import {galacticSunKpc,galacticOffsetAU,eclipticToGalacticTangentAU,propagateKeplerAU,GALACTIC_MODEL} from './galactic-kinematics.mjs';

const atZero=galacticSunKpc(0);
assert.ok(Math.abs(atZero.x-GALACTIC_MODEL.radiusKpc)<1e-12);
assert.ok(Math.abs(atZero.y-GALACTIC_MODEL.sunHeightKpc)<1e-12);
assert.ok(Math.abs(atZero.z)<1e-12);
const drift=galacticOffsetAU(425);
assert.ok(drift.displacementAU>19000 && drift.displacementAU<23000, '425-year Galactic drift should be ~20k AU');
assert.equal(galacticOffsetAU(500,500).displacementAU,0,'re-anchoring must preserve zero displacement');
assert.ok(Math.abs(galacticSunKpc(4e7).radiusKpc-atZero.radiusKpc)>.01,'Galactic path must not be a circle');
assert.ok(Math.abs(galacticSunKpc(2e7).y-atZero.y)>.01,'Galactic path must not be flat');
assert.ok(Number.isFinite(galacticOffsetAU(-230e6).displacementAU));
const testAU=eclipticToGalacticTangentAU([1,0,0]);
assert.ok(Math.abs(Math.hypot(testAU.alongAU,testAU.radialAU,testAU.verticalAU)-1)<1e-6,'rotation retains AU lengths');
const pos=[1,0,0],vel=[0,Math.sqrt(.0002959122082855911),0];
for(const t of [0,365.25,425*365.25,-20000*365.25,230e6*365.25]){
 const p=propagateKeplerAU(pos,vel,t);
 assert.ok(p.pos.every(Number.isFinite));
 assert.ok(Math.abs(Math.hypot(...p.pos)-1)<1e-9,'circular two-body orbit stays bounded');
}
const origin=propagateKeplerAU(pos,vel,0);
assert.ok(Math.hypot(...origin.pos.map((v,i)=>v-pos[i]))<1e-10);
console.log('Galactic motion shared-state and Kepler fallback numeric checks PASS');
