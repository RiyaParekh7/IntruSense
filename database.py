import sqlite3
import random

def init_db():
    conn = sqlite3.connect("intrusense.db")
    c = conn.cursor()

    c.execute("""
    CREATE TABLE IF NOT EXISTS logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user TEXT,
        login_time INTEGER,
        files INTEGER,
        transfer INTEGER,
        device INTEGER,
        its_score REAL,
        severity TEXT
    )
    """)

    conn.commit()
    conn.close()


def insert_log(data):
    conn = sqlite3.connect("intrusense.db")
    c = conn.cursor()

    c.execute("""
        INSERT INTO logs (user, login_time, files, transfer, device, its_score, severity)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, data)

    conn.commit()
    conn.close()


def fetch_logs(user=None):
    conn = sqlite3.connect("intrusense.db")
    c = conn.cursor()

    if user:
        c.execute("SELECT * FROM logs WHERE user=? ORDER BY id DESC", (user,))
    else:
        c.execute("SELECT * FROM logs ORDER BY id DESC")

    rows = c.fetchall()
    conn.close()
    return rows


def seed_enterprise_logs(users: dict):
    """Seed realistic logs for all 35 enterprise users if they have no logs."""
    conn = sqlite3.connect("intrusense.db")
    c = conn.cursor()

    severities = ["NORMAL", "NORMAL", "NORMAL", "MEDIUM", "CRITICAL"]

    for username in users:
        if username == "admin":
            continue
        c.execute("SELECT COUNT(*) FROM logs WHERE user=?", (username,))
        count = c.fetchone()[0]
        if count == 0:
            # Insert 3-6 historical logs per user
            for _ in range(random.randint(3, 6)):
                hr = random.randint(0, 23)
                files = random.randint(1, 95)
                transfer = random.randint(50, 9500)
                device = random.randint(1, 3)
                sev = random.choice(severities)
                score = min(100, int((files * 0.5) + (transfer * 0.005) + (40 if sev == "CRITICAL" else 15 if sev == "MEDIUM" else 0)))
                c.execute("""
                    INSERT INTO logs (user, login_time, files, transfer, device, its_score, severity)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                """, (username, hr, files, transfer, device, score, sev))

    conn.commit()
    conn.close()


def get_severity_risk_level(severity: str) -> str:
    """Map severity string to risk level label."""
    mapping = {"CRITICAL": "HIGH", "MEDIUM": "MEDIUM", "NORMAL": "LOW"}
    return mapping.get(severity, "LOW")