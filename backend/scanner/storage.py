# scanner/storage.py

import os
import json
import sqlite3
from datetime import datetime

DB_PATH = os.path.join(os.getcwd(), "osint.db")

# Ensure table exists
def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS scans (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            domain TEXT NOT NULL,
            start TEXT,
            end TEXT,
            result_json TEXT
        )
    ''')
    conn.commit()
    conn.close()


# Save full result object as JSON
def save_to_history(result: dict):
    init_db()
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
        INSERT INTO scans (domain, start, end, result_json)
        VALUES (?, ?, ?, ?)
    ''', (
        result.get("domain"),
        datetime.utcfromtimestamp(result.get("start")).isoformat(),
        datetime.utcfromtimestamp(result.get("end")).isoformat(),
        json.dumps(result)
    ))
    conn.commit()
    conn.close()


def get_scan_history():
    init_db()
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('SELECT result_json FROM scans ORDER BY id DESC')
    rows = c.fetchall()
    conn.close()
    return [json.loads(row[0]) for row in rows]