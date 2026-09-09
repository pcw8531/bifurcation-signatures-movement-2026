# Data

This folder contains the processed per-subject and per-participant data tables that exactly reproduce SI Tables S1 through S7 of the manuscript. All values are taken from the original publications and licensed CC BY 4.0 (see ../LICENSE-DATA).

## Files

| File | SI Table | Source | n |
|---|---|---|---|
| `running_per_subject.csv` | S1 | Fukuchi et al. 2017 PeerJ, figshare 10.6084/m9.figshare.4543435.v4 | 28 |
| `walking_per_subject_values.csv` | S2 (per-subject values) | Riglet et al. 2024 Sci. Data, figshare 10.6084/m9.figshare.24296217, computed by 02_walking_pipeline.py | 29 |
| `walking_per_subject.csv` | S2 (population summary) | as above | 29 |
| `perception_per_participant.csv` | S3 | Park 2026 Inf. Process. Manag. (reference [25]), Appendix D | 20 |
| `coordination_baseline.csv` | S4 | Park 2026 J. R. Soc. Interface (reference [26]), Table S1a | 8 (Group 1) |
| `coordination_heat.csv` | S5 | Park 2026 J. R. Soc. Interface, Table S2 | 8 (Group 2) |
| `coordination_cold.csv` | S6 | Park 2026 J. R. Soc. Interface, Table S3 | 8 (Group 2) |
| `walking_sensitivity.csv` | S7 | computed by 02_walking_pipeline.py from Riglet archive | 29 |

## Column conventions

**running_per_subject.csv**
subject, var_2.5, var_3.5, var_4.5, R1, R2
Variances in mm², ratios dimensionless. `R1 = var_3.5 / var_2.5`, `R2 = var_4.5 / var_3.5`.

**walking_per_subject_values.csv**
subject, var_Slow, var_Comfortable, var_Fast, R1, R2
Same conventions as running; variance of the per-cycle peak-to-peak vertical pelvic excursion in mm².

**walking_per_subject.csv**
statistic, R1_slow_to_comfortable, R2_comfortable_to_fast
Population summary (median, geometric mean, IQR, Wilcoxon p-values, n) of the per-subject file above.

**perception_per_participant.csv**
participant, group, AE_mean, AE_sd
`group` is "Expert" or "Novice". AE in centimetres on the 20 × 20 cm grid; per-participant mean and within-participant SD over 10 trials. The trajectory-entropy values used for the within-group correlations are reported in the source publication and are not part of this table.

**coordination_baseline.csv**
participant, phase_0500, phase_1200, phase_1700, phase_0000
Shannon entropy H(φ) in bits at each circadian phase.

**coordination_heat.csv** and **coordination_cold.csv**
participant, normal_0500, normal_1700, heat_0500, heat_1700
participant, normal_0500, normal_1700, cold_0500, cold_1700
Z-scored entropy values, normalised within-participant.

**walking_sensitivity.csv**
variable, R1_median, R1_p_vs_phi, R1_p_vs_delta, R2_median, R2_p_vs_phi, R2_p_vs_delta
Variable-dependence sensitivity for four kinematic state variables.

## Reproduction

To regenerate any of these tables from raw archive data, run the corresponding pipeline in `../code/`:

- `01_running_pipeline.py` produces `running_per_subject.csv` from the Fukuchi figshare archive.
- `02_walking_pipeline.py` produces `walking_per_subject_values.csv`, its summary `walking_per_subject.csv`, and `walking_sensitivity.csv` from the Riglet figshare archive; without the archive it reads `walking_per_subject_values.csv` and recomputes the population statistics.
- `03_perception_pipeline.py` reads `perception_per_participant.csv` directly (values from [25], Appendix D).
- `04_coordination_pipeline.py` reads `coordination_baseline.csv`, `coordination_heat.csv`, and `coordination_cold.csv` directly (values from [26], Tables S1a, S2, S3).

Group means and effect magnitudes recompute exactly from these tables. The inferential statistics quoted in the manuscript for perceptual expertise and elementary coordination (t, F, p, d) are the published values of [25] and [26], computed on trial-level data that those studies hold.
