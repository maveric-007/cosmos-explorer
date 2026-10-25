# Earth Mass: 1° Latitude–Longitude Gravitational Flux Experiment

**Date:** 2026-10-15  
**Project:** Home / Gravity Research  
**Status:** **WGS 84 theoretical model verification, NOT independent Earth gravimetry.**

**Related:** [original 91-latitude apparent-mass analysis](Earth-Latitude-Apparent-Mass-Sweep-2026-10-15.md) · [research questions](Gravity-Research.md) · [equations and symbols](Gravity-Equations-and-Variable-Reference.md) · [full 180-band calculation data](Earth-Mass-Gauss-Flux-Latitude-Bands-2026-10-15.csv) · [reproducibility program](earth_mass_gauss_flux.py).

## Research question

We previously evaluated $M_{\rm apparent}=\gamma r^2/G$ separately at integer geodetic latitudes 0° to 90° and averaged 91 results. The exercise varied with latitude, as expected for an oblate rotating body. Can we instead integrate gravitational flux through a closed WGS 84 ellipsoid, accounting for actual oblate geometry and centrifugal acceleration, and compare its output to conventional Earth mass?

**Yes mathematically.** The corrected modeled flux agrees with the published gravitational parameter to its input precision. **But both calculations reuse the same WGS 84 model**: a model consistency test is not independent observational evidence.

## Traditional method vs. our results

The conventional precise quantity is **Earth's gravitational parameter** $\mu=GM$, obtained from gravitational/orbital dynamics with realistic geopotential models, rather than direct weighing in kilograms. A mass in kg requires division by the less certain laboratory gravitational constant $G$.

| Approach | $\mu$ (m³/s²) | Inferred Earth mass (kg) | Delta from WGS 84 | Evidence quality |
|---|---:|---:|---:|---|
| NGA WGS 84 conventional reference | 3.986004418000e+14 | 5.972168494074e+24 | baseline | Published geodetic model/reference |
| Our original unweighted 91-latitude apparent-mass mean | Not coherent as a global GM | 5.957009102342e+24 | -0.253833959% | Incorrect spherical inversion of model effective gravity |
| Our corrected Gauss-law, 1° grid, 4-node per-band quadrature | 3.986004417990e+14 | 5.972168494060e+24 | -2.420619e-10% | Derived from same WGS 84 model, NOT independent |
| NASA/JPL DE440 planetary ephemeris | 3.986004355070e+14 | 5.972168399787e+24 | -1.578774e-6% | Separate ephemeris model; conventions must be reconciled |


**Key comparison:** the old unweighted mean was about **0.253834% low** because the inverted spherical equation was not appropriate to surface normal gravity. The new calculation's remaining relative difference is only about **2.42×10⁻¹²** (fractional), explained by published endpoint-gravity rounding. This improvement does **not** create independent mass data.

## Reference input ledger: definitions, measurements, and inferred values

| ID | Input | Value | Units | Status and source |
|---|---|---:|---|---|
| W01 | $a$: equatorial semimajor axis | 6,378,137.0 | m | NGA WGS 84 **defined** reference ellipsoid; not literal topographic distance |
| W02 | $1/f$: inverse flattening | 298.257223563 | dimensionless | NGA WGS 84 **defined** geometry |
| W03 | $\omega$: Earth mean spin | 7.292115×10⁻⁵ | rad/s | WGS 84 nominal model constant; actual instantaneous spin varies |
| W04 | $\mu_{\rm WGS}=GM$: including atmospheric mass | 3.986004418×10¹⁴ | m³/s² | WGS 84 geocentric gravitational parameter, reference model |
| W05 | $\gamma_e$: equatorial normal gravity | 9.7803253359 | m/s² | **Theoretical**, not an observed independent gravimeter measurement |
| W06 | $\gamma_p$: polar normal gravity | 9.8321849378 | m/s² | **Theoretical**, rounded normal gravity from WGS 84 |
| C01 | $G$: Newtonian gravitational constant | 6.67430(15)×10⁻¹¹ | m³ kg⁻¹ s⁻² | **Experimentally measured**; CODATA 2022 standard uncertainty of 0.00015×10⁻¹¹ |
| J01 | $\mu_{\rm DE440}$: JPL Earth ephemeris parameter | 398600.435507 | km³/s² | Planetary ephemeris estimate; independent parameter source with time/frame/model conventions |
 
