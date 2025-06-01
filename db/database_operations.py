import sqlite3
from .database_setup import create_connection, DATABASE_NAME
from datetime import datetime

def add_member(name, gender, birth_date, phone, emergency_contact_name, emergency_contact_phone, health_notes):
    """添加新会员"""
    conn = create_connection()
    if not conn:
        return False, "数据库连接失败"
    
    sql = ''' INSERT INTO members(name, gender, birth_date, phone, emergency_contact_name, emergency_contact_phone, health_notes, join_date)
              VALUES(?,?,?,?,?,?,?,?) '''
    try:
        cursor = conn.cursor()
        join_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cursor.execute(sql, (name, gender, birth_date, phone, emergency_contact_name, emergency_contact_phone, health_notes, join_date))
        conn.commit()
        return True, "会员添加成功"
    except sqlite3.IntegrityError: # 比如电话号码重复
        return False, "添加失败：电话号码可能已存在。"
    except sqlite3.Error as e:
        return False, f"添加会员时发生数据库错误: {e}"
    finally:
        conn.close()

def get_all_members():
    """获取所有会员信息"""
    conn = create_connection()
    if not conn:
        return []
    
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT id, name, gender, birth_date, phone, emergency_contact_name, emergency_contact_phone, health_notes, join_date, status FROM members ORDER BY id DESC")
        members = cursor.fetchall()
        return members
    except sqlite3.Error as e:
        print(f"查询会员时发生错误: {e}")
        return []
    finally:
        conn.close()

def search_members(search_term):
    """根据姓名或电话搜索会员"""
    conn = create_connection()
    if not conn:
        return []
    try:
        cursor = conn.cursor()
        query = """
            SELECT id, name, gender, birth_date, phone, emergency_contact_name, 
                   emergency_contact_phone, health_notes, join_date, status 
            FROM members 
            WHERE name LIKE ? OR phone LIKE ?
            ORDER BY id DESC
        """
        like_term = f"%{search_term}%"
        cursor.execute(query, (like_term, like_term))
        members = cursor.fetchall()
        return members
    except sqlite3.Error as e:
        print(f"搜索会员时发生错误: {e}")
        return []
    finally:
        conn.close()

def get_member_by_id(member_id):
    """通过ID获取单个会员信息"""
    conn = create_connection()
    if not conn:
        return None
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM members WHERE id = ?", (member_id,))
        member = cursor.fetchone()
        return member
    except sqlite3.Error as e:
        print(f"查询会员 (ID: {member_id}) 时发生错误: {e}")
        return None
    finally:
        conn.close()

def update_member(member_id, name, gender, birth_date, phone, emergency_contact_name, emergency_contact_phone, health_notes, status):
    """更新会员信息"""
    conn = create_connection()
    if not conn:
        return False, "数据库连接失败"
    
    sql = ''' UPDATE members
              SET name = ?,
                  gender = ?,
                  birth_date = ?,
                  phone = ?,
                  emergency_contact_name = ?,
                  emergency_contact_phone = ?,
                  health_notes = ?,
                  status = ?
              WHERE id = ? '''
    try:
        cursor = conn.cursor()
        cursor.execute(sql, (name, gender, birth_date, phone, emergency_contact_name, emergency_contact_phone, health_notes, status, member_id))
        conn.commit()
        if cursor.rowcount == 0:
            return False, "未找到该会员或信息无变化"
        return True, "会员信息更新成功"
    except sqlite3.IntegrityError:
        return False, "更新失败：电话号码可能与他人重复。"
    except sqlite3.Error as e:
        return False, f"更新会员时发生数据库错误: {e}"
    finally:
        conn.close()

