from pathlib import Path
from typing import Iterable, List, Tuple

import pandas as pd


SUPPORTED_EXTENSIONS = {".xlsx", ".xls"}


def list_excel_files(directory: Path) -> List[Path]:
    """Return all Excel files in a directory, sorted by name."""
    if not directory.exists():
        return []
    return sorted(
        [p for p in directory.iterdir() if p.is_file() and p.suffix.lower() in SUPPORTED_EXTENSIONS]
    )


def load_excel_file(path: Path) -> pd.DataFrame:
    """Load first sheet from an Excel file."""
    return pd.read_excel(path, engine="openpyxl")


def load_tabular_file(path: Path) -> pd.DataFrame:
    """
    Load tabular experiment files robustly.
    Supports normal Excel extensions and extensionless Excel exports.
    """
    # Try as Excel first (works even for some extensionless files).
    try:
        return pd.read_excel(path, engine="openpyxl")
    except Exception:
        pass

    try:
        return pd.read_excel(path)
    except Exception:
        pass

    # Fallback to delimited text formats.
    for sep in [None, "\t", ",", ";", r"\s+"]:
        try:
            return pd.read_csv(path, sep=sep, engine="python")
        except Exception:
            continue

    raise ValueError(f"Unsupported or unreadable tabular file: {path}")


def list_tabular_files(directory: Path, allow_extensionless: bool = False) -> List[Path]:
    """Return spreadsheet-like files from a directory."""
    if not directory.exists():
        return []

    files: List[Path] = []
    for file_path in directory.iterdir():
        if not file_path.is_file():
            continue
        suffix = file_path.suffix.lower()
        if suffix in SUPPORTED_EXTENSIONS:
            files.append(file_path)
            continue
        if allow_extensionless and suffix == "":
            files.append(file_path)
    return sorted(files)


def resolve_source_files(
    candidate_dirs: Iterable[Path],
    allow_extensionless: bool = False,
) -> Tuple[Path | None, List[Path]]:
    """
    Return first candidate directory containing valid files and the files list.
    """
    for directory in candidate_dirs:
        files = list_tabular_files(directory, allow_extensionless=allow_extensionless)
        if files:
            return directory, files
    return None, []


def sanitize_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Normalize column names for easier matching."""
    df = df.copy()
    df.columns = [str(c).strip() for c in df.columns]
    return df


def match_column(df: pd.DataFrame, keywords: List[str]) -> str:
    """
    Match a column by keyword priority.
    Returns the first column that contains any keyword (case-insensitive).
    """
    lowered = {c: c.lower() for c in df.columns}
    for key in keywords:
        key_lower = key.lower()
        for col, col_lower in lowered.items():
            if key_lower in col_lower:
                return col
    raise ValueError(f"Could not find required column. Available columns: {list(df.columns)}")

