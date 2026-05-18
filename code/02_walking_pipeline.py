"""
02_walking_pipeline.py

Reproduces Section 2.1.2 of the manuscript and Section S3 of the SI.

Population-scale walking variance-amplification analysis on the Riglet
walking dataset (Riglet et al. 2024, Sci. Data, figshare 10.6084/m9.figshare.24296217).

The state variable is the vertical pelvic-marker excursion (PELVISO_Z) per
gait cycle, bracketed left-foot-strike to left-foot-strike. Consecutive
variance ratios (Equation 9) are tested at the population level under the
Wilcoxon signed-rank test (Equation 10) against R = 1, phi, delta.

Expected output:
    R1 median = 1.409, vs phi p = 0.031, vs delta p < 0.0001
    R2 median = 1.256, vs phi p = 0.001, vs delta p < 0.0001
"""
import numpy as np
import pandas as pd
from pathlib import Path
from scipy.stats import wilcoxon

DATA2 = Path("./riglet_archive")
PROCESSED = Path(__file__).resolve().parent.parent / "data" / "walking_per_subject.csv"

PHI = (1 + np.sqrt(5)) / 2
DELTA = 4.6692016091029


def parse_riglet_csv(filepath, channel="PELVISO", axis="Z"):
    """Parse Riglet post-processed CSV: hierarchical metadata + events + 100 Hz point block."""
    AXIS_OFFSET = {"X": 0, "Y": 1, "Z": 2}
    with open(filepath, "r", encoding="utf-8", errors="replace") as f:
        lines = f.readlines()
    metadata = {}
    i = 0
    while i < len(lines) and lines[i].strip():
        parts = lines[i].strip().split(",")
        if len(parts) >= 2 and parts[0]:
            try:
                metadata[parts[0]] = int(parts[1]) if parts[1].isdigit() else float(parts[1])
            except ValueError:
                metadata[parts[0]] = parts[1]
        i += 1
    n_frames = int(metadata.get("FrameNumber", 0))
    fs = int(metadata.get("PointFrequency", 100))
    while i < len(lines) and not lines[i].strip():
        i += 1
    events = {}
    while i < len(lines):
        s = lines[i].strip()
        if not s:
            i += 1
            continue
        if s.split(",")[0].startswith(("Left_", "Right_")):
            parts = s.split(",")
            events[parts[0]] = [int(round(float(p) * fs)) for p in parts[1:] if p.strip()]
            i += 1
        else:
            break
    while i < len(lines) and not lines[i].strip():
        i += 1
    header_idx = i
    L10 = lines[header_idx].rstrip().split(",")
    target_col = None
    for col_i, name in enumerate(L10):
        if name.strip() == channel:
            target_col = col_i + AXIS_OFFSET[axis]
            break
    if target_col is None:
        return None
    df_raw = pd.read_csv(filepath, skiprows=header_idx + 3, header=None,
                         usecols=[target_col], low_memory=False)
    sig = pd.to_numeric(df_raw[target_col], errors="coerce").values
    if n_frames > 0:
        sig = sig[:n_frames]
    return dict(signal=sig, fs=fs, events=events)


def cycle_pp_variance(parsed):
    """Per-cycle peak-to-peak excursion, variance across cycles (Equation 8)."""
    sig = parsed["signal"]
    strikes = parsed["events"].get("Left_Foot_Strike", [])
    if len(strikes) < 11:
        return None
    excursions = []
    for i in range(len(strikes) - 1):
        start, end = strikes[i], strikes[i + 1]
        if start < 0 or end > len(sig) or end <= start:
            continue
        seg = sig[start:end]
        if not np.any(np.isfinite(seg)):
            continue
        excursions.append(float(np.nanmax(seg) - np.nanmin(seg)))
    if len(excursions) < 10:
        return None
    return float(np.var(np.array(excursions), ddof=1)), len(excursions)


def run_from_raw(data_dir):
    SPEED_FOLDERS = [("Slow", "Treadmill_Walk_Slow"),
                     ("Comfortable", "Treadmill_Walk_Comfortable"),
                     ("Fast", "Treadmill_Walk_Fast")]
    subjects = sorted([d.name for d in data_dir.iterdir()
                       if d.is_dir() and d.name not in ("Python Code",)])
    rows = []
    for subj in subjects:
        row = {"subject": subj}
        ok = True
        for label, folder in SPEED_FOLDERS:
            fpath = (data_dir / subj / "Session1" / "Treadmill_Walk"
                     / folder / "Post_Process" / f"{folder}.csv")
            if not fpath.exists():
                ok = False
                break
            parsed = parse_riglet_csv(fpath, "PELVISO", "Z")
            if parsed is None:
                ok = False
                break
            result = cycle_pp_variance(parsed)
            if result is None:
                ok = False
                break
            row[f"var_{label}"] = result[0]
        if ok:
            row["R1"] = row["var_Comfortable"] / row["var_Slow"]
            row["R2"] = row["var_Fast"] / row["var_Comfortable"]
            rows.append(row)
    return pd.DataFrame(rows)


def population_stats(R1, R2):
    out = {}
    for label, vals in [("R1", R1), ("R2", R2)]:
        out[label] = {
            "median": float(np.median(vals)),
            "geometric_mean": float(np.exp(np.mean(np.log(vals)))),
            "n": int(len(vals)),
        }
        for ref_name, ref_val in [("1.0", 1.0), ("phi", PHI), ("delta", DELTA)]:
            _, p = wilcoxon(np.log(vals) - np.log(ref_val))
            out[label][f"p_vs_{ref_name}"] = float(p)
    return out


if __name__ == "__main__":
    if DATA2.exists():
        print(f"Running from raw archive at {DATA2}")
        df = run_from_raw(DATA2)
        R1 = df["R1"].dropna().values
        R2 = df["R2"].dropna().values
    else:
        print(f"Loading processed summary from {PROCESSED}")
        df_summary = pd.read_csv(PROCESSED)
        print(df_summary)
        # The summary file has already-computed statistics
        print("\nNote: per-subject raw values require the Riglet figshare archive.")
        print("Set DATA2 path at top of file to recompute from raw data.")
        raise SystemExit

    stats = population_stats(R1, R2)
    print(f"\nRiglet walking, n = {len(df)}")
    for ratio in ["R1", "R2"]:
        s = stats[ratio]
        print(f"\n{ratio}: median = {s['median']:.3f}, "
              f"geometric mean = {s['geometric_mean']:.3f}")
        print(f"   p vs 1.0   = {s['p_vs_1.0']:.4f}")
        print(f"   p vs phi   = {s['p_vs_phi']:.4f}")
        print(f"   p vs delta = {s['p_vs_delta']:.4f}")
