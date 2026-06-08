import sqlite3
from datetime import datetime, date
import random
import os

DB_PATH = os.path.join(os.path.dirname(__file__), 'sks_quest.db')

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    cursor = conn.cursor()
    
    # Таблица клиентов
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS clients (
            id INTEGER PRIMARY KEY,
            phone TEXT,
            name TEXT,
            balance INTEGER DEFAULT 350,
            streak INTEGER DEFAULT 5,
            status_level TEXT DEFAULT 'Золотой',
            last_checkin TEXT,
            last_spin TEXT
        )
    ''')
    
    # Таблица квестов
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS quests (
            id INTEGER PRIMARY KEY,
            title TEXT,
            description TEXT,
            reward INTEGER,
            type TEXT,
            cooldown_days INTEGER DEFAULT 1
        )
    ''')
    
    # Таблица выполненных квестов
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS completed_quests (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            client_id INTEGER,
            quest_id INTEGER,
            completed_date TEXT
        )
    ''')
    
    # Таблица слов для Wordle
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS wordle_words (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            word TEXT NOT NULL
        )
    ''')
    
    # Таблица призов для колеса
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS wheel_prizes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            value INTEGER DEFAULT 0
        )
    ''')
    
    # ========== ЗАПОЛНЯЕМ ДАННЫМИ ==========
    
    # Клиент
    cursor.execute("SELECT * FROM clients WHERE id = 1")
    if not cursor.fetchone():
        cursor.execute("INSERT INTO clients (id, phone, name) VALUES (1, '+79991234567', 'Алексей')")
    
    # Квесты
    cursor.execute("SELECT * FROM quests")
    if not cursor.fetchone():
        cursor.execute("INSERT INTO quests (id, title, description, reward, type, cooldown_days) VALUES (1, 'Слово дня', 'Угадай слово из 5 букв', 30, 'wordgame', 1)")
        cursor.execute("INSERT INTO quests (id, title, description, reward, type, cooldown_days) VALUES (2, 'Викторина', 'Ответь на вопросы о золоте', 25, 'quiz', 3)")
        cursor.execute("INSERT INTO quests (id, title, description, reward, type, cooldown_days) VALUES (3, 'Колесо фортуны', 'Покрути колесо и получи приз', 25, 'wheel', 7)")
    
    # Слова для Wordle
    cursor.execute("SELECT * FROM wordle_words")
    if not cursor.fetchone():
        words = ['ЗОЛОТО', 'СЛИТОК', 'АЛМАЗ', 'РУБИН', 'САПФИР', 'ИЗУМРД', 'БРИЛЛ', 'ЖЕМЧУ', 'ОПАЛЫ', 'АГАТЫ']
        for w in words:
            cursor.execute("INSERT INTO wordle_words (word) VALUES (?)", (w,))
    
    # Призы для колеса
    cursor.execute("SELECT * FROM wheel_prizes")
    if not cursor.fetchone():
        prizes = [
            ('10 бонусов', 10),
            ('20 бонусов', 20),
            ('50 бонусов', 50),
            ('100 бонусов', 100),
            ('Спасибо за участие', 0),
        ]
        for name, val in prizes:
            cursor.execute("INSERT INTO wheel_prizes (name, value) VALUES (?, ?)", (name, val))
    
    conn.commit()
    conn.close()
    print("База данных готова!")

# ========== ФУНКЦИИ ДЛЯ API ==========

def get_wordle_word():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT word FROM wordle_words ORDER BY RANDOM() LIMIT 1")
    row = cursor.fetchone()
    conn.close()
    return row[0] if row else 'ЗОЛОТО'

def get_wheel_prize():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT name, value FROM wheel_prizes ORDER BY RANDOM() LIMIT 1")
    row = cursor.fetchone()
    conn.close()
    return {'name': row[0], 'value': row[1]} if row else {'name': '10 бонусов', 'value': 10}

def get_client(client_id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT id, phone, name, balance, streak, status_level, last_checkin FROM clients WHERE id = ?", (client_id,))
    row = cursor.fetchone()
    conn.close()
    return dict(row) if row else None

def do_checkin(client_id):
    conn = get_db()
    cursor = conn.cursor()
    today = date.today().isoformat()
    
    cursor.execute("SELECT balance, streak, last_checkin FROM clients WHERE id = ?", (client_id,))
    row = cursor.fetchone()
    
    if row['last_checkin'] == today:
        conn.close()
        return None
    
    new_balance = row['balance'] + 5
    new_streak = row['streak'] + 1
    cursor.execute("UPDATE clients SET balance = ?, streak = ?, last_checkin = ? WHERE id = ?", (new_balance, new_streak, today, client_id))
    conn.commit()
    conn.close()
    return {'new_balance': new_balance, 'new_streak': new_streak}

def get_quests(client_id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT id, title, description, reward, type, cooldown_days FROM quests")
    quests = cursor.fetchall()
    cursor.execute("SELECT quest_id FROM completed_quests WHERE client_id = ?", (client_id,))
    completed = [row['quest_id'] for row in cursor.fetchall()]
    conn.close()
    
    result = []
    for q in quests:
        result.append({
            'id': q['id'],
            'title': q['title'],
            'description': q['description'],
            'reward': q['reward'],
            'type': q['type'],
            'cooldown_days': q['cooldown_days'],
            'completed': q['id'] in completed
        })
    return result

def complete_quest(client_id, quest_id):
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute("SELECT reward FROM quests WHERE id = ?", (quest_id,))
    quest = cursor.fetchone()
    if not quest:
        conn.close()
        return None
    
    cursor.execute("SELECT * FROM completed_quests WHERE client_id = ? AND quest_id = ?", (client_id, quest_id))
    if cursor.fetchone():
        conn.close()
        return None
    
    now = datetime.now().isoformat()
    cursor.execute("INSERT INTO completed_quests (client_id, quest_id, completed_date) VALUES (?, ?, ?)", (client_id, quest_id, now))
    cursor.execute("UPDATE clients SET balance = balance + ? WHERE id = ?", (quest['reward'], client_id))
    cursor.execute("SELECT balance FROM clients WHERE id = ?", (client_id,))
    new_balance = cursor.fetchone()[0]
    
    conn.commit()
    conn.close()
    return {'reward': quest['reward'], 'new_balance': new_balance}