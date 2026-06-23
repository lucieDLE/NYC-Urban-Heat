from pathlib import Path

ROOT = Path(__file__).parent.parent

PROCESSED_DIR = ROOT / 'data/processed'

DEFAULT_SCENE = "20230809_20230812"

DEMOGRAPHICS_CSV = PROCESSED_DIR / "nyc_nta_race_ethnicity_2020_exclusive.csv"

ntatype_mapping = {
    '0':"Residential",
    '5':"Rikers Island",
    '6':"Other Special Areas",
    '7':"Cemetery",
    '8':"Airport",
    '9':"Park"
    }
