#!/usr/bin/env python3
"""SPARC: pair galaxies of similar estimated baryonic mass but different disk scale lengths.

Reproduces the companion 2026-10-19 observational diagnostic. Python 3 stdlib.
Downloads original-format SPARC tables from a public mirror, or accepts local
copies. Verifies expected Git blob SHAs to prevent unnoticed upstream drift.
Results are descriptive and selection-dependent, NOT new physics.
"""
import argparse
import hashlib
import json
import math
import re
import statistics
from pathlib import Path
from urllib.request import urlopen

BASE = "https://raw.githubusercontent.com/JustinSchneider/baryonic-omega-analysis/main/data/raw/"
MASSFILE = "MassModels_Lelli2016c.mrt"
GALFILE = "SPARC_Lelli2016c.mrt"
EXPECTED_GIT_BLOBS = {
    MASSFILE: "3f0ea8e3577ec9e0226e4f6a65f1019d45f1aec6",
    GALFILE: "8cdfb503c58bf5f4fc6321e976f7caec6e353bf3",
}


def get_source(name, directory=None):
    data = ((Path(directory) / name).read_bytes() if directory
            else urlopen(BASE + name, timeout=30).read())
    git_sha = hashlib.sha1(b"blob " + str(len(data)).encode("ascii")
                           + b"\x00" + data).hexdigest()
    if git_sha != EXPECTED_GIT_BLOBS[name]:
        raise ValueError(f"Input {name} Git blob SHA changed: {git_sha}. "
                         "Manually verify published source before use.")
    return data.decode("utf-8")


def read_tables(mass_text, galaxy_text):
    mass = []
    for line in mass_text.splitlines():
        if not re.match(r"^[A-Za-z0-9][A-Za-z0-9+\- ]{0,10}\s+\d", line):
            continue
        cols = line.strip().split()
        if len(cols) != 10:
            raise ValueError("Unexpected mass-model row: " + line)
        mass.append(dict(id=cols[0], r=float(cols[2]), v=float(cols[3]),
                         vg=float(cols[5]), vd=float(cols[6]), vb=float(cols[7])))
    gal = []
    for line in galaxy_text.splitlines():
        if not re.match(r"^\s*[A-Za-z0-9+\-]+\s+\d{1,2}\s+\d+\.\d+", line):
            continue
        cols = line.strip().split()
        if len(cols) != 19:
            raise ValueError("Unexpected sample row: " + line)
        gal.append(dict(id=cols[0], quality=int(cols[17]),
                        inc=float(cols[5]), L36=float(cols[7]),
                        rd=float(cols[11]), MHI=float(cols[13])))
    if len(gal) != 175 or len(mass) != 3391:
        raise ValueError("Unexpected source table counts")
    return mass, gal


def at_relative_radius(mass, galaxy, disk_ml=0.5, bulge_ml=0.7,
                       max_quality=2, min_inclination=30):
    by_id = {}
    for row in mass:
        by_id.setdefault(row["id"], []).append(row)
    output = []
    eligible = 0
    for g in galaxy:
        if (g["quality"] > max_quality or g["inc"] < min_inclination
                or g["rd"] <= 0 or g["L36"] <= 0 or g["MHI"] < 0):
            continue
        eligible += 1
        # Compare at the same relative stellar disk radius 2.2 x Rd,
        # NOT at the same absolute distance in kpc.
        target = 2.2 * g["rd"]
        rows = sorted(by_id.get(g["id"], []), key=lambda row: row["r"])
        if not rows or target < rows[0]["r"] or target > rows[-1]["r"]:
            continue  # no extrapolation outside data extent
        right = next((i for i in range(1, len(rows)) if rows[i]["r"] >= target), None)
        if right is None:
            continue  # do not extrapolate outside observed curve
        lo, hi = rows[right - 1], rows[right]
        if hi["r"] <= lo["r"]:
            continue
        f = (target - lo["r"]) / (hi["r"] - lo["r"])

        def vbar_squared(row):
            # SPARC signed gas term includes helium. Stars from 3.6um M/L=1.
            return (row["vg"] * abs(row["vg"])
                    + disk_ml * row["vd"] ** 2 + bulge_ml * row["vb"] ** 2)

        vbar2 = (1 - f) * vbar_squared(lo) + f * vbar_squared(hi)
        vobs2 = (1 - f) * lo["v"] ** 2 + f * hi["v"] ** 2
        if vbar2 <= 0 or vobs2 <= 0:
            continue
        # Total stellar mass approximated by disk M/L times 3.6um L,
        # plus neutral H I *1.33. This is an INCOMPLETE baryon inventory.
        mstar = disk_ml * g["L36"] * 1e9
        gas = 1.33 * g["MHI"] * 1e9
        mtot = mstar + gas
        output.append(dict(id=g["id"], Mbar=mtot, rd=g["rd"],
                           r=target, fg=gas / mtot,
                           vbar=math.sqrt(vbar2), vobs=math.sqrt(vobs2),
                           gbar_relative=vbar2 / target, discrepancy=vobs2 / vbar2))
    return output, eligible