def delete_member_logically(member_id):
    """逻辑删除会员 (将其状态标记为inactive)"""
    conn = create_connection()
    if not conn:
        return False, "数据库连接失败"
    
    sql = ''' UPDATE members
              SET status = 'inactive'
              WHERE id = ? AND status != 'inactive' '''
    try:
        cursor = conn.cursor()
        cursor.execute(sql, (member_id,))
        conn.commit()
        if cursor.rowcount == 0:
            return False, "未找到该会员或会员已为非活动状态"
        return True, "会员已设为非活动状态"
    except sqlite3.Error as e:
        return False, f"逻辑删除会员时发生数据库错误: {e}"
    finally:
        conn.close()

# --- Membership Card Type Operations ---

def add_card_type(name, price, duration_days, description):
    """添加新的会员卡类型"""
    conn = create_connection()
    if not conn:
        return False, "数据库连接失败"
    
    sql = ''' INSERT INTO membership_card_types(name, price, duration_days, description)
              VALUES(?,?,?,?) '''
    try:
        cursor = conn.cursor()
        cursor.execute(sql, (name, price, duration_days, description))
        conn.commit()
        return True, "会员卡类型添加成功"
    except sqlite3.IntegrityError: # 比如名称重复
        return False, "添加失败：会员卡类型名称可能已存在。"
    except sqlite3.Error as e:
        return False, f"添加会员卡类型时发生数据库错误: {e}"
    finally:
        conn.close()

def get_all_card_types():
    """获取所有会员卡类型信息"""
    conn = create_connection()
    if not conn:
        return []
    
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT id, name, price, duration_days, description FROM membership_card_types ORDER BY id DESC")
        card_types = cursor.fetchall()
        return card_types
    except sqlite3.Error as e:
        print(f"查询会员卡类型时发生错误: {e}")
        return []
    finally:
        conn.close()

def search_card_types(search_term):
    """根据名称搜索会员卡类型"""
    conn = create_connection()
    if not conn:
        return []
    try:
        cursor = conn.cursor()
        query = """
            SELECT id, name, price, duration_days, description 
            FROM membership_card_types
            WHERE name LIKE ?
            ORDER BY id DESC
        """
        like_term = f"%{search_term}%"
        cursor.execute(query, (like_term,))
        card_types = cursor.fetchall()
        return card_types
    except sqlite3.Error as e:
        print(f"搜索会员卡类型时发生错误: {e}")
        return []
    finally:
        conn.close()

def get_card_type_by_id(card_type_id):
    """通过ID获取单个会员卡类型信息"""
    conn = create_connection()
    if not conn:
        return None
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT id, name, price, duration_days, description FROM membership_card_types WHERE id = ?", (card_type_id,))
        card_type = cursor.fetchone()
        return card_type
    except sqlite3.Error as e:
        print(f"查询会员卡类型 (ID: {card_type_id}) 时发生错误: {e}")
        return None
    finally:
        conn.close()

def update_card_type(card_type_id, name, price, duration_days, description):
    """更新会员卡类型信息"""
    conn = create_connection()
    if not conn:
        return False, "数据库连接失败"
    
    sql = ''' UPDATE membership_card_types
              SET name = ?,
                  price = ?,
                  duration_days = ?,
                  description = ?
              WHERE id = ? '''
    try:
        cursor = conn.cursor()
        cursor.execute(sql, (name, price, duration_days, description, card_type_id))
        conn.commit()
        if cursor.rowcount == 0:
            return False, "未找到该会员卡类型或信息无变化"
        return True, "会员卡类型信息更新成功"
    except sqlite3.IntegrityError:
        return False, "更新失败：会员卡类型名称可能与现有类型重复。"
    except sqlite3.Error as e:
        return False, f"更新会员卡类型时发生数据库错误: {e}"
    finally:
        conn.close()

