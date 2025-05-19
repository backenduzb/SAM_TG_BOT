import sqlite3

def get_teacher_id(teacher_name):
    conn = sqlite3.connect("data/base.db")
    cursor = conn.cursor()

    cursor.execute("""
        SELECT telegram_id
        FROM teachers
        WHERE full_name = ?
    """, (teacher_name.strip(),))  

    result = cursor.fetchone()
    conn.close()

    if result:  
        return result[0] 
    else:
        return None  

def get_teacher_id(teacher_name):
    conn = sqlite3.connect("data/base.db")
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id
        FROM teachers
        WHERE full_name = ?
    """, (teacher_name.strip(),))  

    result = cursor.fetchone()
    conn.close()

    if result:  
        return result[0] 
    else:
        return None  
