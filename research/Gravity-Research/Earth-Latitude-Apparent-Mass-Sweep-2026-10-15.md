# Earth mass inference by latitude — 1° sweep (0°–90°)

> **Gravity Research working experiment — 2026-10-15** | Owner: HOME / personal science | **Status: model computation, not independent Earth-mass measurement.**
>
> Companion references: [Gravity Research](Gravity-Research.md) · [Equations and Variable Reference](Gravity-Equations-and-Variable-Reference.md) · [Project index](README.md).

## Research question

Starting at the equator, rotate an Earth-centered line toward the north/south poles by **one geodetic latitude degree at a time**. At each endpoint, compute (a) the Earth-center-to-reference-ellipsoid radius, (b) normal surface gravity at that latitude, and (c) an **apparent** Earth mass using the same simple spherical formula. Keep all 91 latitude results, calculate their unweighted arithmetic mean, and compare the behavior with the WGS 84 Earth gravitational parameter. The opposite endpoints at +φ and −φ are numerically identical for this north–south symmetric reference model; they are not independent measurements.

## Key result

| Metric | Computed value |
|---|---:|
| Number of distinct sampled latitudes | **91** (0° through 90°, inclusive) |
| **Arithmetic mean of apparent mass** | **5.957009102342e+24 kg** |
| Equatorial apparent mass, 0° | 5.961221578707e+24 kg |
| Polar apparent mass, 90° | 5.952712321461e+24 kg |
| Equator minus pole | 8.509257245253e+21 kg |
| WGS 84 parameter-based reference, $GM/G$ | 5.972168494074e+24 kg |
| Sweep mean minus reference | -1.515939173184e+22 kg |
| Sweep mean deviation from reference | **-0.253834%** |

**Conclusion:** The value of $g(\phi)r(\phi)^2/G$ decreases steadily from equator to pole with these inputs. Its simple arithmetic mean is **not an independent determination of Earth's actual mass**. The variation is produced by applying the spherical point-mass formula to an oblate, rotating-Earth model that includes centrifugal effects in its normal gravity.

## Inputs and provenance

| Symbol | Meaning | Value | Status |
|---|---|---|---|
| $a$ | WGS 84 equatorial semiaxis | 6,378,137.0 m | Exact **within the defined reference ellipsoid** |
| $1/f$ | WGS 84 inverse flattening | 298.257223563 | Defined model constant |
| $b=a(1-f)$ | Derived polar semiaxis | 6356752.314245179 m | Derived reference geometry |
| $\gamma_e$ | WGS 84 normal gravity at equator | 9.7803253359 m/s² | Model normal-gravity input, *not independently observed* |
| $\gamma_p$ | WGS 84 normal gravity at pole | 9.8321849378 m/s² | Model normal-gravity input, *not independently observed* |
| $G$ | Newtonian universal gravitational constant | 6.67430 × 10⁻¹¹ m³ kg⁻¹ s⁻² | CODATA 2022 experimentally inferred value, nonzero uncertainty |
| $\mu_\oplus=GM_\oplus$ | WGS 84 geocentric gravitational parameter (atmosphere included) | 3.986004418 × 10¹⁴ m³ s⁻² | Model reference parameter |

