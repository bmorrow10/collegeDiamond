import logging
import sqlite3
from pathlib import Path

import pandas as pd

# -------------------------
# CONFIG
# -------------------------
BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data" / "raw"
DB_PATH = BASE_DIR / "data" / "processed" / "college_baseball.db"
TEAM_NAME = "MSST"

DB_PATH.parent.mkdir(parents=True, exist_ok=True)

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)


# -------------------------
# TABLE CREATION
# -------------------------
def create_tables(conn):
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS batting_stats (
            player TEXT,
            season INTEGER,
            team TEXT,
            avg REAL,
            ab INTEGER,
            r INTEGER,
            h INTEGER,
            hr INTEGER,
            rbi INTEGER,
            obp REAL,
            slg REAL,
            UNIQUE(player, season, team)
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS pitching_stats (
            player TEXT,
            season INTEGER,
            team TEXT,
            era REAL,
            w_l TEXT,
            app INTEGER,
            ip REAL,
            so INTEGER,
            hr INTEGER,
            UNIQUE(player, season, team)
        )
    """)

    # ---- INDEXES ----
    cur.execute(
        "CREATE INDEX IF NOT EXISTS idx_batting_player ON batting_stats(player)"
    )
    cur.execute(
        "CREATE INDEX IF NOT EXISTS idx_batting_season ON batting_stats(season)"
    )
    cur.execute(
        "CREATE INDEX IF NOT EXISTS idx_pitching_player ON pitching_stats(player)"
    )
    cur.execute(
        "CREATE INDEX IF NOT EXISTS idx_pitching_season ON pitching_stats(season)"
    )

    conn.commit()


# -------------------------
# HELPERS
# -------------------------
def normalize_cols(df):
    df.columns = (
        df.columns.str.lower()
        .str.strip()
        .str.replace("%", "", regex=False)
        .str.replace("-", "_", regex=False)
        .str.replace(" ", "_", regex=False)
    )
    return df


def coerce_numeric(df, cols):
    for col in cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")
    return df


def clean_player_column(df):
    if "name" in df.columns and "player" not in df.columns:
        df = df.rename(columns={"name": "player"})

    if "player" in df.columns:
        df["player"] = (
            df["player"].astype(str).str.strip().replace({"nan": None, "": None})
        )
        df = df.dropna(subset=["player"])

    return df


def safe_read_csv(path):
    try:
        return pd.read_csv(path, encoding="utf-8", engine="python")
    except Exception as e:
        log.warning(f"Failed reading {path}: {e}")
        return pd.DataFrame()


# -------------------------
# BATTING LOAD
# -------------------------
def load_batting(conn):
    for csv in sorted(DATA_DIR.glob("batting_*.csv")):
        year = int(csv.stem.split("_")[1])
        log.info(f"Loading batting {year}")

        df = safe_read_csv(csv)
        if df.empty:
            log.warning(f"Skipping empty file {csv}")
            continue

        df = normalize_cols(df)
        df = clean_player_column(df)

        # ---- COLUMN ALIASES ----
        rename_map = {
            "ob_pct": "obp",
            "ob": "obp",
            "onbasepct": "obp",
            "onbase": "obp",
            "slg_pct": "slg",
            "slug": "slg",
            "slugging": "slg",
        }
        df = df.rename(columns=rename_map)

        # ---- REMOVE NON-PLAYERS ----
        if "player" in df.columns:
            df = df[~df["player"].isin(["Totals", "Opponents"])]

        df["season"] = year
        df["team"] = TEAM_NAME

        wanted = [
            "player",
            "season",
            "team",
            "avg",
            "ab",
            "r",
            "h",
            "hr",
            "rbi",
            "obp",
            "slg",
        ]

        df = df[[c for c in wanted if c in df.columns]]

        df = coerce_numeric(df, ["avg", "ab", "r", "h", "hr", "rbi", "obp", "slg"])

        # Drop rows with no OBP/SLG
        if "obp" in df.columns and "slg" in df.columns:
            df = df.dropna(subset=["obp", "slg"], how="all")

        # ---- TRANSACTION SAFE OVERWRITE ----
        with conn:
            conn.execute("DELETE FROM batting_stats WHERE season = ?", (year,))
            df.to_sql("batting_stats", conn, if_exists="append", index=False)


# -------------------------
# PITCHING LOAD
# -------------------------
def load_pitching(conn):
    for csv in sorted(DATA_DIR.glob("pitching_*.csv")):
        year = int(csv.stem.split("_")[1])
        log.info(f"Loading pitching {year}")

        df = safe_read_csv(csv)
        if df.empty:
            log.warning(f"Skipping empty file {csv}")
            continue

        df = normalize_cols(df)
        df = clean_player_column(df)

        df["season"] = year
        df["team"] = TEAM_NAME

        wanted = ["player", "season", "team", "era", "w_l", "app_gs", "ip", "so", "hr"]

        df = df[[c for c in wanted if c in df.columns]]
        df = df.rename(columns={"app_gs": "app"})

        df = coerce_numeric(df, ["era", "app", "ip", "so", "hr"])

        with conn:
            conn.execute("DELETE FROM pitching_stats WHERE season = ?", (year,))
            df.to_sql("pitching_stats", conn, if_exists="append", index=False)


# -------------------------
# MAIN
# -------------------------
def main():
    with sqlite3.connect(DB_PATH) as conn:
        create_tables(conn)
        load_batting(conn)
        load_pitching(conn)

    log.info("Database fully loaded.")


if __name__ == "__main__":
    main()
