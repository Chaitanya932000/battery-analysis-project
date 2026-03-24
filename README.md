# Battery Electrochemical Data Analysis Project

Author: Chaitanya Rajendra Patil

## Project Overview

This project provides a complete Python workflow to analyze battery electrochemical experiments from Excel datasets. It supports three common test types:

- Cyclic Voltammetry (CV)
- Galvanostatic Charge-Discharge (GCD)
- Electrochemical Impedance Spectroscopy (EIS)

The pipeline automatically reads raw experiment files, generates comparative plots, extracts key metrics, and exports summary tables for reporting.

## Project Structure

```text
battery-analysis-project/
├── data/
│   ├── raw/
│   │   ├── CV/
│   │   ├── GCD/
│   │   └── EIS/
│   └── processed/
├── notebooks/
├── src/
├── outputs/
│   ├── figures/
│   └── tables/
├── README.md
├── requirements.txt
├── main.py
└── dashboard.py
```

## Dataset Description

Place your experiment datasets as Excel files in the following folders:

- `data/raw/CV` for cyclic voltammetry files
- `data/raw/GCD` for charge-discharge files
- `data/raw/EIS` for impedance files

The loader also auto-detects legacy locations if the project folders are empty:

- `D:\chai\CV`
- `D:\chai\GCD` (including extensionless instrument exports)
- EIS files in `D:\chai` matching `*imp*.xlsx`

The code performs flexible column matching (for example, `Potential`, `Voltage`, `Current`, `Frequency`, and impedance column variants) so it can work with typical instrument exports.

## Analysis Workflow

1. **Data Loading**
   - Read all `.xlsx`/`.xls` files from each experiment folder.
2. **CV Analysis**
   - Plot potential vs current curves.
   - Compare scans/files on one graph.
   - Extract anodic and cathodic peak currents.
   - Save `cv_peak_summary.csv`.
3. **GCD Analysis**
   - Standardize columns to `Time_s` and `Voltage_V`.
   - Plot time vs voltage curves for all files.
   - Estimate charge/discharge durations.
   - Save `gcd_summary.csv`.
4. **EIS Analysis**
   - Create Nyquist plots (`Z'` vs `-Z''`).
   - Create Bode magnitude plots (frequency vs `|Z|`).
   - Save `eis_summary.csv`.
5. **Run Summary**
   - Save `analysis_run_summary.csv` with processed record counts.

## Results and Insights

Generated outputs are saved automatically:

- **Figures**: `outputs/figures`
  - `cv_comparison.png`
  - `gcd_comparison.png`
  - `eis_nyquist.png`
  - `eis_bode.png`
- **Tables**: `outputs/tables`
  - `cv_peak_summary.csv`
  - `gcd_summary.csv`
  - `eis_summary.csv`
  - `analysis_run_summary.csv`

These outputs support interpretation of kinetics, charge-discharge behavior, and impedance trends across multiple operating conditions.

## Technologies Used

- Python 3.x
- pandas
- numpy
- matplotlib
- seaborn
- scipy
- openpyxl
- jupyter
- streamlit

## Setup and Usage

1. Open terminal in project root:
   - `D:\chai\battery-analysis-project`
2. Create virtual environment (recommended):
   - `python -m venv .venv`
   - `.venv\Scripts\activate`
3. Install dependencies:
   - `pip install -r requirements.txt`
4. Add raw Excel datasets into their respective folders under `data/raw`.
5. Run complete analysis:
   - `python main.py`
6. Launch notebooks (optional):
   - `jupyter notebook`
7. Launch dashboard:
   - `streamlit run dashboard.py`

## Dashboard Features

- Interactive tabs for CV, GCD, EIS, and Summary.
- Visual comparison of:
  - CV: Potential vs Current curves across files/scan rates
  - GCD: Time vs Voltage curves across files/current densities
  - EIS: Nyquist and Bode plots across impedance files
- Live summary tables shown in-app.
- One-click full pipeline execution from dashboard and table preview.

## GitHub Readiness

- Clean modular source code in `src/`
- Reproducible outputs saved in dedicated folders
- Documented project structure and execution steps
- Notebook workflow for exploratory and report-ready analysis

