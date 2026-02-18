import sqlite3
from pathlib import Path

import numpy as np
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "data" / "processed" / "college_baseball.db"


# -------------------------
# BATTING METRICS
# -------------------------
def add_batting_metrics(conn):
    df = pd.read_sql("SELECT * FROM batting_stats", conn)

    # ---- SAFETY ----
    df["ab"] = pd.to_numeric(df["ab"], errors="coerce")
    df = df[df["ab"] > 0]

    # ---- CORE ----
    df["ops"] = df["obp"] + df["slg"]
    df["iso"] = df["slg"] - df["avg"]

    # ---- RATE STATS ----
    df["runs_per_ab"] = df["r"] / df["ab"]
    df["hr_rate"] = df["hr"] / df["ab"]
    df["rbi_rate"] = df["rbi"] / df["ab"]

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

    # ---- CLEAN ----
    df.replace([np.inf, -np.inf], np.nan, inplace=True)

    df.to_sql("batting_metrics", conn, if_exists="replace", index=False)


# -------------------------
# PITCHING METRICS
# -------------------------
def add_pitching_metrics(conn):
    df = pd.read_sql("SELECT * FROM pitching_stats", conn)

    df["ip"] = pd.to_numeric(df["ip"], errors="coerce")
    df = df[df["ip"] > 0]

    # ---- CORE ----
    df["k9"] = (df["so"] / df["ip"]) * 9
    df["hr9"] = (df["hr"] / df["ip"]) * 9

    # ---- ADDITIONS ----
    df["k_per_ip"] = df["so"] / df["ip"]
    df["k_hr_ratio"] = df["so"] / df["hr"]

    df.replace([np.inf, -np.inf], np.nan, inplace=True)

    df.to_sql("pitching_metrics", conn, if_exists="replace", index=False)


# -------------------------
# MAIN
# -------------------------
def main():
    with sqlite3.connect(DB_PATH) as conn:
        add_batting_metrics(conn)
        add_pitching_metrics(conn)

    print("Metrics calculated.")


if __name__ == "__main__":
    main()
