import sqlite3
from pathlib import Path

# --- Database Path ---
DB_PATH = Path(__file__).parent / "guild-settings.db"

# --- Helper to get connection ---
def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  # Allows dict-style access
    return conn

# --- Initialize Table ---
def init_db():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS guild_settings (
            guild_id INTEGER PRIMARY KEY,
            welcome_enabled INTEGER DEFAULT 0,
            logging_enabled INTEGER DEFAULT 0,
            feature_c INTEGER DEFAULT 0
        )
    """)
    conn.commit()
    conn.close()

# --- Add a new guild if it doesn't exist ---
def add_guild(guild_id: int):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT OR IGNORE INTO guild_settings (guild_id)
        VALUES (?)
    """, (guild_id,))
    conn.commit()
    conn.close()

# --- Toggle a specific setting column ---
def toggle_guild_setting(guild_id: int, setting: str) -> bool:
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(f"SELECT {setting} FROM guild_settings WHERE guild_id = ?", (guild_id,))
    current = cur.fetchone()
    if not current:
        conn.close()
        raise ValueError(f"No guild found with id {guild_id}")

    current_value = current[0] or 0
    new_value = 0 if current_value else 1

    cur.execute(f"UPDATE guild_settings SET {setting} = ? WHERE guild_id = ?", (new_value, guild_id))
    conn.commit()
    conn.close()

    return bool(new_value)

# --- Fetch entire guild row ---
def get_guild(guild_id: int):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM guild_settings WHERE guild_id = ?", (guild_id,))
    row = cur.fetchone()
    conn.close()
    return row  # Access like a dict: row['logging_enabled'], row['welcome_enabled']
