import sqlite3

import pandas as pd

from config import DB_PATH, DEFAULT_TOP_N


def get_batting(conn):
    return pd.read_sql_query("SELECT * FROM batting_metrics", conn)


def get_pitching(conn):
    return pd.read_sql_query("SELECT * FROM pitching_metrics", conn)


def print_board(title, df, cols):
    print("\n" + "=" * 50)
    print(title)
    print("=" * 50)
    print(df[cols].head(DEFAULT_TOP_N))


def batting_leaderboards(conn):
    df = get_batting(conn)

    df = df.dropna(subset=["ops", "ab"])

    print_board(
        "Top OPS Seasons",
        df.sort_values("ops", ascending=False),
        ["player", "season", "team", "ops", "ab"],
    )

    print_board(
        "Top OPS+ Seasons",
        df.sort_values("ops_plus", ascending=False),
        ["player", "season", "team", "ops_plus", "ab"],
    )

    print_board(
        "Best Power (ISO)",
        df.sort_values("iso", ascending=False),
        ["player", "season", "team", "iso", "ab"],
    )

    print_board(
        "Home Run Rate",
        df.sort_values("hr_rate", ascending=False),
        ["player", "season", "team", "hr_rate", "ab"],
    )

    print_board(
        "Run Production (RBI/AB)",
        df.sort_values("rbi_rate", ascending=False),
        ["player", "season", "team", "rbi_rate", "ab"],
    )


def pitching_leaderboards(conn):
    df = get_pitching(conn)
    df = df.dropna(subset=["ip"])

    print_board(
        "Strikeout Kings (K/9)",
        df.sort_values("k9", ascending=False),
        ["player", "season", "team", "k9", "ip"],
    )

    print_board(
        "Home Run Suppression (HR/9)",
        df.sort_values("hr9", ascending=True),
        ["player", "season", "team", "hr9", "ip"],
    )

    print_board(
        "Dominance (K/HR Ratio)",
        df.sort_values("k_hr_ratio", ascending=False),
        ["player", "season", "team", "k_hr_ratio", "ip"],
    )


def main():
    with sqlite3.connect(DB_PATH) as conn:
        batting_leaderboards(conn)
        pitching_leaderboards(conn)


if __name__ == "__main__":
    main()
