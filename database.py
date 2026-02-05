import sqlite3

DB_NAME = "college_baseball.db"

def create_tables():
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS players (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS batting_stats (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            player_id INTEGER,
            avg REAL,
            hr INTEGER,
            rbi INTEGER,
            FOREIGN KEY(player_id) REFERENCES players(id)
        )
    """)

    conn.commit()
    conn.close()

if __name__ == "__main__":
    create_tables()
    print("Database initialized.")
