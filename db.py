import sqlite3

DB_PATH = "sync_state.db"

def init_db():
    con = sqlite3.connect(DB_PATH)
    con.execute("""
        CREATE TABLE IF NOT EXISTS synced_orders (
            etsy_order_id TEXT PRIMARY KEY,
            synced_at     TEXT DEFAULT (datetime('now'))
        )
    """)
    con.commit()
    con.close()

def is_synced(order_id: str) -> bool:
    con = sqlite3.connect(DB_PATH)
    row = con.execute(
        "SELECT 1 FROM synced_orders WHERE etsy_order_id = ?", (str(order_id),)
    ).fetchone()
    con.close()
    return row is not None

def mark_synced(order_id: str):
    con = sqlite3.connect(DB_PATH)
    con.execute(
        "INSERT OR IGNORE INTO synced_orders (etsy_order_id) VALUES (?)", (str(order_id),)
    )
    con.commit()
    con.close()