"""SQLite-backed job application tracker."""
import sqlite3
from datetime import date

DB_PATH = "applications.db"

STATUSES = ["Saved", "Applied", "Interviewing", "Offer", "Rejected", "Withdrawn"]

_SCHEMA = """
CREATE TABLE IF NOT EXISTS applications (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    company TEXT NOT NULL,
    role TEXT NOT NULL,
    job_url TEXT,
    match_score REAL,
    status TEXT NOT NULL DEFAULT 'Saved',
    date_added TEXT NOT NULL,
    notes TEXT
);
"""


def get_connection(db_path: str = DB_PATH) -> sqlite3.Connection:
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn


def init_db(db_path: str = DB_PATH) -> None:
    conn = get_connection(db_path)
    try:
        conn.execute(_SCHEMA)
        conn.commit()
    finally:
        conn.close()


def add_application(
    company: str,
    role: str,
    job_url: str = "",
    match_score: float = None,
    status: str = "Saved",
    notes: str = "",
    db_path: str = DB_PATH,
) -> int:
    conn = get_connection(db_path)
    try:
        cur = conn.execute(
            """INSERT INTO applications (company, role, job_url, match_score,
               status, date_added, notes) VALUES (?, ?, ?, ?, ?, ?, ?)""",
            (company, role, job_url, match_score, status, date.today().isoformat(), notes),
        )
        conn.commit()
        return cur.lastrowid
    finally:
        conn.close()


def get_applications(db_path: str = DB_PATH):
    conn = get_connection(db_path)
    try:
        rows = conn.execute(
            "SELECT * FROM applications ORDER BY date_added DESC, id DESC"
        ).fetchall()
        return [dict(row) for row in rows]
    finally:
        conn.close()


def update_status(app_id: int, status: str, db_path: str = DB_PATH) -> None:
    conn = get_connection(db_path)
    try:
        conn.execute("UPDATE applications SET status = ? WHERE id = ?", (status, app_id))
        conn.commit()
    finally:
        conn.close()


def delete_application(app_id: int, db_path: str = DB_PATH) -> None:
    conn = get_connection(db_path)
    try:
        conn.execute("DELETE FROM applications WHERE id = ?", (app_id,))
        conn.commit()
    finally:
        conn.close()
