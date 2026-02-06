# College Baseball Data Project

An open-source effort to standardize and analyze college baseball statistics, starting with Mississippi State University baseball data.

This project focuses on building a reproducible data pipeline that ingests official athletics statistics, stores them in a structured database, and enables analytics and visualization using Python and R.

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

collegeBaseball/
fetchHTML.py # Downloads raw HTML stats
parseHTML.py # Parses HTML into structured data
database.py # Creates SQLite database
queries.py # Example SQL queries
data/ # Raw and processed data
notebooks/
leaderboard.R # Example ggplot visualization


---

## Requirements

- Python 3.10+
- R (optional for visualization)

Python packages:

pip install requests pandas


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

This project is not affiliated with Mississippi State University.

---

## Inspiration / Related Projects

- https://github.com/nathanblumenfeld/collegebaseball
- https://github.com/CodeMateo15/CollegeBaseballStatsPackage

No code has been directly copied; these repositories served as conceptual inspiration.

---

## License

MIT License