def delete_card_type(card_type_id):
    """删除会员卡类型 (物理删除)"""
    # 注意：如果已有会员卡实例关联此类型，可能需要更复杂的处理或阻止删除
    conn = create_connection()
    if not conn:
        return False, "数据库连接失败"
    
    sql = 'DELETE FROM membership_card_types WHERE id = ?'
    try:
        cursor = conn.cursor()
        cursor.execute(sql, (card_type_id,))
        conn.commit()
        if cursor.rowcount == 0:
            return False, "未找到该会员卡类型"
        return True, "会员卡类型删除成功"
    except sqlite3.Error as e:
        # 检查是否因为外键约束导致删除失败
        if "FOREIGN KEY constraint failed" in str(e):
            return False, f"删除失败：该会员卡类型可能已被会员卡实例使用。请先处理关联的会员卡。"
        return False, f"删除会员卡类型时发生数据库错误: {e}"
    finally:
        conn.close()

# --- Trainer Operations ---

def add_trainer(name, specialty, contact_info):
    """添加新教练"""
    conn = create_connection()
    if not conn:
        return False, "数据库连接失败"
    
    sql = ''' INSERT INTO trainers(name, specialty, contact_info, status)
              VALUES(?,?,?, 'active') '''
    try:
        cursor = conn.cursor()
        cursor.execute(sql, (name, specialty, contact_info))
        conn.commit()
        return True, "教练添加成功"
    except sqlite3.Error as e:
        return False, f"添加教练时发生数据库错误: {e}"
    finally:
        conn.close()

def get_all_trainers(active_only=False): # Modified to accept active_only flag
    """获取所有教练信息"""
    conn = create_connection()
    if not conn:
        return []
    
    try:
        cursor = conn.cursor()
        if active_only:
            cursor.execute("SELECT id, name, specialty, contact_info, status FROM trainers WHERE status = 'active' ORDER BY name")
        else:
            cursor.execute("SELECT id, name, specialty, contact_info, status FROM trainers ORDER BY id DESC")
        trainers = cursor.fetchall()
        return trainers
    except sqlite3.Error as e:
        print(f"查询教练时发生错误: {e}")
        return []
    finally:
        conn.close()

def search_trainers(search_term):
    """根据姓名或专长搜索教练"""
    conn = create_connection()
    if not conn:
        return []
    try:
        cursor = conn.cursor()
        query = """
            SELECT id, name, specialty, contact_info, status 
            FROM trainers 
            WHERE (name LIKE ? OR specialty LIKE ?) AND status = 'active'
            ORDER BY name
        """
        # 使用 % 通配符进行模糊匹配
        term = f"%{search_term}%"
        cursor.execute(query, (term, term))
        trainers = cursor.fetchall()
        return trainers
    except sqlite3.Error as e:
        print(f"搜索教练时发生错误: {e}")
        return []
    finally:
        conn.close()

def get_trainer_by_id(trainer_id):
    """通过ID获取单个教练信息"""
    conn = create_connection()
    if not conn:
        return None
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT id, name, specialty, contact_info, status FROM trainers WHERE id = ?", (trainer_id,))
        trainer = cursor.fetchone()
        return trainer
    except sqlite3.Error as e:
        print(f"查询教练 (ID: {trainer_id}) 时发生错误: {e}")
        return None
    finally:
        conn.close()

def update_trainer(trainer_id, name, specialty, contact_info, status):
    """更新教练信息"""
    conn = create_connection()
    if not conn:
        return False, "数据库连接失败"
    
    sql = ''' UPDATE trainers
              SET name = ?,
                  specialty = ?,
                  contact_info = ?,
                  status = ?
              WHERE id = ? '''
    try:
        cursor = conn.cursor()
        cursor.execute(sql, (name, specialty, contact_info, status, trainer_id))
        conn.commit()
        if cursor.rowcount == 0:
            return False, "未找到该教练或信息无变化"
        return True, "教练信息更新成功"
    except sqlite3.Error as e:
        return False, f"更新教练时发生数据库错误: {e}"
    finally:
        conn.close()

def delete_trainer_logically(trainer_id):
    """逻辑删除教练 (将其状态标记为inactive)"""
    conn = create_connection()
    if not conn:
        return False, "数据库连接失败"
    
    sql = ''' UPDATE trainers
              SET status = 'inactive'
              WHERE id = ? AND status != 'inactive' '''
    try:
        cursor = conn.cursor()
        cursor.execute(sql, (trainer_id,))
        conn.commit()
        if cursor.rowcount == 0:
            return False, "未找到该教练或教练已为非活动状态"
        return True, "教练已设为非活动状态"
    except sqlite3.Error as e:
        return False, f"逻辑删除教练时发生数据库错误: {e}"

