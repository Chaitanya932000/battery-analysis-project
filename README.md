# Battery Electrochemical Data Analysis

![Python](https://img.shields.io/badge/Python-3.x-blue) ![pandas](https://img.shields.io/badge/pandas-data%20wrangling-150458) ![Streamlit](https://img.shields.io/badge/Streamlit-dashboard-FF4B4B)

An end-to-end Python pipeline that turns raw battery lab exports into clean data, comparison plots and report-ready summary tables, with an interactive Streamlit dashboard on top.

**Author:** Chaitanya Rajendra Patil

## Overview

Electrochemical lab instruments export data in inconsistent formats, with column names, units and file types that change between runs. Processing them by hand is slow and error-prone. This project automates the whole workflow in one run for three common test types:

- **Cyclic Voltammetry (CV)**
- **Galvanostatic Charge-Discharge (GCD)**
- **Electrochemical Impedance Spectroscopy (EIS)**

## Key features

- Automatic loading of every `.xlsx` / `.xls` file per test type
- Flexible column matching (e.g. Potential/Voltage, Current, Frequency, Z′/Z″ variants) so it works with typical instrument exports
- Data cleaning and standardisation (e.g. GCD columns normalised to `Time_s`, `Voltage_V`)
- Automated plots: CV curves, GCD curves, Nyquist and Bode plots
- Metric extraction: anodic/cathodic peak currents, charge/discharge durations, impedance summaries
- CSV summary tables for reporting
- Streamlit dashboard with tabs for CV, GCD, EIS and Summary, plus one-click pipeline runs

## Skills demonstrated

Data cleaning and wrangling (pandas, NumPy) · scientific analysis (SciPy) · data visualisation (Matplotlib, Seaborn) · dashboarding (Streamlit) · modular, reusable Python code · exploratory analysis in Jupyter

## Project structure

```
battery-analysis-project/
├── src/
│   ├── config.py          # paths and settings
│   ├── io_utils.py        # file loading and column matching
│   ├── cv_analysis.py     # CV plots and peak extraction
│   ├── gcd_analysis.py    # GCD plots and durations
│   ├── eis_analysis.py    # Nyquist / Bode plots and summaries
│   └── pipeline.py        # runs the full workflow
├── notebooks/             # 01_data_loading → 05_summary
├── data/raw/{CV,GCD,EIS}/ # put your Excel exports here
├── outputs/               # generated figures and tables (created on run)
├── main.py                # run the full pipeline
├── dashboard.py           # Streamlit dashboard
└── requirements.txt
```

## Getting started

```bash
git clone https://github.com/Chaitanya932000/battery-analysis-project.git
cd battery-analysis-project

python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate

pip install -r requirements.txt
```

1. Put your Excel exports into `data/raw/CV`, `data/raw/GCD` and `data/raw/EIS`.
2. Run the full analysis:
   ```bash
   python main.py
   ```
3. Or open the interactive dashboard:
   ```bash
   streamlit run dashboard.py
   ```
4. Optional: explore step by step in the `notebooks/` folder with `jupyter notebook`.

## Outputs

| Type | Files (saved to `outputs/`) |
|---|---|
| Figures | `cv_comparison.png`, `gcd_comparison.png`, `eis_nyquist.png`, `eis_bode.png` |
| Tables | `cv_peak_summary.csv`, `gcd_summary.csv`, `eis_summary.csv`, `analysis_run_summary.csv` |

These outputs make it quick to compare reaction kinetics, charge-discharge behaviour and impedance trends across samples and operating conditions.

## What I learned

- Pre-processing and standardising datasets from different instrument exports
- Generating scientific plots programmatically
- Extracting KPIs into clean, report-ready CSV tables
- Building a repeatable workflow that can be reused for future experiments

## Tech stack

Python · pandas · NumPy · SciPy · Matplotlib · Seaborn · openpyxl · Jupyter · Streamlit
