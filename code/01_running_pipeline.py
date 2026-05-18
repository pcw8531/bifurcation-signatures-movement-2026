"""
01_running_pipeline.py

Reproduces Section 2.1.1 of the manuscript and Section S2 of the SI.

Population-scale running variance-amplification analysis on the Fukuchi
running dataset (Fukuchi et al. 2017, PeerJ, figshare 10.6084/m9.figshare.4543435.v4).

The state variable is the antisymmetric pelvic-obliquity signal
    x(t) = L.ASIS_Y(t) - R.ASIS_Y(t)
(Equation 8 of main manuscript). Consecutive variance ratios
    R1 = var(3.5) / var(2.5)
    R2 = var(4.5) / var(3.5)
(Equation 9) are tested at the population level against three reference scales
under the Wilcoxon signed-rank test on log-ratios (Equation 10):
    null R = 1, R = phi ~ 1.618, R = delta ~ 4.669.

Expected output:
    R1 median = 1.623, vs phi p = 0.295, vs delta p < 0.0001
    R2 median = 1.546, vs phi p = 0.022, vs delta p < 0.0001
"""
import numpy as np
import pandas as pd
from pathlib import Path
from scipy.stats import wilcoxon
import re

# === Configuration ===
# Point this to your local copy of the Fukuchi figshare archive.
# The repository ships per-subject summaries in ../data/running_per_subject.csv
# that reproduce these statistics without requiring the raw archive.
DATA1 = Path("./fukuchi_archive")     # raw archive location, set if running from raw
PROCESSED = Path(__file__).resolve().parent.parent / "data" / "running_per_subject.csv"

PHI = (1 + np.sqrt(5)) / 2            # ~ 1.6180
DELTA = 4.6692016091029               # Feigenbaum constant

# === Per-subject variance computation (Equation 8) ===
def running_pelvis_variance(filepath):
    """Compute variance of the antisymmetric pelvic-obliquity signal."""
    df = pd.read_csv(filepath, sep="\t")
    diff = df["L.ASISY"].values - df["R.ASISY"].values
    diff = diff[np.isfinite(diff)]
    return float(np.var(diff, ddof=1)), len(diff)


def run_from_raw(data_dir):
    """Walk the figshare archive and compute per-subject variance and ratios."""
    subjects = sorted(set(
        re.match(r"RBDS(\d{3})", f.name).group(1)
        for f in data_dir.iterdir()
        if f.is_file() and re.match(r"RBDS\d{3}", f.name)
    ))
    SPEEDS = [("2.5", "T25"), ("3.5", "T35"), ("4.5", "T45")]
    rows = []
    for s in subjects:
        row = {"subject": f"RBDS{s}"}
        for speed_label, code in SPEEDS:
            fpath = data_dir / f"RBDS{s}run{code}markers.txt"
            var, _ = running_pelvis_variance(fpath)
            row[f"var_{speed_label}"] = var
        row["R1"] = row["var_3.5"] / row["var_2.5"]
        row["R2"] = row["var_4.5"] / row["var_3.5"]
        rows.append(row)
    return pd.DataFrame(rows)


def population_stats(df):
    """Population-level Wilcoxon signed-rank inference on log-ratios (Equation 10)."""
    out = {}
    for ratio in ["R1", "R2"]:
        vals = df[ratio].dropna().values
        out[ratio] = {
            "median": float(np.median(vals)),
            "geometric_mean": float(np.exp(np.mean(np.log(vals)))),
            "IQR_lower": float(np.percentile(vals, 25)),
            "IQR_upper": float(np.percentile(vals, 75)),
            "n": int(len(vals)),
        }
        for ref_name, ref_val in [("1.0", 1.0), ("phi", PHI), ("delta", DELTA)]:
            _, p = wilcoxon(np.log(vals) - np.log(ref_val))
            out[ratio][f"p_vs_{ref_name}"] = float(p)
    return out


if __name__ == "__main__":
    if DATA1.exists():
        print(f"Running from raw archive at {DATA1}")
        df = run_from_raw(DATA1)
    else:
        print(f"Loading processed per-subject table from {PROCESSED}")
        df = pd.read_csv(PROCESSED)

    print(f"\nFukuchi running, n = {len(df)}")
    stats = population_stats(df)
    for ratio in ["R1", "R2"]:
        s = stats[ratio]
        print(f"\n{ratio}: median = {s['median']:.3f}, "
              f"geometric mean = {s['geometric_mean']:.3f}, "
              f"IQR = [{s['IQR_lower']:.3f}, {s['IQR_upper']:.3f}]")
        print(f"   p vs 1.0   = {s['p_vs_1.0']:.4f}")
        print(f"   p vs phi   = {s['p_vs_phi']:.4f}")
        print(f"   p vs delta = {s['p_vs_delta']:.4f}")
