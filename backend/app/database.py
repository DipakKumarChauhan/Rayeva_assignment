"""
Database module — SQLite setup and helper functions.
"""
import sqlite3
import uuid
from datetime import datetime
from app.config import settings


def get_connection() -> sqlite3.Connection:
    conn = sqlite3.connect(settings.DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db() -> None:
    """Create all tables if they do not exist."""
    conn = get_connection()
    cursor = conn.cursor()

    # AI prompt/response log
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS ai_logs (
            id          TEXT PRIMARY KEY,
            module      TEXT NOT NULL,
            prompt      TEXT NOT NULL,
            response    TEXT NOT NULL,
            latency_ms  INTEGER,
            created_at  TEXT NOT NULL
        )
    """)

    # Module 1: categorised products
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS products (
            product_id              TEXT PRIMARY KEY,
            name                    TEXT NOT NULL,
            description             TEXT NOT NULL,
            primary_category        TEXT NOT NULL,
            sub_category            TEXT NOT NULL,
            seo_tags                TEXT NOT NULL,
            sustainability_filters  TEXT NOT NULL,
            raw_ai_response         TEXT NOT NULL,
            created_at              TEXT NOT NULL
        )
    """)

    # Module 2: B2B proposals
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS proposals (
            proposal_id             TEXT PRIMARY KEY,
            company_name            TEXT NOT NULL,
            industry                TEXT NOT NULL,
            total_budget            REAL NOT NULL,
            preferences             TEXT NOT NULL,
            quantity_needed         INTEGER NOT NULL,
            use_case                TEXT NOT NULL,
            product_mix             TEXT NOT NULL,
            budget_allocation       TEXT NOT NULL,
            cost_breakdown          TEXT NOT NULL,
            impact_summary          TEXT NOT NULL,
            raw_ai_response         TEXT NOT NULL,
            created_at              TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()


def new_id() -> str:
    return str(uuid.uuid4())


def now_iso() -> str:
    return datetime.utcnow().isoformat() + "Z"
