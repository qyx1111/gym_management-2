# NUAA健身房管理系统数据库课设实验报告

**项目： NUAA健身房管理系统**
**学号： 162220312**
**姓名： 邱裕轩**
**班级： 1622203**
**指导老师：周良**

## 目录

[TOC]

## 一、实验环境

**前端： HTML5 + CSS3 + JavaScript ** 
**后端： Python Flask框架** 
**数据库： SQLite**
**开发工具： Visual Studio Code** 
**操作系统： Windows** 
**API架构： RESTful API**

## 二、项目组织

```
Database/
├── backend/
│   ├── app.py                    # Flask主应用文件
│   ├── production_config.py      # 生产环境配置
│   └── requirements.txt          # 项目依赖包
├── db/
│   ├── database_operations.py    # 数据库操作封装
│   ├── database_setup.py         # 数据库初始化脚本
│   └── gym_management.db         # SQLite数据库文件
├── frontend/
│   ├── index.html                # 系统主页面
│   ├── scripts/
│   │   ├── api.js                # API客户端封装
│   │   ├── main.js               # 主要功能和导航
│   │   ├── members.js            # 会员管理模块
│   │   ├── memberDetail.js       # 会员详情管理
│   │   ├── trainers.js           # 教练管理模块
│   │   ├── trainerDetail.js      # 教练详情管理
│   │   ├── courses.js            # 课程管理模块
│   │   └── cardTypes.js          # 会员卡类型管理
│   └── styles/
│       └── main.css              # 系统样式文件
```

## 三、实验目的

设计并实现一个完整的健身房管理系统，涵盖健身房运营的核心业务流程。通过本项目掌握：

1. **数据库设计能力**：完整的E-R建模、关系模式设计、数据字典编写
2. **SQL应用能力**：复杂查询、多表连接、聚合函数、事务处理
3. **系统架构设计**：前后端分离、RESTful API设计、模块化开发
4. **业务逻辑实现**：健身房完整业务流程的数字化实现
5. **用户界面设计**：响应式设计、交互体验优化

## 四、数据库设计

### 需求分析

NUAA健身房管理系统是一个综合性的业务管理平台，需要支持以下核心功能：

#### 核心业务模块

📋 **会员管理系统**
- 会员基本信息管理（姓名、联系方式、个人信息）
- 会员状态跟踪（活跃、注销）
- 会员搜索和详情查看

📋 **教练管理系统**
- 教练基本信息管理
- 教练专业技能和认证管理
- 教练工作状态管理（活跃、离职）

📋 **课程管理系统**
- 课程基本信息配置（名称、描述、时长、价格）
- 课程状态管理（活跃、停用）
- 课程搜索和筛选

📋 **会员卡类型管理**
- 卡类型配置（价格、有效期、权益描述）
- 卡类型的启用/停用管理

#### 关联业务模块

💳 **会员卡管理**
- 会员持卡记录管理
- 卡片购买日期和到期日期跟踪
- 卡片状态管理（有效、过期、暂停）

📚 **课程报名管理**
- 会员课程报名记录
- 报名状态跟踪（已报名、进行中、已完成、已取消）
- 报名时间管理

👥 **教练指派管理**
- 教练与会员的指派关系
- 指派类型管理（私教、团体课、咨询、体能评估）
- 指派时间和状态跟踪

🎯 **教练课程分配**
- 教练教授课程的分配关系
- 教练课程负责状态管理

### E-R图设计

![image-20250609211733884](C:\Users\Lenovo\AppData\Roaming\Typora\typora-user-images\image-20250609211733884.png)

### 系统设计

#### 逻辑设计——关系模式

**将E-R图转换为关系模式如下（下划线为主键）：**

1. **会员表 Members(<u>会员编号</u>, 姓名, 联系电话, 电子邮箱, 性别, 出生日期, 入会日期, 会员状态)**
2. **教练表 Trainers(<u>教练编号</u>, 姓名, 联系电话, 电子邮箱, 专业领域, 入职日期, 教练状态)**
3. **课程表 Courses(<u>课程编号</u>, 课程名称, 课程描述, 课程时长, 课程价格, 课程状态)**
4. **会员卡类型表 CardTypes(<u>卡类型编号</u>, 卡类型名称, 卡类型价格, 有效期天数, 权益描述)**
5. **会员卡表 MemberCards(<u>会员卡编号</u>, 会员编号, 卡类型编号, 购买日期, 到期日期, 卡片状态)**
6. **课程报名表 CourseEnrollments(<u>报名编号</u>, 会员编号, 课程编号, 报名日期, 报名状态)**
7. **教练指派表 TrainerAssignments(<u>指派编号</u>, 教练编号, 会员编号, 指派日期, 指派类型, 指派状态)**
8. **教练课程表 TrainerCourses(<u>分配编号</u>, 教练编号, 课程编号, 分配日期, 分配状态)**

#### 物理设计——数据字典

**会员表 (members)**

| 字段名 | 含义 | 数据类型 | 约束 | 说明 |
|--------|------|----------|------|------|
| id | 会员唯一标识 | INTEGER | PRIMARY KEY AUTOINCREMENT | 自动递增主键 |
| name | 会员姓名 | TEXT | NOT NULL | 会员真实姓名 |
| phone | 手机号码 | TEXT | | 联系电话 |
| email | 电子邮箱 | TEXT | | 电子邮件地址 |
| gender | 性别 | TEXT | | 男/女/其他 |
| birth_date | 出生日期 | TEXT | | YYYY-MM-DD格式 |
| join_date | 注册日期 | TEXT | | 会员注册时间 |
| status | 会员状态 | TEXT | DEFAULT 'active' | active/inactive|

**教练表 (trainers)**

| 字段名 | 含义 | 数据类型 | 约束 | 说明 |
|--------|------|----------|------|------|
| id | 教练唯一标识 | INTEGER | PRIMARY KEY AUTOINCREMENT | 自动递增主键 |
| name | 教练姓名 | TEXT | NOT NULL | 教练真实姓名 |
| phone | 手机号码 | TEXT | | 联系电话 |
| email | 电子邮箱 | TEXT | | 电子邮件地址 |
| specialization | 专业领域 | TEXT | | 如：瑜伽、力量训练等 |
| hire_date | 入职日期 | TEXT | | 教练入职时间 |
| status | 教练状态 | TEXT | DEFAULT 'active' | active/inactive |

**课程表 (courses)**

| 字段名 | 含义 | 数据类型 | 约束 | 说明 |
|--------|------|----------|------|------|
| id | 课程唯一标识 | INTEGER | PRIMARY KEY AUTOINCREMENT | 自动递增主键 |
| name | 课程名称 | TEXT | NOT NULL | 课程标题 |
| description | 课程描述 | TEXT | | 详细介绍 |
| duration | 课程时长 | INTEGER | | 以分钟为单位 |
| price | 课程价格 | REAL | | 单次课程费用 |
| status | 课程状态 | TEXT | DEFAULT 'active' | active/inactive |

**会员卡类型表 (card_types)**

| 字段名 | 含义 | 数据类型 | 约束 | 说明 |
|--------|------|----------|------|------|
| id | 卡类型唯一标识 | INTEGER | PRIMARY KEY AUTOINCREMENT | 自动递增主键 |
| name | 卡类型名称 | TEXT | NOT NULL | 如：月卡、季卡、年卡 |
| price | 卡类型价格 | REAL | NOT NULL | 办卡费用 |
| validity_days | 有效期天数 | INTEGER | NOT NULL | 卡片有效天数 |
| description | 卡类型描述 | TEXT | | 权益说明 |

**会员卡表 (member_cards)**

| 字段名 | 含义 | 数据类型 | 约束 | 说明 |
|--------|------|----------|------|------|
| id | 会员卡唯一标识 | INTEGER | PRIMARY KEY AUTOINCREMENT | 自动递增主键 |
| member_id | 会员ID | INTEGER | NOT NULL, FOREIGN KEY | 关联会员表 |
| card_type_id | 卡类型ID | INTEGER | NOT NULL, FOREIGN KEY | 关联卡类型表 |
| purchase_date | 购买日期 | TEXT | NOT NULL | 办卡日期 |
| expiry_date | 到期日期 | TEXT | NOT NULL | 卡片到期时间 |
| status | 卡片状态 | TEXT | DEFAULT 'active' | active/inactive |

**课程报名表 (course_enrollments)**

| 字段名 | 含义 | 数据类型 | 约束 | 说明 |
|--------|------|----------|------|------|
| id | 报名记录唯一标识 | INTEGER | PRIMARY KEY AUTOINCREMENT | 自动递增主键 |
| member_id | 会员ID | INTEGER | NOT NULL, FOREIGN KEY | 关联会员表 |
| course_id | 课程ID | INTEGER | NOT NULL, FOREIGN KEY | 关联课程表 |
| enrollment_date | 报名日期 | TEXT | NOT NULL | 报名时间 |
| status | 报名状态 | TEXT | DEFAULT 'active' | enrolled/in_progress/completed/cancelled |

**教练指派表 (trainer_assignments)**

| 字段名 | 含义 | 数据类型 | 约束 | 说明 |
|:-------|------|----------|------|------|
| id | 指派记录唯一标识 | INTEGER | PRIMARY KEY AUTOINCREMENT | 自动递增主键 |
| trainer_id | 教练ID | INTEGER | NOT NULL, FOREIGN KEY | 关联教练表 |
| member_id | 会员ID | INTEGER | NOT NULL, FOREIGN KEY | 关联会员表 |
| assignment_date | 指派日期 | TEXT | NOT NULL | 指派时间 |
| assignment_type | 指派类型 | TEXT | NOT NULL | 私教/团体课/咨询/体能评估 |
| status | 指派状态 | TEXT | DEFAULT 'active' | active/inactive |

**教练课程分配表 (trainer_course_assignments)**

| 字段名          | 含义             | 数据类型 | 约束                      | 说明                                 |
| --------------- | ---------------- | -------- | ------------------------- | ------------------------------------ |
| id              | 分配记录唯一标识 | INTEGER  | PRIMARY KEY AUTOINCREMENT | 自动递增主键                         |
| trainer_id      | 教练ID           | INTEGER  | NOT NULL, FOREIGN KEY     | 关联trainers表的id                   |
| course_id       | 课程ID           | INTEGER  | NOT NULL, FOREIGN KEY     | 关联courses表的id                    |
| assignment_date | 分配日期         | TEXT     | NOT NULL                  | YYYY-MM-DD格式，课程分配给教练的日期 |
| course_type     | 课程类型         | TEXT     |                           | 如：常规课程/私教课程/团体课等       |
| notes           | 备注信息         | TEXT     |                           | 分配相关的额外说明                   |

## 五、功能实现与演示

### 5.1 DDL：数据库的建立

#### 数据库初始化脚本

````python
# filepath: database_setup.py
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
            # 会员卡实例表 (会员拥有的卡) - 这是"会员与会员卡的关系表"
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
                    FOREIGN KEY (member_id) REFERENCES members (id) ON DELETE CASCADE ON UPDATE CASCADE,
                    FOREIGN KEY (card_type_id) REFERENCES membership_card_types (id) ON DELETE CASCADE ON UPDATE CASCADE
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
                    FOREIGN KEY (member_id) REFERENCES members (id) ON DELETE CASCADE ON UPDATE CASCADE,
                    FOREIGN KEY (course_id) REFERENCES courses (id) ON DELETE CASCADE ON UPDATE CASCADE
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
                    FOREIGN KEY (member_id) REFERENCES members (id) ON DELETE CASCADE ON UPDATE CASCADE,
                    FOREIGN KEY (trainer_id) REFERENCES trainers (id) ON DELETE CASCADE ON UPDATE CASCADE
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
                    FOREIGN KEY (trainer_id) REFERENCES trainers (id) ON DELETE CASCADE ON UPDATE CASCADE,
                    FOREIGN KEY (course_id) REFERENCES courses (id) ON DELETE CASCADE ON UPDATE CASCADE
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
````

#### 数据库操作封装

````python
# filepath: db/database_operations.py
import sqlite3
import os
from datetime import datetime, timedelta

