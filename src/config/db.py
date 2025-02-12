import sqlite3

# Database setup
DB_PATH = "summaries.db"


def initialize_db():
    """
    Initializes the SQLite database and creates the summaries table if it doesn't exist.
    """
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS summaries (
                path TEXT PRIMARY KEY,
                summary TEXT
            )
            """
        )
        conn.commit()

__all__ = [
    DB_PATH,
    initialize_db,
]
