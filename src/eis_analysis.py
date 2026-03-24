from pathlib import Path
from typing import Dict

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

from .config import EIS_DATA_DIR, FIGURES_DIR, LEGACY_EIS_DATA_DIR, LEGACY_ROOT, TABLES_DIR
from .io_utils import list_tabular_files, load_tabular_file, match_column, resolve_source_files, sanitize_columns


def load_eis_data(directory: Path = EIS_DATA_DIR) -> Dict[str, pd.DataFrame]:
    """Load all EIS files."""
    _, files = resolve_source_files([directory, LEGACY_EIS_DATA_DIR], allow_extensionless=False)
    # Additional fallback: some setups store EIS files directly in legacy root (e.g., "imp.xlsx").
    if not files and LEGACY_ROOT.exists():
        files = [p for p in list_tabular_files(LEGACY_ROOT) if "imp" in p.stem.lower()]

    data = {}
    for file_path in files:
        df = sanitize_columns(load_tabular_file(file_path))
        data[file_path.stem] = df
    return data


def _extract_eis_columns(df: pd.DataFrame) -> tuple[str, str, str]:
    z_real_col = match_column(df, ["z'", "real", "re(z)", "zreal"])
    z_imag_col = match_column(df, ["z''", "imag", "im(z)", "zimag"])
    freq_col = match_column(df, ["freq", "frequency", "hz"])
    return z_real_col, z_imag_col, freq_col


def plot_nyquist(eis_data: Dict[str, pd.DataFrame], figure_path: Path = FIGURES_DIR / "eis_nyquist.png") -> None:
    """Plot Nyquist curves (Z' vs -Z'')."""
    if not eis_data:
        return

    sns.set_theme(style="whitegrid")
    plt.figure(figsize=(8, 6))
    for sample_name, df in eis_data.items():
        z_real_col, z_imag_col, _ = _extract_eis_columns(df)
        plt.plot(df[z_real_col], -df[z_imag_col], marker="o", linestyle="-", markersize=3, label=sample_name)

    plt.xlabel("Z' (Ohm)")
    plt.ylabel("-Z'' (Ohm)")
    plt.title("Nyquist Plot Comparison")
    plt.legend()
    plt.tight_layout()
    plt.savefig(figure_path, dpi=300)
    plt.close()


def plot_bode(eis_data: Dict[str, pd.DataFrame], figure_path: Path = FIGURES_DIR / "eis_bode.png") -> None:
    """Plot Bode magnitude curves (Frequency vs |Z|)."""
    if not eis_data:
        return

    sns.set_theme(style="whitegrid")
    plt.figure(figsize=(8, 6))
    for sample_name, df in eis_data.items():
        z_real_col, z_imag_col, freq_col = _extract_eis_columns(df)
        z_mag = np.sqrt(df[z_real_col] ** 2 + df[z_imag_col] ** 2)
        plt.semilogx(df[freq_col], z_mag, marker="o", linestyle="-", markersize=3, label=sample_name)

    plt.xlabel("Frequency (Hz)")
    plt.ylabel("|Z| (Ohm)")
    plt.title("Bode Plot Comparison")
    plt.legend()
    plt.tight_layout()
    plt.savefig(figure_path, dpi=300)
    plt.close()


def create_eis_summary(eis_data: Dict[str, pd.DataFrame]) -> pd.DataFrame:
    """Create simple EIS summary statistics."""
    rows = []
    for sample_name, df in eis_data.items():
        z_real_col, z_imag_col, freq_col = _extract_eis_columns(df)
        z_mag = np.sqrt(df[z_real_col] ** 2 + df[z_imag_col] ** 2)
        rows.append(
            {
                "sample": sample_name,
                "frequency_min_hz": df[freq_col].min(),
                "frequency_max_hz": df[freq_col].max(),
                "z_real_min_ohm": df[z_real_col].min(),
                "z_real_max_ohm": df[z_real_col].max(),
                "z_imag_min_ohm": df[z_imag_col].min(),
                "z_imag_max_ohm": df[z_imag_col].max(),
                "z_magnitude_max_ohm": z_mag.max(),
            }
        )
    return pd.DataFrame(rows)


def run_eis_analysis() -> pd.DataFrame:
    """Execute full EIS analysis and save outputs."""
    eis_data = load_eis_data()
    plot_nyquist(eis_data)
    plot_bode(eis_data)
    summary_df = create_eis_summary(eis_data)
    if not summary_df.empty:
        summary_df.to_csv(TABLES_DIR / "eis_summary.csv", index=False)
    return summary_df

