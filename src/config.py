from pathlib import Path

# Project paths
PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_ROOT = PROJECT_ROOT / "data"
RAW_DATA_ROOT = DATA_ROOT / "raw"
PROCESSED_DATA_ROOT = DATA_ROOT / "processed"

CV_DATA_DIR = RAW_DATA_ROOT / "CV"
GCD_DATA_DIR = RAW_DATA_ROOT / "GCD"
EIS_DATA_DIR = RAW_DATA_ROOT / "EIS"

# Legacy data locations (auto-detected if project raw folders are empty)
LEGACY_ROOT = Path("D:/chai")
LEGACY_CV_DATA_DIR = LEGACY_ROOT / "CV"
LEGACY_GCD_DATA_DIR = LEGACY_ROOT / "GCD"
LEGACY_EIS_DATA_DIR = LEGACY_ROOT / "EIS"

OUTPUT_ROOT = PROJECT_ROOT / "outputs"
FIGURES_DIR = OUTPUT_ROOT / "figures"
TABLES_DIR = OUTPUT_ROOT / "tables"


def ensure_output_dirs() -> None:
    """Create output directories if missing."""
    FIGURES_DIR.mkdir(parents=True, exist_ok=True)
    TABLES_DIR.mkdir(parents=True, exist_ok=True)
    PROCESSED_DATA_ROOT.mkdir(parents=True, exist_ok=True)