# --- Course Operations ---

def add_course(name, description, default_duration_minutes):
    """添加新课程"""
    conn = create_connection()
    if not conn:
        return False, "数据库连接失败"
    
    sql = ''' INSERT INTO courses(name, description, default_duration_minutes, status)
              VALUES(?,?,?, 'active') '''
    try:
        cursor = conn.cursor()
        cursor.execute(sql, (name, description, default_duration_minutes))
        conn.commit()
        return True, "课程添加成功"
    except sqlite3.IntegrityError: # 课程名称唯一
        return False, "添加失败：课程名称可能已存在。"
    except sqlite3.Error as e:
        return False, f"添加课程时发生数据库错误: {e}"
    finally:
        conn.close()

def get_all_courses(active_only=False): # Modified to accept active_only flag
    """获取所有课程信息"""
    conn = create_connection()
    if not conn:
        return []
    
    try:
        cursor = conn.cursor()
        if active_only:
            cursor.execute("SELECT id, name, description, default_duration_minutes, status FROM courses WHERE status = 'active' ORDER BY name")
        else:
            cursor.execute("SELECT id, name, description, default_duration_minutes, status FROM courses ORDER BY id DESC")
        courses = cursor.fetchall()
        return courses
    except sqlite3.Error as e:
        print(f"查询课程时发生错误: {e}")
        return []
    finally:
        conn.close()

def search_courses(search_term):
    """根据名称搜索课程"""
    conn = create_connection()
    if not conn:
        return []
    try:
        cursor = conn.cursor()
        query = """
            SELECT id, name, description, default_duration_minutes, status 
            FROM courses
            WHERE name LIKE ?
            ORDER BY id DESC
        """
        like_term = f"%{search_term}%"
        cursor.execute(query, (like_term,))
        courses = cursor.fetchall()
        return courses
    except sqlite3.Error as e:
        print(f"搜索课程时发生错误: {e}")
        return []
    finally:
        conn.close()

def get_course_by_id(course_id):
    """通过ID获取单个课程信息"""
    conn = create_connection()
    if not conn:
        return None
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT id, name, description, default_duration_minutes, status FROM courses WHERE id = ?", (course_id,))
        course = cursor.fetchone()
        return course
    except sqlite3.Error as e:
        print(f"查询课程 (ID: {course_id}) 时发生错误: {e}")
        return None
    finally:
        conn.close()

def update_course(course_id, name, description, default_duration_minutes, status):
    """更新课程信息"""
    conn = create_connection()
    if not conn:
        return False, "数据库连接失败"
    
    sql = ''' UPDATE courses
              SET name = ?,
                  description = ?,
                  default_duration_minutes = ?,
                  status = ?
              WHERE id = ? '''
    try:
        cursor = conn.cursor()
        cursor.execute(sql, (name, description, default_duration_minutes, status, course_id))
        conn.commit()
        if cursor.rowcount == 0:
            return False, "未找到该课程或信息无变化"
        return True, "课程信息更新成功"
    except sqlite3.IntegrityError:
         return False, "更新失败：课程名称可能与现有课程重复。"
    except sqlite3.Error as e:
        return False, f"更新课程时发生数据库错误: {e}"
    finally:
        conn.close()

def delete_course_logically(course_id):
    """逻辑删除课程 (将其状态标记为inactive)"""
    conn = create_connection()
    if not conn:
        return False, "数据库连接失败"
    
    sql = ''' UPDATE courses
              SET status = 'inactive'
              WHERE id = ? AND status != 'inactive' '''
    try:
        cursor = conn.cursor()
        cursor.execute(sql, (course_id,))
        conn.commit()
        if cursor.rowcount == 0:
            return False, "未找到该课程或课程已为非活动状态"
        return True, "课程已设为非活动状态"
    except sqlite3.Error as e:
        return False, f"逻辑删除课程时发生数据库错误: {e}"
    finally:
        conn.close()

