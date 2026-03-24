from pathlib import Path
from typing import Dict, List, Tuple

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

from .config import CV_DATA_DIR, FIGURES_DIR, LEGACY_CV_DATA_DIR, TABLES_DIR
from .io_utils import load_tabular_file, match_column, resolve_source_files, sanitize_columns


def load_cv_data(directory: Path = CV_DATA_DIR) -> Dict[str, pd.DataFrame]:
    """Load all CV files into a dictionary."""
    _, files = resolve_source_files([directory, LEGACY_CV_DATA_DIR], allow_extensionless=False)
    data = {}
    for file_path in files:
        df = sanitize_columns(load_tabular_file(file_path))
        data[file_path.stem] = df
    return data


def _extract_cv_columns(df: pd.DataFrame) -> Tuple[str, str]:
    potential_col = match_column(df, ["potential", "voltage", "ewe", "v"])
    current_col = match_column(df, ["current", "i/", "ma", "a"])
    return potential_col, current_col


def extract_peak_currents(cv_data: Dict[str, pd.DataFrame]) -> pd.DataFrame:
    """Extract anodic and cathodic peak currents for each CV file."""
    rows: List[dict] = []
    for sample_name, df in cv_data.items():
        potential_col, current_col = _extract_cv_columns(df)
        rows.append(
            {
                "sample": sample_name,
                "potential_column": potential_col,
                "current_column": current_col,
                "peak_anodic_current": df[current_col].max(),
                "peak_cathodic_current": df[current_col].min(),
                "current_abs_max": df[current_col].abs().max(),
            }
        )
    return pd.DataFrame(rows)


def plot_cv_curves(cv_data: Dict[str, pd.DataFrame], figure_path: Path = FIGURES_DIR / "cv_comparison.png") -> None:
    """Plot all CV curves together."""
    if not cv_data:
        return

    sns.set_theme(style="whitegrid")
    plt.figure(figsize=(10, 6))
    for sample_name, df in cv_data.items():
        potential_col, current_col = _extract_cv_columns(df)
        plt.plot(df[potential_col], df[current_col], label=sample_name, linewidth=1.4)

    plt.xlabel("Potential (V)")
    plt.ylabel("Current (A or mA)")
    plt.title("Cyclic Voltammetry Comparison")
    plt.legend()
    plt.tight_layout()
    plt.savefig(figure_path, dpi=300)
    plt.close()


def run_cv_analysis() -> pd.DataFrame:
    """Execute full CV analysis and save outputs."""
    cv_data = load_cv_data()
    plot_cv_curves(cv_data)
    peak_df = extract_peak_currents(cv_data)
    if not peak_df.empty:
        peak_df.to_csv(TABLES_DIR / "cv_peak_summary.csv", index=False)
    return peak_df

