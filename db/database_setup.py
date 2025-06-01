import sqlite3
import os

DATABASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE_NAME = os.path.join(DATABASE_DIR, 'gym_management.db')

def create_connection():
    """创建数据库连接到SQLite数据库"""
    conn = None
    try:
        conn = sqlite3.connect(DATABASE_NAME)
        return conn
    except sqlite3.Error as e:
        print(f"数据库连接错误: {e}")
    return conn

def create_tables():
    """创建数据库表"""
    conn = create_connection()
    if conn is not None:
        try:
            cursor = conn.cursor()
            # 会员表
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS members (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    gender TEXT,
                    birth_date TEXT,
                    phone TEXT UNIQUE,
                    emergency_contact_name TEXT,
                    emergency_contact_phone TEXT,
                    health_notes TEXT,
                    join_date TEXT NOT NULL,
                    membership_card_id INTEGER, 
                    status TEXT DEFAULT 'active' 
                );
            """)
            # 会员卡类型表
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS membership_card_types (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL UNIQUE,
                    price REAL NOT NULL,
                    duration_days INTEGER NOT NULL,
                    description TEXT
                );
            """)
            # 会员卡实例表
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS member_cards (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    member_id INTEGER NOT NULL,
                    card_type_id INTEGER NOT NULL,
                    purchase_date TEXT NOT NULL,
                    expiry_date TEXT NOT NULL,
                    status TEXT DEFAULT 'active', -- active, frozen, expired
                    FOREIGN KEY (member_id) REFERENCES members (id),
                    FOREIGN KEY (card_type_id) REFERENCES membership_card_types (id)
                );
            """)
            # 课程表
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS courses (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL UNIQUE,
                    description TEXT,
                    default_duration_minutes INTEGER,
                    status TEXT DEFAULT 'active' -- active, inactive
                );
            """)
            # 教练表
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS trainers (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    specialty TEXT,
                    contact_info TEXT,
                    status TEXT DEFAULT 'active' -- active, inactive
                );
            """)
            conn.commit()
            print("数据库表创建成功或已存在。")
        except sqlite3.Error as e:
            print(f"创建表时出错: {e}")
        finally:
            conn.close()
    else:
        print("错误！无法创建数据库连接。")

if __name__ == '__main__':
    # 确保db目录存在
    if not os.path.exists(DATABASE_DIR):
        os.makedirs(DATABASE_DIR)
    create_tables()