# --- 其他模块的数据库操作函数将在此处添加 ---

# --- Member Card Instance Operations ---

def assign_card_to_member(member_id, card_type_id, purchase_date, activation_date, expiry_date, status, notes):
    """为会员办理新卡"""
    conn = create_connection()
    if not conn:
        return False, "数据库连接失败"
    sql = '''INSERT INTO member_cards (member_id, card_type_id, purchase_date, activation_date, expiry_date, status, notes)
             VALUES (?, ?, ?, ?, ?, ?, ?)'''
    try:
        cursor = conn.cursor()
        cursor.execute(sql, (member_id, card_type_id, purchase_date, activation_date, expiry_date, status, notes))
        conn.commit()
        return True, "会员卡办理成功"
    except sqlite3.Error as e:
        return False, f"办理会员卡时发生数据库错误: {e}"
    finally:
        conn.close()

def get_cards_for_member(member_id):
    """获取指定会员的所有会员卡信息"""
    conn = create_connection()
    if not conn:
        return []
    sql = """
        SELECT mc.id, mct.name, mc.purchase_date, mc.activation_date, mc.expiry_date, mc.status, mc.notes, mc.card_type_id
        FROM member_cards mc
        JOIN membership_card_types mct ON mc.card_type_id = mct.id
        WHERE mc.member_id = ?
        ORDER BY mc.purchase_date DESC
    """
    try:
        cursor = conn.cursor()
        cursor.execute(sql, (member_id,))
        return cursor.fetchall()
    except sqlite3.Error as e:
        print(f"查询会员卡信息时发生错误: {e}")
        return []
    finally:
        conn.close()

def get_member_card_details(member_card_id):
    """获取特定会员卡实例的详细信息"""
    conn = create_connection()
    if not conn:
        return None
    sql = "SELECT id, member_id, card_type_id, purchase_date, activation_date, expiry_date, status, notes FROM member_cards WHERE id = ?"
    try:
        cursor = conn.cursor()
        cursor.execute(sql, (member_card_id,))
        return cursor.fetchone()
    except sqlite3.Error as e:
        print(f"获取会员卡详情时出错: {e}")
        return None
    finally:
        conn.close()


def update_member_card_details(member_card_id, card_type_id, purchase_date, activation_date, expiry_date, status, notes):
    """更新会员卡信息"""
    conn = create_connection()
    if not conn:
        return False, "数据库连接失败"
    sql = '''UPDATE member_cards 
             SET card_type_id = ?, purchase_date = ?, activation_date = ?, expiry_date = ?, status = ?, notes = ?
             WHERE id = ?'''
    try:
        cursor = conn.cursor()
        cursor.execute(sql, (card_type_id, purchase_date, activation_date, expiry_date, status, notes, member_card_id))
        conn.commit()
        if cursor.rowcount == 0:
            return False, "未找到该会员卡或信息无变化"
        return True, "会员卡信息更新成功"
    except sqlite3.Error as e:
        return False, f"更新会员卡信息时发生数据库错误: {e}"
    finally:
        conn.close()

def delete_member_card(member_card_id):
    """删除会员的某张卡"""
    conn = create_connection()
    if not conn:
        return False, "数据库连接失败"
    sql = "DELETE FROM member_cards WHERE id = ?"
    try:
        cursor = conn.cursor()
        cursor.execute(sql, (member_card_id,))
        conn.commit()
        if cursor.rowcount == 0:
            return False, "未找到要删除的会员卡"
        return True, "会员卡删除成功"
    except sqlite3.Error as e:
        return False, f"删除会员卡时发生数据库错误: {e}"
    finally:
        conn.close()

# --- Member Course Enrollment Operations ---

