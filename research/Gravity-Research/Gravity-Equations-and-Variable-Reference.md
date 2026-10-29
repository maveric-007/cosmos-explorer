# Gravity Research — Equations, Variables, Derivations, and Tests

> **Research reference v0.1 — 2026-10-14** | Domain: **HOME / personal science project** | Status: **Annotated learning/reference material; not a validated model or discovery**  
> Companion: [Gravity Research — Open Questions and Test Plan](Gravity-Research.md)  
> **Purpose:** Explain the equations needed to investigate ordinary gravity, the apparent missing-gravity problem, possible modified-gravity behavior, and independent observational tests. Every mathematical symbol is defined where introduced; derived quantities point to their supporting equations. This is a **comprehensive project working set**, not every equation in modern physics.

## How to read this document

**Read in order:** 1 → 2 → 3 (our local control) → 4 (galaxies) → 5–6 (competing explanations) → 7–11 (independent constraints) → 12 (testing) → 13 (worked examples). Sections 14–15 provide the terminology and sources.

**Three labels:**
- **Law/model:** A physical theory with explicit conditions or assumptions.
- **Definition/identity:** A mathematical relationship that follows from the definitions; it does *not* independently prove a mechanism.
- **Empirical fit:** A relationship measured in data; matching it does *not* identify the underlying cause.

**Notation and units:** Use SI internally: meters (m), kilograms (kg), seconds (s), newtons (N), radians (rad). Bold symbols denote vectors, ordinary symbols usually denote magnitudes. A subscript identifies a component; 0 often means the present epoch, and “obs,” “bar,” and “DM” mean observed, baryonic, and dark matter. The symbol $\simeq$ means approximately; $\Delta$ denotes a difference. Every dataset must retain its *original units* until converted explicitly.

## 1. Constants, units, and the basic mathematics

### E1 — Physical constants and conversions (inputs, not fitted parameters)

| Symbol | Meaning | Working value / unit | Source/meaning |
|---|---|---|---|
| $G$ | Newtonian gravitational constant | $6.67430\times10^{-11}\ \mathrm{m^3\,kg^{-1}\,s^{-2}}$ | Measured universal constant; carries experimental uncertainty |
| $c$ | Speed of light in vacuum | $299\,792\,458\ \mathrm{m\,s^{-1}}$ (exact) | Defined SI value |
| $M_\odot$ | Solar mass | $\simeq1.9885\times10^{30}\ \mathrm{kg}$ | Approximate solar mass, not exact |
| $\mu_\odot=GM_\odot$ | Solar gravitational parameter | $\simeq1.3271244\times10^{20}\ \mathrm{m^3\,s^{-2}}$ | Prefer current JPL value in orbit comparisons |
| $\mathrm{AU}$ | Astronomical unit | $149\,597\,870\,700\ \mathrm{m}$ (exact) | Defined length |
| $\mathrm{pc}$ | Parsec | $\simeq3.08567758\times10^{16}\ \mathrm{m}$ | $1\,\mathrm{kpc}=10^3\,\mathrm{pc}$; $1\,\mathrm{Mpc}=10^6\,\mathrm{pc}$ |
| $\mathrm{km/s}$ | Kilometers per second | $1\,\mathrm{km/s}=1000\,\mathrm{m/s}$ | For rotation curves |
| $\hbar$ | Reduced Planck constant | $h_{\rm P}/(2\pi)\ \mathrm{J\,s}$ | Do not confuse $h_{\rm P}$ with dimensionless cosmological $h$ |
| $k_B$ | Boltzmann constant | $1.380649\times10^{-23}\ \mathrm{J\,K^{-1}}$ (exact) | Used for atmospheric pressure |
| $\pi$ | Circle constant | $\simeq3.14159265$ | Dimensionless |

Derived units: $1\ \mathrm{N}=1\ \mathrm{kg\,m\,s^{-2}}$; acceleration in $\mathrm{m\,s^{-2}}$; density in $\mathrm{kg\,m^{-3}}$. An angular rate in radians per second is not the same thing as linear speed.

### E2 — Change and calculus (tools, not extra forces)

$$
\mathbf v=\frac{d\mathbf x}{dt},\qquad
\mathbf a=\frac{d\mathbf v}{dt},\qquad
\nabla\Phi=\left(\frac{\partial\Phi}{\partial x},
\frac{\partial\Phi}{\partial y},\frac{\partial\Phi}{\partial z}\right).
$$

**Terms:** $\mathbf x$ = position vector (m); $t$ = elapsed time (s); $\mathbf v$ = velocity (m/s); $\mathbf a$ = acceleration (m/s²); $d/dt$ = rate of change in time; $\partial/\partial x$ = rate of change in one coordinate while others are held fixed; $\nabla$ = gradient operator; $\Phi$ = gravitational potential per unit mass (m²/s²). These definitions underpin orbital dynamics and field equations.

## 2. Newtonian gravity — the foundation

### N1 — Universal gravitational attraction (law)

$$
F=\frac{Gm_1m_2}{r^2}.
$$

**Terms:** $F$ = magnitude of attractive force (N); $G$ = constant E1; $m_1,m_2$ = masses (kg); $r$ = separation between point masses or centers of *spherically symmetric* bodies (m). **Meaning:** Double one mass → double force; double distance → one-quarter force. A galaxy is a flattened, extended object, so this formula alone cannot replace a proper mass-distribution calculation.

**Supporting mass equations:**

$$
m=\rho V\quad\text{for constant density};\qquad
M=\int_V\rho(\mathbf x)\,d^3x\quad\text{in general}.
$$

**New terms:** $m,M$ = mass (kg); $\rho$ = mass per volume (kg/m³); $V$ = volume (m³); $d^3x$ = tiny volume element; $\int_V$ = sum of these elements throughout the volume. **Not all mass emits light:** the equation applies to luminous and nonluminous mass alike.

### N2 — Newton's second law and gravitational acceleration (law + consequence)

$$
\mathbf F_{\rm net}=m\mathbf a,\qquad
g_N=\frac{GM}{r^2}.
$$

**Terms:** $\mathbf F_{\rm net}$ = vector sum of *all* forces (N); $m$ = accelerated body's mass (kg); $\mathbf a$ = its acceleration (m/s²); $g_N$ = magnitude of Newtonian gravitational acceleration from a spherical source (m/s²); $M$ = attracting mass (kg); $r$, $G$ as N1. Because gravitational force and inertia both scale with test-body mass, $m$ cancels in $g_N$ for ideal free fall.

**Vector version for a point source:**

$$
\mathbf a_N(\mathbf x)=-GM\frac{\mathbf x-\mathbf x_M}{|\mathbf x-\mathbf x_M|^3}.
$$

**New terms:** $\mathbf x_M$ = source position (m); $|\,\cdot\,|$ = vector length; the minus sign means the acceleration points toward the source.

### N3 — Potential and the field of distributed matter (law, Newtonian limit)

$$
\mathbf g_N=-\nabla\Phi,\qquad
\nabla^2\Phi=4\pi G\rho.
$$

**Terms:** $\mathbf g_N$ = gravitational acceleration vector (m/s²); $\Phi$ = potential per mass (m²/s²); $\nabla\Phi$ = spatial slope of potential; $\nabla^2\Phi=\partial_x^2\Phi+\partial_y^2\Phi+\partial_z^2\Phi$ = Laplacian; $\rho$ = mass density (kg/m³). The second equation is **Poisson's equation**.

**Supporting integral for an extended distribution:**

