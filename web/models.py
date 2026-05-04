"""
models.py
---------
Models de la base de dades SQLite per AutoEstima.
Usuaris, historial de prediccions i vehicles favorits.
"""

import sqlite3
import os
from datetime import datetime

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "autoestima.db")


def get_db():
    """Retorna una connexió a la base de dades."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """Crea les taules si no existeixen."""
    conn = get_db()
    conn.executescript("""
        CREATE TABLE IF NOT EXISTS users (
            id       INTEGER PRIMARY KEY AUTOINCREMENT,
            name     TEXT    NOT NULL,
            email    TEXT    NOT NULL UNIQUE,
            password TEXT    NOT NULL,
            created  TEXT    NOT NULL
        );

        CREATE TABLE IF NOT EXISTS predictions (
            id         INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id    INTEGER NOT NULL,
            make       TEXT    NOT NULL,
            fuel_type  TEXT    NOT NULL,
            gear_type  TEXT    NOT NULL,
            sale_type  TEXT    NOT NULL,
            months_old INTEGER NOT NULL,
            power      INTEGER NOT NULL,
            kms        INTEGER NOT NULL,
            num_owners INTEGER NOT NULL,
            price      INTEGER NOT NULL,
            price_low  INTEGER NOT NULL,
            price_high INTEGER NOT NULL,
            created    TEXT    NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users(id)
        );

        CREATE TABLE IF NOT EXISTS favorites (
            id         INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id    INTEGER NOT NULL,
            make       TEXT    NOT NULL,
            model      TEXT    NOT NULL,
            price      INTEGER NOT NULL,
            kms        INTEGER NOT NULL,
            months_old INTEGER NOT NULL,
            power      INTEGER NOT NULL,
            fuel_type  TEXT    NOT NULL,
            gear_type  TEXT    NOT NULL,
            sale_type  TEXT    NOT NULL,
            num_owners INTEGER NOT NULL,
            created    TEXT    NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users(id)
        );
    """)
    conn.commit()
    conn.close()


# ── Usuaris ───────────────────────────────────────────────

def create_user(name, email, password_hash):
    conn = get_db()
    try:
        conn.execute(
            "INSERT INTO users (name, email, password, created) VALUES (?, ?, ?, ?)",
            (name, email, password_hash, datetime.now().isoformat())
        )
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()


def get_user_by_email(email):
    conn = get_db()
    user = conn.execute("SELECT * FROM users WHERE email = ?", (email,)).fetchone()
    conn.close()
    return user


def get_user_by_id(user_id):
    conn = get_db()
    user = conn.execute("SELECT * FROM users WHERE id = ?", (user_id,)).fetchone()
    conn.close()
    return user


# ── Prediccions ───────────────────────────────────────────

def save_prediction(user_id, data, price, price_low, price_high):
    conn = get_db()
    conn.execute("""
        INSERT INTO predictions
        (user_id, make, fuel_type, gear_type, sale_type,
         months_old, power, kms, num_owners, price, price_low, price_high, created)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        user_id, data["make"], data["fuel_type"], data["gear_type"], data["sale_type"],
        data["months_old"], data["power"], data["kms"], data["num_owners"],
        price, price_low, price_high, datetime.now().isoformat()
    ))
    conn.commit()
    conn.close()


def get_predictions(user_id):
    conn = get_db()
    rows = conn.execute(
        "SELECT * FROM predictions WHERE user_id = ? ORDER BY created DESC LIMIT 20",
        (user_id,)
    ).fetchall()
    conn.close()
    return [dict(r) for r in rows]


# ── Favorits ──────────────────────────────────────────────

def save_favorite(user_id, car):
    conn = get_db()
    # Evitar duplicats
    existing = conn.execute("""
        SELECT id FROM favorites
        WHERE user_id=? AND make=? AND model=? AND price=?
    """, (user_id, car["make"], car.get("model",""), car["price"])).fetchone()
    if existing:
        conn.close()
        return False
    conn.execute("""
        INSERT INTO favorites
        (user_id, make, model, price, kms, months_old, power,
         fuel_type, gear_type, sale_type, num_owners, created)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        user_id, car["make"], car.get("model",""), car["price"],
        car.get("kms", 0), car.get("months_old", 0), car.get("power", 0),
        car.get("fuel_type",""), car.get("gear_type",""),
        car.get("sale_type",""), car.get("num_owners", 1),
        datetime.now().isoformat()
    ))
    conn.commit()
    conn.close()
    return True


def delete_favorite(user_id, fav_id):
    conn = get_db()
    conn.execute("DELETE FROM favorites WHERE id=? AND user_id=?", (fav_id, user_id))
    conn.commit()
    conn.close()


def get_favorites(user_id):
    conn = get_db()
    rows = conn.execute(
        "SELECT * FROM favorites WHERE user_id=? ORDER BY created DESC",
        (user_id,)
    ).fetchall()
    conn.close()
    return [dict(r) for r in rows]
