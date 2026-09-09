# bifurcation-signatures-movement-2026

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![License: CC BY 4.0](https://img.shields.io/badge/Data%20License-CC%20BY%204.0-lightgrey.svg)](LICENSE-DATA)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)

Data and code for: **Convergent bifurcation signatures in movement: a systemic analysis across locomotion, perceptual expertise, and elementary coordination**

Revised reproducibility package, September 2026. Archived release: Zenodo DOI to be inserted after the v1.1.0 release.

## Overview

This repository contains the complete reproducibility package for the manuscript. It applies a systemic variance-modulation analysis to four publicly available datasets that cover three categories of movement, and tests whether a bifurcation-precursor signature appears as a shared pattern across categories.

- **Locomotion (running, n = 28)**: consecutive-speed variance ratios tested against the golden ratio φ and the Feigenbaum constant δ.
- **Locomotion (walking, n = 29)**: same procedure on an independent walking dataset.
- **Perceptual expertise (n = 20)**: bimodal partition of absolute-error means across experts and novices, mapped to a supercritical pitchfork normal form.
- **Elementary coordination (n = 16)**: bimanual relative-phase Shannon entropy under circadian and thermal modulation, with a 2 × 2 repeated-measures ANOVA and simple-effects decomposition.

A damped extension of the logistic map (Equations 5 to 7 of the manuscript) reconciles the category-specific signatures within a single account.

## Repository structure

```
bifurcation-signatures-movement-2026/
├── README.md                          this file
├── LICENSE                            MIT for code
├── LICENSE-DATA                       CC BY 4.0 for data tables and figures
├── CITATION.cff                       machine-readable citation metadata
├── requirements.txt                   pinned Python dependencies (pip)
├── environment.yml                    conda environment specification
├── .gitignore                         standard Python ignores
│
├── code/                              standalone Python pipelines
│   ├── 01_running_pipeline.py         Section S2 of SI, Section 2.1.1 of paper
│   ├── 02_walking_pipeline.py         Section S3 of SI, Section 2.1.2 of paper
│   ├── 03_perception_pipeline.py      Section S4 of SI, Section 2.2 of paper
│   ├── 04_coordination_pipeline.py    Section S5 of SI, Section 2.3 of paper
│   └── 05_damped_simulation.py        Section S11 of SI, Section 3.2 of paper
│
├── notebooks/                         Jupyter master replication
│   └── 00_master_replication.ipynb    end-to-end run of all four pipelines
│
├── data/                              processed per-subject tables (Tables S1-S7)
│   ├── README.md                      data source documentation
│   ├── running_per_subject.csv        SI Table S1 (n = 28)
│   ├── walking_per_subject_values.csv SI Table S2, per-subject values (n = 29)
│   ├── walking_per_subject.csv        SI Table S2, population summary
│   ├── perception_per_participant.csv SI Table S3 (n = 20)
│   ├── coordination_baseline.csv      SI Table S4 (Group 1, n = 8)
│   ├── coordination_heat.csv          SI Table S5 (Group 2, n = 8)
│   ├── coordination_cold.csv          SI Table S6 (Group 2, n = 8)
│   └── walking_sensitivity.csv        SI Table S7
│
└── figures/                           figure documentation
    ├── README.md                      figures are provided with the manuscript; data sources in data/README.md
    └── fig_damped_simulation.png      supplementary figure written by 05_damped_simulation.py
```

## Data sources

All four primary datasets are previously published and openly accessible. This repository contains the processed per-subject tables reproduced verbatim from the original publications. To re-run the pipelines from raw data, the original archives are at:

| Dataset | Reference | Access |
|---|---|---|
| Running biomechanics, n = 28 | Fukuchi et al. (2017) PeerJ | figshare [10.6084/m9.figshare.4543435.v4](https://doi.org/10.6084/m9.figshare.4543435.v4) |
| Walking 3D motion capture, n = 29 | Riglet et al. (2024) Scientific Data | figshare [10.6084/m9.figshare.24296217](https://doi.org/10.6084/m9.figshare.24296217) |
| Haptic perception, n = 20 | Park (2026) Inf. Process. Manag., reference [25] of the manuscript | https://github.com/pcw8531/Dimensional-motor-expertise |
| Bimanual coordination, n = 16 | Park (2026) J. R. Soc. Interface, reference [26] | Zenodo [10.5281/zenodo.19201270](https://doi.org/10.5281/zenodo.19201270) and https://github.com/pcw8531/thermodynamic-motor-control |

## Reproduction

### Environment setup

With pip:

```bash
python -m venv .venv
source .venv/bin/activate    # on Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

With conda:

```bash
conda env create -f environment.yml
conda activate bifurcation-movement
```

### Running the pipelines

Each pipeline is standalone and corresponds to one Section of the manuscript and one Section of the SI:

```bash
python code/01_running_pipeline.py        # reproduces Section 2.1.1 statistics
python code/02_walking_pipeline.py        # reproduces Section 2.1.2 statistics
python code/03_perception_pipeline.py     # reproduces Section 2.2 statistics
python code/04_coordination_pipeline.py   # reproduces Section 2.3 statistics
python code/05_damped_simulation.py       # reproduces Section 3.2 γ mapping
```

For the locomotion pipelines (01 and 02), point the `DATA1` / `DATA2` paths in the script to local copies of the figshare archives to recompute from raw marker data; without the archives they read the per-subject tables in `data/` (Tables S1 and S2) and reproduce the population statistics from them. Pipelines 03 and 04 read the per-participant tables in `data/` directly.

For a single end-to-end run, open `notebooks/00_master_replication.ipynb` in JupyterLab.

### Expected outputs

- `01_running_pipeline.py`: R₁ median = 1.623, R₂ median = 1.546, p vs φ = 0.295 (R₁) and 0.020 (R₂; 0.022 with φ rounded to 1.618 as in the manuscript), p vs δ < 0.0001 (both).
- `02_walking_pipeline.py`: R₁ median = 1.409, R₂ median = 1.256, geometric means 1.380 and 1.183, p vs φ = 0.031 / 0.001, p vs δ < 0.0001.
- `03_perception_pipeline.py`: novice M = 4.215, expert M = 2.130, no participant in the AE gap (2.5, 3.7). Recomputed on the ten per-participant means per group, the t-test gives t(18) = 14.44, d = 6.46; the manuscript reports the values of the source publication [25], computed on the trial-level data of that study, t(18) = 15.36, d = 6.9. The within-group entropy–AE correlations are printed as reported in [25], because the trajectory-entropy values are not part of the shipped table.
- `04_coordination_pipeline.py`: baseline means 05:00 = 5.246, 12:00 = 5.010, 17:00 = 4.544, 00:00 = 5.200; simple-effect magnitudes heat +0.154 / −0.645 and cold +0.203 / −0.668 z-units at 05:00 / 17:00. The ANOVA F values and simple-effect t values in the manuscript are those of the source publication [26], computed on the trial-level data (six trials per participant and cell); the script prints them as reported values next to the paired t values recomputed on the per-participant cell means.
- `05_damped_simulation.py`: γ mapping for the four locomotion ratios under κ = 1, running 1.06 and 1.10, walking 1.20 and 1.31; writes `figures/fig_damped_simulation.png`.

What recomputes from the shipped tables and what is quoted: every locomotion statistic (Sections 2.1.1 and 2.1.2) and every group mean and effect magnitude in Sections 2.2 and 2.3 are recomputed here. The inferential statistics of Sections 2.2 and 2.3 (t, F, p, d) are the published values of [25] and [26], whose trial-level data are held by those studies; the two scripts label them as such in their output.

## Citation

If you use this code or data, please cite the manuscript and this repository.

```bibtex
@article{park2026bifurcation,
  author  = {Park, Chulwook},
  title   = {Convergent bifurcation signatures in movement: a systemic analysis across locomotion, perceptual expertise, and elementary coordination},
  year    = {2026},
  note    = {manuscript under review},
  doi     = {[DOI on publication]}
}

@software{park2026bifurcation_code,
  author    = {Park, Chulwook},
  title     = {bifurcation-signatures-movement-2026: Reproducibility package},
  year      = {2026},
  publisher = {Zenodo},
  version   = {1.1.0},
  doi       = {[Zenodo DOI, inserted after the v1.1.0 release]},
  url       = {https://github.com/pcw8531/bifurcation-signatures-movement-2026}
}
```

A `CITATION.cff` file is included so GitHub displays a "Cite this repository" button.

## License

- **Code** (everything in `code/`, `notebooks/`, and `figures/`) is released under the **MIT License**. See [LICENSE](LICENSE).
- **Data tables** (everything in `data/`), the **README**, and the **figure files** are released under **Creative Commons Attribution 4.0 International (CC BY 4.0)**. See [LICENSE-DATA](LICENSE-DATA).

## Contact

Chulwook Park · BK21 FOUR, Department of Physical Education, Seoul National University · ORCID [0000-0001-8714-5760](https://orcid.org/0000-0001-8714-5760)
GitHub: [@pcw8531](https://github.com/pcw8531)
