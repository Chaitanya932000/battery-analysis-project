import pandas as pd

from .config import TABLES_DIR, ensure_output_dirs
from .cv_analysis import run_cv_analysis
from .eis_analysis import run_eis_analysis
from .gcd_analysis import run_gcd_analysis


def run_full_analysis() -> None:
    """Run CV, GCD and EIS analysis pipelines and save outputs."""
    ensure_output_dirs()

    cv_summary = run_cv_analysis()
    gcd_summary = run_gcd_analysis()
    eis_summary = run_eis_analysis()

    combined = {
        "cv_rows": len(cv_summary),
        "gcd_rows": len(gcd_summary),
        "eis_rows": len(eis_summary),
    }
    pd.DataFrame([combined]).to_csv(TABLES_DIR / "analysis_run_summary.csv", index=False)

