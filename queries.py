import sqlite3

import pandas as pd

conn = sqlite3.connect("college_baseball.db")

df = pd.read_sql(
    """
SELECT player, hr
FROM batting_stats
ORDER BY hr DESC
LIMIT 10
""",
    conn,
)

print(df)