**Primary reference links:** [NGA official WGS 84 reference](https://earth-info.nga.mil/?action=wgs84&dir=wgs84); [USGS WGS 84 normal gravity constants](https://pubs.usgs.gov/of/2006/1204/Gravity/computations.pdf); [NIST CODATA 2022 values and uncertainty](https://physics.nist.gov/cuu/Constants/); [NASA/JPL DE440 Earth GM](https://ssd.jpl.nasa.gov/astro_par.html); [NASA satellite tracking and gravity field estimation](https://earth.gsfc.nasa.gov/geo/missions/grace).

**Derived, not measured:** polar radius $b=a(1-f)=$ 6356752.314245179 m; first eccentricity squared $e^2=1-b^2/a^2=$ 0.00669437999014133; Somigliana coefficient $k=b\gamma_p/(a\gamma_e)-1=$ 0.00193185264639606; reference volume $V=4\pi a^2b/3=$ 1.083207319801e+21 m³. Both $\gamma_e$ and $\gamma_p$ are already dependent on the adopted $GM$. The calculation therefore has an explicit **circularity** that must not be hidden.

## Why our first mean was biased

The simple spherical equation $M=gr^2/G$ follows from a point-mass or spherically symmetric exterior field, and uses the **gravitational** acceleration $g$. At Earth's surface, WGS 84 $\gamma$ describes **effective (gravitational plus centrifugal)** acceleration, and real gravity is not radial relative to an exact sphere. Calculating $\gamma r^2/G$ at every latitude is a valid diagnostic of **model mismatch**, but averaging the outputs cannot magically remove the bias. Our original mean is retained above, not reinterpreted as actual mass.

## Core equations and definitions

### 1. Gauss's law for Newtonian gravity

$$
\oint_S\mathbf g_{\rm grav}\cdot d\mathbf A=-4\pi G M_{\rm enclosed},
\qquad
\mu_{\rm flux}=-\frac{1}{4\pi}\oint_S\mathbf g_{\rm grav}\cdot d\mathbf A,
\qquad
M_{\rm flux}=\frac{\mu_{\rm flux}}{G}.
$$

- $S$: **closed** integration surface; here an idealized WGS 84 ellipsoid.
- $d\mathbf A=\hat{\mathbf n}\,dA$: small outward area vector (m²). $\hat{\mathbf n}$ is unit outward normal.
- $\mathbf g_{\rm grav}$: **true gravitational** acceleration vector (m/s²), not effective gravity including centrifugal effects.
- $M_{\rm enclosed}$: enclosed Newtonian mass in kg; $\mu=GM$ in m³/s².

### 2. Ellipsoidal geometry (no assumed single Earth radius)

Let $\phi$ be **geodetic latitude**, $\lambda$ longitude, and $a,b$ the semimajor/semiminor axes. The geodetic angle follows the surface normal, not the center-to-surface line.

$$
e^2=1-\frac{b^2}{a^2},\quad
N(\phi)=\frac{a}{\sqrt{1-e^2\sin^2\phi}},\quad
R_M(\phi)=\frac{a(1-e^2)}{(1-e^2\sin^2\phi)^{3/2}}.
$$

$$
\mathbf r=(N\cos\phi\cos\lambda,\;N\cos\phi\sin\lambda,\;N(1-e^2)\sin\phi),
\quad
\hat{\mathbf n}=(\cos\phi\cos\lambda,\;\cos\phi\sin\lambda,\;\sin\phi).
$$

$$
dA=R_M(\phi)N(\phi)\cos\phi\,d\phi\,d\lambda.
$$

Here $N$ is the prime-vertical curvature radius (m), $R_M$ the meridional curvature radius (m), and $\mathbf r=(x,y,z)$ the Earth-centered surface coordinate (m). For the diagnostic table, the distinct *geocentric distance to surface* is

$$
r(\phi)=\sqrt{\frac{a^4\cos^2\phi+b^4\sin^2\phi}{a^2\cos^2\phi+b^2\sin^2\phi}}.
$$

### 3. Normal gravity and correcting for rotation

$$
k=\frac{b\gamma_p}{a\gamma_e}-1,\qquad
\gamma(\phi)=\gamma_e\frac{1+k\sin^2\phi}{\sqrt{1-e^2\sin^2\phi}}.
$$

On the reference ellipsoid, the modeled effective gravity is $\mathbf g_{\rm eff}=-\gamma\hat{\mathbf n}$. Centrifugal acceleration points *outward* from the rotation axis: $\mathbf a_{\rm cf}=\omega^2(x,y,0)$. Therefore

$$
\mathbf g_{\rm grav}=\mathbf g_{\rm eff}-\mathbf a_{\rm cf}
=-\gamma\hat{\mathbf n}-\omega^2(x,y,0),\quad
\mathbf a_{\rm cf}\cdot\hat{\mathbf n}=\omega^2N\cos^2\phi.
$$

This correction makes the inferred inward gravitational acceleration stronger than the effective acceleration. It is **not** simply adding Earth's angular speed to scalar gravity.

### 4. Corrected closed-ellipsoid gravitational flux

$$
\boxed{\mu_{\rm flux}=\frac{1}{4\pi}\int_{-\pi/2}^{\pi/2}\int_0^{2\pi}
\left[\gamma(\phi)+\omega^2N(\phi)\cos^2\phi\right]
R_M(\phi)N(\phi)\cos\phi\,d\lambda\,d\phi}
$$

Define $\mu_{\rm normal}=(4\pi)^{-1}\oint\gamma\,dA$ and $\mu_{\rm rot}=(4\pi)^{-1}\oint\omega^2N\cos^2\phi\,dA$. Then $\mu_{\rm flux}=\mu_{\rm normal}+\mu_{\rm rot}$.

**Independent mathematical check:** the divergence of the centrifugal vector field is $\nabla\cdot[\omega^2(x,y,0)]=2\omega^2$. Thus by the divergence theorem $\mu_{\rm rot}=\omega^2 V/(2\pi)$, using ellipsoid volume $V=4\pi a^2b/3$.

## Numerical method: all one-degree latitude and longitude cells

We partition the surface into **180 latitude intervals** (−90° to +90°, 1° each) times **360 longitude intervals** (0° to 360°, 1° each): **64,800 modeled cells**, not 64,800 physical readings. WGS 84 normal gravity and reference geometry are *axisymmetric* and north–south symmetric, so every one-degree longitude cell in a given latitude ring has the same model area and flux contribution. The actual longitude sum is evaluated **analytically**, equivalent to adding all 360 identical longitude cells; it does not artificially invent longitude variation.

**Do not sample only the center of a 1° latitude band for its full flux.** Instead, within each latitude band we use **four-point Gauss–Legendre quadrature** at normalized offsets ±0.339981043585 and ±0.861136311594, with corresponding weights 0.652145154863 and 0.347854845137. Weights, area element, and normal-gravity values are evaluated at all quadrature points. The interval midpoint gravity and radius printed in the ledger below are **annotations**, not the actual flux integration samples.

A 90-row table represents all 180 1° latitude bands by pairing north/south counterparts. Each line explicitly covers **two** 1° bands and all 360 one-degree longitude cells for each, i.e. **720 conceptual cells per line**. No area is left out or counted twice.

## Computed numerical totals

| Quantity | Result | Meaning |
|---|---:|---|
| Ellipsoid surface area | 5.100656217241e+14 m² | Computed integral of $dA$ |
| $\mu_{\rm normal}$ | 3.976837175152e+14 m³/s² | Normal/effective gravity flux |
| $\mu_{\rm rot}$ | 9.167242838283e+11 m³/s² | Spin correction; independently check via volume |
| **Corrected $\mu_{\rm flux}$** | **3.986004417990e+14 m³/s²** | Entire oblate reference surface |
| **Our inferred model Earth mass** | **5.972168494060e+24 kg** | $\mu_{\rm flux}/G$ |
| Conventional WGS 84 $GM$ | 3.986004418000e+14 m³/s² | Reference input for the normal field |
| $\mu_{\rm flux}-\mu_{\rm WGS}$ | -964.875 m³/s² | Tiny expected rounding residual, not new physics |
| Flux-derived mass minus WGS 84 mass | -1.445685991834e+13 kg | Far below uncertainty from laboratory $G$ |
| $\sigma_M$ from $G$ uncertainty alone | 1.342201090918e+20 kg | One-standard-deviation approximate uncertainty |
| $\sigma_M/M$ from $G$ alone | 0.002247427 % | Does NOT include all other Earth model uncertainties |

### Convergence check (same 1° grid; node count per latitude band varies)

| Nodes per band | Calculated $\mu$ (m³/s²) | Residual versus WGS 84 (m³/s²) | Comment |
|---|---:|---:|---|
| 1 node (midpoint) | 3.986055527597e+14 | 5.110960e+9 | Midpoint integration bias |
| 2 nodes | 3.986004417896e+14 | -1.040906e+4 | Numerical convergence check |
| 3 nodes | 3.986004417990e+14 | -9.651875e+2 | Numerical convergence check |
| 4 nodes | 3.986004417990e+14 | -9.651875e+2 | Numerical convergence check |


Using a single midpoint leads to a visible integration bias. Four nodes per one-degree band converge numerically to the WGS 84 model's expected parameter. **Numerical convergence is not physical measurement accuracy.**

## All one-degree model latitude-band contributions

All rows list both symmetric latitude bands $+[d,d+1]$ and $-[d,d+1]$, using the magnitude $|\phi|$ for the midpoint. The **area** and $\Delta\mu$ columns are already sums over **both** hemispheres **and all 360 longitude cells** per hemisphere. Endpoint fields and geometry use the same declared WGS 84 parameter set. Pairing is possible **only** because this is the symmetric reference model, not Earth observed at every longitude.

The radius is **geocentric center-to-ellipsoid distance**, in meters; the gravity is **modeled effective normal gravity**, in m/s². Area is in m², all $\Delta\mu$ contributions are m³/s². Integrate each band rather than treating the midpoint gravity as constant.

| Latitude bands, both hemispheres | Model midpoint ±latitude | Model geocentric radius (m) | Model $\gamma$ (m/s²) | Combined area (m²) | $\Delta\mu_{\rm normal}$ | $\Delta\mu_{\rm rot}$ | $\Delta\mu_{\rm total}$ |
|---|---:|---:|---:|---:|---:|---:|---:|
| ±0°–1° | ±0.5° | 6378135.385 | 9.7803292677 | 8.8620940e+12 | 6.897314398e+12 | 2.391571679e+10 | 6.921230115e+12 |
| ±1°–2° | ±1.5° | 6378122.469 | 9.7803607151 | 8.8594668e+12 | 6.895291802e+12 | 2.389411320e+10 | 6.919185915e+12 |
| ±2°–3° | ±2.5° | 6378096.652 | 9.7804235720 | 8.8542129e+12 | 6.891247014e+12 | 2.385095095e+10 | 6.915097965e+12 |
| ±3°–4° | ±3.5° | 6378057.965 | 9.7805177630 | 8.8463336e+12 | 6.885180845e+12 | 2.378631985e+10 | 6.908967165e+12 |
| ±4°–5° | ±4.5° | 6378006.453 | 9.7806431747 | 8.8358307e+12 | 6.877094511e+12 | 2.370035428e+10 | 6.900794865e+12 |
| ±5°–6° | ±5.5° | 6377942.179 | 9.7807996563 | 8.8227066e+12 | 6.866989634e+12 | 2.359323291e+10 | 6.890582866e+12 |
| ±6°–7° | ±6.5° | 6377865.218 | 9.7809870197 | 8.8069643e+12 | 6.854868246e+12 | 2.346517826e+10 | 6.878333425e+12 |
| ±7°–8° | ±7.5° | 6377775.661 | 9.7812050396 | 8.7886076e+12 | 6.840732792e+12 | 2.331645608e+10 | 6.864049249e+12 |
| ±8°–9° | ±8.5° | 6377673.616 | 9.7814534538 | 8.7676406e+12 | 6.824586129e+12 | 2.314737478e+10 | 6.847733504e+12 |
| ±9°–10° | ±9.5° | 6377559.204 | 9.7817319633 | 8.7440682e+12 | 6.806431529e+12 | 2.295828457e+10 | 6.829389813e+12 |
| ±10°–11° | ±10.5° | 6377432.560 | 9.7820402333 | 8.7178958e+12 | 6.786272686e+12 | 2.274957663e+10 | 6.809022263e+12 |
| ±11°–12° | ±11.5° | 6377293.836 | 9.7823778928 | 8.6891297e+12 | 6.764113718e+12 | 2.252168213e+10 | 6.786635400e+12 |
| ±12°–13° | ±12.5° | 6377143.196 | 9.7827445353 | 8.6577765e+12 | 6.739959169e+12 | 2.227507112e+10 | 6.762234240e+12 |
| ±13°–14° | ±13.5° | 6376980.820 | 9.7831397198 | 8.6238435e+12 | 6.713814016e+12 | 2.201025140e+10 | 6.735824267e+12 |
| ±14°–15° | ±14.5° | 6376806.901 | 9.7835629703 | 8.5873388e+12 | 6.685683672e+12 | 2.172776718e+10 | 6.707411439e+12 |
| ±15°–16° | ±15.5° | 6376621.646 | 9.7840137772 | 8.5482710e+12 | 6.655573994e+12 | 2.142819779e+10 | 6.677002191e+12 |
| ±16°–17° | ±16.5° | 6376425.277 | 9.7844915977 | 8.5066493e+12 | 6.623491283e+12 | 2.111215615e+10 | 6.644603439e+12 |
| ±17°–18° | ±17.5° | 6376218.026 | 9.7849958560 | 8.4624836e+12 | 6.589442296e+12 | 2.078028727e+10 | 6.610222583e+12 |
| ±18°–19° | ±18.5° | 6376000.142 | 9.7855259447 | 8.4157844e+12 | 6.553434247e+12 | 2.043326661e+10 | 6.573867513e+12 |
| ±19°–20° | ±19.5° | 6375771.885 | 9.7860812246 | 8.3665630e+12 | 6.515474815e+12 | 2.007179839e+10 | 6.535546613e+12 |
| ±20°–21° | ±20.5° | 6375533.527 | 9.7866610265 | 8.3148311e+12 | 6.475572151e+12 | 1.969661379e+10 | 6.495268765e+12 |
| ±21°–22° | ±21.5° | 6375285.353 | 9.7872646511 | 8.2606014e+12 | 6.433734884e+12 | 1.930846912e+10 | 6.453043353e+12 |
| ±22°–23° | ±22.5° | 6375027.660 | 9.7878913701 | 8.2038869e+12 | 6.389972128e+12 | 1.890814388e+10 | 6.408880272e+12 |
| ±23°–24° | ±23.5° | 6374760.755 | 9.7885404273 | 8.1447014e+12 | 6.344293486e+12 | 1.849643883e+10 | 6.362789925e+12 |
| ±24°–25° | ±24.5° | 6374484.959 | 9.7892110393 | 8.0830596e+12 | 6.296709062e+12 | 1.807417392e+10 | 6.314783236e+12 |
| ±25°–26° | ±25.5° | 6374200.602 | 9.7899023962 | 8.0189766e+12 | 6.247229466e+12 | 1.764218621e+10 | 6.264871652e+12 |
| ±26°–27° | ±26.5° | 6373908.024 | 9.7906136628 | 7.9524682e+12 | 6.195865818e+12 | 1.720132776e+10 | 6.213067146e+12 |
| ±27°–28° | ±27.5° | 6373607.577 | 9.7913439798 | 7.8835511e+12 | 6.142629761e+12 | 1.675246343e+10 | 6.159382225e+12 |
| ±28°–29° | ±28.5° | 6373299.621 | 9.7920924643 | 7.8122425e+12 | 6.087533464e+12 | 1.629646869e+10 | 6.103829932e+12 |
| ±29°–30° | ±29.5° | 6372984.527 | 9.7928582111 | 7.7385603e+12 | 6.030589628e+12 | 1.583422742e+10 | 6.046423856e+12 |
| ±30°–31° | ±30.5° | 6372662.672 | 9.7936402939 | 7.6625233e+12 | 5.971811499e+12 | 1.536662957e+10 | 5.987178129e+12 |
| ±31°–32° | ±31.5° | 6372334.444 | 9.7944377661 | 7.5841507e+12 | 5.911212870e+12 | 1.489456894e+10 | 5.926107439e+12 |
| ±32°–33° | ±32.5° | 6372000.238 | 9.7952496623 | 7.5034628e+12 | 5.848808089e+12 | 1.441894088e+10 | 5.863227030e+12 |
| ±33°–34° | ±33.5° | 6371660.457 | 9.7960749989 | 7.4204803e+12 | 5.784612066e+12 | 1.394063999e+10 | 5.798552706e+12 |
| ±34°–35° | ±34.5° | 6371315.511 | 9.7969127760 | 7.3352246e+12 | 5.718640280e+12 | 1.346055778e+10 | 5.732100838e+12 |
| ±35°–36° | ±35.5° | 6370965.815 | 9.7977619779 | 7.2477181e+12 | 5.650908786e+12 | 1.297958044e+10 | 5.663888367e+12 |
| ±36°–37° | ±36.5° | 6370611.793 | 9.7986215748 | 7.1579838e+12 | 5.581434219e+12 | 1.249858652e+10 | 5.593932805e+12 |
| ±37°–38° | ±37.5° | 6370253.872 | 9.7994905236 | 7.0660453e+12 | 5.510233801e+12 | 1.201844467e+10 | 5.522252245e+12 |
| ±38°–39° | ±38.5° | 6369892.484 | 9.8003677696 | 6.9719272e+12 | 5.437325346e+12 | 1.154001140e+10 | 5.448865358e+12 |
| ±39°–40° | ±39.5° | 6369528.069 | 9.8012522474 | 6.8756545e+12 | 5.362727269e+12 | 1.106412884e+10 | 5.373791398e+12 |
| ±40°–41° | ±40.5° | 6369161.066 | 9.8021428825 | 6.7772532e+12 | 5.286458584e+12 | 1.059162263e+10 | 5.297050207e+12 |
| ±41°–42° | ±41.5° | 6368791.922 | 9.8030385923 | 6.6767499e+12 | 5.208538914e+12 | 1.012329972e+10 | 5.218662214e+12 |
| ±42°–43° | ±42.5° | 6368421.085 | 9.8039382876 | 6.5741721e+12 | 5.128988492e+12 | 9.659946293e+9 | 5.138648439e+12 |
| ±43°–44° | ±43.5° | 6368049.005 | 9.8048408737 | 6.4695478e+12 | 5.047828168e+12 | 9.202325762e+9 | 5.057030493e+12 |
| ±44°–45° | ±44.5° | 6367676.134 | 9.8057452521 | 6.3629061e+12 | 4.965079406e+12 | 8.751176763e+9 | 4.973830583e+12 |
| ±45°–46° | ±45.5° | 6367302.926 | 9.8066503215 | 6.2542764e+12 | 4.880764293e+12 | 8.307211259e+9 | 4.889071504e+12 |
| ±46°–47° | ±46.5° | 6366929.837 | 9.8075549793 | 6.1436891e+12 | 4.794905538e+12 | 7.871112691e+9 | 4.802776651e+12 |
| ±47°–48° | ±47.5° | 6366557.321 | 9.8084581227 | 6.0311754e+12 | 4.707526474e+12 | 7.443534222e+9 | 4.714970009e+12 |
| ±48°–49° | ±48.5° | 6366185.832 | 9.8093586504 | 5.9167671e+12 | 4.618651058e+12 | 7.025097046e+9 | 4.625676155e+12 |
| ±49°–50° | ±49.5° | 6365815.824 | 9.8102554639 | 5.8004967e+12 | 4.528303871e+12 | 6.616388797e+9 | 4.534920259e+12 |
| ±50°–51° | ±50.5° | 6365447.750 | 9.8111474685 | 5.6823976e+12 | 4.436510119e+12 | 6.217962033e+9 | 4.442728081e+12 |
| ±51°–52° | ±51.5° | 6365082.061 | 9.8120335750 | 5.5625037e+12 | 4.343295634e+12 | 5.830332835e+9 | 4.349125967e+12 |
| ±52°–53° | ±52.5° | 6364719.202 | 9.8129127008 | 5.4408498e+12 | 4.248686867e+12 | 5.453979484e+9 | 4.254140846e+12 |
| ±53°–54° | ±53.5° | 6364359.621 | 9.8137837715 | 5.3174715e+12 | 4.152710887e+12 | 5.089341264e+9 | 4.157800228e+12 |
| ±54°–55° | ±54.5° | 6364003.757 | 9.8146457220 | 5.1924047e+12 | 4.055395383e+12 | 4.736817351e+9 | 4.060132200e+12 |
| ±55°–56° | ±55.5° | 6363652.047 | 9.8154974977 | 5.0656865e+12 | 3.956768653e+12 | 4.396765832e+9 | 3.961165419e+12 |
| ±56°–57° | ±56.5° | 6363304.925 | 9.8163380563 | 4.9373543e+12 | 3.856859604e+12 | 4.069502827e+9 | 3.860929107e+12 |
| ±57°–58° | ±57.5° | 6362962.816 | 9.8171663687 | 4.8074464e+12 | 3.755697746e+12 | 3.755301732e+9 | 3.759453047e+12 |
| ±58°–59° | ±58.5° | 6362626.141 | 9.8179814202 | 4.6760018e+12 | 3.653313182e+12 | 3.454392580e+9 | 3.656767575e+12 |
| ±59°–60° | ±59.5° | 6362295.316 | 9.8187822120 | 4.5430601e+12 | 3.549736608e+12 | 3.166961533e+9 | 3.552903569e+12 |
| ±60°–61° | ±60.5° | 6361970.748 | 9.8195677625 | 4.4086614e+12 | 3.444999298e+12 | 2.893150485e+9 | 3.447892449e+12 |
| ±61°–62° | ±61.5° | 6361652.837 | 9.8203371082 | 4.2728468e+12 | 3.339133102e+12 | 2.633056801e+9 | 3.341766159e+12 |
| ±62°–63° | ±62.5° | 6361341.976 | 9.8210893053 | 4.1356577e+12 | 3.232170432e+12 | 2.386733182e+9 | 3.234557165e+12 |
| ±63°–64° | ±63.5° | 6361038.550 | 9.8218234305 | 3.9971362e+12 | 3.124144253e+12 | 2.154187653e+9 | 3.126298441e+12 |
| ±64°–65° | ±64.5° | 6360742.932 | 9.8225385824 | 3.8573252e+12 | 3.015088075e+12 | 1.935383685e+9 | 3.017023458e+12 |
| ±65°–66° | ±65.5° | 6360455.489 | 9.8232338827 | 3.7162680e+12 | 2.905035936e+12 | 1.730240442e+9 | 2.906766176e+12 |
| ±66°–67° | ±66.5° | 6360176.577 | 9.8239084769 | 3.5740085e+12 | 2.794022396e+12 | 1.538633161e+9 | 2.795561029e+12 |
| ±67°–68° | ±67.5° | 6359906.542 | 9.8245615359 | 3.4305911e+12 | 2.682082517e+12 | 1.360393656e+9 | 2.683442911e+12 |
| ±68°–69° | ±68.5° | 6359645.717 | 9.8251922567 | 3.2860611e+12 | 2.569251857e+12 | 1.195310947e+9 | 2.570447168e+12 |
| ±69°–70° | ±69.5° | 6359394.427 | 9.8257998635 | 3.1404638e+12 | 2.455566448e+12 | 1.043132022e+9 | 2.456609580e+12 |
| ±70°–71° | ±70.5° | 6359152.984 | 9.8263836087 | 2.9938453e+12 | 2.341062782e+12 | 9.035627124e+8 | 2.341966345e+12 |
| ±71°–72° | ±71.5° | 6358921.686 | 9.8269427740 | 2.8462523e+12 | 2.225777800e+12 | 7.762686966e+8 | 2.226554069e+12 |
| ±72°–73° | ±72.5° | 6358700.823 | 9.8274766708 | 2.6977317e+12 | 2.109748870e+12 | 6.608766206e+8 | 2.110409746e+12 |
| ±73°–74° | ±73.5° | 6358490.668 | 9.8279846418 | 2.5483311e+12 | 1.993013769e+12 | 5.569753323e+8 | 1.993570745e+12 |
| ±74°–75° | ±74.5° | 6358291.482 | 9.8284660612 | 2.3980983e+12 | 1.875610671e+12 | 4.641172295e+8 | 1.876074788e+12 |
| ±75°–76° | ±75.5° | 6358103.514 | 9.8289203359 | 2.2470816e+12 | 1.757578119e+12 | 3.818197157e+8 | 1.757959939e+12 |
| ±76°–77° | ±76.5° | 6357926.997 | 9.8293469061 | 2.0953298e+12 | 1.638955015e+12 | 3.095667607e+8 | 1.639264582e+12 |
| ±77°–78° | ±77.5° | 6357762.152 | 9.8297452458 | 1.9428920e+12 | 1.519780592e+12 | 2.468105599e+8 | 1.520027403e+12 |
| ±78°–79° | ±78.5° | 6357609.184 | 9.8301148641 | 1.7898175e+12 | 1.400094400e+12 | 1.929732902e+8 | 1.400287374e+12 |
| ±79°–80° | ±79.5° | 6357468.283 | 9.8304553051 | 1.6361561e+12 | 1.279936281e+12 | 1.474489545e+8 | 1.280083730e+12 |
| ±80°–81° | ±80.5° | 6357339.626 | 9.8307661490 | 1.4819579e+12 | 1.159346346e+12 | 1.096053114e+8 | 1.159455951e+12 |
| ±81°–82° | ±81.5° | 6357223.372 | 9.8310470122 | 1.3272731e+12 | 1.038364958e+12 | 7.878588396e+7 | 1.038443744e+12 |
| ±82°–83° | ±82.5° | 6357119.667 | 9.8312975482 | 1.1721522e+12 | 9.170327064e+11 | 5.431204102e+7 | 9.170870184e+11 |
| ±83°–84° | ±83.5° | 6357028.639 | 9.8315174480 | 1.0166461e+12 | 7.953903844e+11 | 3.548514557e+7 | 7.954258695e+11 |
| ±84°–85° | ±84.5° | 6356950.404 | 9.8317064401 | 8.6080577e+11 | 6.734789659e+11 | 2.158876351e+7 | 6.735005547e+11 |
| ±85°–86° | ±85.5° | 6356885.058 | 9.8318642913 | 7.0468226e+11 | 5.513395825e+11 | 1.189092602e+7 | 5.513514734e+11 |
| ±86°–87° | ±86.5° | 6356832.683 | 9.8319908067 | 5.4832687e+11 | 4.290134992e+11 | 5.646439124e+6 | 4.290191456e+11 |
| ±87°–88° | ±87.5° | 6356793.344 | 9.8320858301 | 3.9179103e+11 | 3.065420908e+11 | 2.099233152e+6 | 3.065441900e+11 |
| ±88°–89° | ±88.5° | 6356767.091 | 9.8321492443 | 2.3512623e+11 | 1.839668176e+11 | 4.847451753e+5 | 1.839673023e+11 |
| ±89°–90° | ±89.5° | 6356753.956 | 9.8321809710 | 7.8384011e+10 | 6.132920093e+10 | 3.232720110e+4 | 6.132923325e+10 |
| **TOTAL / all 180 latitude bands** | — | — | — | **5.100656217241e+14** | **3.976837175152e+14** | **9.167242838283e+11** | **3.986004417990e+14** |


The last three columns must satisfy $\Delta\mu_{\rm total}=\Delta\mu_{\rm normal}+\Delta\mu_{\rm rot}$ for every pair. Their column totals produce the complete enclosing-surface result. To reconstruct a specific longitude cell from a paired row, divide its area and flux numbers by **720**, since it represents 360 longitude cells in each of two hemispheres.

The [CSV file](Earth-Mass-Gauss-Flux-Latitude-Bands-2026-10-15.csv) includes all **180** latitude bands individually, preserving 360 cells per band and higher numeric resolution than Markdown.

## Interpretation and limitations

1. **Circular model verification, not independent weighing.** WGS 84 normal gravity is constructed from a potential parameterized by the same $GM$ used for comparison. Agreement validates the integration and proper correction, not a new empirical value.
2. **Reference ellipsoid versus physical atmosphere.** WGS 84 $GM$ includes atmosphere, yet much of the real atmosphere is **outside** the reference ellipsoid. Flux through *actual gravitational field* on an ellipsoid would not enclose the mass of the atmosphere above it. Here we integrated the ideal mathematical normal potential, which is not an observed gravitational field on the real surface. A physically complete Earth-plus-atmosphere test requires a suitable enclosing region and treatment of diffuse atmospheric material.
3. **Local longitude, mountains, oceans and tides ignored by normal model.** This field has no longitude dependence; a higher-resolution grid simply repeats the same synthetic model at each longitude. Independent observation needs a true observed/empirically fitted 3D gravity field (e.g. satellite tracking and the Earth's spherical harmonic field).
4. **Use the gravitational vector flux**, not a sum of magnitudes without normal projection. Normal gravity is ellipsoid-normal by model construction; real gravity generally is not.
5. **Physical uncertainty remains.** The reported many arithmetic digits do not eliminate the experimental uncertainty of $G$ or systematic errors in observed $GM$, rotation, potential models, frames, tidal corrections, or time dependence.
6. **Distinct conventional Earth parameters.** WGS 84 and JPL DE440 use different determinations/conventions; small differences do not represent independently proved missing matter.
7. **Modified-gravity hypotheses:** This is explicitly a Newtonian calculation. It tests the handling of Earth shape/rotation within Newtonian gravity, not a modified-gravity theory.

## What is required for a genuinely independent next test

- Obtain independent satellite orbit/ranging observables or gravity-field coefficients with documented origin and uncertainty, or calibrated terrestrial gravity vectors plus observation geometry.
- Harmonize terrestrial/celestial frames, timescales, elevations, atmosphere and tides; estimate the *external* gravitational field on a closed 3D surface surrounding the mass defined.
- Compute $\oint\mathbf g_{\rm grav}\cdot d\mathbf A$ using **actual measured or independently estimated vectors**, with area weights and uncertainties; compare with a separately estimated $\mu$.
- Avoid initializing the field from the identical WGS 84 normal parameter that we later attempt to confirm. Treat discrepancies as hypotheses for calibration, interpolation, model error, or physics; never assume novel physics from a residual.

**Source for real gridded/spherical-harmonic follow-up:** [NGA Earth Gravitational Model](https://earth-info.nga.mil/geograv); [NASA GRACE satellite gravity](https://earth.gsfc.nasa.gov/geo/missions/grace).

## Reproducibility record

- This experiment is documented as **theoretical/model-derived**, not 64,800 collected gravimeter readings.
- 180 one-degree latitude bands; 360 theoretical longitude cells per band; Gauss–Legendre 4 nodes inside each latitude band; analytical longitude integral.
- All variable definitions, source links, formula derivations, radius/normal-gravity band annotations, summed gravity flux and independent numerical convergence tests are given above.
- Raw 180-band CSV and an executable, standard-library Python script are stored next to this Markdown and linked at the top.
- **Result:** our old latitude average was an invalid global mass estimator; the correctly projected closed-surface gravitational flux reproduces the reference $GM$ built into the model to rounding precision.
