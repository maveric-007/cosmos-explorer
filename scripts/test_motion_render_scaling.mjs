#!/usr/bin/env node
import assert from 'node:assert/strict';
import { visualOrbitOffsetAU, projectedMotionMarker, MOTION_ORBIT_VISUAL_SCALE } from './motion-render-scaling.mjs';

const mer=visualOrbitOffsetAU({alongAU:.387,radialAU:0,verticalAU:0});
const earth=visualOrbitOffsetAU({alongAU:1,radialAU:0,verticalAU:0});
const jup=visualOrbitOffsetAU({alongAU:5.203,radialAU:0,verticalAU:0});
assert.ok(mer.x > 7 && earth.x > mer.x + 7 && jup.x > earth.x + 20, 'Inner planet orbits must be distinguishable');
assert.equal(visualOrbitOffsetAU({alongAU:0,radialAU:0,verticalAU:0}).x,0);
assert.ok(Math.abs(earth.x - MOTION_ORBIT_VISUAL_SCALE*Math.log(2))<1e-10);
for(const cameraDist of [.5, 2, 15, 50, 225, 500, 2000]){
 for(const h of [320,568,844,1200]){
  for(const fov of [47,78]){
   const values=['Sun','Mercury','Venus','Earth','Mars','Jupiter','Saturn','Uranus','Neptune','Planet Nine (hypothesis)'];
   for(const name of values){
    const radius=projectedMotionMarker(name,cameraDist,h,fov);
    assert.ok(Number.isFinite(radius.worldRadius) && radius.worldRadius>0, 'Marker radius must be finite');
    assert.ok(radius.projectedRadiusPx <= radius.maxPx + 1e-8, name+' exceeded screen cap at '+cameraDist);
   }
  }
 }
}
const zoom=projectedMotionMarker('Sun',.5,844,78);
assert.ok(zoom.projectedRadiusPx<=9.01 && zoom.projectedRadiusPx>=8.99,'Extremely close Sun must stay below 18 px diameter');
const j=projectedMotionMarker('Jupiter',.5,844,78);
assert.ok(j.projectedRadiusPx <= 5.51,'Jupiter must not become a huge foreground disc');
console.log('Mobile projected body sizes and monotonic motion-orbit spacing PASS');
