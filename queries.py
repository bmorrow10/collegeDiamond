import sqlite3

import pandas as pd

conn = sqlite3.connect("college_baseball.db")

df = pd.read_sql(
    """
    SELECT player, season, ROUND(obp+slg,3) AS ops
    FROM batting_stats
    ORDER BY ops DESC;
""",
    conn,
)

print(df)
