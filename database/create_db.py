"""
Database setup script for Smart Face Attendance System.
Run this once before launching the application to initialise the SQLite database.
"""

import sqlite3

conn = sqlite3.connect('attendance.db')
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS attendance (
    id    INTEGER PRIMARY KEY AUTOINCREMENT,
    name  TEXT NOT NULL,
    date  TEXT NOT NULL,
    time  TEXT NOT NULL
)
''')

conn.commit()
conn.close()
print("[INFO] attendance.db and attendance table created successfully.")
