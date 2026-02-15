import sqlite3
from pathlib import Path

import pandas as pd

# -------------------------
# PATHS
# -------------------------
BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data" / "raw"
DB_PATH = BASE_DIR / "data" / "processed" / "college_baseball.db"

# Ensure processed dir exists
DB_PATH.parent.mkdir(parents=True, exist_ok=True)


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
        df["player"] = df["player"].astype(str).str.strip()
    return df


# -------------------------
# BATTING LOAD
# -------------------------
def load_batting(conn):
    for csv in sorted(DATA_DIR.glob("batting_*.csv")):
        year = int(csv.stem.split("_")[1])
        print(f"Loading batting {year}")

        df = pd.read_csv(csv)
        df = normalize_cols(df)
        df = clean_player_column(df)

        # Column aliases
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

        # Remove non-players
        if "player" in df.columns:
            df = df[~df["player"].isin(["Totals", "Opponents"])]

        # Add season/team
        df["season"] = year
        df["team"] = "MSST"

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

        # Prevent duplicates by season overwrite
        conn.execute("DELETE FROM batting_stats WHERE season = ?", (year,))

        df.to_sql("batting_stats", conn, if_exists="append", index=False)


# -------------------------
# PITCHING LOAD
# -------------------------
def load_pitching(conn):
    for csv in sorted(DATA_DIR.glob("pitching_*.csv")):
        year = int(csv.stem.split("_")[1])
        print(f"Loading pitching {year}")

        df = pd.read_csv(csv)
        df = normalize_cols(df)
        df = clean_player_column(df)

        df["season"] = year
        df["team"] = "MSST"

        wanted = [
            "player",
            "season",
            "team",
            "era",
            "w_l",
            "app_gs",
            "ip",
            "so",
            "hr",
        ]

        df = df[[c for c in wanted if c in df.columns]]
        df = df.rename(columns={"app_gs": "app"})

        df = coerce_numeric(df, ["era", "app", "ip", "so", "hr"])

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

    print("Database fully loaded.")


if __name__ == "__main__":
    main()