def enroll_member_in_course(member_id, course_id, enrollment_date, status='enrolled', notes=''):
    """为会员报名课程"""
    conn = create_connection()
    if not conn:
        return False, "数据库连接失败"
    sql = '''INSERT INTO member_course_enrollments (member_id, course_id, enrollment_date, status, notes)
             VALUES (?, ?, ?, ?, ?)'''
    try:
        cursor = conn.cursor()
        if isinstance(enrollment_date, (datetime, datetime.date)):
            enrollment_date_str = enrollment_date.strftime('%Y-%m-%d')
        else:
            enrollment_date_str = enrollment_date # Assume it's already a string in correct format

        cursor.execute(sql, (member_id, course_id, enrollment_date_str, status, notes))
        conn.commit()
        return True, "课程报名成功"
    except sqlite3.Error as e:
        return False, f"课程报名时发生数据库错误: {e}"
    finally:
        conn.close()

def get_enrollments_for_member(member_id):
    """获取指定会员的所有课程报名信息"""
    conn = create_connection()
    if not conn:
        return []
    sql = """
        SELECT mce.id, c.name, mce.enrollment_date, mce.status, mce.notes, mce.course_id
        FROM member_course_enrollments mce
        JOIN courses c ON mce.course_id = c.id
        WHERE mce.member_id = ?
        ORDER BY mce.enrollment_date DESC
    """
    try:
        cursor = conn.cursor()
        cursor.execute(sql, (member_id,))
        return cursor.fetchall() # (mce.id, c.name, mce.enrollment_date, mce.status, mce.notes, mce.course_id)
    except sqlite3.Error as e:
        print(f"查询会员课程报名信息时发生错误: {e}")
        return []
    finally:
        conn.close()

def get_member_enrollment_details(enrollment_id):
    """获取特定课程报名记录的详细信息"""
    conn = create_connection()
    if not conn:
        return None
    sql = "SELECT id, member_id, course_id, enrollment_date, status, notes FROM member_course_enrollments WHERE id = ?"
    try:
        cursor = conn.cursor()
        cursor.execute(sql, (enrollment_id,))
        return cursor.fetchone() # (id, member_id, course_id, enrollment_date, status, notes)
    except sqlite3.Error as e:
        print(f"获取课程报名详情时出错: {e}")
        return None
    finally:
        conn.close()

def update_enrollment_details(enrollment_id, course_id, enrollment_date, status, notes):
    """更新课程报名信息"""
    conn = create_connection()
    if not conn:
        return False, "数据库连接失败"
    sql = '''UPDATE member_course_enrollments
             SET course_id = ?, enrollment_date = ?, status = ?, notes = ?
             WHERE id = ?'''
    try:
        cursor = conn.cursor()
        if isinstance(enrollment_date, (datetime, datetime.date)):
            enrollment_date_str = enrollment_date.strftime('%Y-%m-%d')
        else:
            enrollment_date_str = enrollment_date

        cursor.execute(sql, (course_id, enrollment_date_str, status, notes, enrollment_id))
        conn.commit()
        if cursor.rowcount == 0:
            return False, "未找到该报名记录或信息无变化"
        return True, "课程报名信息更新成功"
    except sqlite3.Error as e:
        return False, f"更新课程报名信息时发生数据库错误: {e}"
    finally:
        conn.close()

def unenroll_member_from_course(enrollment_id):
    """取消会员的课程报名"""
    conn = create_connection()
    if not conn:
        return False, "数据库连接失败"
    sql = "DELETE FROM member_course_enrollments WHERE id = ?"
    try:
        cursor = conn.cursor()
        cursor.execute(sql, (enrollment_id,))
        conn.commit()
        if cursor.rowcount == 0:
            return False, "未找到要取消的报名记录"
        return True, "课程报名取消成功"
    except sqlite3.Error as e:
        return False, f"取消课程报名时发生数据库错误: {e}"
    finally:
        conn.close()

# --- Member Trainer Assignment Operations ---

