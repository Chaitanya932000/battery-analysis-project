from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import streamlit as st

from src.config import (
    CV_DATA_DIR,
    EIS_DATA_DIR,
    GCD_DATA_DIR,
    LEGACY_CV_DATA_DIR,
    LEGACY_GCD_DATA_DIR,
    LEGACY_ROOT,
    TABLES_DIR,
    ensure_output_dirs,
)
from src.cv_analysis import extract_peak_currents, load_cv_data
from src.eis_analysis import create_eis_summary, load_eis_data
from src.gcd_analysis import calculate_gcd_summary, load_gcd_data
from src.pipeline import run_full_analysis


st.set_page_config(page_title="Battery Electrochemical Dashboard", layout="wide")


def _show_empty_message(test_name: str) -> None:
    st.warning(
        f"No readable {test_name} files detected. "
        "Dashboard searches project raw folders and legacy D:\\chai folders automatically."
    )
    st.caption(
        "Searched paths: "
        f"`{CV_DATA_DIR}`, `{GCD_DATA_DIR}`, `{EIS_DATA_DIR}`, "
        f"`{LEGACY_CV_DATA_DIR}`, `{LEGACY_GCD_DATA_DIR}`, `{LEGACY_ROOT}`"
    )


@st.cache_data(show_spinner=False)
def get_cv_data() -> dict[str, pd.DataFrame]:
    return load_cv_data()


@st.cache_data(show_spinner=False)
def get_gcd_data() -> dict[str, pd.DataFrame]:
    return load_gcd_data()


@st.cache_data(show_spinner=False)
def get_eis_data() -> dict[str, pd.DataFrame]:
    return load_eis_data()


def _match_col(columns: list[str], keywords: list[str]) -> str | None:
    lowered = {c: c.lower() for c in columns}
    for key in keywords:
        key_lower = key.lower()
        for col, low in lowered.items():
            if key_lower in low:
                return col
    return None


def render_cv_tab() -> None:
    st.subheader("Cyclic Voltammetry (CV)")
    cv_data = get_cv_data()
    if not cv_data:
        _show_empty_message("CV")
        return
    st.caption(f"Loaded {len(cv_data)} CV files")

    fig, ax = plt.subplots(figsize=(9, 5))
    for name, df in cv_data.items():
        cols = list(df.columns)
        potential = _match_col(cols, ["potential", "voltage", "ewe", "v"])
        current = _match_col(cols, ["current", "i/", "ma", "a"])
        if potential and current:
            ax.plot(df[potential], df[current], label=name, linewidth=1.4)
    ax.set_xlabel("Potential (V)")
    ax.set_ylabel("Current (A or mA)")
    ax.set_title("Potential vs Current (scan rate/file comparison)")
    ax.grid(alpha=0.25)
    ax.legend(fontsize=8)
    st.pyplot(fig, clear_figure=True)

    peak_df = extract_peak_currents(cv_data)
    st.markdown("**Peak Current Summary**")
    st.dataframe(peak_df, use_container_width=True)


def render_gcd_tab() -> None:
    st.subheader("Galvanostatic Charge-Discharge (GCD)")
    gcd_data = get_gcd_data()
    if not gcd_data:
        _show_empty_message("GCD")
        return
    st.caption(f"Loaded {len(gcd_data)} GCD files")

    fig, ax = plt.subplots(figsize=(9, 5))
    for name, df in gcd_data.items():
        if {"Time_s", "Voltage_V"}.issubset(df.columns):
            ax.plot(df["Time_s"], df["Voltage_V"], label=name, linewidth=1.4)
    ax.set_xlabel("Time (s)")
    ax.set_ylabel("Voltage (V)")
    ax.set_title("Time vs Voltage (current density/file comparison)")
    ax.grid(alpha=0.25)
    ax.legend(fontsize=8)
    st.pyplot(fig, clear_figure=True)

    summary_df = calculate_gcd_summary(gcd_data)
    st.markdown("**Charge/Discharge Summary**")
    st.dataframe(summary_df, use_container_width=True)


