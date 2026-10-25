
import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent.parent / "rfp_evaluation.db"

DEFAULT_CRITERIA = [
    {
        "name": "Technical Capability",
        "description": "Architecture, integrations, scalability, and technical fit",
        "weight": 30,
        "max_score": 10,
    },
    {
        "name": "Implementation Plan",
        "description": "Timeline, milestones, staffing, and risk plan",
        "weight": 20,
        "max_score": 10,
    },
    {
        "name": "Commercial Value",
        "description": "Pricing clarity, total cost, and assumptions",
        "weight": 20,
        "max_score": 10,
    },
    {
        "name": "Security & Compliance",
        "description": "Controls, certifications, privacy, and auditability",
        "weight": 20,
        "max_score": 10,
    },
    {
        "name": "Support & Experience",
        "description": "Support model, similar projects, and references",
        "weight": 10,
        "max_score": 10,
    },
]


def get_connection():
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    return connection


def initialize_database():
    with get_connection() as connection:
        connection.execute("""
            CREATE TABLE IF NOT EXISTS evaluation_criteria (
                criterion_id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE,
                description TEXT NOT NULL,
                weight REAL NOT NULL CHECK(weight >= 0),
                max_score REAL NOT NULL CHECK(max_score > 0),
                is_active INTEGER NOT NULL DEFAULT 1
            )
        """)

        connection.execute("""
            CREATE TABLE IF NOT EXISTS rfp_runs (
                rfp_run_id TEXT PRIMARY KEY,
                created_at TEXT NOT NULL,
                status TEXT NOT NULL
            )
        """)

        connection.execute("""
            CREATE TABLE IF NOT EXISTS supplier_results (
                result_id INTEGER PRIMARY KEY AUTOINCREMENT,
                rfp_run_id TEXT NOT NULL,
                supplier_name TEXT NOT NULL,
                submission_date TEXT NOT NULL,
                experience_rating REAL NOT NULL,
                absolute_score REAL,
                ppi REAL,
                final_rank INTEGER,
                result_json TEXT,
                FOREIGN KEY (rfp_run_id)
                    REFERENCES rfp_runs(rfp_run_id)
            )
        """)

        count = connection.execute(
            "SELECT COUNT(*) FROM evaluation_criteria"
        ).fetchone()[0]

        if count == 0:
            connection.executemany("""
                INSERT INTO evaluation_criteria
                (name, description, weight, max_score, is_active)
                VALUES (:name, :description, :weight, :max_score, 1)
            """, DEFAULT_CRITERIA)


def get_active_criteria():
    with get_connection() as connection:
        rows = connection.execute("""
            SELECT criterion_id, name, description, weight, max_score
            FROM evaluation_criteria
            WHERE is_active = 1
            ORDER BY criterion_id
        """).fetchall()

    return [dict(row) for row in rows]


if __name__ == "__main__":
    initialize_database()
    criteria = get_active_criteria()

    print("Database initialized successfully.")
    print(f"Database location: {DB_PATH}")
    print("\nActive evaluation criteria:")

    for criterion in criteria:
        print(
            f"{criterion['criterion_id']}. "
            f"{criterion['name']} — "
            f"{criterion['weight']}%"
        )

    print(
        "\nTotal active weight:",
        sum(item["weight"] for item in criteria),
        "%"
    )
