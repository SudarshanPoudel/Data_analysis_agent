import sqlite3
from src.config.db import DB_PATH

def get_summary_from_db(path: str) -> str:
    """
    Retrieves a summary from the database if it exists.

    Args:
        path (str): The file path for which to retrieve the summary.

    Returns:
        str | None: The summary if found, otherwise None.
    """
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT summary FROM summaries WHERE path = ?", (path,))
        result = cursor.fetchone()
        return result[0] if result else None


def store_summary_in_db(path: str, summary: str):
    """
    Stores a summary in the database.

    Args:
        path (str): The file path associated with the summary.
        summary (str): The summary text.
    """
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO summaries (path, summary) VALUES (?, ?)", (path, summary)
        )
        conn.commit()
        
def delete_summary_from_db(path: str):
    """
    Deletes a summary from the database.

    Args:
        path (str): The file path associated with the summary.
    """
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute(
            "DELETE FROM summaries WHERE path = ?", (path,)
        )
        conn.commit()
