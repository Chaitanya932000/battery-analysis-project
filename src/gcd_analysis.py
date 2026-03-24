from pathlib import Path
from typing import Dict, List, Tuple

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

from .config import FIGURES_DIR, GCD_DATA_DIR, LEGACY_GCD_DATA_DIR, TABLES_DIR
from .io_utils import load_tabular_file, match_column, resolve_source_files, sanitize_columns


def load_gcd_data(directory: Path = GCD_DATA_DIR) -> Dict[str, pd.DataFrame]:
    """Load all GCD files and standardize key columns."""
    _, files = resolve_source_files([directory, LEGACY_GCD_DATA_DIR], allow_extensionless=True)
    data: Dict[str, pd.DataFrame] = {}
    for file_path in files:
        df = sanitize_columns(load_tabular_file(file_path))
        if df.shape[1] < 2:
            continue

        try:
            time_col = match_column(df, ["time", "t/s", "s"])
            voltage_col = match_column(df, ["voltage", "potential", "ewe", "v"])
        except ValueError:
            # Fallback for instrument exports with generic names like "Column 1/2".
            time_col, voltage_col = df.columns[0], df.columns[1]

        renamed = df.rename(columns={time_col: "Time_s", voltage_col: "Voltage_V"}).copy()
        renamed["Time_s"] = pd.to_numeric(renamed["Time_s"], errors="coerce")
        renamed["Voltage_V"] = pd.to_numeric(renamed["Voltage_V"], errors="coerce")
        renamed = renamed.dropna(subset=["Time_s", "Voltage_V"])
        if renamed.empty:
            continue
        data[file_path.stem] = renamed
    return data


def _split_charge_discharge(df: pd.DataFrame) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """
    Approximate split by locating maximum voltage point.
    Charge: start -> max V, Discharge: max V -> end.
    """
    max_idx = df["Voltage_V"].idxmax()
    charge_df = df.loc[:max_idx]
    discharge_df = df.loc[max_idx:]
    return charge_df, discharge_df


def calculate_gcd_summary(gcd_data: Dict[str, pd.DataFrame]) -> pd.DataFrame:
    """Compute charge/discharge duration statistics."""
    rows: List[dict] = []
    for sample_name, df in gcd_data.items():
        charge_df, discharge_df = _split_charge_discharge(df)
        total_duration = df["Time_s"].iloc[-1] - df["Time_s"].iloc[0]
        charge_duration = charge_df["Time_s"].iloc[-1] - charge_df["Time_s"].iloc[0]
        discharge_duration = discharge_df["Time_s"].iloc[-1] - discharge_df["Time_s"].iloc[0]
        rows.append(
            {
                "sample": sample_name,
                "total_duration_s": total_duration,
                "charge_duration_s": charge_duration,
                "discharge_duration_s": discharge_duration,
                "max_voltage_v": df["Voltage_V"].max(),
                "min_voltage_v": df["Voltage_V"].min(),
            }
        )
    return pd.DataFrame(rows)


def plot_gcd_curves(
    gcd_data: Dict[str, pd.DataFrame], figure_path: Path = FIGURES_DIR / "gcd_comparison.png"
) -> None:
    """Plot Time vs Voltage for all GCD files."""
    if not gcd_data:
        return

    sns.set_theme(style="whitegrid")
    plt.figure(figsize=(10, 6))
    for sample_name, df in gcd_data.items():
        plt.plot(df["Time_s"], df["Voltage_V"], label=sample_name, linewidth=1.4)

    plt.xlabel("Time (s)")
    plt.ylabel("Voltage (V)")
    plt.title("Galvanostatic Charge-Discharge Comparison")
    plt.legend()
    plt.tight_layout()
    plt.savefig(figure_path, dpi=300)
    plt.close()


def run_gcd_analysis() -> pd.DataFrame:
    """Execute full GCD analysis and save outputs."""
    gcd_data = load_gcd_data()
    plot_gcd_curves(gcd_data)
    summary_df = calculate_gcd_summary(gcd_data)
    if not summary_df.empty:
        summary_df.to_csv(TABLES_DIR / "gcd_summary.csv", index=False)
    return summary_df

