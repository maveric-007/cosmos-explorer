#!/usr/bin/env python3
"""Reproduce synthetic WGS 84 ellipsoid gravitational flux at 1 degree resolution.

Uses no external libraries. The input normal gravity comes from the WGS 84
reference potential, so its mass estimate is a MODEL CONSISTENCY CHECK,
not independently measured Earth mass.

Run:
  python earth_mass_gauss_flux.py
  python earth_mass_gauss_flux.py --all-cells

The optional flag creates 64,800 equal-1-degree longitude/latitude cells,
all THEORETICAL; it does not invent geographic observations.
"""
import argparse
import csv
import math
from pathlib import Path

A = 6378137.0
B = A * (1.0 - 1.0 / 298.257223563)
E2 = 1.0 - B**2/A**2
OMEGA = 7.292115e-5
G = 6.67430e-11
G_SIGMA = 0.00015e-11
GE = 9.7803253359
GP = 9.8321849378
K = B*GP/(A*GE) - 1.0
MU_WGS = 3.986004418e14

# Gauss-Legendre quadrature on [-1, 1], order 4.
NODES = (-.8611363115940526, -.3399810435848563,
          .3399810435848563,  .8611363115940526)
WEIGHTS = (.3478548451374538, .6521451548625461,
           .6521451548625461, .3478548451374538)


def field(phi):
    """At geodetic latitude phi [radians]: N [m], R_meridional [m], gamma [m/s^2]."""
    sin2 = math.sin(phi)**2
    t = 1.0 - E2*sin2
    return (
        A/math.sqrt(t),
        A*(1.0-E2)/t**1.5,
        GE*(1.0+K*sin2)/math.sqrt(t)
    )


def latitude_band(lo):
    """Surface-flux contribution for [lo, lo+1] geodetic degrees, all 360 longitudes."""
    mid = math.radians(lo + .5)
    h = math.radians(.5)
    area_parts = []
    normal_parts = []
    rot_parts = []
    for x, weight in zip(NODES, WEIGHTS):
        phi = mid + h*x
        n, rmer, gamma = field(phi)
        c = math.cos(phi)
        # Integral over longitude is 2*pi because ideal WGS84 is axisymmetric.
        # Area element: dA = N*Rmer*cos(phi) dphi dlambda
        area = 2.0*math.pi*h*weight*n*rmer*c
        area_parts.append(area)
        normal_parts.append(gamma*area/(4.0*math.pi))
        rot_parts.append(OMEGA**2*n*c*c*area/(4.0*math.pi))
    n, _, gamma_mid = field(mid)
    c, s = math.cos(mid), math.sin(mid)
    r_mid = math.sqrt((A**4*c*c+B**4*s*s)/(A*A*c*c+B*B*s*s))
    normal = math.fsum(normal_parts)
    rotation = math.fsum(rot_parts)
    return dict(
        latitude_lo_deg=lo,
        latitude_hi_deg=lo+1,
        mid_geodetic_latitude_deg=lo+.5,
        mid_geocentric_radius_m=r_mid,
        mid_normal_gravity_m_s2=gamma_mid,
        band_area_m2=math.fsum(area_parts),
        mu_normal_contribution_m3_s2=normal,
        mu_rotation_contribution_m3_s2=rotation,
        mu_total_contribution_m3_s2=normal+rotation,
        band_mass_equivalent_kg=(normal+rotation)/G,
        longitude_grid_cells=360,
        provenance="WGS84_THEORETICAL_NOT_MEASURED"
    )


def write_csv(path, rows):
    with path.open("w", encoding="utf8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--all-cells", action="store_true",
                        help="also export 64,800 theoretical 1-degree lat-lon cells")
    args = parser.parse_args()
    bands = [latitude_band(lo) for lo in range(-90,90)]
    assert len(bands) == 180
    here = Path(__file__).resolve().parent
    path = here/"Earth-Mass-Gauss-Flux-Latitude-Bands-2026-10-15.csv"
    write_csv(path, bands)

    if args.all_cells:
        cells = []
        for band in bands:
            for lon in range(360):
                cells.append({
                    "latitude_lo_deg":band["latitude_lo_deg"],
                    "latitude_hi_deg":band["latitude_hi_deg"],
                    "longitude_lo_deg":lon,
                    "longitude_hi_deg":lon+1,
                    "area_m2":band["band_area_m2"]/360.0,
                    "mu_normal_m3_s2":band["mu_normal_contribution_m3_s2"]/360.0,
                    "mu_rotation_m3_s2":band["mu_rotation_contribution_m3_s2"]/360.0,
                    "mu_total_m3_s2":band["mu_total_contribution_m3_s2"]/360.0,
                    "provenance":"WGS84_THEORETICAL_NOT_MEASURED"
                })
        assert len(cells)==64800
        write_csv(here/"Earth-Mass-Gauss-Flux-64800-Cells-2026-10-15.csv", cells)
        print("Generated", len(cells), "theoretical 1° grid cells")

    mu_n=math.fsum(row["mu_normal_contribution_m3_s2"] for row in bands)
    mu_r=math.fsum(row["mu_rotation_contribution_m3_s2"] for row in bands)
    mu=mu_n+mu_r
    volume=4.0*math.pi*A*A*B/3.0
    # Volume theorem independently checks centrifugal surface integral.
    assert abs(mu_r-OMEGA**2*volume/(2*math.pi)) < .25
    print("WGS84 theoretical model (not independent Earth measurements)")
    print("180 latitude bands, 360 longitude cells each")
    print("mu_normal m^3/s^2:", format(mu_n,".6f"))
    print("mu_rotation m^3/s^2:", format(mu_r,".6f"))
    print("mu_total m^3/s^2:", format(mu,".6f"))
    print("mu_WGS m^3/s^2:", format(MU_WGS,".6f"))
    print("mu residual:", format(mu-MU_WGS,".6f"))
    print("mass kg:", format(mu/G, ".12e"))
    print("WGS84 mass kg:", format(MU_WGS/G, ".12e"))
    print("mass std uncertainty from G alone kg:",
          format(MU_WGS/G*G_SIGMA/G, ".12e"))


if __name__=="__main__":
    main()
