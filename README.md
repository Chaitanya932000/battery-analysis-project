# 🔋 Battery Electrochemical Data Analysis

![Python](https://img.shields.io/badge/Python-3.x-3776AB?logo=python&logoColor=white) ![pandas](https://img.shields.io/badge/pandas-150458?logo=pandas&logoColor=white) ![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?logo=streamlit&logoColor=white) ![Jupyter](https://img.shields.io/badge/Jupyter-F37626?logo=jupyter&logoColor=white)

**From a folder of messy lab files to clean charts and summary tables, in one command.**

---

## Why I built this

Battery experiments produce a lot of data, and none of it arrives tidy. Each test type (CV, GCD, EIS) exports in its own format, column names change from one file to the next (`Potential` in one, `Voltage` in another), and some files don't even have an extension.

Doing this by hand meant opening every file, renaming columns, copying data into plots and calculating the same numbers over and over. It was slow, and it was easy to make mistakes.

So I automated it. I wanted one workflow I could point at a folder of raw files and get back results I could trust and put straight into a report. That way I could spend my time on **what the results mean**, not on reformatting spreadsheets.

## What it does

```
raw Excel files  →  load & match columns  →  clean & standardise  →  analyse  →  charts + CSV tables + dashboard
```

| Test | What you get |
|---|---|
| **Cyclic Voltammetry (CV)** | Potential vs current curves compared across files, plus anodic and cathodic peak currents |
| **Charge-Discharge (GCD)** | Voltage vs time curves, with charge and discharge durations estimated automatically |
| **Impedance (EIS)** | Nyquist and Bode plots, plus an impedance summary |

The trickiest part was making the loader **forgiving**. It recognises many different column-name variants and handles inconsistent instrument exports, so new data usually just works without editing any code.

## The dashboard

`streamlit run dashboard.py` opens an interactive app with tabs for **CV, GCD, EIS and Summary**. You can compare curves across files, check the summary tables, and re-run the whole pipeline with one click, no code needed.

## Try it yourself

```bash
git clone https://github.com/Chaitanya932000/battery-analysis-project.git
cd battery-analysis-project

python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
```

1. Put your Excel exports in `data/raw/CV`, `data/raw/GCD` and `data/raw/EIS`
2. Run everything: `python main.py`
3. Or explore interactively: `streamlit run dashboard.py`
4. Want to see each step? Open the notebooks in `notebooks/` (`01_data_loading` → `05_summary`)

Results are saved to `outputs/figures/` (CV, GCD, Nyquist and Bode plots) and `outputs/tables/` (peak, GCD, EIS and run summaries as CSV).

## How it's organised

```
battery-analysis-project/
├── src/
│   ├── io_utils.py        # finds files and matches messy column names
│   ├── cv_analysis.py     # CV curves + peak currents
│   ├── gcd_analysis.py    # GCD curves + durations
│   ├── eis_analysis.py    # Nyquist / Bode + summaries
│   ├── pipeline.py        # runs everything in order
│   └── config.py          # paths and settings
├── notebooks/             # step-by-step walkthrough
├── main.py                # one-command run
├── dashboard.py           # Streamlit app
└── requirements.txt
```

## What I took away from it

- **Real data is never clean.** Writing flexible loaders taught me more about data quality than any tutorial.
- **Structure pays off.** Splitting the code into small modules made it easy to add the dashboard later without rewriting anything.
- **Automation builds trust.** When every file goes through the same steps, results are consistent and easy to reproduce.
- It connected my physics background with practical data work, which is exactly where I want to keep going.

## Built with

Python · pandas · NumPy · SciPy · Matplotlib · Seaborn · openpyxl · Jupyter · Streamlit

---

<sub>Made by **Chaitanya Patil** · [LinkedIn](https://www.linkedin.com/in/chaitanya932000) · [More of my work](https://github.com/Chaitanya932000)</sub>