$$
\Phi(\mathbf x)=-G\int\frac{\rho(\mathbf x')}{|\mathbf x-\mathbf x'|}\,d^3x'.
$$

**New terms:** $\mathbf x'$ = position of each source element; $d^3x'$ = source volume element; $|\mathbf x-\mathbf x'|$ = distance between source element and measurement location. This is how we account for the gravitational pull of an entire galactic disk—not just a center mass.

### N4 — Circular motion and orbital speed (kinematics + Newtonian dynamics)

$$
a_{\rm cent}=\frac{v_c^2}{r}=\omega^2r,\qquad
v_c=\omega r,\qquad
\omega=\frac{2\pi}{T}.
$$

**Terms:** $a_{\rm cent}$ = required inward/centripetal acceleration (m/s²); $v_c$ = circular speed (m/s); $r$ = orbital radius (m); $\omega$ = angular speed (rad/s); $T$ = orbital period (s); $\pi$ as E1. Centripetal acceleration is **not** a new fundamental force; it describes changing velocity direction.

**For a nearly circular orbit around one approximately spherical central mass:**

$$
\frac{v_c^2}{r}=\frac{GM}{r^2},
\qquad v_c=\sqrt{\frac{GM}{r}},
\qquad T=2\pi\sqrt{\frac{r^3}{GM}}.
$$

**Terms:** $M$ = mass effectively enclosed within the orbit (kg); all other symbols are above. **Critical assumption:** these simplified equalities do *not* apply unchanged to a strongly flattened disk or eccentric orbit.

### N5 — Elliptical orbits, energy, and Kepler (two-body approximation)

$$
v^2=\mu\left(\frac{2}{r}-\frac{1}{a_{\rm orb}}\right),
\qquad T^2=\frac{4\pi^2a_{\rm orb}^3}{\mu},
\qquad \mu=G(M+m).
$$

**Terms:** $v$ = relative orbital speed (m/s); $r$ = instantaneous separation (m); $a_{\rm orb}$ = ellipse semimajor axis (m), **not acceleration**; $\mu$ = two-body gravitational parameter (m³/s²); $M,m$ = two masses (kg); $T$ = period. First relation = **vis-viva equation**; second = Kepler's third law in Newtonian form.

**Supporting energy:**

$$
E=\frac12\mu_{\rm red}v^2-\frac{GMm}{r},\qquad
\mu_{\rm red}=\frac{Mm}{M+m}.
$$

**New terms:** $E$ = two-body orbital mechanical energy (J); $\mu_{\rm red}$ = reduced mass (kg), distinct from $\mu=G(M+m)$; first term = kinetic energy, second = gravitational potential energy. Bound elliptical motion has $E<0$.

### N6 — Many-body gravity and tides (numerical Solar System reference)

$$
\ddot{\mathbf x}_i=-G\sum_{j\ne i}
m_j\frac{\mathbf x_i-\mathbf x_j}{|\mathbf x_i-\mathbf x_j|^3},
\qquad
\Delta\mathbf a=\mathbf a(\mathbf x_1)-\mathbf a(\mathbf x_2).
$$

**Terms:** $\mathbf x_i$ = position of body $i$ (m); $\ddot{\mathbf x}_i$ = second time derivative, its acceleration (m/s²); $\sum$ = sum over all other bodies $j$; $m_j$ = mass of body $j$; $\Delta\mathbf a$ = acceleration *difference* between two points (m/s²). **Why this matters:** a distant gravitational field may accelerate Earth and Sun *together* while barely perturbing the distance between them.

**First-order tidal approximation:**

$$
\Delta a_i\simeq\sum_j\mathcal T_{ij}\,\Delta x_j,\qquad
\mathcal T_{ij}=\frac{\partial a_i}{\partial x_j}.
$$

**New terms:** $\mathcal T_{ij}$ = component of tidal-gradient matrix (s⁻²); $a_i$ = component of acceleration; $\Delta x_j$ = separation component (m); indices $i,j$ here label spatial directions. Approximation assumes the acceleration field varies smoothly across the separation.

### N7 — Other known influences (do not quietly omit them)

$$
\mathbf F_{\rm EM}=q(\mathbf E+\mathbf v\times\mathbf B),
\qquad
\mathbf a_{\rm pressure}=-\frac{\nabla P}{\rho}.
$$

**Terms:** $\mathbf F_{\rm EM}$ = electromagnetic force (N) on a charge; $q$ = electric charge (C); $\mathbf E$ = electric field (N/C); $\mathbf v$ = charged particle velocity (m/s); $\mathbf B$ = magnetic flux density (tesla); $\times$ = vector cross product; $P$ = gas pressure (Pa); $\rho$ = gas mass density (kg/m³). Strong and weak nuclear forces govern short-range nuclear processes; they are not substitutes for the long-range galaxy-scale gravitational field. Gas pressure, magnetic fields, radiation and noncircular motion *can* affect some astronomical tracers. Do not treat every non-gravitational acceleration as dark matter or modified gravity.

## 3. Solar System, Earth, and atmosphere — high-precision control (O-04, O-11)

### S1 — Earth–Sun acceleration and circular-speed baseline

$$
g_{\odot@\oplus}=\frac{\mu_\odot}{r_{\oplus\odot}^2},
\qquad
v_{\oplus,\rm circ}=\sqrt{\frac{\mu_\odot}{r_{\oplus\odot}}}.
$$

**Terms:** $g_{\odot@\oplus}$ = Sun's acceleration at Earth's distance (m/s²); $\mu_\odot=GM_\odot$ = solar gravitational parameter (E1); $r_{\oplus\odot}$ = Earth–Sun separation (m), approximated by 1 AU here; $v_{\oplus,\rm circ}$ = *hypothetical circular-orbit* speed (m/s). The real orbit is eccentric and influenced by other bodies.

**Approximate check with $r=1$ AU:** $g_{\odot@\oplus}\simeq0.0059301\ \mathrm{m/s^2}$, $v_{\oplus,\rm circ}\simeq29.785\ \mathrm{km/s}$. **These are derived baseline estimates, not a fit to JPL ephemerides.**

### S2 — Earth's surface gravity and atmospheric retention

$$
g_\oplus\simeq\frac{GM_\oplus}{R_\oplus^2},\qquad
\frac{dP}{dh}=-\rho_{\rm air}g_\oplus.
$$

**Terms:** $g_\oplus$ = Earth surface gravitational acceleration (~9.8 m/s²); $M_\oplus$ = Earth's mass (kg); $R_\oplus$ = Earth's mean radius (m); $h$ = height above reference surface (m); $P$ = atmospheric pressure (Pa); $\rho_{\rm air}$ = air density (kg/m³). The hydrostatic equation assumes stationary air locally; Earth's shape/rotation and weather produce corrections.

**Sub-equations for ideal, isothermal gas:**

$$
P=nk_BT_{\rm gas}=\frac{\rho_{\rm air}}{\bar m}k_BT_{\rm gas},\quad
H_{\rm atm}=\frac{k_BT_{\rm gas}}{\bar m g_\oplus},\quad
P(h)=P_0e^{-h/H_{\rm atm}}.
$$

**New terms:** $n$ = number of molecules per m³; $k_B$ = Boltzmann constant E1; $T_{\rm gas}$ = temperature (K); $\bar m$ = mean mass of an air molecule (kg); $H_{\rm atm}$ = atmospheric scale height (m); $P_0$ = pressure at height zero. The exponential law assumes constant temperature and $g_\oplus$ over the height considered. A gas atmosphere does not require an additional galaxy-scale binding force.

### S3 — Illustrative local dark-matter mass and tidal scale

$$
M_{\rm uniform}(<r)=\frac{4\pi}{3}\rho_{\rm local}r^3,
\qquad
g_{\rm uniform}(r)=\frac{4\pi G\rho_{\rm local}r}{3}.
$$

**Terms:** $\rho_{\rm local}$ = *assumed* spatially uniform local halo density (kg/m³); $r$ = radius around the idealized sphere's center (m); $M_{\rm uniform}$ = mass *inside that hypothetical sphere* (kg); $g_{\rm uniform}$ = inward acceleration produced by that ideal symmetric distribution. These relations are an **order-of-magnitude toy model** and must **not** be mistaken for the true galactocentric halo field or a measurement of a Sun-centered cloud.

**Convert commonly quoted particle-physics density:**

$$
0.3\ \mathrm{GeV}/(c^2\,\mathrm{cm}^3)
\simeq5.35\times10^{-22}\ \mathrm{kg/m^3}.
$$

**Terms:** GeV/$c^2$ = a mass unit; $c$ = speed of light; $\mathrm{cm}^3=10^{-6}\,\mathrm{m}^3$. **Example only:** at $r=1$ AU, $M_{\rm uniform}\simeq7.5\times10^{12}\,\mathrm{kg}$ and $g_{\rm uniform}\simeq2.24\times10^{-20}\,\mathrm{m/s^2}$ (about $3.8\times10^{-18}$ of S1 solar acceleration). There is an unknown real local DM density and spatial structure; the uniform sphere is just a controlled scale comparison.

**Real two-body test:** compute $\Delta\mathbf a_{\rm DM}=\mathbf a_{\rm DM}(\mathbf x_\oplus)-\mathbf a_{\rm DM}(\mathbf x_\odot)$ using N6, then test against observed ephemerides, not absolute galactocentric acceleration.

### S4 — Observational discrepancy for a position or orbit

$$
\mathbf r_{\rm res}(t)=
\mathbf x_{\rm JPL}(t)-\mathbf x_{\rm model}(t),\qquad
\mathbf v_{\rm res}(t)=
\mathbf v_{\rm JPL}(t)-\mathbf v_{\rm model}(t).
$$

**Terms:** $\mathbf x_{\rm JPL},\mathbf v_{\rm JPL}$ = state vectors exported from a specified Horizons ephemeris in an explicitly chosen reference frame, origin, and time scale; $\mathbf x_{\rm model},\mathbf v_{\rm model}$ = outputs from *our* numerical model; $t$ = time; “res” = difference. **A two-body model will have nonzero residuals even if gravity is correct**, because actual JPL integrations include other solar-system bodies, relativistic and other corrections. Never infer a new force from such an intentionally incomplete comparison.

## 4. Galaxy rotation curves and measured acceleration (O-01, O-05)

### G1 — Circular-equivalent observed acceleration (definition under dynamical assumptions)

$$
g_{\rm obs}(R)=\frac{V_{\rm obs}^2(R)}{R}.
$$

**Terms:** $R$ = galactocentric radius in disk plane (m); $V_{\rm obs}(R)$ = inferred circular rotation speed from observational velocity fields (m/s); $g_{\rm obs}$ = circular-equivalent radial acceleration (m/s²). **Assumptions:** axisymmetry, near-circular equilibrium, appropriate inclination and pressure/noncircular corrections. “Observed acceleration” is *derived from measured motion*, not measured by an accelerometer.

**Supporting line-of-sight correction (ideal tilted rotating disk):**

$$
V_{\rm obs}\simeq\frac{V_{\rm los}-V_{\rm sys}}{\sin i\,\cos\theta}.
$$

**Terms:** $V_{\rm los}$ = measured line-of-sight velocity at location (m/s); $V_{\rm sys}$ = galaxy systemic line-of-sight velocity; $i$ = inclination (0° = face-on); $\theta$ = azimuth in disk measured from projected major axis; division assumes $\sin i\cos\theta\ne0$, so observations near face-on/minor-axis are poorly constrained. Actual pipeline rotation-curve fitting is more elaborate; do *not* apply this correction again to already deprojected SPARC $V_{\rm obs}$.

### G2 — Stellar luminosity and mass-to-light ratio (model-dependent)

$$
M_\star=\Upsilon_\star L_\star,\qquad
L=4\pi D^2f\quad\text{(isotropic, bolometric approximation)}.
$$

**Terms:** $M_\star$ = estimated stellar mass (kg or $M_\odot$); $\Upsilon_\star$ = stellar mass-to-light ratio (mass/luminosity); $L_\star,L$ = stellar or total luminosity (W or solar luminosities in a specified band); $D$ = source distance (m); $f$ = observed flux (W/m²). Stellar $\Upsilon_\star$ depends on population modeling and bandpass. **Do not** use $L=4\pi D^2f$ without accounting for extinction, band corrections and distance definitions where relevant.

**Supporting radial surface density:**

$$
\Sigma_\star(R)=\Upsilon_\star I_\star(R),\qquad
\Sigma(R)=\int_{-\infty}^{\infty}\rho(R,z)\,dz.
$$

**New terms:** $\Sigma_\star$ = stellar mass per disk area (kg/m²); $I_\star$ = surface luminosity per area; $\Sigma$ = surface mass density; $z$ = height above galaxy disk plane; $\rho(R,z)$ = 3D mass density. The gravitational field from a flattened mass distribution must be obtained from N3, not simply from a point-mass formula.

### G3 — Gas + stellar disk + bulge: SPARC baryonic mass-model accounting

$$
V_{\rm bar}^2(R)=
V_{\rm gas}(R)|V_{\rm gas}(R)|
+\Upsilon_{\rm d}V_{\rm disk}^2(R)
+\Upsilon_{\rm b}V_{\rm bulge}^2(R),
\qquad
g_{\rm bar}(R)=\frac{V_{\rm bar}^2(R)}{R}.
$$

**Terms:** $V_{\rm bar}^2$ = squared circular-speed equivalent from **ordinary matter**, with units m²/s²; $V_{\rm gas}$ = gas mass-model contribution encoded as a velocity by the catalog; its *sign is retained* as $V_{\rm gas}|V_{\rm gas}|$ when the tabulated gas velocity is negative; $V_{\rm disk}$ = catalog stellar disk speed contribution at the catalog's reference $\Upsilon=1$; $V_{\rm bulge}$ = corresponding bulge contribution; $\Upsilon_{\rm d},\Upsilon_{\rm b}$ = adopted mass-to-light ratios in $M_\odot/L_\odot$ consistent with the catalog normalization; $g_{\rm bar}$ = baryonic Newtonian radial acceleration. Components add in **acceleration / speed squared**, *not* linearly in speeds.

**Prerequisite:** inspect the SPARC dataset ReadMe and actual column definitions before using this exact equation. The sign treatment is especially important for negative $V_{\rm gas}$. Do not put a square root around a negative total $V_{\rm bar}^2$; flag invalid/uncertain radii. The numerical $\Upsilon$ values must be selected, fitted, or taken from published baseline assumptions—not secretly fixed to prove a conclusion.

### G4 — Circular speed from a general axisymmetric gravitational potential

$$
V_c^2(R)=R\left.\frac{\partial\Phi(R,z)}{\partial R}\right|_{z=0},
\qquad
g_R(R)=-\left.\frac{\partial\Phi(R,z)}{\partial R}\right|_{z=0}.
$$

**Terms:** $V_c$ = theoretical circular speed (m/s); $\Phi(R,z)$ = gravitational potential (N3); $g_R$ = signed radial acceleration (negative inward) (m/s²); $R$ = cylindrical radius (m), $z=0$ = disk midplane. This is the correct **axisymmetric disk** alternative to treating all mass as a sphere.

### G5 — Useful mass discrepancy and residual definitions

$$
\mathcal D(R)=\frac{g_{\rm obs}}{g_{\rm bar}}
=\frac{V_{\rm obs}^2}{V_{\rm bar}^2},\qquad
\Delta g(R)=g_{\rm obs}-g_{\rm bar}.
$$

**Terms:** $\mathcal D$ = unitless mass-discrepancy *ratio* (not measured extra mass); $\Delta g$ = acceleration residual (m/s²); other terms from G1–G3. An unequal result **does not itself tell us why**: an additional mass distribution, gravity law, errors, or assumptions may contribute. Ratios require $g_{\rm bar}>0$.

**Only if mass can be approximated spherically:**

$$
M_{\rm dyn}(<R)=\frac{V_{\rm obs}^2R}{G},\qquad
M_{\rm deficit}(<R)\equiv M_{\rm dyn}(<R)-M_{\rm bar}(<R).
$$

**Terms:** $M_{\rm dyn}$ = dynamically inferred spherical enclosed mass (kg); $M_{\rm bar}$ = independently estimated enclosed ordinary matter (kg); $M_{\rm deficit}$ = *model-dependent* inferred mass shortfall (kg). **Do not apply these formulas directly to the flattened-disk SPARC baryonic models.**

## 5. Conventional dark-matter models: what the hypothesis predicts (O-02)

### D1 — Baryons plus a dark halo (Newtonian circular modeling)

$$
V_{\rm model}^2(R)=V_{\rm bar}^2(R)+V_{\rm halo}^2(R),
\qquad
g_{\rm halo}=\frac{V_{\rm halo}^2}{R}.
$$

**Terms:** $V_{\rm model}$ = predicted circular speed; $V_{\rm bar}$ = baryonic circular-equivalent term G3; $V_{\rm halo}$ = halo contribution (m/s); $g_{\rm halo}$ = gravitational acceleration from modeled halo (m/s²). The conventional model uses Newtonian/GR gravity with an additional gravitating mass distribution; it does *not* require knowing the mass of an individual hypothetical particle to model orbital motion.

### D2 — Spherical halo density and enclosed mass

$$
M_{\rm halo}(<r)=4\pi\int_0^r\rho_{\rm halo}(s)s^2\,ds,
\qquad
V_{\rm halo}^2(r)=\frac{GM_{\rm halo}(<r)}{r}.
$$

**Terms:** $r$ = spherical radius (m); $s$ = integration radius (m); $\rho_{\rm halo}$ = hypothesized halo density (kg/m³); $M_{\rm halo}$ = enclosed halo mass (kg); $V_{\rm halo}$ = halo's equivalent circular-speed contribution. Uses spherical symmetry. **Mass within radius is not particle mass.**

### D3 — Example NFW halo: density → mass → speed (specified model, not established unique profile)

$$
x=\frac r{r_s},\qquad
\rho_{\rm NFW}(r)=\frac{\rho_s}{x(1+x)^2},
$$

$$
M_{\rm NFW}(<r)=4\pi\rho_s r_s^3
\left[\ln(1+x)-\frac{x}{1+x}\right],\qquad
V_{\rm NFW}^2(r)=\frac{GM_{\rm NFW}(<r)}{r}.
$$

**Terms:** $r_s$ = scale radius (m); $\rho_s$ = scale density (kg/m³); $x=r/r_s$ = unitless radius; $\ln$ = natural logarithm; $M_{\rm NFW}$ = integrated halo mass; $V_{\rm NFW}$ = halo circular-speed contribution. The NFW profile diverges in total mass when extended to infinite radius and must be assigned a finite physical/operational halo boundary when calculating total mass.

**Optional parameterization:**

$$
c_\Delta=\frac{r_\Delta}{r_s},\qquad
M_\Delta=\frac{4\pi}{3}\Delta\rho_{\rm crit}(z)r_\Delta^3.
$$

**New terms:** $c_\Delta$ = concentration (unitless); $r_\Delta$ = radius where mean enclosed halo density equals $\Delta$ times critical density (m); $M_\Delta$ = corresponding enclosed mass; $\Delta$ = specified dimensionless overdensity (often 200); $\rho_{\rm crit}(z)$ = cosmological critical density at redshift $z$ from C3.

### D4 — Virial theorem: independent dynamical mass clues

$$
2\langle K\rangle+\langle W\rangle=0,\quad
K=\frac12\sum_i m_i v_i^2,\quad
W=-\sum_{i<j}\frac{Gm_im_j}{r_{ij}}.
$$

**Terms:** $\langle\cdot\rangle$ = long-time average; $K$ = kinetic energy (J); $W$ = Newtonian gravitational potential energy (J); $m_i,m_j$ = component masses; $v_i$ = speed in the system center-of-mass frame; $r_{ij}$ = separation of particles $i,j$. Applicable to approximately steady, isolated, gravitationally bound systems; a cluster out of equilibrium can violate assumptions and produce biased estimates.

## 6. Modified-gravity and acceleration-law comparisons (O-01, O-04)

### M1 — Empirical radial-acceleration relation (RAR; fit, not fundamental law)

$$
g_{\rm RAR}(g_{\rm bar})=
\frac{g_{\rm bar}}{1-\exp[-\sqrt{g_{\rm bar}/g_\dagger}]}.
$$

**Terms:** $g_{\rm RAR}$ = fitted acceleration (m/s²); $g_{\rm bar}$ = baryonic acceleration G3; $\exp$ = exponential function $e^x$; $\sqrt{\cdot}$ = square root; $g_\dagger\simeq1.2\times10^{-10}\ \mathrm{m/s^2}$ = empirically inferred characteristic acceleration scale. **Published prior art**, not a new equation. For $g_{\rm bar}>0$, compare against observations.

**Limiting cases (important predictions):**

$$
g_{\rm RAR}\simeq g_{\rm bar}\quad(g_{\rm bar}\gg g_\dagger),\qquad
g_{\rm RAR}\simeq\sqrt{g_{\rm bar}g_\dagger}
\quad(g_{\rm bar}\ll g_\dagger).
$$

**New notation:** $\gg$ = much greater; $\ll$ = much smaller. This explains *why* a model can predict essentially Newtonian behavior in our high-acceleration Solar System and an appreciable difference in low-acceleration outer galaxies. This does not settle its viability for lensing and cosmology.

### M2 — MOND-style algebraic equation (model prescription, limited regime)

$$
g\,\mu\!\left(\frac g{a_0}\right)=g_N,\qquad
\mu(y)=\frac{y}{1+y}\quad\text{(one example interpolation)}.
$$

**Terms:** $g$ = modeled actual acceleration magnitude (m/s²); $g_N$ = Newtonian baryonic prediction (m/s²); $a_0$ = model's characteristic acceleration (m/s²), often near $1.2\times10^{-10}$; $\mu(y)$ = dimensionless interpolation function; $y=g/a_0$ = dimensionless argument. **Several different** $\mu$ functions exist. The simple algebraic relation applies only in specified regimes; general 3D modified-gravity theories require field equations and can display environmental effects.

**Solving the illustrated interpolation:**

$$
g=\frac{g_N+\sqrt{g_N^2+4a_0g_N}}{2}.
$$

**Terms:** identical to M2; this solution belongs to this particular $\mu$, **not** to M1's exponential RAR. Do not claim two different prescriptions are identical.

### M3 — Deep-MOND limit, predicted flat speeds and baryonic Tully–Fisher scaling

$$
g\simeq\sqrt{a_0g_N},\qquad
g_N\simeq\frac{GM_b}{r^2},\qquad
v_f^4\simeq G M_b a_0.
$$

**Terms:** $M_b$ = nearly all baryonic mass effectively enclosed within outer radii (kg), assumed approximately isolated/asymptotic; $r$ = radius (m); $v_f$ = asymptotic flat rotation speed (m/s); other terms from M2 and N2/N4. The last equation follows by substituting $g=v_f^2/r$, and is an approximate deep-MOND isolated-system prediction. A galaxy's geometry and environment complicate finite-radius application.

### M4 — Hypothetical extra acceleration: a research *parameterization*, not yet an identified force

$$
\mathbf g_{\rm inferred}(\mathbf x)=
\mathbf g_{\rm baryonic}(\mathbf x)+\mathbf g_{\rm extra}(\mathbf x;\boldsymbol\theta),
$$

$$
\mathbf g_{\rm extra}=\mathbf g_{\rm inferred}-\mathbf g_{\rm baryonic}.
$$

**Terms:** $\mathbf x$ = position; $\boldsymbol\theta$ = set of unknown model parameters; $\mathbf g_{\rm inferred}$ = acceleration inferred from appropriately modeled motion; $\mathbf g_{\rm baryonic}$ = acceleration from known matter under a chosen law; $\mathbf g_{\rm extra}$ = *residual vector*. A residual does **not** establish a fifth force, dark matter, or a modified law. **Test requirement:** specify a predictive mathematical form *before* testing withheld observations, and ensure the same form respects Solar System and galaxy constraints.

## 7. Einstein's general relativity — when Newton's model is insufficient (O-04, O-08, O-09)

### R1 — Spacetime interval and metric (geometric definition)

$$
ds^2=g_{\mu\nu}\,dx^\mu dx^\nu.
$$

**Terms:** $ds^2$ = invariant spacetime interval squared (m² with $x^0=ct$); $g_{\mu\nu}$ = spacetime metric tensor, encoding distances/time and curvature; $x^\mu$ = four spacetime coordinates, $\mu,\nu\in\{0,1,2,3\}$; $dx^\mu$ = infinitesimal coordinate changes; repeated indices are summed. The metric has signature $(-+++)$ in this document. Flat Minkowski spacetime has $ds^2=-c^2dt^2+dx^2+dy^2+dz^2$.

### R2 — Einstein field equation (law of classical GR)

$$
R_{\mu\nu}-\tfrac12 Rg_{\mu\nu}+\Lambda g_{\mu\nu}
=\frac{8\pi G}{c^4}T_{\mu\nu}.
$$

**Terms:** $R_{\mu\nu}$ = Ricci curvature tensor (m⁻²); $R$ = Ricci curvature scalar (m⁻²); $g_{\mu\nu}$ = metric (R1); $\Lambda$ = cosmological constant (m⁻²); $T_{\mu\nu}$ = energy-momentum/stress tensor (energy density, momentum flow, pressure); $G,c$ = E1. The left side describes geometry, the right describes the matter/energy sourcing it. This equation replaces the simpler Newtonian Poisson description where relativity matters.

**Supporting curvature definitions (not a full differential-geometry course):**

$$
R=g^{\mu\nu}R_{\mu\nu},\qquad
R_{\mu\nu}=R^\alpha{}_{\mu\alpha\nu},
$$

$$
\Gamma^\alpha_{\mu\nu}
=\frac12 g^{\alpha\beta}
(\partial_\mu g_{\beta\nu}+
\partial_\nu g_{\beta\mu}-
\partial_\beta g_{\mu\nu}).
$$

**New terms:** $g^{\mu\nu}$ = inverse metric; $R^\alpha{}_{\mu\beta\nu}$ = Riemann curvature tensor, calculated from metric derivatives; $\Gamma^\alpha_{\mu\nu}$ = Christoffel connection coefficients; $\partial_\mu$ = coordinate partial derivative; Greek indices label spacetime dimensions. **Sub-equation for Riemann curvature** (chosen sign convention):

$$
R^\rho{}_{\sigma\mu\nu}
=\partial_\mu\Gamma^\rho_{\nu\sigma}
-\partial_\nu\Gamma^\rho_{\mu\sigma}
+\Gamma^\rho_{\mu\lambda}\Gamma^\lambda_{\nu\sigma}
-\Gamma^\rho_{\nu\lambda}\Gamma^\lambda_{\mu\sigma}.
$$

**New terms:** $\lambda,\rho,\sigma$ = further spacetime indices; summation over repeated $\lambda$. This is how derivatives of the metric lead to curvature; different references can adopt the opposite Riemann sign convention.

**Example source tensor for a perfect fluid:**

$$
T^{\mu\nu}=(\varepsilon+p)\frac{u^\mu u^\nu}{c^2}
+p\,g^{\mu\nu}.
$$

**New terms:** $\varepsilon$ = total energy density (J/m³), including mass energy; $p$ = isotropic pressure (Pa = J/m³); $u^\mu$ = fluid four-velocity, normalized by $g_{\mu\nu}u^\mu u^\nu=-c^2$. For cold matter, $\varepsilon\simeq\rho c^2$. The perfect-fluid model does not describe all astrophysical stresses.

### R3 — Geodesic equation (motion given a metric)

$$
\frac{d^2x^\mu}{d\tau^2}
+\Gamma^\mu_{\alpha\beta}
\frac{dx^\alpha}{d\tau}\frac{dx^\beta}{d\tau}=0.
$$

**Terms:** $x^\mu$ = coordinates R1; $\tau$ = proper time along a freely falling massive body's path (s); $\Gamma^\mu_{\alpha\beta}$ = connection R2; $dx^\alpha/d\tau$ = four-velocity coordinate components; $d^2x^\mu/d\tau^2$ = second proper-time derivative. **Meaning:** free-fall motion follows spacetime geometry. For light, use an appropriate affine parameter rather than proper time ($d\tau=0$ for a null path).

### R4 — Selected, testable weak-field GR effects (conditional approximations)

$$
\Delta\varpi_{\rm orbit}
\simeq\frac{6\pi GM}{a_{\rm orb}(1-e^2)c^2}
\quad\text{radians per orbit},
$$

$$
\frac{\Delta f}{f}\simeq-\frac{\Delta\Phi}{c^2}
\quad\text{(weak-field, stationary observers)},
$$

$$
\Delta t_{\rm Shapiro}\simeq\frac{2GM}{c^3}
\ln\left(\frac{r_1+r_2+R}{r_1+r_2-R}\right)
\quad\text{(leading one-way delay, point mass)}.
$$

**Terms:** $\Delta\varpi_{\rm orbit}$ = advance of orbit's periapsis angle in one revolution (rad); $M$ = central mass (kg); $a_{\rm orb}$ = semimajor axis (m); $e$ = orbital eccentricity (unitless, $0\le e<1$); $\Delta f/f$ = fractional shift in photon frequency between observers, using their potential difference under the stated sign convention; $\Delta\Phi=\Phi_{\rm receiver}-\Phi_{\rm emitter}$ (m²/s²); $\Delta t_{\rm Shapiro}$ = gravitational light-travel-time delay (s); $r_1,r_2$ = distances of transmitter and receiver from gravitating body; $R$ = their Euclidean separation. **Caution:** the minus sign is defined for $\Delta\Phi=\Phi_{\rm receiver}-\Phi_{\rm emitter}$; photons climbing out of a well are redshifted. Range, geometry, bodies, and PPN/relativistic model details matter for precision.

## 8. Gravitational lensing — an independent mass/geometry test (O-03)

### L1 — Point-mass deflection (weak field, GR, light ray away from strong field)

$$
\hat\alpha\simeq\frac{4GM}{bc^2}.
$$

**Terms:** $\hat\alpha$ = physical bending angle of light (rad); $M$ = isolated lensing mass (kg); $b$ = closest-approach impact parameter (m); $G,c$ E1. **Important:** this measures the gravitational field affecting photons, not just orbiting stars. A proposed explanation of rotation curves has to match light deflection too.

### L2 — Thin-lens Einstein angle and critical projected density

$$
\theta_E=\sqrt{\frac{4GM}{c^2}\frac{D_{ls}}{D_lD_s}},
\qquad
\Sigma_{\rm crit}=\frac{c^2}{4\pi G}
\frac{D_s}{D_lD_{ls}},\qquad
\kappa=\frac{\Sigma_{\rm proj}}{\Sigma_{\rm crit}}.
$$

**Terms:** $\theta_E$ = Einstein-ring angular radius (rad) for a perfectly aligned point lens; $D_l$ = observer-to-lens angular-diameter distance (m); $D_s$ = observer-to-source angular-diameter distance (m); $D_{ls}$ = lens-to-source angular-diameter distance (m), defined cosmologically; $\Sigma_{\rm crit}$ = critical surface mass density (kg/m²); $\Sigma_{\rm proj}$ = projected lens mass per area (kg/m²); $\kappa$ = dimensionless lensing convergence. **Caution:** $D_{ls}\ne D_s-D_l$ in a general expanding curved cosmology. Interpreting $\kappa$ as surface mass uses standard GR lensing.

**Supporting projection:**

$$
\Sigma_{\rm proj}(R_\perp)=
\int_{-\infty}^{\infty}
\rho\!\left(\sqrt{R_\perp^2+z^2}\right)dz
\quad\text{(spherical lens approximation)}.
$$

**New terms:** $R_\perp$ = projected radial distance from lens center (m); $z$ = line-of-sight depth; $\rho$ = 3D mass density from N1/D2. For galaxy-cluster maps, a general 2D mass reconstruction is needed.

## 9. Milky Way stellar motion and cluster dynamics (O-05)

### J1 — Distance/parallax and transverse stellar motion (simplified astrometry)

$$
d_{\rm pc}\simeq\frac{1}{\varpi_{\rm arcsec}},\qquad
v_t[\mathrm{km/s}]\simeq4.74047\,
\mu_{\rm pm}[\mathrm{arcsec/yr}]\,d_{\rm pc}.
$$

**Terms:** $d_{\rm pc}$ = stellar distance (parsecs); $\varpi_{\rm arcsec}$ = measured parallax (arcseconds); $v_t$ = transverse speed (km/s); $\mu_{\rm pm}$ = observed angular proper motion (arcseconds per year); 4.74047 = AU/year converted to km/s per arcsec·pc geometry. **This naive parallax inversion is unreliable for small/negative or very uncertain parallaxes**: account for Gaia systematics/zero point, distance priors and covariance. Convert proper motion in milliarcseconds per year by dividing by 1000 first.

### J2 — Spherical Jeans equation (steady-state, tracer model)

$$
\frac{1}{\nu}\frac{d(\nu\sigma_r^2)}{dr}
+\frac{2\beta\sigma_r^2}{r}
=-\frac{d\Phi}{dr},\qquad
\beta=1-\frac{\sigma_\theta^2+\sigma_\phi^2}{2\sigma_r^2}.
$$

**Terms:** $\nu(r)$ = spatial number density of tracer stars (number/m³); $\sigma_r,\sigma_\theta,\sigma_\phi$ = radial and two tangential velocity dispersions (m/s); $\beta$ = velocity-anisotropy parameter (dimensionless); $r$ = spherical radius (m); $\Phi$ = gravitational potential N3. Assumes equilibrium, spherical symmetry and relevant collisionless tracer behavior. **Mass–anisotropy degeneracy:** uncertain $\beta$ can imitate uncertain gravitational mass.

**Using the spherical Newtonian relation to estimate mass:**

$$
M(<r)=-\frac{r^2}{G}\left[
\frac{1}{\nu}\frac{d(\nu\sigma_r^2)}{dr}
+\frac{2\beta\sigma_r^2}{r}\right].
$$

**Terms:** $M(<r)$ = dynamically inferred enclosed mass (kg); remaining symbols as above. Do not treat this as direct observed dark-matter mass.

## 10. Cosmology, dark energy, and the CMB (O-06, O-07)

### C1 — Cosmic expansion and redshift (model + observable)

$$
H(t)=\frac{\dot a}{a},\qquad
1+z=\frac{a(t_0)}{a(t_{\rm emit})}
=\frac{\lambda_{\rm obs}}{\lambda_{\rm emit}}\quad\text{(cosmological redshift)}.
$$

**Terms:** $a(t)$ = dimensionless universe scale factor; $\dot a=da/dt$; $H(t)$ = expansion rate (s⁻¹), often km s⁻¹ Mpc⁻¹; $z$ = redshift (unitless); $t_0$ = present time; $t_{\rm emit}$ = emission time; $\lambda_{\rm obs},\lambda_{\rm emit}$ = observed/emitted wavelengths (same units). Convention: $a(t_0)=1$. Measured redshift can include Doppler and local-gravitational contributions; do not interpret every measured shift as pure cosmological expansion.

### C2 — Friedmann background expansion (GR under homogeneous/isotropic FLRW assumptions)

$$
H^2=\frac{8\pi G}{3}\rho-\frac{Kc^2}{a^2}
+\frac{\Lambda c^2}{3},
$$

$$
\frac{\ddot a}{a}=
-\frac{4\pi G}{3}\left(\rho+\frac{3P}{c^2}\right)
+\frac{\Lambda c^2}{3}.
$$

**Terms:** $H,a$ = C1; $\rho$ = total matter+radiation *mass-equivalent* density excluding separately displayed $\Lambda$ (kg/m³); $K$ = curvature constant (m⁻² when $a$ is dimensionless); $\Lambda$ = cosmological constant (m⁻²); $P$ = total pressure of included non-$\Lambda$ components (Pa); $\ddot a$ = second time derivative of $a$ (s⁻²); $G,c$ E1. The first sets expansion rate; the second describes acceleration/deceleration. **Do not double count** dark energy in $\rho,P$ and $\Lambda$.

**Supporting equation of state:**

$$
P_i=w_i\rho_i c^2,\qquad
\rho_i(a)=\rho_{i0}\,a^{-3(1+w_i)}
\quad\text{for constant }w_i.
$$

**New terms:** $i$ = component (e.g., matter, radiation, dark energy); $w_i$ = pressure-to-energy-density ratio (dimensionless); $\rho_i$ = density of that component; $\rho_{i0}$ = its present density. Standard approximations: nonrelativistic matter $w=0$, radiation $w=1/3$, cosmological constant $w=-1$.

### C3 — Critical density, density fractions and ΛCDM expansion

$$
\rho_{\rm crit}(z)=\frac{3H(z)^2}{8\pi G},
\qquad
\Omega_{i0}=\frac{\rho_{i0}}{\rho_{{\rm crit},0}},
$$

$$
\frac{H(z)^2}{H_0^2}=
\Omega_{r0}(1+z)^4+
\Omega_{m0}(1+z)^3+
\Omega_{K0}(1+z)^2+
\Omega_{\Lambda0}.
$$

**Terms:** $\rho_{\rm crit}(z)$ = critical mass-equivalent density (kg/m³); $H(z)$ = expansion rate at redshift $z$; $H_0$ = rate today; $\Omega_{i0}$ = present component $i$'s density in units of present critical density; $\Omega_{r0}$ = radiation fraction; $\Omega_{m0}$ = *total matter fraction* including baryons and dark matter (and appropriate neutrino treatment); $\Omega_{K0}$ = spatial-curvature contribution; $\Omega_{\Lambda0}$ = cosmological-constant contribution. **This last form assumes ΛCDM and standard redshift scaling; treating massive neutrinos exactly requires additional terms/solvers.**

**Supporting present matter decomposition and curvature convention:**

$$
\Omega_{m0}=\Omega_{b0}+\Omega_{{\rm cdm},0}
+\Omega_{\nu0}\quad\text{(consistent component convention)},
\qquad
\Omega_{K0}=-\frac{Kc^2}{H_0^2},
$$

$$
\Omega_{\Lambda0}=\frac{\Lambda c^2}{3H_0^2},
\qquad
1=\Omega_{r0}+\Omega_{m0}+\Omega_{K0}+\Omega_{\Lambda0}.
$$

**New terms:** $\Omega_{b0}$ = ordinary-baryon density fraction; $\Omega_{{\rm cdm},0}$ = cold-dark-matter fraction; $\Omega_{\nu0}$ = neutrino contribution; $K$ = curvature C2. **Cosmological density fractions are inferred from a multi-observation model fit**, not the mass of a particle and not a direct measurement of local DM density.

### C4 — Cosmic density growth (linear, Newtonian/subhorizon, pressureless approximation)

$$
\ddot\delta+2H\dot\delta-4\pi G\rho_m\delta\simeq0,\qquad
\delta=\frac{\rho_m(\mathbf x,t)-\bar\rho_m(t)}{\bar\rho_m(t)}.
$$

**Terms:** $\delta$ = unitless matter-density contrast; $\rho_m(\mathbf x,t)$ = local matter density; $\bar\rho_m$ = mean background density; $\dot\delta,\ddot\delta$ = first/second derivatives in time; $H$ = expansion rate; $G$ = constant. This growth equation is **not valid as written at all scales, for all fluids, or in arbitrary modified-gravity models**.

### C5 — CMB temperature pattern and angular power spectrum (measurement/statistic)

$$
\frac{\Delta T(\hat{\mathbf n})}{\bar T}
=\sum_{\ell=0}^\infty\sum_{m=-\ell}^{\ell}
a_{\ell m}Y_{\ell m}(\hat{\mathbf n}),\qquad
\widehat C_\ell=\frac{1}{2\ell+1}
\sum_{m=-\ell}^{\ell}|a_{\ell m}|^2.
$$

**Terms:** $T(\hat{\mathbf n})$ = CMB temperature along sky direction $\hat{\mathbf n}$; $\bar T$ = mean CMB temperature (K); $\Delta T=T-\bar T$; $\ell$ = angular multipole (integer ≥0, roughly sets angular scale); $m$ = mode index between $-\ell$ and $+\ell$; $Y_{\ell m}$ = spherical harmonic function; $a_{\ell m}$ = spherical-harmonic coefficient; $\widehat C_\ell$ = power-spectrum estimator (dimensionless here because temperature was divided by $\bar T$). A cosmological model predicts **statistical** $C_\ell$ using Boltzmann solvers and detailed physics; this equation is how a map is summarized, not a stand-alone theory of CMB peak positions.

## 11. Gravitational waves and quantum-gravity scales (O-08, O-09)

### W1 — Leading binary-inspiral gravitational-wave frequency evolution (GR, approximation)

$$
\mathcal M=\frac{(m_1m_2)^{3/5}}{(m_1+m_2)^{1/5}},
\qquad
\frac{df}{dt}=
\frac{96}{5}\pi^{8/3}
\left(\frac{G\mathcal M}{c^3}\right)^{5/3}f^{11/3}.
$$

**Terms:** $\mathcal M$ = chirp mass (kg), a particular combination of component masses; $m_1,m_2$ = binary component masses (kg); $f$ = dominant gravitational-wave frequency (Hz); $df/dt$ = frequency increase per second (Hz/s); $G,c$ E1. **Validity:** leading-order, quasi-circular inspiral for an isolated compact binary. Spin, eccentricity, propagation effects and higher post-Newtonian terms require a full waveform model. We can compare future gravity models to observed waveforms, rather than assuming a galaxy fit suffices.

### Q1 — Planck scale (dimensional combination; not a detected quantum force)

$$
\ell_{\rm P}=\sqrt{\frac{\hbar G}{c^3}},
\qquad
t_{\rm P}=\sqrt{\frac{\hbar G}{c^5}},
\qquad
m_{\rm P}=\sqrt{\frac{\hbar c}{G}}.
$$

**Terms:** $\ell_{\rm P}$ = Planck length (m); $t_{\rm P}$ = Planck time (s); $m_{\rm P}$ = Planck mass (kg); $\hbar=h_{\rm P}/(2\pi)$ from E1; $G,c$ from E1. These *constructed scales* indicate where quantum and gravitational effects might both be important. Their existence does not prove a new gravity mechanism at galaxy scales.

## 12. Proper scientific testing: quantities, uncertainty, and falsification (O-10)

### T1 — Measurement uncertainty propagation (first-order, independent small errors)

$$
g=\frac{V^2}{R},\qquad
\left(\frac{\sigma_g}{g}\right)^2
\simeq
4\left(\frac{\sigma_V}{V}\right)^2+
\left(\frac{\sigma_R}{R}\right)^2.
$$

**Terms:** $g$ = derived acceleration (m/s²); $V$ = measured/inferred speed (m/s); $R$ = radius (m); $\sigma_g,\sigma_V,\sigma_R$ = estimated standard uncertainties in corresponding quantities. **Assumes** small errors and independent $V,R$. Correlated inclination/distance/systematic errors need a covariance treatment.

**General supporting uncertainty equation:**

$$
\operatorname{Var}(f)\simeq
\sum_{i,j}\frac{\partial f}{\partial x_i}
C_{ij}\frac{\partial f}{\partial x_j}.
$$

**New terms:** $f=f(x_1,\dots,x_n)$ = derived function of inputs; $x_i$ = input variable $i$; $C_{ij}=\operatorname{Cov}(x_i,x_j)$ = covariance matrix entries (units are product of input units); $\operatorname{Var}(f)=\sigma_f^2$ = output variance. This handles correlations and is preferable when comparing galaxy models.

### T2 — Fit residuals, logarithmic acceleration difference and chi-square

$$
r_i=y_i-y_{\rm model}(\mathbf x_i;\boldsymbol\theta),\qquad
\epsilon_i=\log_{10}g_{{\rm obs},i}
-\log_{10}g_{{\rm pred},i},
$$

$$
\chi^2=\mathbf r^{\,T}C^{-1}\mathbf r,\qquad
\chi^2_{\rm red}=\frac{\chi^2}{N-k}\quad(N>k).
$$

**Terms:** $i$ = measurement index; $y_i$ = measured or derived target in chosen units; $y_{\rm model}$ = model prediction; $\mathbf x_i$ = predictors; $\boldsymbol\theta$ = fitted parameters; $r_i$ = residual; $g_{\rm obs},g_{\rm pred}>0$ = observed and predicted accelerations; $\log_{10}$ = base-10 logarithm; $\epsilon_i$ = residual in dex; $\mathbf r$ = vector of residuals; $C$ = covariance matrix of residual errors; $C^{-1}$ = inverse covariance; superscript $T$ = transpose; $N$ = number of independent measurements; $k$ = count of fitted parameters; $\chi^2_{\rm red}$ = reduced chi-square, interpretable only if error model and degrees-of-freedom assumptions are suitable. **For the logarithmic expression, accelerations must share the same reference unit** (so their ratio is dimensionless).

**Equivalent safe logarithmic form:**

$$
\epsilon_i=\log_{10}\left(\frac{g_{{\rm obs},i}}{g_{{\rm pred},i}}\right).
$$

### T3 — Likelihood and model complexity (comparison, not truth detector)

$$
\ln\mathcal L=
-\frac12\left(\mathbf r^{\,T}C^{-1}\mathbf r
+\ln|C|+N\ln(2\pi)\right),
$$

$$
\mathrm{AIC}=2k-2\ln\widehat{\mathcal L},\qquad
\mathrm{BIC}=k\ln N-2\ln\widehat{\mathcal L}.
$$

**Terms:** $\mathcal L$ = Gaussian likelihood of the residuals conditional on model and error assumptions; $|C|$ = determinant of covariance matrix; $\widehat{\mathcal L}$ = maximized likelihood; AIC = Akaike information criterion; BIC = Bayesian information criterion; $k,N$ as T2. **Lower** AIC/BIC can indicate better fit-complexity tradeoffs *within their assumptions*; these are not independent evidence of a force. For hierarchical/correlated galaxy data, raw point count $N$ is not always an appropriate independent sample size.

### T4 — Cross-validation and predictive error (prevent “discovering” our own curve fit)

$$
\mathrm{MAE}_{\rm holdout}=
\frac1{N_{\rm test}}\sum_{i\in\mathcal I_{\rm test}}
|y_i-\widehat y_i|,\qquad
\mathrm{RMSE}_{\rm holdout}=
\sqrt{\frac1{N_{\rm test}}\sum_{i\in\mathcal I_{\rm test}}
(y_i-\widehat y_i)^2}.
$$

**Terms:** $\mathcal I_{\rm test}$ = withheld test set of indices, ideally entire *galaxies* rather than intermingled radii of the same object; $N_{\rm test}$ = withheld count; $y_i$ = ground-truth measurement or derived observable; $\widehat y_i$ = model prediction made without fitting on that test galaxy; MAE = mean absolute error; RMSE = root mean squared error, in the same units as $y$. **Predeclare** selection rules, fitting priors, nuisance parameters, and comparison metric.

### T5 — Falsifiable model and rejection rule

$$
H_0:\ g_{\rm obs}\sim g_{\rm known\ matter+halo}
\quad\text{versus}\quad
H_1:\ g_{\rm obs}\sim g_{\rm gravity\ modification},
$$

$$
\Delta\mathrm{MAE}=
\mathrm{MAE}(H_1)-\mathrm{MAE}(H_0).
$$

**Terms:** $H_0,H_1$ = competing hypotheses/models, **not** the Hubble constant $H_0$ in cosmology (context distinguishes them); “$\sim$” means “modeled by,” *not* equality or probability distribution here; $\Delta\mathrm{MAE}$ = comparison in same observable units. Negative $\Delta\mathrm{MAE}$ would favor $H_1$ for that particular held-out sample/metric, *not* establish gravity modification. To make the test honest, require adequate parameter control, uncertainties, robust comparisons, and successful independent lensing/cosmology/Solar System predictions.

## 13. Worked examples — from arithmetic to falsifiable checks

### Example A — Earth orbit: all quantities accounted for

1. **Inputs:** JPL solar $\mu_\odot\simeq1.3271244\times10^{20}\ \mathrm{m^3/s^2}$; defined $\mathrm{AU}=1.495978707\times10^{11}\ \mathrm m$.
2. **Required inward acceleration:** $g=\mu_\odot/\mathrm{AU}^2\simeq5.9301\times10^{-3}\ \mathrm{m/s^2}$ (S1).
3. **Circular speed:** $v=\sqrt{\mu_\odot/\mathrm{AU}}\simeq2.9785\times10^4\ \mathrm{m/s}$ = 29.785 km/s (S1).
4. **Toy smooth local halo:** with $\rho=5.35\times10^{-22}\ \mathrm{kg/m^3}$, S3 gives $M(<1\ \mathrm{AU})\simeq7.5\times10^{12}\ \mathrm{kg}$ and $g_{\rm uniform}\simeq2.24\times10^{-20}\ \mathrm{m/s^2}$.
5. **Relative scale:** $g_{\rm uniform}/g_{\odot@\oplus}\simeq3.8\times10^{-18}$. This is why a globally distributed component can be important across a galaxy but extremely difficult to notice in Earth–Sun *relative* motion. The true halo tidal field requires N6 and a galactocentric distribution.
6. **What would disprove a proposed new model here?** A predicted Earth–Sun difference above well-characterized ephemeris residual tolerances after correctly modeling known planetary forces and measurement uncertainty. Do *not* compare an uncorrected two-body orbit directly with a full JPL solution and call the difference new physics.

### Example B — A distant galactic star, purely illustrative numbers

Assume **for illustration only**, not from a specific SPARC record, $g_{\rm bar}=1.0\times10^{-11}\ \mathrm{m/s^2}$ and the established RAR parameter $g_\dagger=1.2\times10^{-10}\ \mathrm{m/s^2}$.

$$
g_{\rm RAR}=
\frac{1.0\times10^{-11}}
{1-\exp[-\sqrt{(1.0\times10^{-11})/(1.2\times10^{-10})}]}
\simeq4.0\times10^{-11}\ \mathrm{m/s^2}.
$$

**Terms:** $g_{\rm bar}$ = baryonic acceleration G3; $g_\dagger$ = RAR fit acceleration M1; $g_{\rm RAR}$ = prediction from M1. **Meaning:** the fitted relation predicts a much larger acceleration at low $g_{\rm bar}$. **It does not tell us whether the underlying cause is a halo, modified gravity, or something else.** The next step is a dataset-level comparison with errors, not another hand-selected example.

### Example C — What will actually be calculated from SPARC

For *each radius $R_i$ in each selected galaxy*: convert catalog units → preserve measured $V_{\rm obs}$, inclination/distance metadata, and uncertainties → calculate $V_{\rm bar}^2$ with signed gas contribution and documented $\Upsilon$ (G3) → compute $g_{{\rm obs},i}$ and $g_{{\rm bar},i}$ (G1/G3) → compare baryons alone, a fitted halo (D1–D3), and published RAR/MOND baseline (M1/M2) → evaluate residuals with covariance (T1–T4) → withhold whole galaxies for final testing. Validate against the original SPARC/RAR publications. Additional independent checks use JPL (S4), lensing (L1–L2), Gaia (J1–J2), Planck (C1–C5) and gravitational-wave constraints (W1).

## 14. Index: from each research open seam to equations

| Research issue | Equations to start with | What must be checked |
|---|---|---|
| O-01 Galaxy rotation / radial acceleration | N3, N4, G1–G5, M1–M3, D1–D3, T1–T4 | SPARC units, gas sign, mass-to-light priors, disk geometry |
| O-02 Dark-matter identity/distribution | D1–D4, G5, C3 | Model halo mass versus individual particle properties |
| O-03 Lensing / cluster mergers | R2–R3, L1–L2, D2–D3 | Light bending and projected mass; not just rotations |
| O-04 Solar System | N1–N6, S1–S4, R4 | Differential acceleration and precision ephemerides |
| O-05 Milky Way stellar dynamics | N3, J1–J2, D4 | Parallax, proper motion, tracer equilibrium/anisotropy |
| O-06 CMB / early cosmology | R2, C1–C5 | Consistent early-universe evolution and angular spectra |
| O-07 Cosmic acceleration | C1–C3 | Dark energy equation of state; separate from galactic DM |
| O-08 Quantum gravity | R1–R3, Q1 | A real quantum prediction—not scale numerology |
| O-09 Gravitational waves | R2–R3, W1 | Binary inspiral and wave-propagation tests |
| O-10 Measurement/model assumptions | E1–E2, G1–G3, T1–T5 | Units, correlated errors, nuisance parameters, withheld galaxies |
| O-11 Gravity vs practical levitation | N2, N7, S2 | Distinguish gravity itself from forces counteracting gravity |

## 15. Verified starting references and provenance

These are external sources for the definitions, published benchmark forms, and public observational data. **The equations above are synthesized explanations and are not copies of complete analyses, code, or finished model validation.** Some equations are elementary physics; others are explicitly attributed published empirical/halo models.

1. **SPARC (Lelli, McGaugh & Schombert 2016):** [Official data portal](https://astroweb.case.edu/SPARC/) and [original paper](https://arxiv.org/abs/1606.09251) — 175 disk galaxies, rotation curves and baryonic components.
2. **Radial acceleration relation (McGaugh, Lelli & Schombert 2016):** [Physical Review Letters DOI](https://doi.org/10.1103/PhysRevLett.117.201101) and [technical discussion of fitting form](https://academic.oup.com/mnras/article/487/2/2148/5487525) — M1 and limiting regime. Published prior art.
3. **Original SPARC-style machine-readable column documentation:** [CDS ReadMe for SPARC mass models](https://cdsarc.cds.unistra.fr/viz-bin/ReadMe/J/MNRAS/480/2292?format=html&tex=true). Always inspect the exact download's accompanying dictionary.
4. **NASA/JPL Horizons:** [Manual](https://ssd.jpl.nasa.gov/horizons/manual.html) and [API reference](https://ssd-api.jpl.nasa.gov/doc/horizons.html) — ephemerides, reference frames, gravitational parameters, S4.
5. **NFW profile / mass integral:** [General Relativity and Gravitation review](https://link.springer.com/article/10.1007/s10714-020-02715-w) — D3.
6. **GR fundamentals:** [NASA Glenn field equations and motion](https://www.grc.nasa.gov/www/k-12/Numbers/Math/Mathematical_Thinking/field_equations.htm) — R1–R4.
7. **ESA Gaia archive:** [Data archive](https://gea.esac.esa.int/archive/) — J1–J2; inspect DR3 documentation and astrometric quality before any distance inference.
8. **Planck cosmological constraints:** [Planck 2018 parameter paper](https://doi.org/10.1051/0004-6361/201833910) and [ESA Planck Legacy Archive](https://pla.esac.esa.int/) — C1–C5.
9. **DESI public survey data:** [Data releases/documentation](https://data.desi.lbl.gov/doc/) — additional independent clustering and expansion constraints.
10. **LIGO/Virgo/KAGRA:** [LIGO science summaries](https://ligo.org/science-summaries/) — independent gravity/waveform constraints.

### Before we call any result “evidence for a new force”

- [ ] Every variable has units; every measured field has an exact dataset/column name, release, uncertainty, and provenance.
- [ ] Known Newtonian/GR predictions and published dark-halo/RAR alternatives reproduced to stated tolerances.
- [ ] Assumptions (spherical vs disk, circular vs eccentric orbit, equilibrium vs merger) documented explicitly.
- [ ] Error propagation and correlations accounted for; negative/poor-quality data handled transparently.
- [ ] Model fit performed on training galaxies; final prediction evaluated on untouched galaxies.
- [ ] Solar System, lensing, clusters, cosmology and gravitational-wave constraints checked where physically applicable.
- [ ] Negative evidence and falsification recorded; model complexity and post hoc tuning disclosed.
- [ ] Nothing called “proved” until supported by reproducible, independently checked measurements.

**Next action:** Start with Sections 1–4 and Example A, then run the first SPARC reproduction from the main research checklist. This document is the durable equation/variable reference; maintain one canonical copy here.