# Figures

This folder holds the seven main-text figures and the SI figure produced by `code/05_damped_simulation.py`.

## Main-text figures

| File | Source | Description |
|---|---|---|
| `fig_01_canonical_signatures.png` | Manuscript Figure 1 | Three-panel reconstruction of canonical bifurcation signatures (motor-learning, logistic map, HKB) |
| `fig_02_running_amplification.png` | Manuscript Figure 2 | Running variance amplification tracking phi |
| `fig_03_walking_amplification.png` | Manuscript Figure 3 | Walking variance amplification in the [1, phi] band |
| `fig_04_pitchfork_perception.png` | Manuscript Figure 4 | Bimodal pitchfork organisation of perceptual expertise |
| `fig_05_circadian_coordination.png` | Manuscript Figure 5 | Circadian and thermal modulation of bimanual coordination |
| `fig_06_cross_category_synthesis.png` | Manuscript Figure 6 | Cross-category bifurcation integration on the damped logistic-map representation |
| `fig_07_three_category_schematic.png` | Manuscript Figure 7 | Three-category schematic of data sources |

## Generated figures

| File | Source | Description |
|---|---|---|
| `fig_damped_simulation.png` | `code/05_damped_simulation.py` | Supplementary figure: R(gamma) curve with empirical points overlaid |

## Reproduction

Main-text figure source code is not included in this initial release. Each figure can be regenerated from the per-subject data tables in `../data/` using standard plotting tools (matplotlib, seaborn). Plot scripts will be added in a subsequent release.

The supplementary `fig_damped_simulation.png` regenerates automatically when `05_damped_simulation.py` is run.
