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
            avg REAL,
            ab INTEGER,
            r INTEGER,
            h INTEGER,
            hr INTEGER,
            rbi INTEGER,
            obp REAL,
            season INTEGER,
            team TEXT
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS pitching_stats (
            player TEXT,
            era REAL,
            w TEXT,
            app TEXT,
            ip REAL,
            so INTEGER,
            hr INTEGER,
            season INTEGER,
            team TEXT
        )
    """)

    conn.commit()


def load_batting(conn):
    for csv in DATA_DIR.glob("batting_*.csv"):
        year = int(csv.stem.split("_")[1])
        print(f"Loading batting {year}")

        df = pd.read_csv(csv)

        df = df.rename(
            columns={
                "Player": "player",
                "avg": "avg",
                "ab": "ab",
                "r": "r",
                "h": "h",
                "hr": "hr",
                "rbi": "rbi",
                "ob%": "obp",
            }
        )

        df["season"] = year
        df["team"] = "MSST"

        df = df[["player", "avg", "ab", "r", "h", "hr", "rbi", "obp", "season", "team"]]

        df.to_sql("batting_stats", conn, if_exists="append", index=False)


def load_pitching(conn):
    for csv in DATA_DIR.glob("pitching_*.csv"):
        year = int(csv.stem.split("_")[1])
        print(f"Loading pitching {year}")

        df = pd.read_csv(csv)

        # Normalize column names
        df.columns = (
            df.columns.str.lower()
            .str.strip()
            .str.replace("%", "")
            .str.replace("-", "")
            .str.replace(" ", "")
        )

        # Debug once if needed
        # print(year, df.columns)

        rename_map = {
            "player": "player",
            "era": "era",
            "wl": "w",
            "appgs": "app",
            "ip": "ip",
            "so": "so",
            "hr": "hr",
        }

        df = df.rename(columns=rename_map)

        df["season"] = year
        df["team"] = "MSST"

        # Keep only columns that actually exist
        wanted = ["player", "era", "w", "app", "ip", "so", "hr", "season", "team"]
        df = df[[c for c in wanted if c in df.columns]]

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
