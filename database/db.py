import sqlite3
import os
from werkzeug.security import generate_password_hash

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "expense_tracker.db")


def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db():
    conn = get_db()
    conn.executescript("""
        CREATE TABLE IF NOT EXISTS users (
            id            INTEGER PRIMARY KEY AUTOINCREMENT,
            name          TEXT    NOT NULL,
            email         TEXT    NOT NULL UNIQUE,
            password_hash TEXT    NOT NULL,
            created_at    TEXT    DEFAULT CURRENT_TIMESTAMP
        );

        CREATE TABLE IF NOT EXISTS categories (
            id   INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT    NOT NULL UNIQUE
        );

        CREATE TABLE IF NOT EXISTS expenses (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id     INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
            category_id INTEGER          REFERENCES categories(id) ON DELETE SET NULL,
            amount      REAL    NOT NULL CHECK(amount > 0),
            description TEXT,
            date        TEXT    NOT NULL,
            created_at  TEXT    DEFAULT CURRENT_TIMESTAMP
        );
    """)
    conn.commit()
    conn.close()


def seed_db():
    init_db()
    conn = get_db()

    conn.executemany(
        "INSERT OR IGNORE INTO categories (name) VALUES (?)",
        [("Food",), ("Transport",), ("Entertainment",)],
    )

    conn.execute(
        "INSERT OR IGNORE INTO users (name, email, password_hash) VALUES (?, ?, ?)",
        ("Demo User", "demo@example.com", generate_password_hash("password123")),
    )

    conn.commit()

    user = conn.execute("SELECT id FROM users WHERE email = 'demo@example.com'").fetchone()
    cats = {
        row["name"]: row["id"]
        for row in conn.execute("SELECT id, name FROM categories").fetchall()
    }

    sample_expenses = [
        (user["id"], cats["Food"],          12.50, "Lunch at cafe",       "2026-05-01"),
        (user["id"], cats["Transport"],      3.20, "Bus fare",             "2026-05-02"),
        (user["id"], cats["Entertainment"], 15.00, "Movie ticket",         "2026-05-03"),
    ]

    conn.executemany(
        "INSERT INTO expenses (user_id, category_id, amount, description, date) VALUES (?, ?, ?, ?, ?)",
        sample_expenses,
    )

    conn.commit()
    conn.close()


def get_user_by_email(email):
    conn = get_db()
    user = conn.execute("SELECT * FROM users WHERE email = ?", (email,)).fetchone()
    conn.close()
    return user


def create_user(name, email, password_hash):
    conn = get_db()
    try:
        conn.execute(
            "INSERT INTO users (name, email, password_hash) VALUES (?, ?, ?)",
            (name, email, password_hash),
        )
        conn.commit()
        return get_user_by_email(email)
    except sqlite3.IntegrityError:
        return None
    finally:
        conn.close()
