import sqlite3
import pandas as pd

DB_NAME = "college_baseball.db"

def top_avg():
    conn = sqlite3.connect(DB_NAME)

    query = """
        SELECT p.name, b.avg
        FROM players p
        JOIN batting_stats b ON p.id = b.player_id
        ORDER BY b.avg DESC
        LIMIT 5
    """

    df = pd.read_sql(query, conn)
    print(df)

if __name__ == "__main__":
    top_avg()
