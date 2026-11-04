/**
 * Optional Planet Nine HYPOTHESIS visualization; NOT an observed planet.
 * Display assumptions a=500 AU, e=0.35, i=16 degrees fall within published
 * theoretical proposal ranges; argument of perihelion, node, and orbital
 * phase are intentionally arbitrary. No measured sky position is inferred.
 *
 * Sources:
 * https://science.nasa.gov/solar-system/planet-x/
 * https://arxiv.org/abs/2108.09868
 */
export const PLANET_NINE_NAME = 'Planet Nine (hypothesis)';
export const PLANET_NINE_SCENARIO = Object.freeze({
  status:'UNCONFIRMED HYPOTHESIS — DEMONSTRATION ORBIT',
  semimajorAxisAU:500,
  eccentricity:0.35,
  inclinationDegrees:16,
  periodYears:Math.sqrt(500**3),
  phaseAtEpochRadians:1.1,
  nodeDegrees:200,
  argumentOfPerihelionDegrees:80,
  positionStatus:'unknown: arbitrary model phase, node and orientation',
  epoch:'2026-10-24'
});
export function planetNineScenarioAU(yearsSinceEpoch){
 const p=PLANET_NINE_SCENARIO,e=p.eccentricity;
 const turns=yearsSinceEpoch%p.periodYears/p.periodYears;
 const mean=((p.phaseAtEpochRadians+2*Math.PI*turns)%(2*Math.PI)+2*Math.PI)%(2*Math.PI);
 let E=mean;for(let j=0;j<14;j++){const d=(E-e*Math.sin(E)-mean)/(1-e*Math.cos(E));E-=d;if(Math.abs(d)<1e-13)break;}
 const x=p.semimajorAxisAU*(Math.cos(E)-e);
 const y=p.semimajorAxisAU*Math.sqrt(1-e*e)*Math.sin(E);
 const w=p.argumentOfPerihelionDegrees*Math.PI/180,i=p.inclinationDegrees*Math.PI/180,n=p.nodeDegrees*Math.PI/180;
 const X=x*Math.cos(w)-y*Math.sin(w),Y=x*Math.sin(w)+y*Math.cos(w);
 return [X*Math.cos(n)-Y*Math.cos(i)*Math.sin(n),X*Math.sin(n)+Y*Math.cos(i)*Math.cos(n),Y*Math.sin(i)];
}
