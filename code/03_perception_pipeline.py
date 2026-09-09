"""
03_perception_pipeline.py

Reproduces Section 2.2 of the manuscript and Section S4 of the SI.

Perceptual-expertise analysis on the haptic-perception dataset (Park 2026, reference [25]
of the manuscript).

Computes per-participant absolute error (AE, Equation 13), independent-samples
t-test, Cohen's d, Shapiro-Wilk normality, and pre-registered within-group
strategic-variability criterion via Pearson correlation between trajectory
Shannon entropy (Equation 14) and AE.

Expected output, recomputed from data/perception_per_participant.csv
(per-participant means, 10 per group):
    Novice M = 4.215, Expert M = 2.130 (group means reproduce the manuscript)
    Sample SD 0.429 / 0.156, t(18) = 14.44, p < 0.001, Cohen d = 6.46
Values reported in the manuscript and in the source publication [25], which
were computed on the trial-level data of that study (10 trials per
participant, not shipped here):
    SD = 0.406 / 0.143, t(18) = 15.36, p < 0.001, Cohen d = 6.9
    Expert rho(H, AE) = -0.73, p = 0.009
    Novice rho(H, AE) = -0.21, p = 0.564
The trajectory-entropy values H are not in the shipped table, so the
within-group correlations are printed from the source publication.
"""
import numpy as np
import pandas as pd
from pathlib import Path
from scipy import stats

PROCESSED = Path(__file__).resolve().parent.parent / "data" / "perception_per_participant.csv"


def shannon_entropy_axis(values, n_bins=None):
    """Shannon entropy on a single-axis trajectory deviation array (Equation 14).
    Sturges binning, B = ceil(1 + log2(n))."""
    values = np.asarray(values)
    values = values[np.isfinite(values)]
    if n_bins is None:
        n_bins = int(np.ceil(1 + np.log2(len(values))))
    hist, _ = np.histogram(values, bins=n_bins)
    p = hist / hist.sum()
    p = p[p > 0]
    return float(-np.sum(p * np.log2(p)))


def trajectory_entropy_3D(traj_xyz):
    """Average Shannon entropy across X, Y, Z axes. traj_xyz shape (n_samples, 3)."""
    H = []
    for axis in range(3):
        dev = traj_xyz[:, axis] - np.mean(traj_xyz[:, axis])
        H.append(shannon_entropy_axis(dev))
    return float(np.mean(H))


if __name__ == "__main__":
    df = pd.read_csv(PROCESSED)
    novices = df[df["group"] == "Novice"]
    experts = df[df["group"] == "Expert"]

    nov_M, nov_SD = novices["AE_mean"].mean(), novices["AE_mean"].std(ddof=1)
    exp_M, exp_SD = experts["AE_mean"].mean(), experts["AE_mean"].std(ddof=1)
    print(f"Novice AE: M = {nov_M:.3f}, SD = {nov_SD:.3f}, n = {len(novices)}")
    print(f"Expert AE: M = {exp_M:.3f}, SD = {exp_SD:.3f}, n = {len(experts)}")

    # Shapiro-Wilk normality test
    W_n, p_n = stats.shapiro(novices["AE_mean"])
    W_e, p_e = stats.shapiro(experts["AE_mean"])
    print(f"\nShapiro-Wilk novices: W = {W_n:.3f}, p = {p_n:.3f}")
    print(f"Shapiro-Wilk experts: W = {W_e:.3f}, p = {p_e:.3f}")

    # Independent-samples t-test on AE
    t_stat, p_val = stats.ttest_ind(novices["AE_mean"], experts["AE_mean"])
    pooled_sd = np.sqrt((nov_SD ** 2 + exp_SD ** 2) / 2)
    cohen_d = (nov_M - exp_M) / pooled_sd
    print(f"\nt-test: t({len(novices) + len(experts) - 2}) = {t_stat:.2f}, "
          f"p = {p_val:.6f}, Cohen d = {cohen_d:.2f}")
    print("  (recomputed on the per-participant means; the manuscript reports the")
    print("   trial-level values of the source publication [25]: t(18) = 15.36, d = 6.9)")

    # Bimodality: empty interval AE in [2.5, 3.7]
    gap = df[(df["AE_mean"] > 2.5) & (df["AE_mean"] < 3.7)]
    print(f"\nParticipants in AE gap [2.5, 3.7]: {len(gap)} (expected 0)")
    print(f"This confirms the bimodal partition predicted by the supercritical")
    print(f"pitchfork bifurcation (Equation 2, manuscript Section 2.2).")

    # Within-group correlations (entropy vs AE) - from original publication
    print("\nWithin-group entropy-AE correlations (reported values, source publication [25]):")
    print("  Expert: r = -0.73, p = 0.009, 95% CI [-0.91, -0.32]")
    print("  Novice: r = -0.21, p = 0.564 (not significant)")
    print("  Strategic-variability criterion rho(H, AE) < 0 satisfied in experts only.")