def render_eis_tab() -> None:
    st.subheader("Electrochemical Impedance Spectroscopy (EIS)")
    eis_data = get_eis_data()
    if not eis_data:
        _show_empty_message("EIS")
        return
    st.caption(f"Loaded {len(eis_data)} EIS files")

    nyq_fig, nyq_ax = plt.subplots(figsize=(8, 5))
    for name, df in eis_data.items():
        cols = list(df.columns)
        z_real = _match_col(cols, ["z'", "real", "re(z)", "zreal"])
        z_imag = _match_col(cols, ["z''", "imag", "im(z)", "zimag"])
        if z_real and z_imag:
            nyq_ax.plot(df[z_real], -df[z_imag], marker="o", markersize=3, linewidth=1.2, label=name)
    nyq_ax.set_xlabel("Z' (Ohm)")
    nyq_ax.set_ylabel("-Z'' (Ohm)")
    nyq_ax.set_title("Nyquist Plot")
    nyq_ax.grid(alpha=0.25)
    nyq_ax.legend(fontsize=8)
    st.pyplot(nyq_fig, clear_figure=True)

    bode_fig, bode_ax = plt.subplots(figsize=(8, 5))
    for name, df in eis_data.items():
        cols = list(df.columns)
        z_real = _match_col(cols, ["z'", "real", "re(z)", "zreal"])
        z_imag = _match_col(cols, ["z''", "imag", "im(z)", "zimag"])
        freq = _match_col(cols, ["freq", "frequency", "hz"])
        if z_real and z_imag and freq:
            z_mag = np.sqrt(df[z_real] ** 2 + df[z_imag] ** 2)
            bode_ax.semilogx(df[freq], z_mag, marker="o", markersize=3, linewidth=1.2, label=name)
    bode_ax.set_xlabel("Frequency (Hz)")
    bode_ax.set_ylabel("|Z| (Ohm)")
    bode_ax.set_title("Bode Plot")
    bode_ax.grid(alpha=0.25)
    bode_ax.legend(fontsize=8)
    st.pyplot(bode_fig, clear_figure=True)

    summary_df = create_eis_summary(eis_data)
    st.markdown("**Impedance Summary**")
    st.dataframe(summary_df, use_container_width=True)


def render_summary_tab() -> None:
    st.subheader("Outputs and Run Summary")
    st.write("Use this section to generate and review saved figures/tables.")

    if st.button("Run Full Analysis Pipeline", type="primary"):
        ensure_output_dirs()
        run_full_analysis()
        st.cache_data.clear()
        st.success("Analysis completed. Outputs updated in outputs/figures and outputs/tables.")

    table_files = sorted(TABLES_DIR.glob("*.csv"))
    if not table_files:
        st.info("No summary tables found yet. Click the run button above.")
        return

    chosen = st.selectbox("Select summary table", [p.name for p in table_files])
    selected_path = TABLES_DIR / chosen
    st.markdown(f"**Preview: `{selected_path}`**")
    st.dataframe(pd.read_csv(selected_path), use_container_width=True)


def main() -> None:
    st.title("Battery Electrochemical Experiments Dashboard")
    st.caption("Author: Chaitanya Rajendra Patil")
    st.markdown(
        "Interactive dashboard for CV, GCD, and EIS datasets with automatic summaries and output generation."
    )
    with st.sidebar:
        st.markdown("### Data Status")
        st.write(f"CV files: {len(get_cv_data())}")
        st.write(f"GCD files: {len(get_gcd_data())}")
        st.write(f"EIS files: {len(get_eis_data())}")
        if st.button("Refresh Data Cache"):
            st.cache_data.clear()
            st.success("Cache cleared. Data will reload on next view.")

    tab_cv, tab_gcd, tab_eis, tab_summary = st.tabs(["CV", "GCD", "EIS", "Summary"])
    with tab_cv:
        render_cv_tab()
    with tab_gcd:
        render_gcd_tab()
    with tab_eis:
        render_eis_tab()
    with tab_summary:
        render_summary_tab()


if __name__ == "__main__":
    main()

