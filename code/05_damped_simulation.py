"""
05_damped_simulation.py

Reproduces Section 3.2 of the manuscript and Section S11 of the SI.

Damped logistic-map simulation linking the empirical consecutive-ratio
observations to bifurcation-theoretic predictions through Equations 5 to 7.

    Equation 5: x_{n+1} = r * x_n * (1 - x_n) - gamma * x_n
    Equation 6: R(gamma) ~ delta * exp(-kappa * gamma)
    Equation 7: gamma_empirical = -(1/kappa) * ln(R_obs / delta)

Expected gamma mapping (kappa = 1):
    Running R1 = 1.62 -> gamma = 1.057
    Running R2 = 1.55 -> gamma = 1.101
    Walking R1 = 1.41 -> gamma = 1.197
    Walking R2 = 1.26 -> gamma = 1.310
    phi reference     -> gamma = 1.058
    delta reference   -> gamma = 0.000 (unregulated Feigenbaum cascade)
"""
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

PHI = (1 + np.sqrt(5)) / 2
DELTA = 4.6692016091029
KAPPA = 1.0   # minimal-model convention


def damped_logistic(x, r, gamma):
    """Equation 5 of main manuscript."""
    return r * x * (1.0 - x) - gamma * x


def R_of_gamma(gamma, delta=DELTA, kappa=KAPPA):
    """Equation 6 of main manuscript."""
    return delta * np.exp(-kappa * gamma)


def gamma_of_R(R_obs, delta=DELTA, kappa=KAPPA):
    """Equation 7 of main manuscript."""
    return -(1.0 / kappa) * np.log(R_obs / delta)


if __name__ == "__main__":
    EMPIRICAL = {
        "Running R1": 1.62,
        "Running R2": 1.55,
        "Walking R1": 1.41,
        "Walking R2": 1.26,
        "phi reference":   PHI,
        "delta reference": DELTA,
    }

    print("=== gamma mapping under the damped logistic-map model ===")
    print(f"{'label':<20}  {'R_obs':>7}  {'gamma':>7}")
    print("-" * 40)
    for label, R in EMPIRICAL.items():
        g = gamma_of_R(R)
        print(f"{label:<20}  {R:>7.3f}  {g:>7.3f}")

    # Rank-ordering check
    running_g = np.mean([gamma_of_R(1.62), gamma_of_R(1.55)])
    walking_g = np.mean([gamma_of_R(1.41), gamma_of_R(1.26)])
    print(f"\nMean gamma (running) = {running_g:.3f}")
    print(f"Mean gamma (walking) = {walking_g:.3f}")
    print(f"Rank ordering gamma_running < gamma_walking: {running_g < walking_g}")

    # === Supplementary figure: R(gamma) curve with empirical overlay ===
    gamma_grid = np.linspace(0.0, 2.0, 200)
    R_curve = R_of_gamma(gamma_grid)
    empirical_pts = {
        "Running R1": (gamma_of_R(1.62), 1.62),
        "Running R2": (gamma_of_R(1.55), 1.55),
        "Walking R1": (gamma_of_R(1.41), 1.41),
        "Walking R2": (gamma_of_R(1.26), 1.26),
    }
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.plot(gamma_grid, R_curve, color="#1f3a8a", lw=2,
            label=r"$R(\gamma)=\delta\,e^{-\kappa\gamma}$")
    ax.axhline(PHI,   ls="--", color="#888", label=r"$\varphi$ ($\approx$ 1.618)")
    ax.axhline(DELTA, ls=":",  color="#888", label=r"$\delta$ ($\approx$ 4.669)")
    for label, (gx, ry) in empirical_pts.items():
        ax.scatter([gx], [ry], s=60, zorder=5)
        ax.annotate(label, (gx, ry), xytext=(5, 5), textcoords="offset points", fontsize=9)
    ax.set_xlabel(r"Regulatory damping coefficient $\gamma$")
    ax.set_ylabel(r"Variance-amplification ratio $R$")
    ax.set_yscale("log")
    ax.legend(loc="upper right")
    ax.grid(alpha=0.3)
    plt.tight_layout()
    out = Path(__file__).resolve().parent.parent / "figures" / "fig_damped_simulation.png"
    out.parent.mkdir(exist_ok=True)
    plt.savefig(out, dpi=200)
    print(f"\nSaved supplementary figure: {out}")
