import sqlite3

import pandas as pd

DB_PATH = "data/processed/college_baseball.db"


def get_data(conn):
    return pd.read_sql_query(
        """
        SELECT player, season, team, ops
        FROM batting_metrics
        ORDER BY ops DESC
        LIMIT 20
    """,
        conn,
    )


def apply_min_ab(df):
    filtered = []

    for season, group in df.groupby("season"):
        max_ab = group["ab"].max()
        min_ab = max_ab * 0.30

        g = group[group["ab"] >= min_ab]
        filtered.append(g)

    return pd.concat(filtered)


def top_ops(df, n=10):
    return df.sort_values("ops", ascending=False).head(n)


def main():
    conn = sqlite3.connect(DB_PATH)

    df = get_data(conn)
    df = df.dropna(subset=["ops", "ab"])

    qualified = apply_min_ab(df)
    leaders = top_ops(qualified, 15)

    print("\nTop OPS Seasons\n")
    print(leaders[["player", "season", "team", "ops", "ab"]])

    conn.close()


if __name__ == "__main__":
    main()
