# College Diamond: A College Baseball Data Project

College Diamond is an open-source sabermetrics project focused on bringing advanced baseball analytics to NCAA college baseball data.

The project collects publicly available team statistics, normalizes them into a structured database, and calculates modern performance metrics such as OPS, OPS+, ISO, and advanced pitching rates.

Features

 - Automated stat scraping and CSV ingestion
 - SQLite database pipeline
 - Batting metrics (OPS, OPS+, ISO, rate stats)
 - Pitching metrics (K/9, HR/9, K/HR ratio)
 - Dynamic leaderboards
 - R and Python notebook support

---

## Project Goals

- Collect structured college baseball statistics
- Normalize and store data in SQL
- Enable sabermetric analysis at the college level
- Provide visualization tools using ggplot and R
- Lay groundwork for future dashboards and park factor modeling

Phase 1 focuses on **Mississippi State Baseball – 2025 Season**.

2008–2009 pending parser support due to legacy HTML format.


---

## Project Structure

collegeDiamond/
│
├── data/
│   ├── raw/         # Source CSV/XML files
│   └── processed/   # SQLite database
│
├── database.py       # ETL pipeline (CSV → SQLite)
├── metrics.py        # Sabermetric calculations
├── leaderboards.py   # Console analytics output
├── fetchHTML.py      # Data retrieval
├── config.py         # Central configuration
│
├── notebooks/
│   └── leaderboard.R # Example ggplot visualization
│
├── requirements.txt
└── README.md



---

## Requirements

- Python 3.10+
- R (optional for visualization)

Python packages:

pip install -r requirements.txt


---

## How to Run

From the project root directory:

### 1. Fetch Data

python fetchHTML.py


### 2. Parse XML

python parseHTML.py


### 3. Initialize Database

python database.py


### 4. Run Queries

python queries.py


### 5. (Optional) R Visualization
Open `notebooks/leaderboard.R` in RStudio and run.

---

## Data Source

Statistics are sourced from official Mississippi State Athletics:

https://hailstate.com

This project is not affiliated with Mississippi State University and is intended for educational and analytical purposes only.

---

## Inspiration / Related Projects

- https://github.com/nathanblumenfeld/collegebaseball
- https://github.com/CodeMateo15/CollegeBaseballStatsPackage

No code has been directly copied; these repositories served as conceptual inspiration.

---

## License

MIT License
