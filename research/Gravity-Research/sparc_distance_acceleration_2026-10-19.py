#!/usr/bin/env python3
"""Exploratory SPARC galaxy-radius vs baryonic-acceleration diagnostic.

Python 3 standard library; deterministic 5-fold galaxy-held-out comparison.
Source tables are original Lelli et al. SPARC data mirrored at:
https://github.com/JustinSchneider/baryonic-omega-analysis/tree/main/data/raw
Source Git blob SHAs: mass models 3f0ea8e3577ec9e0226e4f6a65f1019d45f1aec6;
galaxy sample 8cdfb503c58bf5f4fc6321e976f7caec6e353bf3.
For scientific use cross-check mirror bytes and source table documentation
against https://astroweb.case.edu/SPARC/. No mass-model proof follows from fits.
"""
import argparse
import json
import math
import re
from collections import Counter, defaultdict
from pathlib import Path
from urllib.request import urlopen

BASE = "https://raw.githubusercontent.com/JustinSchneider/baryonic-omega-analysis/main/data/raw/"
MASS = "MassModels_Lelli2016c.mrt"
SAMPLE = "SPARC_Lelli2016c.mrt"
KPC_M = 3.085677581491367e19
A0 = 1.2e-10  # illustrative, published RAR scale; NOT fitted in this script


def load(filename, directory=None):
    """Read a local original table, or fetch the referenced public mirror."""
    if directory:
        return (Path(directory) / filename).read_text(encoding="utf-8")
    with urlopen(BASE + filename, timeout=30) as response:
        return response.read().decode("utf-8")


def source_rows(mass_text, sample_text):
    mass = []
    for line in mass_text.splitlines():
        if not re.match(r"^[A-Za-z0-9][A-Za-z0-9+\- ]{0,10}\s+\d", line):
            continue
        a = line.strip().split()
        if len(a) != 10:
            raise ValueError("Unexpected SPARC mass-model row: " + line)
        mass.append({"id": a[0], "r": float(a[2]), "v": float(a[3]),
                     "vg": float(a[5]), "vd": float(a[6]), "vb": float(a[7])})
    galaxy = []
    for line in sample_text.splitlines():
        if not re.match(r"^\s*[A-Za-z0-9+\-]+\s+\d{1,2}\s+\d+\.\d+", line):
            continue
        a = line.strip().split()
        if len(a) != 19:
            raise ValueError("Unexpected SPARC galaxy row: " + line)
        galaxy.append({"id": a[0], "inc": float(a[5]), "q": int(a[17])})
    if len(mass) != 3391 or len(galaxy) != 175:
        raise ValueError("Source cardinality drift; inspect provenance/format")
    return mass, galaxy


def linear_solve(aug):
    """Gaussian elimination with partial pivoting for weighted normal equations."""
    n = len(aug)
    for i in range(n):
        pivot_row = max(range(i, n), key=lambda k: abs(aug[k][i]))
        aug[i], aug[pivot_row] = aug[pivot_row], aug[i]
        pivot = aug[i][i]
        if abs(pivot) < 1e-11:
            raise ValueError("Singular normal equations")
        for j in range(i, n + 1):
            aug[i][j] /= pivot
        for k in range(n):
            if k == i:
                continue
            scale = aug[k][i]
            for j in range(i, n + 1):
                aug[k][j] -= scale * aug[i][j]
    return [row[n] for row in aug]


def fit(data, keys):
    """Each galaxy has total weight 1, regardless of number of radii."""
    p = len(keys) + 1
    aug = [[0.0] * (p + 1) for _ in range(p)]
    for d in data:
        x = [1.0] + [d[k] for k in keys]
        for i in range(p):
            for j in range(p):
                aug[i][j] += d["w"] * x[i] * x[j]
            aug[i][p] += d["w"] * x[i] * d["y"]
    return linear_solve(aug)


def test_case(mass, galaxy, disk=0.5, bulge=0.7, min_inc=30.0, max_quality=2):
    accepted = {g["id"] for g in galaxy if g["inc"] >= min_inc and g["q"] <= max_quality}
    data = []
    for m in mass:
        if m["id"] not in accepted:
            continue
        # SPARC Vgas has a negative sign in some radial gas mass models.
        vbar_sq = (m["vg"] * abs(m["vg"]) + disk * m["vd"] ** 2
                   + bulge * m["vb"] ** 2)
        if m["r"] <= 0 or m["v"] <= 0 or vbar_sq <= 0:
            continue
        gbar = (vbar_sq / m["r"]) * 1e6 / KPC_M
        gobs = (m["v"] ** 2 / m["r"]) * 1e6 / KPC_M
        rar_pred = gbar / (-math.expm1(-math.sqrt(gbar / A0)))
        data.append({"id": m["id"], "y": math.log10(gobs / gbar),
                     "logr": math.log10(m["r"]),
                     "loglow": math.log10(1e-10 / gbar),
                     "bar_err": math.log10(gbar / gobs),
                     "rar_err": math.log10(rar_pred / gobs)})
    counts = Counter(d["id"] for d in data)
    ids = sorted(counts)
    folds = {gid: i % 5 for i, gid in enumerate(ids)}
    for d in data:
        d["w"] = 1.0 / counts[d["id"]]
        d["fold"] = folds[d["id"]]

    def rmse_by_galaxy(squared_by_id):
        return math.sqrt(sum(squared_by_id.values()) / len(squared_by_id))

    def fixed_metric(err_key):
        errors = defaultdict(float)
        for d in data:
            errors[d["id"]] += d["w"] * d[err_key] ** 2
        return rmse_by_galaxy(errors)

    def cross_validated(keys):
        errors = defaultdict(float)
        for f in range(5):
            training = [d for d in data if d["fold"] != f]
            coef = fit(training, keys)
            for d in data:
                if d["fold"] == f:
                    pred = coef[0] + sum(coef[i + 1] * d[k] for i, k in enumerate(keys))
                    errors[d["id"]] += d["w"] * (pred - d["y"]) ** 2
        return {"rmse_dex": rmse_by_galaxy(errors), "all_data_coefficients": fit(data, keys)}
    return {
        "galaxies": len(ids), "radii": len(data),
        "disk_ML": disk, "bulge_ML": bulge,
        "min_inclination_degrees": min_inc, "max_quality_flag": max_quality,
        "fixed_baryon_only_rmse_dex": fixed_metric("bar_err"),
        "fixed_RAR_a0_1p2e_minus10_rmse_dex": fixed_metric("rar_err"),
        "constant_fit": cross_validated([]),
        "radius_fit": cross_validated(["logr"]),
        "low_acceleration_fit": cross_validated(["loglow"]),
        "acceleration_plus_radius_fit": cross_validated(["logr", "loglow"]),
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source-dir", help="Use two original .mrt files from this folder")
    args = parser.parse_args()
    mass, galaxy = source_rows(load(MASS, args.source_dir), load(SAMPLE, args.source_dir))
    cases = {
        "primary": test_case(mass, galaxy),
        "quality_1_only": test_case(mass, galaxy, max_quality=1),
        "all_inclinations": test_case(mass, galaxy, min_inc=0),
        "disk_ML_0p2": test_case(mass, galaxy, disk=0.2),
        "disk_ML_0p4": test_case(mass, galaxy, disk=0.4),
        "disk_ML_0p6": test_case(mass, galaxy, disk=0.6),
        "disk_ML_0p8": test_case(mass, galaxy, disk=0.8),
    }
    print(json.dumps(cases, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
