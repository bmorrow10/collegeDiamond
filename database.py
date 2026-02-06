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
            season INTEGER
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
            season INTEGER
        )
    """)

    conn.commit()


def load_csv_to_db(conn):
    batting_path = DATA_DIR / "batting_2025.csv"
    pitching_path = DATA_DIR / "pitching_2025.csv"

    batting_df = pd.read_csv(batting_path)
    pitching_df = pd.read_csv(pitching_path)

    # ---- RENAME COLUMNS ----
    batting_df = batting_df.rename(
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

    pitching_df = pitching_df.rename(
        columns={
            "Player": "player",
            "era": "era",
            "w-l": "w",
            "app-gs": "app",
            "ip": "ip",
            "so": "so",
            "hr": "hr",
        }
    )

    # ---- ADD SEASON ----
    batting_df["season"] = 2025
    pitching_df["season"] = 2025

    # ---- FILTER COLUMNS ----
    batting_df = batting_df[
        ["player", "avg", "ab", "r", "h", "hr", "rbi", "obp", "season"]
    ]

    pitching_df = pitching_df[["player", "era", "w", "app", "ip", "so", "hr", "season"]]

    # ---- WRITE TO DB ----
    batting_df.to_sql("batting_stats", conn, if_exists="append", index=False)
    pitching_df.to_sql("pitching_stats", conn, if_exists="append", index=False)


def main():
    conn = sqlite3.connect(DB_NAME)

    create_tables(conn)
    load_csv_to_db(conn)

    conn.close()
    print("Database loaded successfully.")


if __name__ == "__main__":
    main()