**Sources:** [NGA — WGS 84 defining parameters](https://earth-info.nga.mil/?action=wgs84&dir=wgs84); [USGS — WGS 84 normal gravity constants](https://pubs.usgs.gov/of/2006/1204/Gravity/computations.pdf); [NOAA/NGS — normal gravity equation](https://geodesy.noaa.gov/GRAV-D/data/NGS_GRAV-D_General_Airborne_Gravity_Data_User_Manual_v2.0.pdf); [NIST — 2022 CODATA constants](https://physics.nist.gov/cuu/Constants/). Numerical values quoted are reference-model inputs, not zero-uncertainty measurements of the physical Earth.

## Equations, definitions, and units

**Geodetic latitude** $\phi$: latitude in degrees measured relative to the normal (perpendicular) to the WGS 84 ellipsoid, rather than angle from the Earth's center. The computed **geocentric radius** is the straight-line distance from ellipsoid center to the ellipsoid surface at geodetic latitude $\phi$.

1. Ellipsoid flattening and eccentricity:

$$
f=\frac{1}{298.257223563},\quad
b=a(1-f),\quad e^2=1-\frac{b^2}{a^2}.
$$

2. Geocentric distance to the ellipsoidal surface **at geodetic latitude** $\phi$:

$$
r(\phi)=\sqrt{\frac{a^4\cos^2\phi+b^4\sin^2\phi}{a^2\cos^2\phi+b^2\sin^2\phi}}.
$$

3. WGS 84 **normal (effective) gravity** with Somigliana's relation:

$$
k=\frac{b\gamma_p}{a\gamma_e}-1,\qquad
\gamma(\phi)=\frac{\gamma_e(1+k\sin^2\phi)}{\sqrt{1-e^2\sin^2\phi}}.
$$

Normal gravity includes Earth's rotation in the reference potential; it is not identical to pure Newtonian gravitational attraction or a locally measured free-fall field.

4. Deliberately simplified **apparent mass estimator**:

$$
M_{\mathrm{app}}(\phi)=\frac{\gamma(\phi)\,[r(\phi)]^2}{G}.
$$

5. Requested **unweighted** arithmetic mean:

$$
\overline{M}_{\mathrm{app}}=\frac{1}{91}\sum_{j=0}^{90}M_{\mathrm{app}}(j^\circ).
$$

6. Reference and discrepancy:

$$
M_{\mathrm{ref}}=\frac{\mu_\oplus}{G},\qquad
\Delta M=\overline{M}_{\mathrm{app}}-M_{\mathrm{ref}},\qquad
\delta=100\frac{\Delta M}{M_{\mathrm{ref}}}\%.
$$

All computations use meters, seconds, and kilograms. Display digits support numerical reproduction; **they do not represent physical measurement precision**.

**Machine-readable outputs:** [CSV — all 91 latitude rows](Earth-Latitude-Apparent-Mass-Sweep-2026-10-15.csv).

## All 91 latitude calculations

| Geodetic latitude | WGS 84 center-to-surface radius (m) | WGS 84 normal gravity (m/s²) | Apparent mass (kg) |
|---:|---:|---:|---:|
| 0° | 6378137.000000 | 9.7803253359 | 5.961221578707e+24 |
| 1° | 6378130.540947 | 9.7803410620 | 5.961219090207e+24 |
| 2° | 6378111.171461 | 9.7803882212 | 5.961211627367e+24 |
| 3° | 6378078.914549 | 9.7804667569 | 5.961199198159e+24 |
| 4° | 6378033.808530 | 9.7805765748 | 5.961181815867e+24 |
| 5° | 6377975.906993 | 9.7807175426 | 5.961159499078e+24 |
| 6° | 6377905.278736 | 9.7808894910 | 5.961132271671e+24 |
| 7° | 6377822.007691 | 9.7810922131 | 5.961100162807e+24 |
| 8° | 6377726.192833 | 9.7813254652 | 5.961063206907e+24 |
| 9° | 6377617.948072 | 9.7815889667 | 5.961021443640e+24 |
| 10° | 6377497.402124 | 9.7818824006 | 5.960974917892e+24 |
| 11° | 6377364.698376 | 9.7822054139 | 5.960923679748e+24 |
| 12° | 6377219.994719 | 9.7825576179 | 5.960867784456e+24 |
| 13° | 6377063.463383 | 9.7829385888 | 5.960807292399e+24 |
| 14° | 6376895.290741 | 9.7833478678 | 5.960742269055e+24 |
| 15° | 6376715.677103 | 9.7837849623 | 5.960672784958e+24 |
| 16° | 6376524.836497 | 9.7842493460 | 5.960598915655e+24 |
| 17° | 6376322.996430 | 9.7847404594 | 5.960520741655e+24 |
| 18° | 6376110.397633 | 9.7852577108 | 5.960438348379e+24 |
| 19° | 6375887.293794 | 9.7858004769 | 5.960351826101e+24 |
| 20° | 6375653.951276 | 9.7863681033 | 5.960261269888e+24 |
| 21° | 6375410.648817 | 9.7869599058 | 5.960166779535e+24 |
| 22° | 6375157.677218 | 9.7875751704 | 5.960068459491e+24 |
| 23° | 6374895.339014 | 9.7882131548 | 5.959966418785e+24 |
| 24° | 6374623.948138 | 9.7888730890 | 5.959860770947e+24 |
| 25° | 6374343.829558 | 9.7895541762 | 5.959751633918e+24 |
| 26° | 6374055.318915 | 9.7902555939 | 5.959639129961e+24 |
| 27° | 6373758.762140 | 9.7909764947 | 5.959523385563e+24 |
| 28° | 6373454.515058 | 9.7917160072 | 5.959404531332e+24 |
| 29° | 6373142.942982 | 9.7924732373 | 5.959282701888e+24 |
| 30° | 6372824.420294 | 9.7932472692 | 5.959158035750e+24 |
| 31° | 6372499.330014 | 9.7940371662 | 5.959030675214e+24 |
| 32° | 6372168.063359 | 9.7948419722 | 5.958900766228e+24 |
| 33° | 6371831.019288 | 9.7956607127 | 5.958768458255e+24 |
| 34° | 6371488.604040 | 9.7964923955 | 5.958633904139e+24 |
| 35° | 6371141.230662 | 9.7973360129 | 5.958497259956e+24 |
| 36° | 6370789.318521 | 9.7981905419 | 5.958358684866e+24 |
| 37° | 6370433.292818 | 9.7990549459 | 5.958218340951e+24 |
| 38° | 6370073.584084 | 9.7999281758 | 5.958076393053e+24 |
| 39° | 6369710.627672 | 9.8008091715 | 5.957933008602e+24 |
| 40° | 6369344.863240 | 9.8016968628 | 5.957788357442e+24 |
| 41° | 6368976.734231 | 9.8025901710 | 5.957642611647e+24 |
| 42° | 6368606.687340 | 9.8034880100 | 5.957495945330e+24 |
| 43° | 6368235.171982 | 9.8043892878 | 5.957348534451e+24 |
| 44° | 6367862.639748 | 9.8052929077 | 5.957200556616e+24 |
| 45° | 6367489.543863 | 9.8061977693 | 5.957052190870e+24 |
| 46° | 6367116.338640 | 9.8071027708 | 5.956903617486e+24 |
| 47° | 6366743.478919 | 9.8080068091 | 5.956755017749e+24 |
| 48° | 6366371.419523 | 9.8089087823 | 5.956606573733e+24 |
| 49° | 6366000.614693 | 9.8098075900 | 5.956458468078e+24 |
| 50° | 6365631.517537 | 9.8107021356 | 5.956310883754e+24 |
| 51° | 6365264.579466 | 9.8115913269 | 5.956164003833e+24 |
| 52° | 6364900.249640 | 9.8124740779 | 5.956018011246e+24 |
| 53° | 6364538.974409 | 9.8133493099 | 5.955873088541e+24 |
| 54° | 6364181.196756 | 9.8142159529 | 5.955729417642e+24 |
| 55° | 6363827.355747 | 9.8150729471 | 5.955587179598e+24 |
| 56° | 6363477.885980 | 9.8159192438 | 5.955446554338e+24 |
| 57° | 6363133.217037 | 9.8167538071 | 5.955307720413e+24 |
| 58° | 6362793.772941 | 9.8175756148 | 5.955170854751e+24 |
| 59° | 6362459.971625 | 9.8183836603 | 5.955036132398e+24 |
| 60° | 6362132.224397 | 9.8191769531 | 5.954903726269e+24 |
| 61° | 6361810.935417 | 9.8199545204 | 5.954773806891e+24 |
| 62° | 6361496.501181 | 9.8207154086 | 5.954646542153e+24 |
| 63° | 6361189.310015 | 9.8214586838 | 5.954522097053e+24 |
| 64° | 6360889.741577 | 9.8221834336 | 5.954400633448e+24 |
| 65° | 6360598.166362 | 9.8228887680 | 5.954282309811e+24 |
| 66° | 6360314.945232 | 9.8235738205 | 5.954167280981e+24 |
| 67° | 6360040.428942 | 9.8242377491 | 5.954055697923e+24 |
| 68° | 6359774.957689 | 9.8248797377 | 5.953947707497e+24 |
| 69° | 6359518.860668 | 9.8254989967 | 5.953843452216e+24 |
| 70° | 6359272.455642 | 9.8260947644 | 5.953743070027e+24 |
| 71° | 6359036.048527 | 9.8266663076 | 5.953646694084e+24 |
| 72° | 6358809.932991 | 9.8272129228 | 5.953554452534e+24 |
| 73° | 6358594.390070 | 9.8277339369 | 5.953466468308e+24 |
| 74° | 6358389.687797 | 9.8282287083 | 5.953382858921e+24 |
| 75° | 6358196.080847 | 9.8286966274 | 5.953303736274e+24 |
| 76° | 6358013.810205 | 9.8291371177 | 5.953229206472e+24 |
| 77° | 6357843.102843 | 9.8295496363 | 5.953159369643e+24 |
| 78° | 6357684.171421 | 9.8299336745 | 5.953094319773e+24 |
| 79° | 6357537.214007 | 9.8302887589 | 5.953034144548e+24 |
| 80° | 6357402.413808 | 9.8306144515 | 5.952978925201e+24 |
| 81° | 6357279.938932 | 9.8309103507 | 5.952928736379e+24 |
| 82° | 6357169.942163 | 9.8311760913 | 5.952883646012e+24 |
| 83° | 6357072.560754 | 9.8314113455 | 5.952843715198e+24 |
| 84° | 6356987.916245 | 9.8316158230 | 5.952808998098e+24 |
| 85° | 6356916.114306 | 9.8317892714 | 5.952779541843e+24 |
| 86° | 6356857.244585 | 9.8319314766 | 5.952755386452e+24 |
| 87° | 6356811.380599 | 9.8320422631 | 5.952736564763e+24 |
| 88° | 6356778.579628 | 9.8321214942 | 5.952723102376e+24 |
| 89° | 6356758.882642 | 9.8321690720 | 5.952715017607e+24 |
| 90° | 6356752.314245 | 9.8321849378 | 5.952712321461e+24 |

## Interpretation and next experimental controls

- The physical Earth has **one total mass**, not a latitude-dependent mass. The latitude-varying results are the consequence of the intentionally oversimplified inversion $M=gr^2/G$ and reference model assumptions.
- Because the normal gravity field is partly defined using the WGS 84 gravitational parameter, this is a **self-consistency demonstration**, not an independent measurement or validation of $G$, Earth's mass, or a proposed new gravity law.
- **No spatial averaging or weighting** has been performed for the requested mean. Uniform one-degree increments do not cover equal Earth-surface areas; an area-weighted comparison would answer a different question and still would not fix model bias.
- Separate the **centrifugal contribution** from gravitational attraction; incorporate Earth's quadrupole/higher harmonics and the full vector gravity field, or invert independent satellite-tracking measurements for $GM$.
- Test independently measured gravity/position data with explicit geodetic reference, elevation, time, measurement uncertainty, and spherical-harmonic model. Propagate uncertainty in $G$; zero uncertainty in physical mass is not attainable.
- **Atmosphere:** the NGA $GM$ parameter includes Earth's atmosphere, but this is not evidence of an exact physical atmospheric boundary.
- **Reproducibility checks:** 91 ordered results; $r(0)=a$, $r(90)=b$; $\gamma(0)=\gamma_e$, $\gamma(90)=\gamma_p$; symmetry $M(+\phi)=M(-\phi)$ in this ellipsoid model; monotonic decreasing apparent mass from 0° to 90°.

## Experiment log

- **2026-10-15:** Completed 0°–90° by 1° model calculation. Recorded all values, arithmetic mean, and reference comparison. No physical field measurement performed and no new-gravity discovery asserted.
