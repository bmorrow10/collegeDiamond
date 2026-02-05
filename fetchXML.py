import requests
from pathlib import Path

URL = "https://hailstate.com/sports/baseball/stats/2025"
DATA_DIR = Path("data/raw")
DATA_DIR.mkdir(parents=True, exist_ok=True)

def fetch_xml():
    response = requests.get(URL)
    response.raise_for_status()

    file_path = DATA_DIR / "2025.xml"
    with open(file_path, "wb") as f:
        f.write(response.content)

    print(f"Saved XML to {file_path}")

if __name__ == "__main__":
    fetch_xml()