def assign_trainer_to_member(member_id, trainer_id, assignment_date, assignment_type='', notes=''):
    """为会员指派教练"""
    conn = create_connection()
    if not conn:
        return False, "数据库连接失败"
    sql = '''INSERT INTO member_trainer_assignments (member_id, trainer_id, assignment_date, assignment_type, notes)
             VALUES (?, ?, ?, ?, ?)'''
    try:
        cursor = conn.cursor()
        # Ensure assignment_date is in 'YYYY-MM-DD' format if it's a date object
        if isinstance(assignment_date, (datetime, datetime.date)):
            assignment_date_str = assignment_date.strftime('%Y-%m-%d')
        else:
            assignment_date_str = assignment_date # Assume it's already a string in correct format

        cursor.execute(sql, (member_id, trainer_id, assignment_date_str, assignment_type, notes))
        conn.commit()
        return True, "教练指派成功"
    except sqlite3.Error as e:
        return False, f"教练指派时发生数据库错误: {e}"
    finally:
        conn.close()

def get_assignments_for_member(member_id):
    """获取指定会员的所有教练指派信息"""
    conn = create_connection()
    if not conn:
        return []
    sql = """
        SELECT mta.id, t.name, mta.assignment_date, mta.assignment_type, mta.notes, mta.trainer_id
        FROM member_trainer_assignments mta
        JOIN trainers t ON mta.trainer_id = t.id
        WHERE mta.member_id = ?
        ORDER BY mta.assignment_date DESC
    """
    try:
        cursor = conn.cursor()
        cursor.execute(sql, (member_id,))
        return cursor.fetchall()
    except sqlite3.Error as e:
        print(f"查询会员教练指派信息时发生错误: {e}")
        return []
    finally:
        conn.close()

def get_member_assignment_details(assignment_id):
    """获取特定教练指派记录的详细信息"""
    conn = create_connection()
    if not conn:
        return None
    sql = "SELECT id, member_id, trainer_id, assignment_date, assignment_type, notes FROM member_trainer_assignments WHERE id = ?"
    try:
        cursor = conn.cursor()
        cursor.execute(sql, (assignment_id,))
        return cursor.fetchone() # (id, member_id, trainer_id, assignment_date, assignment_type, notes)
    except sqlite3.Error as e:
        print(f"获取教练指派详情时出错: {e}")
        return None
    finally:
        conn.close()

def update_assignment_details(assignment_id, trainer_id, assignment_date, assignment_type, notes):
    """更新教练指派信息"""
    conn = create_connection()
    if not conn:
        return False, "数据库连接失败"
    sql = '''UPDATE member_trainer_assignments
             SET trainer_id = ?, assignment_date = ?, assignment_type = ?, notes = ?
             WHERE id = ?'''
    try:
        cursor = conn.cursor()
        if isinstance(assignment_date, (datetime, datetime.date)):
            assignment_date_str = assignment_date.strftime('%Y-%m-%d')
        else:
            assignment_date_str = assignment_date

        cursor.execute(sql, (trainer_id, assignment_date_str, assignment_type, notes, assignment_id))
        conn.commit()
        if cursor.rowcount == 0:
            return False, "未找到该指派记录或信息无变化"
        return True, "教练指派信息更新成功"
    except sqlite3.Error as e:
        return False, f"更新教练指派信息时发生数据库错误: {e}"
    finally:
        conn.close()

def unassign_trainer_from_member(assignment_id):
    """解除会员的教练指派"""
    conn = create_connection()
    if not conn:
        return False, "数据库连接失败"
    sql = "DELETE FROM member_trainer_assignments WHERE id = ?"
    try:
        cursor = conn.cursor()
        cursor.execute(sql, (assignment_id,))
        conn.commit()
        if cursor.rowcount == 0:
            return False, "未找到要解除的指派记录"
        return True, "教练指派解除成功"
    except sqlite3.Error as e:
        return False, f"解除教练指派时发生数据库错误: {e}"
    finally:
        conn.close()
