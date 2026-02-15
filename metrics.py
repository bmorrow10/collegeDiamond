import sqlite3
from pathlib import Path

import pandas as pd

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "data" / "processed" / "college_baseball.db"


def add_batting_metrics(conn):
    df = pd.read_sql("SELECT * FROM batting_stats", conn)

    # ---- OPS ----
    df["ops"] = df["obp"] + df["slg"]

    # ---- ISO ----
    df["iso"] = df["slg"] - df["avg"]

    # ---- LEAGUE OPS ----
    league_ops = df.groupby("season")["ops"].mean().reset_index()
    league_ops = league_ops.rename(columns={"ops": "league_ops"})

    df = df.merge(league_ops, on="season")

    # ---- OPS+ ----
    df["ops_plus"] = (df["ops"] / df["league_ops"]) * 100

    # ---- DYNAMIC MIN AB ----
    max_ab = df.groupby("season")["ab"].max().reset_index()
    max_ab["min_ab"] = max_ab["ab"] * 0.4

    df = df.merge(max_ab[["season", "min_ab"]], on="season")
    df = df[df["ab"] >= df["min_ab"]]

    # Save view table
    df.to_sql("batting_metrics", conn, if_exists="replace", index=False)


def add_pitching_metrics(conn):
    df = pd.read_sql("SELECT * FROM pitching_stats", conn)

    df["k9"] = (df["so"] / df["ip"]) * 9
    df["hr9"] = (df["hr"] / df["ip"]) * 9

    df.to_sql("pitching_metrics", conn, if_exists="replace", index=False)


def main():
    with sqlite3.connect(DB_PATH) as conn:
        add_batting_metrics(conn)
        add_pitching_metrics(conn)

    print("Metrics calculated.")


if __name__ == "__main__":
    main()
