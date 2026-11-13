# Store chat turns in SQLite, fetch one user's thread in order, and count messages per role.
import sqlite3

conn = sqlite3.connect(":memory:")
conn.execute("""
    CREATE TABLE messages (
        id INTEGER PRIMARY KEY,
        user TEXT,
        role TEXT,
        text TEXT
    )
""")

turns = [
    ("an", "user", "Summarise this PDF."),
    ("an", "assistant", "Here are three key points."),
    ("binh", "user", "Translate to Vietnamese."),
    ("an", "user", "Make it shorter."),
    ("an", "assistant", "One-sentence summary ready."),
]
with conn:
    conn.executemany(
        "INSERT INTO messages (user, role, text) VALUES (?, ?, ?)",
        turns,
    )

an_thread = conn.execute("""
    SELECT id, role, text
    FROM messages
    WHERE user = ?
    ORDER BY id ASC
""", ("an",)).fetchall()

print("An's chat:")
for msg_id, role, text in an_thread:
    print(f"  #{msg_id} [{role}] {text}")

role_counts = conn.execute("""
    SELECT role, COUNT(*)
    FROM messages
    GROUP BY role
    ORDER BY role ASC
""").fetchall()

print("Counts by role:")
for role, total in role_counts:
    print(f"  {role}: {total}")

conn.close()