def matches(valid, max_delta_log_mass=0.1, max_delta_gas_fraction=0.10,
            min_disk_size_factor=2.0):
    """Greedy, disjoint pairs; match by gas-fraction difference first,
    then log-mass difference, then largest disk-size ratio, then names.
    Each galaxy appears only once in the selected pairs.
    """
    candidates = []
    for i, left in enumerate(valid):
        for right in valid[i + 1:]:
            a, b = sorted([left, right], key=lambda item: (item["rd"], item["id"]))
            dmass = abs(math.log10(a["Mbar"] / b["Mbar"]))
            dgas = abs(a["fg"] - b["fg"])
            size = b["rd"] / a["rd"]
            if (dmass <= max_delta_log_mass
                    and dgas <= max_delta_gas_fraction
                    and size >= min_disk_size_factor):
                candidates.append((dgas, dmass, -size, a["id"], b["id"], a, b))
    candidates.sort(key=lambda row: row[:5])
    used = set()
    selected = []
    for _, delta_m, _, a_id, b_id, a, b in candidates:
        if a_id in used or b_id in used:
            continue
        selected.append((a, b))
        used.update((a_id, b_id))
    return selected, len(candidates)


def run_case(mass, gal, quality=2, max_mass_difference_dex=0.1,
             max_gas_difference=0.1, size_factor=2):
    valid, eligible = at_relative_radius(mass, gal, max_quality=quality)
    pairs, all_candidates = matches(valid, max_mass_difference_dex,
                                    max_gas_difference, size_factor)
    summary = dict(
        eligible_galaxies=eligible, interpolated_galaxies=len(valid),
        candidate_pairs=all_candidates, disjoint_pairs=len(pairs),
        extended_lower_baryonic_g=sum(
            b["gbar_relative"] < a["gbar_relative"] for a, b in pairs),
        extended_lower_baryonic_v=sum(
            b["vbar"] < a["vbar"] for a, b in pairs),
        extended_higher_discrepancy=sum(
            b["discrepancy"] > a["discrepancy"] for a, b in pairs),
        extended_higher_observed_v=sum(
            b["vobs"] > a["vobs"] for a, b in pairs),
        median_size_ratio=(statistics.median(b["rd"] / a["rd"]
                                            for a, b in pairs) if pairs else None),
        median_gbar_ratio=(statistics.median(
            b["gbar_relative"] / a["gbar_relative"]
            for a, b in pairs) if pairs else None),
        pairs=[dict(small=a["id"], extended=b["id"],
                    mass_small=a["Mbar"], mass_extended=b["Mbar"],
                    rd_small=a["rd"], rd_extended=b["rd"],
                    gas_fraction_small=a["fg"], gas_fraction_extended=b["fg"],
                    radius_small=a["r"], radius_extended=b["r"],
                    vbar_small=a["vbar"], vbar_extended=b["vbar"],
                    vobs_small=a["vobs"], vobs_extended=b["vobs"],
                    discrepancy_small=a["discrepancy"],
                    discrepancy_extended=b["discrepancy"])
               for a, b in pairs])
    return summary


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source-dir", help="Directory of original .mrt files")
    args = parser.parse_args()
    mass, gal = read_tables(get_source(MASSFILE, args.source_dir),
                            get_source(GALFILE, args.source_dir))
    cases = {
        "main": run_case(mass, gal),
        "quality_1_only": run_case(mass, gal, quality=1),
        "gas_fraction_difference_le_0p05": run_case(mass, gal, max_gas_difference=0.05),
        "mass_difference_le_0p05_dex": run_case(mass, gal, max_mass_difference_dex=0.05),
        "disk_size_at_least_3x": run_case(mass, gal, size_factor=3),
    }
    print(json.dumps(cases, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
