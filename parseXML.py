import xml.etree.ElementTree as ET
from pathlib import Path
import pandas as pd

RAW_FILE = Path("data/raw/2025.xml")

def parse_players():
    tree = ET.parse(RAW_FILE)
    root = tree.getroot()

    players = []

    # You will adjust tags once you inspect structure
    for player in root.findall(".//player"):
        name = player.findtext("name")
        avg = player.findtext("avg")
        hr = player.findtext("hr")
        rbi = player.findtext("rbi")

        players.append({
            "name": name,
            "avg": avg,
            "hr": hr,
            "rbi": rbi
        })

    df = pd.DataFrame(players)
    return df

if __name__ == "__main__":
    df = parse_players()
    print(df.head())
