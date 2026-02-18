from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

DATA_RAW = BASE_DIR / "data" / "raw"
DATA_PROCESSED = BASE_DIR / "data" / "processed"

DB_PATH = DATA_PROCESSED / "college_baseball.db"

TEAM_NAME = "MSST"

# Leaderboard settings
DEFAULT_TOP_N = 20
MIN_AB_RATIO = 0.40
MIN_IP_RATIO = 0.30