class DatabaseOperations:
    def __init__(self):
        self.db_path = os.path.join(os.path.dirname(__file__), 'gym_management.db')
    
    def get_connection(self):
        """获取数据库连接"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row  # 返回字典格式的结果
        return conn
    
    def execute_query(self, query, params=None):
        """执行查询语句"""
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            return cursor.fetchall()
        finally:
            conn.close()
    
    def execute_update(self, query, params=None):
        """执行更新语句"""
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            conn.commit()
            return cursor.lastrowid
        finally:
            conn.close()
````

### 5.2 DML：数据库的数据操作

#### 1. 会员管理功能实现

**会员信息的完整CRUD操作**

````python
# filepath: backend/app.py
from flask import Flask, request, jsonify
import sqlite3
import os
from datetime import datetime

app = Flask(__name__)

def get_db_connection():
    """获取数据库连接"""
    db_path = os.path.join('db', 'gym_management.db')
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn

# 获取所有会员（支持搜索）
@app.route('/api/members', methods=['GET'])
def get_members():
    search = request.args.get('search', '')
    conn = get_db_connection()
    
    if search:
        query = '''
            SELECT * FROM members 
            WHERE name LIKE ? OR phone LIKE ? OR email LIKE ?
            ORDER BY join_date DESC
        '''
        members = conn.execute(query, (f'%{search}%', f'%{search}%', f'%{search}%')).fetchall()
    else:
        members = conn.execute('SELECT * FROM members ORDER BY join_date DESC').fetchall()
    
    conn.close()
    return jsonify([dict(member) for member in members])

# 创建新会员
@app.route('/api/members', methods=['POST'])
def create_member():
    data = request.json
    conn = get_db_connection()
    
    query = '''
        INSERT INTO members (name, phone, email, gender, birth_date, join_date, status)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    '''
    
    cursor = conn.execute(query, (
        data['name'],
        data.get('phone', ''),
        data.get('email', ''),
        data.get('gender', ''),
        data.get('birth_date', ''),
        data.get('join_date', datetime.now().strftime('%Y-%m-%d')),
        data.get('status', 'active')
    ))
    
    conn.commit()
    member_id = cursor.lastrowid
    conn.close()
    
    return jsonify({'id': member_id, 'message': '会员创建成功'})

# 获取特定会员信息
@app.route('/api/members/<int:member_id>', methods=['GET'])
def get_member(member_id):
    conn = get_db_connection()
    member = conn.execute('SELECT * FROM members WHERE id = ?', (member_id,)).fetchone()
    conn.close()
    
    if member:
        return jsonify(dict(member))
    else:
        return jsonify({'error': '会员不存在'}), 404

# 更新会员信息
@app.route('/api/members/<int:member_id>', methods=['PUT'])
def update_member(member_id):
    data = request.json
    conn = get_db_connection()
    
    query = '''
        UPDATE members 
        SET name = ?, phone = ?, email = ?, gender = ?, birth_date = ?, status = ?
        WHERE id = ?
    '''
    
    conn.execute(query, (
        data['name'],
        data.get('phone', ''),
        data.get('email', ''),
        data.get('gender', ''),
        data.get('birth_date', ''),
        data.get('status', 'active'),
        member_id
    ))
    
    conn.commit()
    conn.close()
    
    return jsonify({'message': '会员信息更新成功'})

# 删除会员
@app.route('/api/members/<int:member_id>', methods=['DELETE'])
def delete_member(member_id):
    conn = get_db_connection()
    
    # 检查是否有关联数据
    enrollments = conn.execute('SELECT COUNT(*) as count FROM course_enrollments WHERE member_id = ?', (member_id,)).fetchone()
    cards = conn.execute('SELECT COUNT(*) as count FROM member_cards WHERE member_id = ?', (member_id,)).fetchone()
    assignments = conn.execute('SELECT COUNT(*) as count FROM trainer_assignments WHERE member_id = ?', (member_id,)).fetchone()
    
    if enrollments['count'] > 0 or cards['count'] > 0 or assignments['count'] > 0:
        conn.close()
        return jsonify({'error': '该会员存在相关记录，无法删除'}), 400
    
    conn.execute('DELETE FROM members WHERE id = ?', (member_id,))
    conn.commit()
    conn.close()
    
    return jsonify({'message': '会员删除成功'})
````

#### 2. 教练管理功能实现

````python
# 获取所有教练
@app.route('/api/trainers', methods=['GET'])
def get_trainers():
    search = request.args.get('search', '')
    conn = get_db_connection()
    
    if search:
        query = '''
            SELECT * FROM trainers 
            WHERE name LIKE ? OR specialization LIKE ?
            ORDER BY hire_date DESC
        '''
        trainers = conn.execute(query, (f'%{search}%', f'%{search}%')).fetchall()
    else:
        trainers = conn.execute('SELECT * FROM trainers ORDER BY hire_date DESC').fetchall()
    
    conn.close()
    return jsonify([dict(trainer) for trainer in trainers])

# 创建新教练
@app.route('/api/trainers', methods=['POST'])
def create_trainer():
    data = request.json
    conn = get_db_connection()
    
    query = '''
        INSERT INTO trainers (name, phone, email, specialization, hire_date, status)
        VALUES (?, ?, ?, ?, ?, ?)
    '''
    
    cursor = conn.execute(query, (
        data['name'],
        data.get('phone', ''),
        data.get('email', ''),
        data.get('specialization', ''),
        data.get('hire_date', datetime.now().strftime('%Y-%m-%d')),
        data.get('status', 'active')
    ))
    
    conn.commit()
    trainer_id = cursor.lastrowid
    conn.close()
    
    return jsonify({'id': trainer_id, 'message': '教练创建成功'})

# 获取教练的课程分配
@app.route('/api/trainers/<int:trainer_id>/courses', methods=['GET'])
def get_trainer_courses(trainer_id):
    conn = get_db_connection()
    
    query = '''
        SELECT 
            tc.id,
            tc.trainer_id,
            tc.course_id,
            tc.assignment_date,
            tc.status,
            c.name as course_name,
            c.description as course_description,
            c.duration,
            c.price
        FROM trainer_courses tc
        JOIN courses c ON tc.course_id = c.id
        WHERE tc.trainer_id = ?
        ORDER BY tc.assignment_date DESC
    '''
    
    courses = conn.execute(query, (trainer_id,)).fetchall()
    conn.close()
    
    return jsonify([dict(course) for course in courses])

# 获取教练的会员指派
@app.route('/api/trainers/<int:trainer_id>/members', methods=['GET'])
def get_trainer_members(trainer_id):
    conn = get_db_connection()
    
    query = '''
        SELECT 
            ta.id,
            ta.trainer_id,
            ta.member_id,
            ta.assignment_date,
            ta.assignment_type,
            ta.status,
            m.name as member_name,
            m.phone as member_phone,
            m.email as member_email
        FROM trainer_assignments ta
        JOIN members m ON ta.member_id = m.id
        WHERE ta.trainer_id = ?
        ORDER BY ta.assignment_date DESC
    '''
    
    assignments = conn.execute(query, (trainer_id,)).fetchall()
    conn.close()
    
    return jsonify([dict(assignment) for assignment in assignments])
````

#### 3. 课程管理功能实现

````python
# 获取所有课程
@app.route('/api/courses', methods=['GET'])
def get_courses():
    search = request.args.get('search', '')
    conn = get_db_connection()
    
    if search:
        query = '''
            SELECT * FROM courses 
            WHERE name LIKE ? OR description LIKE ?
            ORDER BY name
        '''
        courses = conn.execute(query, (f'%{search}%', f'%{search}%')).fetchall()
    else:
        courses = conn.execute('SELECT * FROM courses ORDER BY name').fetchall()
    
    conn.close()
    return jsonify([dict(course) for course in courses])

# 创建新课程
@app.route('/api/courses', methods=['POST'])
def create_course():
    data = request.json
    conn = get_db_connection()
    
    query = '''
        INSERT INTO courses (name, description, duration, price, status)
        VALUES (?, ?, ?, ?, ?)
    '''
    
    cursor = conn.execute(query, (
        data['name'],
        data.get('description', ''),
        data.get('duration', 60),
        data.get('price', 0.0),
        data.get('status', 'active')
    ))
    
    conn.commit()
    course_id = cursor.lastrowid
    conn.close()
    
    return jsonify({'id': course_id, 'message': '课程创建成功'})
````

#### 4. 会员详情管理功能

##### **会员卡管理**

````python
# 获取会员的会员卡
@app.route('/api/members/<int:member_id>/cards', methods=['GET'])
def get_member_cards(member_id):
    conn = get_db_connection()
    
    query = '''
        SELECT 
            mc.id,
            mc.member_id,
            mc.card_type_id,
            mc.purchase_date,
            mc.expiry_date,
            mc.status,
            ct.name as card_type_name,
            ct.price as card_type_price,
            ct.validity_days,
            ct.description as card_type_description
        FROM member_cards mc
        JOIN card_types ct ON mc.card_type_id = ct.id
        WHERE mc.member_id = ?
        ORDER BY mc.purchase_date DESC
    '''
    
    cards = conn.execute(query, (member_id,)).fetchall()
    conn.close()
    
    return jsonify([dict(card) for card in cards])

# 为会员添加会员卡
@app.route('/api/members/<int:member_id>/cards', methods=['POST'])
def create_member_card(member_id):
    data = request.json
    conn = get_db_connection()
    
    # 获取卡类型信息以计算到期日期
    card_type = conn.execute('SELECT * FROM card_types WHERE id = ?', (data['card_type_id'],)).fetchone()
    
    if not card_type:
        conn.close()
        return jsonify({'error': '会员卡类型不存在'}), 404
    
    # 计算到期日期
    from datetime import datetime, timedelta
    purchase_date = datetime.strptime(data['purchase_date'], '%Y-%m-%d')
    expiry_date = purchase_date + timedelta(days=card_type['validity_days'])
    
    query = '''
        INSERT INTO member_cards (member_id, card_type_id, purchase_date, expiry_date, status)
        VALUES (?, ?, ?, ?, ?)
    '''
    
    cursor = conn.execute(query, (
        member_id,
        data['card_type_id'],
        data['purchase_date'],
        expiry_date.strftime('%Y-%m-%d'),
        data.get('status', 'active')
    ))
    
    conn.commit()
    card_id = cursor.lastrowid
    conn.close()
    
    return jsonify({'id': card_id, 'message': '会员卡创建成功'})
````

##### **课程报名管理**

````python
# 获取会员的课程报名
@app.route('/api/members/<int:member_id>/enrollments', methods=['GET'])
def get_member_enrollments(member_id):
    conn = get_db_connection()
    
    query = '''
        SELECT 
            ce.id,
            ce.member_id,
            ce.course_id,
            ce.enrollment_date,
            ce.status,
            c.name as course_name,
            c.description as course_description,
            c.duration,
            c.price
        FROM course_enrollments ce
        JOIN courses c ON ce.course_id = c.id
        WHERE ce.member_id = ?
        ORDER BY ce.enrollment_date DESC
    '''
    
    enrollments = conn.execute(query, (member_id,)).fetchall()
    conn.close()
    
    return jsonify([dict(enrollment) for enrollment in enrollments])

# 为会员添加课程报名
@app.route('/api/members/<int:member_id>/enrollments', methods=['POST'])
def create_member_enrollment(member_id):
    data = request.json
    conn = get_db_connection()
    
    # 检查是否已经报名该课程
    existing = conn.execute('''
        SELECT * FROM course_enrollments 
        WHERE member_id = ? AND course_id = ? AND status IN ('enrolled', 'in_progress')
    ''', (member_id, data['course_id'])).fetchone()
    
    if existing:
        conn.close()
        return jsonify({'error': '已经报名该课程'}), 400
    
    query = '''
        INSERT INTO course_enrollments (member_id, course_id, enrollment_date, status)
        VALUES (?, ?, ?, ?)
    '''
    
    cursor = conn.execute(query, (
        member_id,
        data['course_id'],
        data.get('enrollment_date', datetime.now().strftime('%Y-%m-%d')),
        data.get('status', 'enrolled')
    ))
    
    conn.commit()
    enrollment_id = cursor.lastrowid
    conn.close()
    
    return jsonify({'id': enrollment_id, 'message': '课程报名成功'})
````

##### **教练指派管理**

````python
# 获取会员的教练指派
@app.route('/api/members/<int:member_id>/assignments', methods=['GET'])
def get_member_assignments(member_id):
    conn = get_db_connection()
    
    query = '''
        SELECT 
            ta.id,
            ta.trainer_id,
            ta.member_id,
            ta.assignment_date,
            ta.assignment_type,
            ta.status,
            t.name as trainer_name,
            t.specialization as trainer_specialization,
            t.phone as trainer_phone
        FROM trainer_assignments ta
        JOIN trainers t ON ta.trainer_id = t.id
        WHERE ta.member_id = ?
        ORDER BY ta.assignment_date DESC
    '''
    
    assignments = conn.execute(query, (member_id,)).fetchall()
    conn.close()
    
    return jsonify([dict(assignment) for assignment in assignments])

# 为会员添加教练指派
@app.route('/api/members/<int:member_id>/assignments', methods=['POST'])
def create_member_assignment(member_id):
    data = request.json
    conn = get_db_connection()
    
    query = '''
        INSERT INTO trainer_assignments (trainer_id, member_id, assignment_date, assignment_type, status)
        VALUES (?, ?, ?, ?, ?)
    '''
    
    cursor = conn.execute(query, (
        data['trainer_id'],
        member_id,
        data.get('assignment_date', datetime.now().strftime('%Y-%m-%d')),
        data['assignment_type'],
        data.get('status', 'active')
    ))
    
    conn.commit()
    assignment_id = cursor.lastrowid
    conn.close()
    
    return jsonify({'id': assignment_id, 'message': '教练指派成功'})
````

#### 5. 会员卡类型管理

````python
# 获取所有会员卡类型
@app.route('/api/card-types', methods=['GET'])
def get_card_types():
    search = request.args.get('search', '')
    conn = get_db_connection()
    
    if search:
        query = '''
            SELECT * FROM card_types 
            WHERE name LIKE ? OR description LIKE ?
            ORDER BY price
        '''
        card_types = conn.execute(query, (f'%{search}%', f'%{search}%')).fetchall()
    else:
        card_types = conn.execute('SELECT * FROM card_types ORDER BY price').fetchall()
    
    conn.close()
    return jsonify([dict(card_type) for card_type in card_types])

# 创建新的会员卡类型
@app.route('/api/card-types', methods=['POST'])
def create_card_type():
    data = request.json
    conn = get_db_connection()
    
    query = '''
        INSERT INTO card_types (name, price, validity_days, description)
        VALUES (?, ?, ?, ?)
    '''
    
    cursor = conn.execute(query, (
        data['name'],
        data['price'],
        data['validity_days'],
        data.get('description', '')
    ))
    
    conn.commit()
    card_type_id = cursor.lastrowid
    conn.close()
    
    return jsonify({'id': card_type_id, 'message': '会员卡类型创建成功'})
````

#### 6. 统计查询功能

````python
# 获取仪表板统计数据
@app.route('/api/dashboard/stats', methods=['GET'])
def get_dashboard_stats():
    conn = get_db_connection()
    
    # 统计活跃会员数量
    active_members = conn.execute("SELECT COUNT(*) as count FROM members WHERE status = 'active'").fetchone()
    
    # 统计活跃教练数量
    active_trainers = conn.execute("SELECT COUNT(*) as count FROM trainers WHERE status = 'active'").fetchone()
    
    # 统计活跃课程数量
    active_courses = conn.execute("SELECT COUNT(*) as count FROM courses WHERE status = 'active'").fetchone()
    
    # 统计总收入（基于会员卡销售）
    total_revenue = conn.execute('''
        SELECT COALESCE(SUM(ct.price), 0) as total
        FROM member_cards mc
        JOIN card_types ct ON mc.card_type_id = ct.id
        WHERE mc.status = 'active'
    ''').fetchone()
    
    # 统计本月新增会员
    monthly_new_members = conn.execute('''
        SELECT COUNT(*) as count FROM members 
        WHERE strftime('%Y-%m', join_date) = strftime('%Y-%m', 'now')
    ''').fetchone()
    
    conn.close()
    
    return jsonify({
        'activeMembers': active_members['count'],
        'activeTrainers': active_trainers['count'],
        'activeCourses': active_courses['count'],
        'totalRevenue': total_revenue['total'],
        'monthlyNewMembers': monthly_new_members['count']
    })

# 获取课程报名统计
@app.route('/api/stats/course-enrollments', methods=['GET'])
def get_course_enrollment_stats():
    conn = get_db_connection()
    
    query = '''
        SELECT 
            c.name as course_name,
            COUNT(ce.id) as enrollment_count,
            SUM(c.price) as total_revenue
        FROM courses c
        LEFT JOIN course_enrollments ce ON c.id = ce.course_id
        WHERE c.status = 'active'
        GROUP BY c.id, c.name
        ORDER BY enrollment_count DESC
    '''
    
    stats = conn.execute(query).fetchall()
    conn.close()
    
    return jsonify([dict(stat) for stat in stats])
````

### 5.3 前端实现及功能演示

#### 1. API客户端封装

````javascript
// filepath: frontend/scripts/api.js
class GymAPI {
    constructor() {
        this.baseURL = '/api';
    }

    async request(endpoint, options = {}) {
        const url = `${this.baseURL}${endpoint}`;
        const config = {
            headers: {
                'Content-Type': 'application/json',
                ...options.headers
            },
            ...options
        };

        try {
            const response = await fetch(url, config);
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return await response.json();
        } catch (error) {
            console.error('API request failed:', error);
            throw error;
        }
    }

    // 会员相关API
    async getMembers(search = '') {
        const params = search ? `?search=${encodeURIComponent(search)}` : '';
        return this.request(`/members${params}`);
    }

    async getMember(id) {
        return this.request(`/members/${id}`);
    }

    async createMember(memberData) {
        return this.request('/members', {
            method: 'POST',
            body: JSON.stringify(memberData)
        });
    }

    async updateMember(id, memberData) {
        return this.request(`/members/${id}`, {
            method: 'PUT',
            body: JSON.stringify(memberData)
        });
    }

    async deleteMember(id) {
        return this.request(`/members/${id}`, {
            method: 'DELETE'
        });
    }

    // 会员详情相关API
    async getMemberCards(memberId) {
        return this.request(`/members/${memberId}/cards`);
    }

    async createMemberCard(memberId, cardData) {
        return this.request(`/members/${memberId}/cards`, {
            method: 'POST',
            body: JSON.stringify(cardData)
        });
    }

    async getMemberEnrollments(memberId) {
        return this.request(`/members/${memberId}/enrollments`);
    }

    async createMemberEnrollment(memberId, enrollmentData) {
        return this.request(`/members/${memberId}/enrollments`, {
            method: 'POST',
            body: JSON.stringify(enrollmentData)
        });
    }

    async getMemberAssignments(memberId) {
        return this.request(`/members/${memberId}/assignments`);
    }

    async createMemberAssignment(memberId, assignmentData) {
        return this.request(`/members/${memberId}/assignments`, {
            method: 'POST',
            body: JSON.stringify(assignmentData)
        });
    }

    // 教练相关API
    async getTrainers(search = '') {
        const params = search ? `?search=${encodeURIComponent(search)}` : '';
        return this.request(`/trainers${params}`);
    }

    async getTrainer(id) {
        return this.request(`/trainers/${id}`);
    }

    async createTrainer(trainerData) {
        return this.request('/trainers', {
            method: 'POST',
            body: JSON.stringify(trainerData)
        });
    }

    async getTrainerCourses(trainerId) {
        return this.request(`/trainers/${trainerId}/courses`);
    }

    async getTrainerMembers(trainerId) {
        return this.request(`/trainers/${trainerId}/members`);
    }

    // 课程相关API
    async getCourses(search = '') {
        const params = search ? `?search=${encodeURIComponent(search)}` : '';
        return this.request(`/courses${params}`);
    }

    async createCourse(courseData) {
        return this.request('/courses', {
            method: 'POST',
            body: JSON.stringify(courseData)
        });
    }

    // 会员卡类型相关API
    async getCardTypes(search = '') {
        const params = search ? `?search=${encodeURIComponent(search)}` : '';
        return this.request(`/card-types${params}`);
    }

    async createCardType(cardTypeData) {
        return this.request('/card-types', {
            method: 'POST',
            body: JSON.stringify(cardTypeData)
        });
    }

    // 统计相关API
    async getDashboardStats() {
        return this.request('/dashboard/stats');
    }

    async getCourseEnrollmentStats() {
        return this.request('/stats/course-enrollments');
    }
}

// 创建全局API实例
const api = new GymAPI();
````

#### 2. 主要功能和导航管理

![image-20250612132835432](C:\Users\Lenovo\AppData\Roaming\Typora\typora-user-images\image-20250612132835432.png)

````javascript
// filepath: frontend/scripts/main.js
document.addEventListener('DOMContentLoaded', function() {
    initializeApp();
});

function initializeApp() {
    setupNavigation();
    loadDashboard();
}

function setupNavigation() {
    const navTabs = document.querySelectorAll('.nav-tab');
    navTabs.forEach(tab => {
        tab.addEventListener('click', function() {
            const tabName = this.getAttribute('data-tab');
            switchTab(tabName);
            
            // 更新活跃标签样式
            navTabs.forEach(t => t.classList.remove('active'));
            this.classList.add('active');
        });
    });
}

function switchTab(tabName) {
    const mainContent = document.getElementById('main-content');
    
    switch(tabName) {
        case 'dashboard':
            loadDashboard();
            break;
        case 'members':
            loadMembersTab();
            break;
        case 'trainers':
            loadTrainersTab();
            break;
        case 'courses':
            loadCoursesTab();
            break;
        case 'card-types':
            loadCardTypesTab();
            break;
        default:
            loadDashboard();
    }
}

async function loadDashboard() {
    const mainContent = document.getElementById('main-content');
    mainContent.innerHTML = `
        <div class="dashboard">
            <h2>健身房管理系统仪表板</h2>
            <div class="stats-grid">
                <div class="stat-card">
                    <h3>活跃会员</h3>
                    <div class="stat-number" id="activeMembersCount">-</div>
                </div>
                <div class="stat-card">
                    <h3>活跃教练</h3>
                    <div class="stat-number" id="activeTrainersCount">-</div>
                </div>
                <div class="stat-card">
                    <h3>活跃课程</h3>
                    <div class="stat-number" id="activeCoursesCount">-</div>
                </div>
                <div class="stat-card">
                    <h3>总收入</h3>
                    <div class="stat-number" id="totalRevenueCount">-</div>
                </div>
            </div>
        </div>
    `;
    
    await loadDashboardStats();
}

async function loadDashboardStats() {
    try {
        const stats = await api.getDashboardStats();
        document.getElementById('activeMembersCount').textContent = stats.activeMembers;
        document.getElementById('activeTrainersCount').textContent = stats.activeTrainers;
        document.getElementById('activeCoursesCount').textContent = stats.activeCourses;
        document.getElementById('totalRevenueCount').textContent = `¥${stats.totalRevenue || 0}`;
    } catch (error) {
        showMessage('加载统计数据失败', 'error');
        console.error('Failed to load dashboard stats:', error);
    }
}

function loadMembersTab() {
    const mainContent = document.getElementById('main-content');
    mainContent.innerHTML = `
        <div class="members-section">
            <div class="section-header">
                <h2>会员管理</h2>
                <button class="btn btn-primary" onclick="showMemberForm()">添加会员</button>
            </div>
            <div class="search-bar">
                <input type="text" id="memberSearch" placeholder="搜索会员姓名、电话或邮箱...">
                <button onclick="searchMembers()">搜索</button>
            </div>
            <div id="membersContainer" class="content-grid">
                <!-- 会员列表将在这里显示 -->
            </div>
        </div>
    `;
    
    loadMembers();
}

// 模态框管理
function showModal(title, content) {
    const modal = document.getElementById('modal');
    const modalTitle = document.getElementById('modalTitle');
    const modalBody = document.getElementById('modalBody');
    
    modalTitle.textContent = title;
    modalBody.innerHTML = content;
    modal.style.display = 'block';
}

function closeModal() {
    const modal = document.getElementById('modal');
    modal.style.display = 'none';
}

// 消息提示系统
function showMessage(message, type = 'success') {
    const messageDiv = document.createElement('div');
    messageDiv.className = `message message-${type}`;
    messageDiv.textContent = message;
    
    document.body.appendChild(messageDiv);
    
    setTimeout(() => {
        messageDiv.remove();
    }, 3000);
}

// 标签页切换功能
function showTab(tabName) {
    const tabs = document.querySelectorAll('.detail-tab');
    const contents = document.querySelectorAll('.detail-content');
    
    tabs.forEach(tab => {
        tab.classList.remove('active');
        if (tab.getAttribute('data-tab') === tabName) {
            tab.classList.add('active');
        }
    });
    
    contents.forEach(content => {
        content.style.display = 'none';
        if (content.id === `${tabName}Content`) {
            content.style.display = 'block';
        }
    });
}

function showTrainerTab(tabName) {
    const tabs = document.querySelectorAll('.trainer-detail-tab');
    const contents = document.querySelectorAll('.trainer-detail-content');
    
    tabs.forEach(tab => {
        tab.classList.remove('active');
        if (tab.getAttribute('data-tab') === tabName) {
            tab.classList.add('active');
        }
    });
    
    contents.forEach(content => {
        content.style.display = 'none';
        if (content.id === `trainer${tabName.charAt(0).toUpperCase() + tabName.slice(1)}Content`) {
            content.style.display = 'block';
        }
    });
}
````

#### 3. 会员管理模块

##### **插入**

````SQL
-- 插入会员数据
INSERT INTO members (name, gender, birth_date, phone, emergency_contact_name, emergency_contact_phone, health_notes, join_date, status) VALUES
('张三', '男', '1990-05-15', '13812345678', '张母', '13912345678', '无特殊健康问题', '2024-01-15', 'active'),
('李四', '女', '1992-08-22', '13923456789', '李父', '13823456789', '轻微腰椎间盘突出', '2024-02-01', 'active'),
('王五', '男', '1988-12-10', '15034567890', '王妻', '15134567890', '高血压，需要适度运动', '2024-01-20', 'active'),
('赵六', '女', '1995-03-08', '15145678901', '赵夫', '15245678901', '无特殊健康问题', '2024-02-15', 'active'),
('钱七', '男', '1991-07-25', '13656789012', '钱父', '13756789012', '膝盖有旧伤，避免剧烈运动', '2024-01-30', 'active'),
('孙八', '女', '1993-11-18', '13767890123', '孙母', '13867890123', '无特殊健康问题', '2024-02-10', 'active'),
('周九', '男', '1989-04-03', '15878901234', '周妻', '15978901234', '糖尿病，需要监控血糖', '2024-01-25', 'active'),
('吴十', '女', '1994-09-14', '15989012345', '吴父', '16089012345', '无特殊健康问题', '2024-02-20', 'active');
````

![image-20250611193203286](C:\Users\Lenovo\AppData\Roaming\Typora\typora-user-images\image-20250611193203286.png)

##### **查询**

![image-20250611193941758](C:\Users\Lenovo\AppData\Roaming\Typora\typora-user-images\image-20250611193941758.png)

##### **删除（逻辑删除，软删除）**

**删除前**

![image-20250611194054969](C:\Users\Lenovo\AppData\Roaming\Typora\typora-user-images\image-20250611194054969.png)

**删除后**

![image-20250611194140049](C:\Users\Lenovo\AppData\Roaming\Typora\typora-user-images\image-20250611194140049.png)

````javascript
// filepath: frontend/scripts/members.js
async function loadMembers() {
    try {
        const members = await api.getMembers();
        displayMembers(members);
    } catch (error) {
        showMessage('加载会员列表失败', 'error');
        console.error('Failed to load members:', error);
    }
}

async function searchMembers() {
    const searchTerm = document.getElementById('memberSearch').value;
    try {
        const members = await api.getMembers(searchTerm);
        displayMembers(members);
    } catch (error) {
        showMessage('搜索会员失败', 'error');
        console.error('Failed to search members:', error);
    }
}

function displayMembers(members) {
    const container = document.getElementById('membersContainer');
    
    if (members.length === 0) {
        container.innerHTML = '<div class="no-data">暂无会员数据</div>';
        return;
    }
    
    container.innerHTML = members.map(member => `
        <div class="card member-card">
            <div class="card-header">
                <h3>${member.name}</h3>
                <span class="status status-${member.status}">${getStatusText(member.status)}</span>
            </div>
            <div class="card-body">
                <p><strong>电话:</strong> ${member.phone || '未填写'}</p>
                <p><strong>邮箱:</strong> ${member.email || '未填写'}</p>
                <p><strong>性别:</strong> ${member.gender || '未填写'}</p>
                <p><strong>入会日期:</strong> ${member.join_date || '未知'}</p>
            </div>
            <div class="card-actions">
                <button class="btn btn-info" onclick="showMemberDetail(${member.id})">查看详情</button>
                <button class="btn btn-warning" onclick="editMember(${member.id})">编辑</button>
                <button class="btn btn-danger" onclick="deleteMember(${member.id})">删除</button>
            </div>
        </div>
    `).join('');
}

function getStatusText(status) {
    const statusMap = {
        'active': '活跃',
        'inactive': '非活跃',
        'suspended': '暂停'
    };
    return statusMap[status] || status;
}

function showMemberForm(memberId = null) {
    const isEdit = memberId !== null;
    const title = isEdit ? '编辑会员' : '添加会员';
    
    const content = `
        <form id="memberForm">
            <input type="hidden" id="memberId" value="${memberId || ''}">
            <div class="form-group">
                <label for="memberName">姓名 *</label>
                <input type="text" id="memberName" required>
            </div>
            <div class="form-group">
                <label for="memberPhone">电话</label>
                <input type="tel" id="memberPhone">
            </div>
            <div class="form-group">
                <label for="memberEmail">邮箱</label>
                <input type="email" id="memberEmail">
            </div>
            <div class="form-group">
                <label for="memberGender">性别</label>
                <select id="memberGender">
                    <option value="">请选择</option>
                    <option value="男">男</option>
                    <option value="女">女</option>
                    <option value="其他">其他</option>
                </select>
            </div>
            <div class="form-group">
                <label for="memberBirthDate">出生日期</label>
                <input type="date" id="memberBirthDate">
            </div>
            <div class="form-group">
                <label for="memberStatus">状态</label>
                <select id="memberStatus">
                    <option value="active">活跃</option>
                    <option value="inactive">非活跃</option>
                    <option value="suspended">暂停</option>
                </select>
            </div>
            <div class="form-actions">
                <button type="button" class="btn btn-secondary" onclick="closeModal()">取消</button>
                <button type="submit" class="btn btn-primary">保存</button>
            </div>
        </form>
    `;
    
    showModal(title, content);
    
    // 如果是编辑模式，加载会员数据
    if (isEdit) {
        loadMemberForEdit(memberId);
    }
    
    // 绑定表单提交事件
    document.getElementById('memberForm').addEventListener('submit', saveMember);
}

async function loadMemberForEdit(memberId) {
    try {
        const member = await api.getMember(memberId);
        document.getElementById('memberName').value = member.name || '';
        document.getElementById('memberPhone').value = member.phone || '';
        document.getElementById('memberEmail').value = member.email || '';
        document.getElementById('memberGender').value = member.gender || '';
        document.getElementById('memberBirthDate').value = member.birth_date || '';
        document.getElementById('memberStatus').value = member.status || 'active';
    } catch (error) {
        showMessage('加载会员信息失败', 'error');
        console.error('Failed to load member for edit:', error);
    }
}

async function saveMember(event) {
    event.preventDefault();
    
    const form = event.target;
    const formData = new FormData(form);
    const memberId = document.getElementById('memberId').value;
    
    const memberData = {
        name: formData.get('memberName') || document.getElementById('memberName').value,
        phone: document.getElementById('memberPhone').value,
        email: document.getElementById('memberEmail').value,
        gender: document.getElementById('memberGender').value,
        birth_date: document.getElementById('memberBirthDate').value,
        status: document.getElementById('memberStatus').value,
        join_date: new Date().toISOString().split('T')[0]
    };
    
    try {
        if (memberId) {
            await api.updateMember(memberId, memberData);
            showMessage('会员信息更新成功', 'success');
        } else {
            await api.createMember(memberData);
            showMessage('会员创建成功', 'success');
        }
        
        closeModal();
        loadMembers();
    } catch (error) {
        showMessage('保存会员信息失败', 'error');
        console.error('Failed to save member:', error);
    }
}

function editMember(memberId) {
    showMemberForm(memberId);
}

async function deleteMember(memberId) {
    if (!confirm('确定要删除这个会员吗？此操作不可恢复。')) {
        return;
    }
    
    try {
        await api.deleteMember(memberId);
        showMessage('会员删除成功', 'success');
        loadMembers();
    } catch (error) {
        showMessage('删除会员失败', 'error');
        console.error('Failed to delete member:', error);
    }
}

function showMemberDetail(memberId) {
    loadMemberDetailTab(memberId);
}
````

#### 4. 会员详情管理模块

##### **插入**

````SQL
-- 插入会员卡数据
INSERT INTO member_cards (member_id, card_type_id, purchase_date, activation_date, expiry_date, status, notes) VALUES
(1, 2, '2024-01-15', '2024-01-16', '2024-04-16', 'active', '正常使用中'),
(2, 4, '2024-02-01', '2024-02-01', '2025-02-01', 'active', '年卡用户，享受全部权益'),
(3, 1, '2024-01-20', '2024-01-21', '2024-02-20', 'expired', '已过期，需要续费'),
(3, 3, '2024-02-20', '2024-02-21', '2024-08-20', 'active', '续费半年卡'),
(4, 5, '2024-02-15', '2024-02-15', '2025-02-15', 'active', 'VIP会员，享受最高级别服务'),
(5, 1, '2024-01-30', '2024-01-31', '2024-03-01', 'active', '月卡用户'),
(6, 2, '2024-02-10', '2024-02-10', '2024-05-11', 'active', '季卡用户'),
(7, 1, '2024-01-25', '2024-01-26', '2024-02-25', 'frozen', '因病暂停使用'),
(8, 3, '2024-02-20', '2024-02-20', '2024-08-19', 'active', '半年卡用户');

-- 插入会员课程报名数据
INSERT INTO member_course_enrollments (member_id, course_id, enrollment_date, status, notes) VALUES
(1, 1, '2024-01-16', 'completed', '已完成初级瑜伽课程'),
(1, 3, '2024-01-20', 'enrolled', '正在进行力量训练基础'),
(2, 2, '2024-02-02', 'enrolled', '参与HIIT训练'),
(2, 5, '2024-02-05', 'enrolled', '参与普拉提核心训练'),
(3, 1, '2024-01-22', 'completed', '完成初级瑜伽'),
(3, 4, '2024-02-21', 'enrolled', '参与搏击有氧'),
(4, 6, '2024-02-16', 'enrolled', 'VIP会员参与游泳技巧提升'),
(4, 8, '2024-02-18', 'enrolled', 'VIP会员参与CrossFit训练'),
(5, 2, '2024-02-01', 'enrolled', '参与HIIT训练'),
(5, 7, '2024-02-03', 'completed', '完成拉伸放松课程'),
(6, 1, '2024-02-12', 'enrolled', '参与初级瑜伽'),
(6, 9, '2024-02-14', 'enrolled', '参与舞蹈健身'),
(7, 11, '2024-01-28', 'enrolled', '参与康复训练'),
(8, 3, '2024-02-22', 'enrolled', '参与力量训练基础'),
(8, 5, '2024-02-23', 'enrolled', '参与普拉提核心训练');

-- 插入会员教练指派数据
INSERT INTO member_trainer_assignments (member_id, trainer_id, assignment_date, assignment_type, notes) VALUES
(1, 1, '2024-01-18', 'personal_training_package', '购买10次私教课程包'),
(2, 2, '2024-02-03', 'personal_training_package', '年卡用户，每月2次私教'),
(3, 1, '2024-02-22', 'consultation', '力量训练咨询'),
(4, 6, '2024-02-17', 'personal_training_package', 'VIP会员无限私教'),
(4, 2, '2024-02-19', 'personal_training_package', 'VIP会员瑜伽私教'),
(5, 3, '2024-02-02', 'personal_training_package', '购买5次有氧私教'),
(6, 2, '2024-02-13', 'consultation', '瑜伽入门指导'),
(7, 8, '2024-01-28', 'personal_training_package', '康复训练专项指导'),
(8, 5, '2024-02-24', 'consultation', '普拉提动作指导'),
(8, 1, '2024-02-25', 'personal_training_package', '力量训练私教');
````

![image-20250611194331060](C:\Users\Lenovo\AppData\Roaming\Typora\typora-user-images\image-20250611194331060.png)

![image-20250611194348208](C:\Users\Lenovo\AppData\Roaming\Typora\typora-user-images\image-20250611194348208.png)

![image-20250611194405465](C:\Users\Lenovo\AppData\Roaming\Typora\typora-user-images\image-20250611194405465.png)

##### **删除**

![image-20250611194502163](C:\Users\Lenovo\AppData\Roaming\Typora\typora-user-images\image-20250611194502163.png)

![image-20250611194627568](C:\Users\Lenovo\AppData\Roaming\Typora\typora-user-images\image-20250611194627568.png)

````javascript
// filepath: frontend/scripts/memberDetail.js
let currentMemberId = null;

async function loadMemberDetailTab(memberId) {
    currentMemberId = memberId;
    
    try {
        const member = await api.getMember(memberId);
        
        const mainContent = document.getElementById('main-content');
        mainContent.innerHTML = `
            <div class="member-detail">
                <div class="detail-header">
                    <button class="btn btn-secondary" onclick="loadMembersTab()">← 返回会员列表</button>
                    <h2>${member.name} - 会员详情</h2>
                </div>
                
                <div class="member-info">
                    <div class="info-grid">
                        <div><strong>姓名:</strong> ${member.name}</div>
                        <div><strong>电话:</strong> ${member.phone || '未填写'}</div>
                        <div><strong>邮箱:</strong> ${member.email || '未填写'}</div>
                        <div><strong>性别:</strong> ${member.gender || '未填写'}</div>
                        <div><strong>入会日期:</strong> ${member.join_date || '未知'}</div>
                        <div><strong>状态:</strong> <span class="status status-${member.status}">${getStatusText(member.status)}</span></div>
                    </div>
                </div>
                
                <div class="detail-tabs">
                    <button class="detail-tab active" data-tab="cards" onclick="showTab('cards')">会员卡管理</button>
                    <button class="detail-tab" data-tab="enrollments" onclick="showTab('enrollments')">课程报名</button>
                    <button class="detail-tab" data-tab="assignments" onclick="showTab('assignments')">教练指派</button>
                </div>
                
                <div id="cardsContent" class="detail-content">
                    <div class="content-header">
                        <h3>会员卡管理</h3>
                        <button class="btn btn-primary" onclick="showMemberCardForm()">添加会员卡</button>
                    </div>
                    <div id="memberCardsContainer"></div>
                </div>
                
                <div id="enrollmentsContent" class="detail-content" style="display: none;">
                    <div class="content-header">
                        <h3>课程报名</h3>
                        <button class="btn btn-primary" onclick="showMemberCourseForm()">报名课程</button>
                    </div>
                    <div id="memberEnrollmentsContainer"></div>
                </div>
                
                <div id="assignmentsContent" class="detail-content" style="display: none;">
                    <div class="content-header">
                        <h3>教练指派</h// filepath: frontend/scripts/memberDetail.js
let currentMemberId = null;

async function loadMemberDetailTab(memberId) {
    currentMemberId = memberId;
    
    try {
        const member = await api.getMember(memberId);
        
        const mainContent = document.getElementById('main-content');
        mainContent.innerHTML = `
            <div class="member-detail">
                <div class="detail-header">
                    <button class="btn btn-secondary" onclick="loadMembersTab()">← 返回会员列表</button>
                    <h2>${member.name} - 会员详情</h2>
                </div>
                
                <div class="member-info">
                    <div class="info-grid">
                        <div><strong>姓名:</strong> ${member.name}</div>
                        <div><strong>电话:</strong> ${member.phone || '未填写'}</div>
                        <div><strong>邮箱:</strong> ${member.email || '未填写'}</div>
                        <div><strong>性别:</strong> ${member.gender || '未填写'}</div>
                        <div><strong>入会日期:</strong> ${member.join_date || '未知'}</div>
                        <div><strong>状态:</strong> <span class="status status-${member.status}">${getStatusText(member.status)}</span></div>
                    </div>
                </div>
                
                <div class="detail-tabs">
                    <button class="detail-tab active" data-tab="cards" onclick="showTab('cards')">会员卡管理</button>
                    <button class="detail-tab" data-tab="enrollments" onclick="showTab('enrollments')">课程报名</button>
                    <button class="detail-tab" data-tab="assignments" onclick="showTab('assignments')">教练指派</button>
                </div>
                
                <div id="cardsContent" class="detail-content">
                    <div class="content-header">
                        <h3>会员卡管理</h3>
                        <button class="btn btn-primary" onclick="showMemberCardForm()">添加会员卡</button>
                    </div>
                    <div id="memberCardsContainer"></div>
                </div>
                
                <div id="enrollmentsContent" class="detail-content" style="display: none;">
                    <div class="content-header">
                        <h3>课程报名</h3>
                        <button class="btn btn-primary" onclick="showMemberCourseForm()">报名课程</button>
                    </div>
                    <div id="memberEnrollmentsContainer"></div>
                </div>
                
                <div id="assignmentsContent" class="detail-content" style="display: none;">
                    <div class="content-header">
                        <h3>教练指派</h
                        <button class="btn btn-primary" onclick="showMemberTrainerForm()">指派教练</button>
                    </div>
                    <div id="memberAssignmentsContainer"></div>
                </div>
            </div>
        `;
        
        // 加载默认标签页内容
        loadMemberCards(memberId);
    } catch (error) {
        showMessage('加载会员详情失败', 'error');
        console.error('Failed to load member detail:', error);
    }
}

// 会员卡管理
async function loadMemberCards(memberId) {
    try {
        const cards = await api.getMemberCards(memberId);
        displayMemberCards(cards);
    } catch (error) {
        showMessage('加载会员卡失败', 'error');
        console.error('Failed to load member cards:', error);
    }
}

function displayMemberCards(cards) {
    const container = document.getElementById('memberCardsContainer');
    
    if (cards.length === 0) {
        container.innerHTML = '<div class="no-data">暂无会员卡记录</div>';
        return;
    }
    
    container.innerHTML = cards.map(card => `
        <div class="card">
            <div class="card-header">
                <h4>${card.card_type_name}</h4>
                <span class="status status-${card.status}">${getCardStatusText(card.status)}</span>
            </div>
            <div class="card-body">
                <p><strong>价格:</strong> ¥${card.card_type_price}</p>
                <p><strong>购买日期:</strong> ${card.purchase_date}</p>
                <p><strong>到期日期:</strong> ${card.expiry_date}</p>
                <p><strong>有效期:</strong> ${card.validity_days}天</p>
                <p><strong>描述:</strong> ${card.card_type_description || '无'}</p>
            </div>
        </div>
    `).join('');
}

function getCardStatusText(status) {
    const statusMap = {
        'active': '有效',
        'expired': '已过期',
        'suspended': '已暂停'
    };
    return statusMap[status] || status;
}

async function showMemberCardForm() {
    try {
        const cardTypes = await api.getCardTypes();
        
        const content = `
            <form id="memberCardForm">
                <div class="form-group">
                    <label for="cardTypeId">会员卡类型 *</label>
                    <select id="cardTypeId" required>
                        <option value="">请选择会员卡类型</option>
                        ${cardTypes.map(type => `
                            <option value="${type.id}">${type.name} - ¥${type.price} (${type.validity_days}天)</option>
                        `).join('')}
                    </select>
                </div>
                <div class="form-group">
                    <label for="purchaseDate">购买日期 *</label>
                    <input type="date" id="purchaseDate" value="${new Date().toISOString().split('T')[0]}" required>
                </div>
                <div class="form-group">
                    <label for="cardStatus">状态</label>
                    <select id="cardStatus">
                        <option value="active">有效</option>
                        <option value="suspended">暂停</option>
                    </select>
                </div>
                <div class="form-actions">
                    <button type="button" class="btn btn-secondary" onclick="closeModal()">取消</button>
                    <button type="submit" class="btn btn-primary">保存</button>
                </div>
            </form>
        `;
        
        showModal('添加会员卡', content);
        document.getElementById('memberCardForm').addEventListener('submit', saveMemberCard);
    } catch (error) {
        showMessage('加载会员卡类型失败', 'error');
        console.error('Failed to load card types:', error);
    }
}

async function saveMemberCard(event) {
    event.preventDefault();
    
    const cardData = {
        card_type_id: parseInt(document.getElementById('cardTypeId').value),
        purchase_date: document.getElementById('purchaseDate').value,
        status: document.getElementById('cardStatus').value
    };
    
    try {
        await api.createMemberCard(currentMemberId, cardData);
        showMessage('会员卡添加成功', 'success');
        closeModal();
        loadMemberCards(currentMemberId);
    } catch (error) {
        showMessage('添加会员卡失败', 'error');
        console.error('Failed to save member card:', error);
    }
}

// 课程报名管理
async function loadMemberEnrollments(memberId) {
    try {
        const enrollments = await api.getMemberEnrollments(memberId);
        displayMemberEnrollments(enrollments);
    } catch (error) {
        showMessage('加载课程报名失败', 'error');
        console.error('Failed to load member enrollments:', error);
    }
}

function displayMemberEnrollments(enrollments) {
    const container = document.getElementById('memberEnrollmentsContainer');
    
    if (enrollments.length === 0) {
        container.innerHTML = '<div class="no-data">暂无课程报名记录</div>';
        return;
    }
    
    container.innerHTML = enrollments.map(enrollment => `
        <div class="card">
            <div class="card-header">
                <h4>${enrollment.course_name}</h4>
                <span class="status status-${enrollment.status}">${getEnrollmentStatusText(enrollment.status)}</span>
            </div>
            <div class="card-body">
                <p><strong>课程描述:</strong> ${enrollment.course_description || '无'}</p>
                <p><strong>课程时长:</strong> ${enrollment.duration}分钟</p>
                <p><strong>课程价格:</strong> ¥${enrollment.price}</p>
                <p><strong>报名日期:</strong> ${enrollment.enrollment_date}</p>
            </div>
        </div>
    `).join('');
}

function getEnrollmentStatusText(status) {
    const statusMap = {
        'enrolled': '已报名',
        'in_progress': '进行中',
        'completed': '已完成',
        'cancelled': '已取消'
    };
    return statusMap[status] || status;
}

async function showMemberCourseForm() {
    try {
        const courses = await api.getCourses();
        
        const content = `
            <form id="memberCourseForm">
                <div class="form-group">
                    <label for="courseId">课程 *</label>
                    <select id="courseId" required>
                        <option value="">请选择课程</option>
                        ${courses.filter(course => course.status === 'active').map(course => `
                            <option value="${course.id}">${course.name} - ¥${course.price} (${course.duration}分钟)</option>
                        `).join('')}
                    </select>
                </div>
                <div class="form-group">
                    <label for="enrollmentDate">报名日期 *</label>
                    <input type="date" id="enrollmentDate" value="${new Date().toISOString().split('T')[0]}" required>
                </div>
                <div class="form-group">
                    <label for="enrollmentStatus">状态</label>
                    <select id="enrollmentStatus">
                        <option value="enrolled">已报名</option>
                        <option value="in_progress">进行中</option>
                        <option value="completed">已完成</option>
                        <option value="cancelled">已取消</option>
                    </select>
                </div>
                <div class="form-actions">
                    <button type="button" class="btn btn-secondary" onclick="closeModal()">取消</button>
                    <button type="submit" class="btn btn-primary">保存</button>
                </div>
            </form>
        `;
        
        showModal('课程报名', content);
        document.getElementById('memberCourseForm').addEventListener('submit', saveMemberCourseEnrollment);
    } catch (error) {
        showMessage('加载课程列表失败', 'error');
        console.error('Failed to load courses:', error);
    }
}

async function saveMemberCourseEnrollment(event) {
    event.preventDefault();
    
    const enrollmentData = {
        course_id: parseInt(document.getElementById('courseId').value),
        enrollment_date: document.getElementById('enrollmentDate').value,
        status: document.getElementById('enrollmentStatus').value
    };
    
    try {
        await api.createMemberEnrollment(currentMemberId, enrollmentData);
        showMessage('课程报名成功', 'success');
        closeModal();
        loadMemberEnrollments(currentMemberId);
    } catch (error) {
        showMessage('课程报名失败', 'error');
        console.error('Failed to save member course enrollment:', error);
    }
}

// 教练指派管理
async function loadMemberAssignments(memberId) {
    try {
        const assignments = await api.getMemberAssignments(memberId);
        displayMemberAssignments(assignments);
    } catch (error) {
        showMessage('加载教练指派失败', 'error');
        console.error('Failed to load member assignments:', error);
    }
}

function displayMemberAssignments(assignments) {
    const container = document.getElementById('memberAssignmentsContainer');
    
    if (assignments.length === 0) {
        container.innerHTML = '<div class="no-data">暂无教练指派记录</div>';
        return;
    }
    
    container.innerHTML = assignments.map(assignment => `
        <div class="card">
            <div class="card-header">
                <h4>${assignment.trainer_name}</h4>
                <span class="status status-${assignment.status}">${getAssignmentStatusText(assignment.status)}</span>
            </div>
            <div class="card-body">
                <p><strong>专业领域:</strong> ${assignment.trainer_specialization || '无'}</p>
                <p><strong>教练电话:</strong> ${assignment.trainer_phone || '未填写'}</p>
                <p><strong>指派类型:</strong> ${getAssignmentTypeText(assignment.assignment_type)}</p>
                <p><strong>指派日期:</strong> ${assignment.assignment_date}</p>
            </div>
        </div>
    `).join('');
}

function getAssignmentStatusText(status) {
    const statusMap = {
        'active': '活跃',
        'completed': '已完成',
        'cancelled': '已取消'
    };
    return statusMap[status] || status;
}

function getAssignmentTypeText(type) {
    const typeMap = {
        'personal_training': '私教',
        'group_class': '团体课',
        'consultation': '咨询',
        'fitness_assessment': '体能评估'
    };
    return typeMap[type] || type;
}

async function showMemberTrainerForm() {
    try {
        const trainers = await api.getTrainers();
        
        const content = `
            <form id="memberTrainerForm">
                <div class="form-group">
                    <label for="trainerId">教练 *</label>
                    <select id="trainerId" required>
                        <option value="">请选择教练</option>
                        ${trainers.filter(trainer => trainer.status === 'active').map(trainer => `
                            <option value="${trainer.id}">${trainer.name} - ${trainer.specialization || '无专业领域'}</option>
                        `).join('')}
                    </select>
                </div>
                <div class="form-group">
                    <label for="assignmentType">指派类型 *</label>
                    <select id="assignmentType" required>
                        <option value="">请选择指派类型</option>
                        <option value="personal_training">私教</option>
                        <option value="group_class">团体课</option>
                        <option value="consultation">咨询</option>
                        <option value="fitness_assessment">体能评估</option>
                    </select>
                </div>
                <div class="form-group">
                    <label for="assignmentDate">指派日期 *</label>
                    <input type="date" id="assignmentDate" value="${new Date().toISOString().split('T')[0]}" required>
                </div>
                <div class="form-group">
                    <label for="assignmentStatus">状态</label>
                    <select id="assignmentStatus">
                        <option value="active">活跃</option>
                        <option value="completed">已完成</option>
                        <option value="cancelled">已取消</option>
                    </select>
                </div>
                <div class="form-actions">
                    <button type="button" class="btn btn-secondary" onclick="closeModal()">取消</button>
                    <button type="submit" class="btn btn-primary">保存</button>
                </div>
            </form>
        `;
        
        showModal('指派教练', content);
        document.getElementById('memberTrainerForm').addEventListener('submit', saveMemberTrainerAssignment);
    } catch (error) {
        showMessage('加载教练列表失败', 'error');
        console.error('Failed to load trainers:', error);
    }
}

async function saveMemberTrainerAssignment(event) {
    event.preventDefault();
    
    const assignmentData = {
        trainer_id: parseInt(document.getElementById('trainerId').value),
        assignment_type: document.getElementById('assignmentType').value,
        assignment_date: document.getElementById('assignmentDate').value,
        status: document.getElementById('assignmentStatus').value
    };
    
    try {
        await api.createMemberAssignment(currentMemberId, assignmentData);
        showMessage('教练指派成功', 'success');
        closeModal();
        loadMemberAssignments(currentMemberId);
    } catch (error) {
        showMessage('教练指派失败', 'error');
        console.error('Failed to save member trainer assignment:', error);
    }
}

// 标签页切换时加载对应内容
function showTab(tabName) {
    const tabs = document.querySelectorAll('.detail-tab');
    const contents = document.querySelectorAll('.detail-content');
    
    tabs.forEach(tab => {
        tab.classList.remove('active');
        if (tab.getAttribute('data-tab') === tabName) {
            tab.classList.add('active');
        }
    });
    
    contents.forEach(content => {
        content.style.display = 'none';
        if (content.id === `${tabName}Content`) {
            content.style.display = 'block';
        }
    });
    
    // 根据选中的标签页加载对应数据
    if (currentMemberId) {
        switch(tabName) {
            case 'cards':
                loadMemberCards(currentMemberId);
                break;
            case 'enrollments':
                loadMemberEnrollments(currentMemberId);
                break;
            case 'assignments':
                loadMemberAssignments(currentMemberId);
                break;
        }
    }
}
````

#### 5. 教练管理模块

##### **插入**

````SQL
-- 插入教练课程分配数据
INSERT INTO trainer_course_assignments (trainer_id, course_id, assignment_date, course_type, notes) VALUES
(1, 3, '2023-06-01', 'group', '负责力量训练基础团体课'),
(1, 8, '2023-12-01', 'group', '负责CrossFit团体训练'),
(2, 1, '2023-08-15', 'group', '负责初级瑜伽团体课'),
(2, 5, '2023-11-01', 'private', '提供普拉提私教服务'),
(3, 2, '2023-09-01', 'group', '负责HIIT团体课'),
(3, 7, '2023-10-15', 'group', '负责拉伸放松课程'),
(4, 4, '2023-10-15', 'group', '负责搏击有氧团体课'),
(4, 8, '2024-01-01', 'special', '特殊搏击训练课程'),
(5, 5, '2023-11-01', 'group', '负责普拉提核心团体课'),
(5, 9, '2024-01-15', 'group', '负责舞蹈健身课程'),
(6, 6, '2024-01-15', 'private', '提供游泳私教服务'),
(6, 10, '2024-02-01', 'group', '负责老年健身课程'),
(7, 8, '2024-01-10', 'group', '负责功能性训练课程'),
(8, 11, '2024-01-05', 'private', '提供康复训练私教'),
(8, 12, '2024-02-01', 'special', '产后恢复专项课程');
````

![image-20250612130633962](C:\Users\Lenovo\AppData\Roaming\Typora\typora-user-images\image-20250612130633962.png)

##### **查询**

![image-20250612130714505](C:\Users\Lenovo\AppData\Roaming\Typora\typora-user-images\image-20250612130714505.png)

##### **删除（逻辑删除，软删除）**

**删除前**

![image-20250612130731397](C:\Users\Lenovo\AppData\Roaming\Typora\typora-user-images\image-20250612130731397.png)

**删除后**

![image-20250612130751873](C:\Users\Lenovo\AppData\Roaming\Typora\typora-user-images\image-20250612130751873.png)

````javascript
async function loadTrainersTab() {
    const mainContent = document.getElementById('main-content');
    mainContent.innerHTML = `
        <div class="trainers-section">
            <div class="section-header">
                <h2>教练管理</h2>
                <button class="btn btn-primary" onclick="showTrainerForm()">添加教练</button>
            </div>
            <div class="search-bar">
                <input type="text" id="trainerSearch" placeholder="搜索教练姓名或专业领域...">
                <button onclick="searchTrainers()">搜索</button>
            </div>
            <div id="trainersContainer" class="content-grid">
                <!-- 教练列表将在这里显示 -->
            </div>
        </div>
    `;
    
    loadTrainers();
}

async function loadTrainers() {
    try {
        const trainers = await api.getTrainers();
        displayTrainers(trainers);
    } catch (error) {
        showMessage('加载教练列表失败', 'error');
        console.error('Failed to load trainers:', error);
    }
}

function displayTrainers(trainers) {
    const container = document.getElementById('trainersContainer');
    
    if (trainers.length === 0) {
        container.innerHTML = '<div class="no-data">暂无教练数据</div>';
        return;
    }
    
    container.innerHTML = trainers.map(trainer => `
        <div class="card trainer-card">
            <div class="card-header">
                <h3>${trainer.name}</h3>
                <span class="status status-${trainer.status}">${getStatusText(trainer.status)}</span>
            </div>
            <div class="card-body">
                <p><strong>电话:</strong> ${trainer.phone || '未填写'}</p>
                <p><strong>邮箱:</strong> ${trainer.email || '未填写'}</p>
                <p><strong>专业领域:</strong> ${trainer.specialization || '未填写'}</p>
                <p><strong>入职日期:</strong> ${trainer.hire_date || '未知'}</p>
            </div>
            <div class="card-actions">
                <button class="btn btn-info" onclick="showTrainerDetail(${trainer.id})">查看详情</button>
                <button class="btn btn-warning" onclick="editTrainer(${trainer.id})">编辑</button>
                <button class="btn btn-danger" onclick="deleteTrainer(${trainer.id})">删除</button>
            </div>
        </div>
    `).join('');
}

function showTrainerDetail(trainerId) {
    loadTrainerDetailTab(trainerId);
}

// filepath: frontend/scripts/trainerDetail.js
let currentTrainerId = null;

async function loadTrainerDetailTab(trainerId) {
    currentTrainerId = trainerId;
    
    try {
        const trainer = await api.getTrainer(trainerId);
        
        const mainContent = document.getElementById('main-content');
        mainContent.innerHTML = `
            <div class="trainer-detail">
                <div class="detail-header">
                    <button class="btn btn-secondary" onclick="loadTrainersTab()">← 返回教练列表</button>
                    <h2>${trainer.name} - 教练详情</h2>
                </div>
                
                <div class="trainer-info">
                    <div class="info-grid">
                        <div><strong>姓名:</strong> ${trainer.name}</div>
                        <div><strong>电话:</strong> ${trainer.phone || '未填写'}</div>
                        <div><strong>邮箱:</strong> ${trainer.email || '未填写'}</div>
                        <div><strong>专业领域:</strong> ${trainer.specialization || '未填写'}</div>
                        <div><strong>入职日期:</strong> ${trainer.hire_date || '未知'}</div>
                        <div><strong>状态:</strong> <span class="status status-${trainer.status}">${getStatusText(trainer.status)}</span></div>
                    </div>
                </div>
                
                <div class="trainer-detail-tabs">
                    <button class="trainer-detail-tab active" data-tab="courses" onclick="showTrainerTab('courses')">课程分配</button>
                    <button class="trainer-detail-tab" data-tab="members" onclick="showTrainerTab('members')">会员指派</button>
                </div>
                
                <div id="trainerCoursesContent" class="trainer-detail-content">
                    <div class="content-header">
                        <h3>课程分配</h3>
                        <button class="btn btn-primary" onclick="showTrainerCourseForm()">分配课程</button>
                    </div>
                    <div id="trainerCoursesContainer"></div>
                </div>
                
                <div id="trainerMembersContent" class="trainer-detail-content" style="display: none;">
                    <div class="content-header">
                        <h3>会员指派</h3>
                    </div>
                    <div id="trainerMembersContainer"></div>
                </div>
            </div>
        `;
        
        // 加载默认标签页内容
        loadTrainerCourses(trainerId);
    } catch (error) {
        showMessage('加载教练详情失败', 'error');
        console.error('Failed to load trainer detail:', error);
    }
}

async function loadTrainerCourses(trainerId) {
    try {
        const courses = await api.getTrainerCourses(trainerId);
        displayTrainerCourses(courses);
    } catch (error) {
        showMessage('加载教练课程失败', 'error');
        console.error('Failed to load trainer courses:', error);
    }
}

function displayTrainerCourses(courses) {
    const container = document.getElementById('trainerCoursesContainer');
    
    if (courses.length === 0) {
        container.innerHTML = '<div class="no-data">暂无课程分配记录</div>';
        return;
    }
    
    container.innerHTML = courses.map(course => `
        <div class="card">
            <div class="card-header">
                <h4>${course.course_name}</h4>
                <span class="status status-${course.status}">${getStatusText(course.status)}</span>
            </div>
            <div class="card-body">
                <p><strong>课程描述:</strong> ${course.course_description || '无'}</p>
                <p><strong>课程时长:</strong> ${course.duration}分钟</p>
                <p><strong>课程价格:</strong> ¥${course.price}</p>
                <p><strong>分配日期:</strong> ${course.assignment_date}</p>
            </div>
        </div>
    `).join('');
}

async function loadTrainerMembers(trainerId) {
    try {
        const members = await api.getTrainerMembers(trainerId);
        displayTrainerMembers(members);
    } catch (error) {
        showMessage('加载教练会员指派失败', 'error');
        console.error('Failed to load trainer members:', error);
    }
}

function displayTrainerMembers(members) {
    const container = document.getElementById('trainerMembersContainer');
    
    if (members.length === 0) {
        container.innerHTML = '<div class="no-data">暂无会员指派记录</div>';
        return;
    }
    
    container.innerHTML = members.map(member => `
        <div class="card">
            <div class="card-header">
                <h4>${member.member_name}</h4>
                <span class="status status-${member.status}">${getAssignmentStatusText(member.status)}</span>
            </div>
            <div class="card-body">
                <p><strong>会员电话:</strong> ${member.member_phone || '未填写'}</p>
                <p><strong>会员邮箱:</strong> ${member.member_email || '未填写'}</p>
                <p><strong>指派类型:</strong> ${getAssignmentTypeText(member.assignment_type)}</p>
                <p><strong>指派日期:</strong> ${member.assignment_date}</p>
            </div>
        </div>
    `).join('');
}

function showTrainerTab(tabName) {
    const tabs = document.querySelectorAll('.trainer-detail-tab');
    const contents = document.querySelectorAll('.trainer-detail-content');
    
    tabs.forEach(tab => {
        tab.classList.remove('active');
        if (tab.getAttribute('data-tab') === tabName) {
            tab.classList.add('active');
        }
    });
    
    contents.forEach(content => {
        content.style.display = 'none';
        if (content.id === `trainer${tabName.charAt(0).toUpperCase() + tabName.slice(1)}Content`) {
            content.style.display = 'block';
        }
    });
    
    // 根据选中的标签页加载对应数据
    if (currentTrainerId) {
        switch(tabName) {
            case 'courses':
                loadTrainerCourses(currentTrainerId);
                break;
            case 'members':
                loadTrainerMembers(currentTrainerId);
                break;
        }
    }
}
````

#### 6. 教练详情管理模块

##### **插入**

````SQL
-- 插入会员教练指派数据（同会员详情模块中的插入数据）
INSERT INTO member_trainer_assignments (member_id, trainer_id, assignment_date, assignment_type, notes) VALUES
(1, 1, '2024-01-18', 'personal_training_package', '购买10次私教课程包'),
(2, 2, '2024-02-03', 'personal_training_package', '年卡用户，每月2次私教'),
(3, 1, '2024-02-22', 'consultation', '力量训练咨询'),
(4, 6, '2024-02-17', 'personal_training_package', 'VIP会员无限私教'),
(4, 2, '2024-02-19', 'personal_training_package', 'VIP会员瑜伽私教'),
(5, 3, '2024-02-02', 'personal_training_package', '购买5次有氧私教'),
(6, 2, '2024-02-13', 'consultation', '瑜伽入门指导'),
(7, 8, '2024-01-28', 'personal_training_package', '康复训练专项指导'),
(8, 5, '2024-02-24', 'consultation', '普拉提动作指导'),
(8, 1, '2024-02-25', 'personal_training_package', '力量训练私教');

-- 插入教练课程分配数据
INSERT INTO trainer_course_assignments (trainer_id, course_id, assignment_date, course_type, notes) VALUES
(1, 3, '2023-06-01', 'group', '负责力量训练基础团体课'),
(1, 8, '2023-12-01', 'group', '负责CrossFit团体训练'),
(2, 1, '2023-08-15', 'group', '负责初级瑜伽团体课'),
(2, 5, '2023-11-01', 'private', '提供普拉提私教服务'),
(3, 2, '2023-09-01', 'group', '负责HIIT团体课'),
(3, 7, '2023-10-15', 'group', '负责拉伸放松课程'),
(4, 4, '2023-10-15', 'group', '负责搏击有氧团体课'),
(4, 8, '2024-01-01', 'special', '特殊搏击训练课程'),
(5, 5, '2023-11-01', 'group', '负责普拉提核心团体课'),
(5, 9, '2024-01-15', 'group', '负责舞蹈健身课程'),
(6, 6, '2024-01-15', 'private', '提供游泳私教服务'),
(6, 10, '2024-02-01', 'group', '负责老年健身课程'),
(7, 8, '2024-01-10', 'group', '负责功能性训练课程'),
(8, 11, '2024-01-05', 'private', '提供康复训练私教'),
(8, 12, '2024-02-01', 'special', '产后恢复专项课程');
````

![image-20250612131154275](C:\Users\Lenovo\AppData\Roaming\Typora\typora-user-images\image-20250612131154275.png)

![image-20250612131224315](C:\Users\Lenovo\AppData\Roaming\Typora\typora-user-images\image-20250612131224315.png)

##### **删除**

![image-20250612131249512](C:\Users\Lenovo\AppData\Roaming\Typora\typora-user-images\image-20250612131249512.png)

![image-20250612131313364](C:\Users\Lenovo\AppData\Roaming\Typora\typora-user-images\image-20250612131313364.png)

![image-20250612131355018](C:\Users\Lenovo\AppData\Roaming\Typora\typora-user-images\image-20250612131355018.png)

![image-20250612131419554](C:\Users\Lenovo\AppData\Roaming\Typora\typora-user-images\image-20250612131419554.png)

````javascript
// 课程类型转换函数
function getCourseTypeText(type) {
    const typeMap = {
        'regular': '常规课程',
        'special': '特色课程',
        'private': '私教课程',
        'group': '团体课程'
    };
    return typeMap[type] || type;
}

// 指派类型转换函数
function getAssignmentTypeText(type) {
    const typeMap = {
        'personal': '私教',
        'group': '团体课',
        'consultation': '咨询',
        'assessment': '体能评估'
    };
    return typeMap[type] || type;
}

// 加载教练课程分配列表
async function loadTrainerCourses(trainerId) {
    const tbody = document.getElementById('trainerCoursesTableBody');
    tbody.innerHTML = '<tr><td colspan="6" class="loading">正在加载教练课程数据...</td></tr>';
    
    const response = await api.getTrainerCourses(trainerId);
    
    if (response.success) {
        tbody.innerHTML = '';
        if (response.data.length === 0) {
            tbody.innerHTML = '<tr><td colspan="6">该教练暂无分配课程</td></tr>';
        } else {
            response.data.forEach(assignment => {
                const row = document.createElement('tr');
                row.innerHTML = `
                    <td>${assignment.id}</td>
                    <td>${assignment.course_name}</td>
                    <td>${formatDate(assignment.assignment_date)}</td>
                    <td>${getCourseTypeText(assignment.course_type)}</td>
                    <td>${assignment.notes || ''}</td>
                    <td>
                        <button class="btn" onclick="editTrainerCourse(${assignment.id})">编辑</button>
                        <button class="btn btn-danger" onclick="deleteTrainerCourse(${assignment.id}, '${assignment.course_name}')">取消</button>
                    </td>
                `;
                tbody.appendChild(row);
            });
        }
    } else {
        tbody.innerHTML = `<tr><td colspan="6">加载失败: ${response.message}</td></tr>`;
    }
}

// 加载教练指派会员列表
async function loadTrainerMembers(trainerId) {
    const tbody = document.getElementById('trainerMembersTableBody');
    tbody.innerHTML = '<tr><td colspan="6" class="loading">正在加载教练会员数据...</td></tr>';
    
    const response = await api.getTrainerMembers(trainerId);
    
    if (response.success) {
        tbody.innerHTML = '';
        if (response.data.length === 0) {
            tbody.innerHTML = '<tr><td colspan="6">该教练暂无指派会员</td></tr>';
        } else {
            response.data.forEach(assignment => {
                const row = document.createElement('tr');
                row.innerHTML = `
                    <td>${assignment.id}</td>
                    <td>${assignment.member_name}</td>
                    <td>${formatDate(assignment.assignment_date)}</td>
                    <td>${getAssignmentTypeText(assignment.assignment_type)}</td>
                    <td>${assignment.notes || ''}</td>
                    <td>
                        <button class="btn" onclick="editTrainerMember(${assignment.id})">编辑</button>
                        <button class="btn btn-danger" onclick="deleteTrainerMember(${assignment.id}, '${assignment.member_name}')">解除</button>
                    </td>
                `;
                tbody.appendChild(row);
            });
        }
    } else {
        tbody.innerHTML = `<tr><td colspan="6">加载失败: ${response.message}</td></tr>`;
    }
}

// 显示教练课程分配表单
async function showTrainerCourseForm(assignmentId = null) {
    const courses = await api.getCourses(true);
    if (!courses.success) {
        showMessage('无法加载课程列表', 'error');
        return;
    }
    
    let assignment = null;
    if (assignmentId) {
        const assignmentsResponse = await api.getTrainerCourses(currentTrainerId);
        if (assignmentsResponse.success) {
            assignment = assignmentsResponse.data.find(a => a.id === assignmentId);
        }
    }
    
    const title = assignment ? '编辑课程分配' : '分配新课程';
    const courseOptions = courses.data.map(course => 
        `<option value="${course.id}" ${assignment && assignment.course_id === course.id ? 'selected' : ''}>${course.name}</option>`
    ).join('');
    
    const formContent = `
        <div class="form">
            <h3>${title}</h3>
            <div class="form-group">
                <label for="trainerCourse">课程 *</label>
                <select id="trainerCourse" required>
                    <option value="">请选择课程</option>
                    ${courseOptions}
                </select>
            </div>
            <div class="form-group">
                <label for="trainerCourseDate">分配日期 *</label>
                <input type="date" id="trainerCourseDate" value="${assignment ? assignment.assignment_date.split(' ')[0] : getTodayDate()}" required>
            </div>
            <div class="form-group">
                <label for="trainerCourseType">课程类型</label>
                <select id="trainerCourseType">
                    <option value="">请选择类型</option>
                    <option value="regular" ${assignment && assignment.course_type === 'regular' ? 'selected' : ''}>常规课程</option>
                    <option value="special" ${assignment && assignment.course_type === 'special' ? 'selected' : ''}>特色课程</option>
                    <option value="private" ${assignment && assignment.course_type === 'private' ? 'selected' : ''}>私教课程</option>
                    <option value="group" ${assignment && assignment.course_type === 'group' ? 'selected' : ''}>团体课程</option>
                </select>
            </div>
            <div class="form-group">
                <label for="trainerCourseNotes">备注</label>
                <textarea id="trainerCourseNotes">${assignment ? assignment.notes || '' : ''}</textarea>
            </div>
            <div class="form-actions">
                <button type="button" class="btn" onclick="closeModal()">取消</button>
                <button type="button" class="btn btn-primary" onclick="saveTrainerCourse(${assignmentId || 'null'})">${assignment ? '更新' : '分配'}</button>
            </div>
        </div>
    `;
    
    showModal(formContent);
}

// 保存教练课程分配
async function saveTrainerCourse(assignmentId) {
    const assignmentData = {
        course_id: parseInt(document.getElementById('trainerCourse').value),
        assignment_date: document.getElementById('trainerCourseDate').value,
        course_type: document.getElementById('trainerCourseType').value,
        notes: document.getElementById('trainerCourseNotes').value.trim()
    };
    
    if (!assignmentData.course_id) {
        showMessage('请选择课程', 'error');
        return;
    }
    
    if (!assignmentData.assignment_date) {
        showMessage('分配日期不能为空', 'error');
        return;
    }
    
    let response;
    if (assignmentId) {
        response = await api.updateTrainerCourse(assignmentId, assignmentData);
    } else {
        response = await api.assignCourseToTrainer(currentTrainerId, assignmentData);
    }
    
    if (response.success) {
        showMessage(response.message, 'success');
        closeModal();
        loadTrainerCourses(currentTrainerId);
    } else {
        showMessage(response.message, 'error');
    }
}

// 显示教练会员指派表单
async function showTrainerMemberForm(assignmentId = null) {
    const members = await api.getMembers();
    if (!members.success) {
        showMessage('无法加载会员列表', 'error');
        return;
    }
    
    let assignment = null;
    if (assignmentId) {
        const assignmentsResponse = await api.getTrainerMembers(currentTrainerId);
        if (assignmentsResponse.success) {
            assignment = assignmentsResponse.data.find(a => a.id === assignmentId);
        }
    }
    
    const title = assignment ? '编辑会员指派' : '指派新会员';
    const memberOptions = members.data.filter(member => member.status === 'active').map(member => 
        `<option value="${member.id}" ${assignment && assignment.member_id === member.id ? 'selected' : ''}>${member.name}</option>`
    ).join('');
    
    const formContent = `
        <div class="form">
            <h3>${title}</h3>
            <div class="form-group">
                <label for="trainerMember">会员 *</label>
                <select id="trainerMember" required>
                    <option value="">请选择会员</option>
                    ${memberOptions}
                </select>
            </div>
            <div class="form-group">
                <label for="trainerMemberDate">指派日期 *</label>
                <input type="date" id="trainerMemberDate" value="${assignment ? assignment.assignment_date.split(' ')[0] : getTodayDate()}" required>
            </div>
            <div class="form-group">
                <label for="trainerMemberType">指派类型</label>
                <select id="trainerMemberType">
                    <option value="">请选择类型</option>
                    <option value="personal" ${assignment && assignment.assignment_type === 'personal' ? 'selected' : ''}>私教</option>
                    <option value="group" ${assignment && assignment.assignment_type === 'group' ? 'selected' : ''}>团体课</option>
                    <option value="consultation" ${assignment && assignment.assignment_type === 'consultation' ? 'selected' : ''}>咨询</option>
                    <option value="assessment" ${assignment && assignment.assignment_type === 'assessment' ? 'selected' : ''}>体能评估</option>
                </select>
            </div>
            <div class="form-group">
                <label for="trainerMemberNotes">备注</label>
                <textarea id="trainerMemberNotes">${assignment ? assignment.notes || '' : ''}</textarea>
            </div>
            <div class="form-actions">
                <button type="button" class="btn" onclick="closeModal()">取消</button>
                <button type="button" class="btn btn-primary" onclick="saveTrainerMember(${assignmentId || 'null'})">${assignment ? '更新' : '指派'}</button>
            </div>
        </div>
    `;
    
    showModal(formContent);
}

// 保存教练会员指派
async function saveTrainerMember(assignmentId) {
    const assignmentData = {
        member_id: parseInt(document.getElementById('trainerMember').value),
        assignment_date: document.getElementById('trainerMemberDate').value,
        assignment_type: document.getElementById('trainerMemberType').value,
        notes: document.getElementById('trainerMemberNotes').value.trim()
    };
    
    if (!assignmentData.member_id) {
        showMessage('请选择会员', 'error');
        return;
    }
    
    if (!assignmentData.assignment_date) {
        showMessage('指派日期不能为空', 'error');
        return;
    }
    
    let response;
    if (assignmentId) {
        response = await api.updateMemberAssignment(assignmentId, assignmentData);
    } else {
        response = await api.assignTrainerToMember(assignmentData.member_id, {
            trainer_id: currentTrainerId,
            assignment_date: assignmentData.assignment_date,
            assignment_type: assignmentData.assignment_type,
            notes: assignmentData.notes
        });
    }
    
    if (response.success) {
        showMessage(response.message, 'success');
        closeModal();
        loadTrainerMembers(currentTrainerId);
    } else {
        showMessage(response.message, 'error');
    }
}

function editTrainerCourse(assignmentId) {
    showTrainerCourseForm(assignmentId);
}

function deleteTrainerCourse(assignmentId, courseName) {
    confirmAction(`确定要取消教练对 "${courseName}" 课程的分配吗？`, async () => {
        const response = await api.deleteTrainerCourse(assignmentId);
        if (response.success) {
            showMessage(response.message, 'success');
            loadTrainerCourses(currentTrainerId);
        } else {
            showMessage(response.message, 'error');
        }
    });
}

function editTrainerMember(assignmentId) {
    showTrainerMemberForm(assignmentId);
}

function deleteTrainerMember(assignmentId, memberName) {
    confirmAction(`确定要解除教练与会员 "${memberName}" 的指派关系吗？`, async () => {
        const response = await api.deleteMemberAssignment(assignmentId);
        if (response.success) {
            showMessage(response.message, 'success');
            loadTrainerMembers(currentTrainerId);
        } else {
            showMessage(response.message, 'error');
        }
    });
}
````

#### 7. 课程管理模块

##### **插入**

````sQL
-- 插入课程数据
INSERT INTO courses (name, description, default_duration_minutes, status) VALUES
('初级瑜伽', '适合初学者的基础瑜伽课程，注重柔韧性和呼吸练习', 60, 'active'),
('高强度间歇训练', 'HIIT训练，快速燃脂，提高心肺功能', 45, 'active'),
('力量训练基础', '器械使用指导和基础力量训练', 90, 'active'),
('搏击有氧', '结合拳击动作的有氧运动，释放压力', 60, 'active'),
('普拉提核心', '专注核心肌群训练的普拉提课程', 50, 'active'),
('游泳技巧提升', '改进游泳技巧，提高游泳效率', 60, 'active'),
('拉伸放松', '全身拉伸和放松训练', 30, 'active'),
('CrossFit训练', '综合功能性训练，挑战极限', 75, 'active'),
('舞蹈健身', '结合舞蹈动作的趣味健身课程', 55, 'active'),
('老年健身', '适合中老年人的温和健身课程', 40, 'active'),
('康复训练', '针对伤病恢复的专业康复训练', 45, 'active'),
('产后恢复', '专为产后女性设计的恢复训练', 50, 'active');
````

![image-20250611200136095](C:\Users\Lenovo\AppData\Roaming\Typora\typora-user-images\image-20250611200136095.png)

##### **查询**

![image-20250611200249204](C:\Users\Lenovo\AppData\Roaming\Typora\typora-user-images\image-20250611200249204.png)

##### 删除（逻辑删除，软删除）

**删除前**

![image-20250612130530613](C:\Users\Lenovo\AppData\Roaming\Typora\typora-user-images\image-20250612130530613.png)

**删除后**

![image-20250612130612033](C:\Users\Lenovo\AppData\Roaming\Typora\typora-user-images\image-20250612130612033.png)

````javascript
async function loadCoursesTab() {
    const mainContent = document.getElementById('main-content');
    mainContent.innerHTML = `
        <div class="courses-section">
            <div class="section-header">
                <h2>课程管理</h2>
                <button class="btn btn-primary" onclick="showCourseForm()">添加课程</button>
            </div>
            <div class="search-bar">
                <input type="text" id="courseSearch" placeholder="搜索课程名称或描述...">
                <button onclick="searchCourses()">搜索</button>
            </div>
            <div id="coursesContainer" class="content-grid">
                <!-- 课程列表将在这里显示 -->
            </div>
        </div>
    `;
    
    loadCourses();
}

async function loadCourses() {
    try {
        const courses = await api.getCourses();
        displayCourses(courses);
    } catch (error) {
        showMessage('加载课程列表失败', 'error');
        console.error('Failed to load courses:', error);
    }
}

async function searchCourses() {
    const searchTerm = document.getElementById('courseSearch').value;
    try {
        const courses = await api.getCourses(searchTerm);
        displayCourses(courses);
    } catch (error) {
        showMessage('搜索课程失败', 'error');
        console.error('Failed to search courses:', error);
    }
}

function displayCourses(courses) {
    const container = document.getElementById('coursesContainer');
    
    if (courses.length === 0) {
        container.innerHTML = '<div class="no-data">暂无课程数据</div>';
        return;
    }
    
    container.innerHTML = courses.map(course => `
        <div class="card course-card">
            <div class="card-header">
                <h3>${course.name}</h3>
                <span class="status status-${course.status}">${getStatusText(course.status)}</span>
            </div>
            <div class="card-body">
                <p><strong>描述:</strong> ${course.description || '无描述'}</p>
                <p><strong>时长:</strong> ${course.duration}分钟</p>
                <p><strong>价格:</strong> ¥${course.price}</p>
            </div>
            <div class="card-actions">
                <button class="btn btn-warning" onclick="editCourse(${course.id})">编辑</button>
                <button class="btn btn-danger" onclick="deleteCourse(${course.id})">删除</button>
            </div>
        </div>
    `).join('');
}

function showCourseForm(courseId = null) {
    const isEdit = courseId !== null;
    const title = isEdit ? '编辑课程' : '添加课程';
    
    const content = `
        <form id="courseForm">
            <input type="hidden" id="courseId" value="${courseId || ''}">
            <div class="form-group">
                <label for="courseName">课程名称 *</label>
                <input type="text" id="courseName" required>
            </div>
            <div class="form-group">
                <label for="courseDescription">课程描述</label>
                <textarea id="courseDescription" rows="3"></textarea>
            </div>
            <div class="form-group">
                <label for="courseDuration">课程时长(分钟) *</label>
                <input type="number" id="courseDuration" min="1" required>
            </div>
            <div class="form-group">
                <label for="coursePrice">课程价格 *</label>
                <input type="number" id="coursePrice" min="0" step="0.01" required>
            </div>
            <div class="form-group">
                <label for="courseStatus">状态</label>
                <select id="courseStatus">
                    <option value="active">活跃</option>
                    <option value="inactive">非活跃</option>
                </select>
            </div>
            <div class="form-actions">
                <button type="button" class="btn btn-secondary" onclick="closeModal()">取消</button>
                <button type="submit" class="btn btn-primary">保存</button>
            </div>
        </form>
    `;
    
    showModal(title, content);
    document.getElementById('courseForm').addEventListener('submit', saveCourse);
}

async function saveCourse(event) {
    event.preventDefault();
    
    const courseData = {
        name: document.getElementById('courseName').value,
        description: document.getElementById('courseDescription').value,
        duration: parseInt(document.getElementById('courseDuration').value),
        price: parseFloat(document.getElementById('coursePrice').value),
        status: document.getElementById('courseStatus').value
    };
    
    try {
        await api.createCourse(courseData);
        showMessage('课程保存成功', 'success');
        closeModal();
        loadCourses();
    } catch (error) {
        showMessage('保存课程失败', 'error');
        console.error('Failed to save course:', error);
    }
}
````

#### 8. 会员卡管理模块

##### **插入**

````sQL
-- 插入会员卡类型数据
INSERT INTO membership_card_types (name, price, duration_days, description) VALUES
('月卡', 299.00, 30, '30天有效期，可使用所有基础设施和团体课程'),
('季卡', 799.00, 90, '90天有效期，包含基础设施、团体课程和2次私教体验'),
('半年卡', 1399.00, 180, '180天有效期，包含所有设施、无限团体课程和4次私教'),
('年卡', 2399.00, 365, '365天有效期，包含所有服务、无限课程和每月2次私教'),
('VIP年卡', 3999.00, 365, '365天有效期，VIP专享区域、无限私教和营养指导');
````

![image-20250612133110324](C:\Users\Lenovo\AppData\Roaming\Typora\typora-user-images\image-20250612133110324.png)

##### **查询**

![image-20250612133132005](C:\Users\Lenovo\AppData\Roaming\Typora\typora-user-images\image-20250612133132005.png)

##### 删除

**删除前**

![image-20250612133153582](C:\Users\Lenovo\AppData\Roaming\Typora\typora-user-images\image-20250612133153582.png)

**删除后**

![image-20250612133217631](C:\Users\Lenovo\AppData\Roaming\Typora\typora-user-images\image-20250612133217631.png)

#### 9. 样式设计

````css
* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    background-color: #f5f5f5;
    color: #333;
}

.container {
    max-width: 1200px;
    margin: 0 auto;
    padding: 20px;
}

header {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    padding: 20px;
    border-radius: 10px;
    margin-bottom: 20px;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

header h1 {
    margin-bottom: 20px;
    text-align: center;
    font-size: 2.5em;
}

.nav-tabs {
    display: flex;
    justify-content: center;
    gap: 10px;
    flex-wrap: wrap;
}

.nav-tab {
    background: rgba(255, 255, 255, 0.2);
    color: white;
    border: none;
    padding: 12px 24px;
    border-radius: 25px;
    cursor: pointer;
    transition: all 0.3s ease;
    font-size: 16px;
}

.nav-tab:hover {
    background: rgba(255, 255, 255, 0.3);
    transform: translateY(-2px);
}

.nav-tab.active {
    background: rgba(255, 255, 255, 0.9);
    color: #667eea;
    font-weight: bold;
}

.dashboard {
    text-align: center;
}

.stats-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
    gap: 20px;
    margin-top: 30px;
}

.stat-card {
    background: white;
    padding: 30px;
    border-radius: 10px;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    transition: transform 0.3s ease;
}

.stat-card:hover {
    transform: translateY(-5px);
}

.stat-card h3 {
    color: #666;
    margin-bottom: 15px;
    font-size: 1.2em;
}

.stat-number {
    font-size: 3em;
    font-weight: bold;
    color: #667eea;
}

.section-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 20px;
    flex-wrap: wrap;
    gap: 10px;
}

.section-header h2 {
    color: #333;
    font-size: 2em;
}

.search-bar {
    display: flex;
    gap: 10px;
    margin-bottom: 20px;
    align-items: center;
}

.search-bar input {
    flex: 1;
    padding: 12px;
    border: 1px solid #ddd;
    border-radius: 6px;
    font-size: 16px;
}

.content-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
    gap: 20px;
}

.card {
    background: white;
    border-radius: 10px;
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
    overflow: hidden;
    transition: all 0.3s ease;
}

.card:hover {
    transform: translateY(-3px);
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.15);
}

.card-header {
    padding: 20px;
    background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
    color: white;
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.card-header h3, .card-header h4 {
    margin: 0;
    font-size: 1.3em;
}

.card-body {
    padding: 20px;
}

.card-body p {
    margin-bottom: 10px;
    line-height: 1.5;
}

.card-actions {
    padding: 15px 20px;
    background: #f8f9fa;
    display: flex;
    gap: 10px;
    flex-wrap: wrap;
}

.btn {
    padding: 8px 16px;
    border: none;
    border-radius: 6px;
    cursor: pointer;
    font-size: 14px;
    font-weight: 500;
    transition: all 0.3s ease;
    text-decoration: none;
    display: inline-block;
    text-align: center;
}

.btn-primary {
    background: #667eea;
    color: white;
}

.btn-primary:hover {
    background: #5a6fd8;
    transform: translateY(-1px);
}

.btn-secondary {
    background: #6c757d;
    color: white;
}

.btn-secondary:hover {
    background: #545b62;
}

.btn-info {
    background: #17a2b8;
    color: white;
}

.btn-info:hover {
    background: #138496;
}

.btn-warning {
    background: #ffc107;
    color: #212529;
}

.btn-warning:hover {
    background: #e0a800;
}

.btn-danger {
    background: #dc3545;
    color: white;
}

.btn-danger:hover {
    background: #c82333;
}

.status {
    padding: 4px 12px;
    border-radius: 15px;
    font-size: 12px;
    font-weight: bold;
    text-transform: uppercase;
}

.status-active {
    background: #d4edda;
    color: #155724;
}

.status-inactive {
    background: #f8d7da;
    color: #721c24;
}

.status-suspended {
    background: #fff3cd;
    color: #856404;
}

/* 模态框样式 */
.modal {
    display: none;
    position: fixed;
    z-index: 1000;
    left: 0;
    top: 0;
    width: 100%;
    height: 100%;
    background-color: rgba(0, 0, 0, 0.5);
}

.modal-content {
    background-color: white;
    margin: 5% auto;
    padding: 0;
    border-radius: 10px;
    width: 90%;
    max-width: 500px;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
}

.modal-header {
    padding: 20px;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    border-radius: 10px 10px 0 0;
}

.modal-body {
    padding: 20px;
}

.form-group {
    margin-bottom: 20px;
}

.form-group label {
    display: block;
    margin-bottom: 5px;
    font-weight: 500;
    color: #333;
}

.form-group input,
.form-group select,
.form-group textarea {
    width: 100%;
    padding: 10px;
    border: 1px solid #ddd;
    border-radius: 6px;
    font-size: 16px;
    transition: border-color 0.3s ease;
}

.form-group input:focus,
.form-group select:focus,
.form-group textarea:focus {
    outline: none;
    border-color: #667eea;
    box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
}

.form-actions {
    display: flex;
    gap: 10px;
    justify-content: flex-end;
    margin-top: 20px;
}

.info-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
    gap: 15px;
    padding: 20px;
    background: white;
    border-radius: 10px;
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
    margin-bottom: 20px;
}

.detail-tabs,
.trainer-detail-tabs {
    display: flex;
    gap: 10px;
    margin-bottom: 20px;
    flex-wrap: wrap;
}

.detail-tab,
.trainer-detail-tab {
    padding: 10px 20px;
    background: white;
    border: 2px solid #ddd;
    border-radius: 25px;
    cursor: pointer;
    transition: all 0.3s ease;
    font-weight: 500;
}

.detail-tab.active,
.trainer-detail-tab.active {
    background: #667eea;
    color: white;
    border-color: #667eea;
}

.detail-content,
.trainer-detail-content {
    background: white;
    border-radius: 10px;
    padding: 20px;
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

.content-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 20px;
}

.no-data {
    text-align: center;
    color: #666;
    font-style: italic;
    padding: 40px;
    background: #f8f9fa;
    border-radius: 10px;
}

/* 消息提示样式 */
.message {
    position: fixed;
    top: 20px;
    right: 20px;
    padding: 15px 20px;
    border-radius: 6px;
    color: white;
    font-weight: 500;
    z-index: 1001;
    animation: slideIn 0.3s ease;
}

.message-success {
    background: #28a745;
}

.message-error {
    background: #dc3545;
}

@keyframes slideIn {
    from {
        transform: translateX(100%);
        opacity: 0;
    }
    to {
        transform: translateX(0);
        opacity: 1;
    }
}

/* 响应式设计 */
@media (max-width: 768px) {
    .container {
        padding: 10px;
    }
    
    .nav-tabs {
        flex-direction: column;
        align-items: center;
    }
    
    .nav-tab {
        width: 200px;
        text-align: center;
    }
    
    .section-header {
        flex-direction: column;
        align-items: stretch;
    }
    
    .content-grid {
        grid-template-columns: 1fr;
    }
    
    .search-bar {
        flex-direction: column;
    }
    
    .card-actions {
        flex-direction: column;
    }
    
    .info-grid {
        grid-template-columns: 1fr;
    }
    
    .detail-tabs,
    .trainer-detail-tabs {
        flex-direction: column;
    }
    
    .modal-content {
        width: 95%;
        margin: 10% auto;
    }
}
````

## 六、实验总结

通过本次健身房管理系统的开发，我获得了全面而深入的学习体验：

### 技术能力提升

🔧 **数据库设计能力**：从需求分析到E-R建模，再到物理设计，完整掌握了数据库设计的全流程。特别是在处理复杂的多对多关系（如会员-课程、教练-会员）时，深刻理解了关系型数据库的设计原则。

📊 **SQL技能精进**：熟练运用了复杂的多表连接查询、聚合函数、子查询等高级SQL技术。在实现会员详情查询、统计分析等功能时，体验了SQL的强大威力。

🌐 **全栈开发经验**：第一次完整实现了前后端分离的架构设计，使用Flask构建RESTful API，JavaScript实现动态前端交互，获得了现代Web开发的完整体验。

### 系统设计思维

🏗️ **模块化架构设计**：项目采用了清晰的模块化设计，前端按功能模块分离，后端API职责单一，这种设计大大提高了代码的可维护性和扩展性。

💡 **业务逻辑理解**：通过健身房管理系统的开发，深入理解了现实业务的复杂性，包括会员生命周期管理、课程运营、教练资源分配等多维度的业务关系。

🔄 **数据流设计**：设计了完整的数据流转机制，从用户操作到数据库更新，再到界面反馈，形成了闭环的数据处理流程。

### 项目亮点总结

✨ **功能完整性**：系统涵盖了健身房运营的核心业务流程，包括8个主要数据表，30多个API接口，实现了完整的CRUD操作。

🎯 **用户体验优化**：采用单页面应用设计，模态框交互，实时消息提示，提供了流畅的用户体验。

📱 **响应式设计**：支持多种设备访问，具有良好的移动端适配性。

🔍 **数据统计分析**：实现了多维度的数据统计功能，为健身房运营提供数据支持。

### 学习收获

📚 **理论与实践结合**：将数据库理论知识成功应用到实际项目中，加深了对数据库设计原理的理解。

🛠️ **问题解决能力**：在开发过程中遇到了外键约束、并发访问、数据一致性等问题，通过查阅资料和实践解决，提升了独立解决问题的能力。

👥 **团队协作意识**：虽然是个人项目，但在设计API接口、编写文档时，培养了团队协作的意识和规范化开发的习惯。
