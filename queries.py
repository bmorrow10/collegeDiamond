import sqlite3

import pandas as pd

conn = sqlite3.connect("college_baseball.db")

df = pd.read_sql(
    """
SELECT player, SUM(hr) AS career_hr
FROM batting_stats
GROUP BY player
ORDER BY career_hr DESC
LIMIT 10
""",
    conn,
)

print(df)
