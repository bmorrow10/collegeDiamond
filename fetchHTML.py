from pathlib import Path

import pandas as pd

url = "https://static.hailstate.com/custompages/stats/bb/2025/teamcume.htm"

tables = pd.read_html(url)

# Create data folder
Path("data").mkdir(exist_ok=True)

# --- Batting ---
batting = tables[1]
batting.columns = batting.iloc[0]
batting = batting[1:]
batting.to_csv("data/batting_2025.csv", index=False)

# --- Pitching ---
pitching = tables[3]
pitching.columns = pitching.iloc[0]
pitching = pitching[1:]
pitching.to_csv("data/pitching_2025.csv", index=False)

print("Saved batting and pitching CSVs.")
