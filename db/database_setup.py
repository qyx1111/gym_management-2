import sqlite3
import os

DATABASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE_NAME = os.path.join(DATABASE_DIR, 'gym_management.db')

def create_connection():
    """创建数据库连接到SQLite数据库"""
    conn = None
    try:
        conn = sqlite3.connect(DATABASE_NAME)
        conn.execute("PRAGMA foreign_keys = ON") # 确保外键约束被激活
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
            # 会员卡实例表 (会员拥有的卡) - 这是“会员与会员卡的关系表”
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS member_cards (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    member_id INTEGER NOT NULL,
                    card_type_id INTEGER NOT NULL,
                    purchase_date TEXT NOT NULL,
                    activation_date TEXT, 
                    expiry_date TEXT NOT NULL,
                    status TEXT DEFAULT 'pending_activation', -- e.g., pending_activation, active, frozen, expired, cancelled
                    notes TEXT,
                    FOREIGN KEY (member_id) REFERENCES members (id) ON DELETE CASCADE,
                    FOREIGN KEY (card_type_id) REFERENCES membership_card_types (id) ON DELETE RESTRICT
                );
            """)
            # 课程表
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS courses (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL UNIQUE,
                    description TEXT,
                    default_duration_minutes INTEGER,
                    status TEXT DEFAULT 'active' 
                );
            """)
            # 教练表
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS trainers (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    specialty TEXT,
                    contact_info TEXT,
                    status TEXT DEFAULT 'active' 
                );
            """)

            # 新增：会员与课程的报名/关系表
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS member_course_enrollments (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    member_id INTEGER NOT NULL,
                    course_id INTEGER NOT NULL,
                    enrollment_date TEXT NOT NULL,
                    status TEXT DEFAULT 'enrolled', -- e.g., enrolled, completed, dropped
                    notes TEXT,
                    FOREIGN KEY (member_id) REFERENCES members (id) ON DELETE CASCADE,
                    FOREIGN KEY (course_id) REFERENCES courses (id) ON DELETE CASCADE 
                );
            """)

            # 新增：会员与教练的分配/关系表
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS member_trainer_assignments (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    member_id INTEGER NOT NULL,
                    trainer_id INTEGER NOT NULL,
                    assignment_date TEXT NOT NULL,
                    assignment_type TEXT, -- e.g., personal_training_package, consultation
                    notes TEXT,
                    FOREIGN KEY (member_id) REFERENCES members (id) ON DELETE CASCADE,
                    FOREIGN KEY (trainer_id) REFERENCES trainers (id) ON DELETE CASCADE
                );
            """)

            # 新增：教练与课程的分配/关系表
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS trainer_course_assignments (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    trainer_id INTEGER NOT NULL,
                    course_id INTEGER NOT NULL,
                    assignment_date TEXT NOT NULL,
                    course_type TEXT, -- e.g., regular, special, private, group
                    notes TEXT,
                    FOREIGN KEY (trainer_id) REFERENCES trainers (id) ON DELETE CASCADE,
                    FOREIGN KEY (course_id) REFERENCES courses (id) ON DELETE CASCADE
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
    if not os.path.exists(DATABASE_DIR):
        os.makedirs(DATABASE_DIR)
    create_tables()
