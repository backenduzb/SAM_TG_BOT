import requests
import sqlite3

conn = sqlite3.connect('base.db')
cursor = conn.cursor()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS topics (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT UNIQUE
    )
""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS teachers (
        id INTEGER PRIMARY KEY,
        full_name TEXT,
        topic_id INTEGER,
        telegram_id INTEGER,
        FOREIGN KEY (topic_id) REFERENCES topics (id)
    )
""")

conn.commit()

url_topics = "http://127.0.0.1:8000/api/topics/"
response = requests.get(url=url_topics)
topics_data = response.json()

for item in topics_data:
    topic = item.get('topic_name')
    if topic:
        try:
            cursor.execute("INSERT OR IGNORE INTO topics (name) VALUES (?)", (topic,))
        except sqlite3.IntegrityError:
            pass

conn.commit()

url_teachers = "http://127.0.0.1:8000/api/teachers/"
response = requests.get(url=url_teachers)
teachers_data = response.json()

for item in teachers_data:
    id_ = item.get('id')
    topic_name = item.get('topic')
    telegram_id = item.get('telegram_id')
    full_name = item.get('full_name')

    if id_ is not None and topic_name and telegram_id is not None and full_name:
        cursor.execute("SELECT id FROM topics WHERE name = ?", (topic_name,))
        result = cursor.fetchone()
        if result:
            topic_id = result[0]
        else:
            cursor.execute("INSERT INTO topics (name) VALUES (?)", (topic_name,))
            topic_id = cursor.lastrowid
        
        cursor.execute(
            "INSERT OR IGNORE INTO teachers (id, full_name, topic_id, telegram_id) VALUES (?, ?, ?, ?)",
            (id_, full_name, topic_id, telegram_id)
        )

conn.commit()
conn.close()

