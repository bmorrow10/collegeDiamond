from pathlib import Path

import pandas as pd

DATA_DIR = Path("data")
DATA_DIR.mkdir(exist_ok=True)


def fetch_year(year):
    url = f"https://static.hailstate.com/custompages/stats/bb/{year}/teamcume.htm"
    print(f"Fetching {year}...")

    try:
        tables = pd.read_html(url)
    except Exception as e:
        print(f"Failed for {year}: {e}")
        return

    # Batting table
    batting = tables[1]
    batting.columns = batting.iloc[0]
    batting = batting[1:]
    batting.to_csv(DATA_DIR / f"batting_{year}.csv", index=False)

    # Pitching table
    pitching = tables[3]
    pitching.columns = pitching.iloc[0]
    pitching = pitching[1:]
    pitching.to_csv(DATA_DIR / f"pitching_{year}.csv", index=False)

    print(f"Saved {year} CSVs")


if __name__ == "__main__":
    # Change range as desired
    for y in range(2025, 2009, -1):
        fetch_year(y)
