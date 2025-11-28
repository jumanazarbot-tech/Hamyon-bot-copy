# db.py
import sqlite3
from config import DB_PATH
from datetime import datetime

conn = sqlite3.connect(DB_PATH, check_same_thread=False)
cur = conn.cursor()

def init_db():
    cur.executescript("""
    CREATE TABLE IF NOT EXISTS users (
      user_id INTEGER PRIMARY KEY,
      username TEXT,
      first_name TEXT,
      balance REAL DEFAULT 0,
      usd_balance REAL DEFAULT 0,
      stars REAL DEFAULT 0,
      referred_by INTEGER,
      ref_bonus_received INTEGER DEFAULT 0,
      is_active INTEGER DEFAULT 1,
      created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
      last_seen TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
      stake_amount REAL DEFAULT 0,
      stake_start TIMESTAMP
    );
    CREATE TABLE IF NOT EXISTS withdraws (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      user_id INTEGER,
      amount REAL,
      status TEXT DEFAULT 'pending',
      created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
      admin_id INTEGER,
      note TEXT
    );
    CREATE TABLE IF NOT EXISTS sell_requests (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      user_id INTEGER,
      item TEXT,
      amount REAL,
      total_price REAL,
      status TEXT DEFAULT 'pending',
      created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    CREATE TABLE IF NOT EXISTS settings (key TEXT PRIMARY KEY, value TEXT);
    CREATE TABLE IF NOT EXISTS promos (code TEXT PRIMARY KEY, reward REAL, uses_left INTEGER, expires_at TIMESTAMP);
    CREATE TABLE IF NOT EXISTS tx_log (id INTEGER PRIMARY KEY AUTOINCREMENT, user_id INTEGER, type TEXT, amount REAL, meta TEXT, created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP);
    CREATE TABLE IF NOT EXISTS support (id INTEGER PRIMARY KEY AUTOINCREMENT, user_id INTEGER, message TEXT, admin_reply TEXT, status TEXT DEFAULT 'open', created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP);
    """)
    conn.commit()

def get_setting(key, default=None):
    cur.execute("SELECT value FROM settings WHERE key=?", (key,))
    r = cur.fetchone()
    return float(r[0]) if r else default

def set_setting(key, val):
    cur.execute("INSERT OR REPLACE INTO settings (key, value) VALUES (?, ?)", (key, str(val)))
    conn.commit()

def log_tx(user_id, tx_type, amount, meta=""):
    cur.execute("INSERT INTO tx_log (user_id, type, amount, meta) VALUES (?, ?, ?, ?)", (user_id, tx_type, amount, meta))
    conn.commit()
