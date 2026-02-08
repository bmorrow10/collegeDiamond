import sqlite3
from pathlib import Path

import pandas as pd

DB_NAME = "college_baseball.db"
DATA_DIR = Path("data")


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
            slg REAL
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS pitching_stats (
            player TEXT,
            season INTEGER,
            team TEXT,
            era REAL,
            w_l TEXT,
            app TEXT,
            ip REAL,
            so INTEGER,
            hr INTEGER
        )
    """)

    conn.commit()


def normalize_cols(df):
    df.columns = (
        df.columns.str.lower()
        .str.strip()
        .str.replace("%", "")
        .str.replace("-", "_")
        .str.replace(" ", "_")
    )
    return df


def load_batting(conn):
    for csv in DATA_DIR.glob("batting_*.csv"):
        year = int(csv.stem.split("_")[1])
        print(f"Loading batting {year}")

        df = pd.read_csv(csv)
        df = normalize_cols(df)

        # ---- COLUMN ALIASES ----
        rename_map = {
            # OBP variants
            "obp": "obp",
            "ob_pct": "obp",
            "ob": "obp",
            "onbasepct": "obp",
            "onbase": "obp",
            # SLG variants
            "slg": "slg",
            "slg_pct": "slg",
            "slug": "slg",
            "slugging": "slg",
        }

        df = df.rename(columns=rename_map)

        # ---- REMOVE NON-PLAYERS ----
        if "player" in df.columns:
            df = df[~df["player"].isin(["Totals", "Opponents"])]

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

        # Optional: drop rows with no OPS components
        if "obp" in df.columns and "slg" in df.columns:
            df = df.dropna(subset=["obp", "slg"], how="all")

        df.to_sql("batting_stats", conn, if_exists="append", index=False)


def load_pitching(conn):
    for csv in DATA_DIR.glob("pitching_*.csv"):
        year = int(csv.stem.split("_")[1])
        print(f"Loading pitching {year}")

        df = pd.read_csv(csv)
        df = normalize_cols(df)

        df["season"] = year
        df["team"] = "MSST"

        wanted = ["player", "season", "team", "era", "w_l", "app_gs", "ip", "so", "hr"]

        df = df[[c for c in wanted if c in df.columns]]
        df = df.rename(columns={"app_gs": "app"})

        df.to_sql("pitching_stats", conn, if_exists="append", index=False)


def main():
    conn = sqlite3.connect(DB_NAME)

    create_tables(conn)
    load_batting(conn)
    load_pitching(conn)

    conn.close()
    print("Database fully loaded.")


if __name__ == "__main__":
    main()
