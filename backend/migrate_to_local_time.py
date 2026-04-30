"""Migrate existing UTC timestamps to local time (UTC+8 Beijing)."""
import sqlite3
import sys
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent / "data" / "app.db"


def migrate():
    conn = sqlite3.connect(str(DB_PATH))
    cur = conn.cursor()

    # Add 8 hours to all created_at / recorded_at timestamps
    tables_cols = [
        ("providers", "created_at"),
        ("usage_records", "recorded_at"),
        ("collection_logs", "created_at"),
    ]

    for table, col in tables_cols:
        cur.execute(f"SELECT COUNT(*) FROM {table} WHERE {col} IS NOT NULL")
        count = cur.fetchone()[0]
        cur.execute(
            f"UPDATE {table} SET {col} = datetime({col}, '+8 hours') "
            f"WHERE {col} IS NOT NULL"
        )
        print(f"  {table}.{col}: {count} rows migrated (+8h)")

    conn.commit()

    # Show sample
    print("\n=== Sample after migration ===")
    for table, col in tables_cols:
        cur.execute(f"SELECT {col} FROM {table} ORDER BY {col} DESC LIMIT 2")
        rows = cur.fetchall()
        print(f"  {table}.{col}: {[r[0] for r in rows]}")

    conn.close()
    print("\nMigration complete.")


if __name__ == "__main__":
    if not DB_PATH.exists():
        print(f"Database not found: {DB_PATH}", file=sys.stderr)
        sys.exit(1)
    migrate()
