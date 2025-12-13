import sqlite3

conn = sqlite3.connect("cerina.db")
cur = conn.cursor()

print("\n=== TABLES ===")
print(cur.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall())

print("\n=== EVENT LOG ===")
try:
    print(cur.execute("SELECT * FROM event_log LIMIT 10").fetchall())
except Exception as e:
    print("event_log error:", e)

print("\n=== CHECKPOINTS ===")
try:
    print(cur.execute("SELECT * FROM checkpoints LIMIT 10").fetchall())
except Exception as e:
    print("checkpoints error:", e)

conn.close()
