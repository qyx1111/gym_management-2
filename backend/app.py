try:
    from flask import Flask, request, jsonify
    from flask_cors import CORS
except ImportError as e:
    print("错误：缺少必要的Python包。请运行以下命令安装依赖：")
    print("pip install flask flask-cors")
    print(f"具体错误：{e}")
    exit(1)

import sys
import os

# 添加父目录到路径以导入db模块
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from db import database_operations as db_ops
    from db import database_setup
except ImportError as e:
    print(f"错误：无法导入数据库模块。请确保db目录存在且包含必要文件。错误：{e}")
    exit(1)

app = Flask(__name__)
CORS(app)  # 允许跨域请求

# 初始化数据库
def init_database():
    """初始化数据库"""
    try:
        print("正在初始化数据库...")
        database_setup.create_tables()
        print("数据库初始化完成。")
    except Exception as e:
        print(f"数据库初始化失败：{e}")
        return False
    return True

# 错误处理装饰器
def handle_api_errors(f):
    def wrapper(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except Exception as e:
            print(f"API错误 in {f.__name__}: {e}")
            return jsonify({'success': False, 'message': f'服务器内部错误: {str(e)}'}), 500
    wrapper.__name__ = f.__name__
    return wrapper

# 健康检查端点
@app.route('/api/health', methods=['GET'])
def health_check():
    """健康检查端点"""
    return jsonify({'success': True, 'message': '服务正常运行'})

# 会员管理API
@app.route('/api/members', methods=['GET'])
@handle_api_errors
def get_members():
    """获取所有会员"""
    members = db_ops.get_all_members()
    return jsonify({
        'success': True,
        'data': [dict(zip(['id', 'name', 'gender', 'birth_date', 'phone', 'emergency_contact_name', 'emergency_contact_phone', 'health_notes', 'join_date', 'status'], member)) for member in members]
    })

@app.route('/api/members', methods=['POST'])
@handle_api_errors
def add_member():
    """添加新会员"""
    data = request.json
    if not data:
        return jsonify({'success': False, 'message': '请求数据为空'}), 400
    
    required_fields = ['name', 'phone']
    for field in required_fields:
        if not data.get(field):
            return jsonify({'success': False, 'message': f'缺少必填字段: {field}'}), 400
    
    success, message = db_ops.add_member(
        data['name'], 
        data.get('gender', ''), 
        data.get('birth_date', ''), 
        data['phone'],
        data.get('emergency_contact_name', ''), 
        data.get('emergency_contact_phone', ''), 
        data.get('health_notes', '')
    )
    return jsonify({'success': success, 'message': message})

@app.route('/api/members/<int:member_id>', methods=['GET'])
@handle_api_errors
def get_member(member_id):
    """获取特定会员信息"""
    member = db_ops.get_member_by_id(member_id)
    if member:
        return jsonify({
            'success': True,
            'data': dict(zip(['id', 'name', 'gender', 'birth_date', 'phone', 'emergency_contact_name', 'emergency_contact_phone', 'health_notes', 'join_date', 'membership_card_id', 'status'], member))
        })
    return jsonify({'success': False, 'message': '会员不存在'})

@app.route('/api/members/<int:member_id>', methods=['PUT'])
@handle_api_errors
def update_member(member_id):
    """更新会员信息"""
    data = request.json
    success, message = db_ops.update_member(
        member_id, data['name'], data['gender'], data['birth_date'], data['phone'],
        data['emergency_contact_name'], data['emergency_contact_phone'], data['health_notes'], data['status']
    )
    return jsonify({'success': success, 'message': message})

@app.route('/api/members/<int:member_id>', methods=['DELETE'])
@handle_api_errors
def delete_member(member_id):
    """删除会员（逻辑删除）"""
    success, message = db_ops.delete_member_logically(member_id)
    return jsonify({'success': success, 'message': message})

# 教练管理API
@app.route('/api/trainers', methods=['GET'])
@handle_api_errors
def get_trainers():
    """获取所有教练"""
    active_only = request.args.get('active_only', 'false').lower() == 'true'
    trainers = db_ops.get_all_trainers(active_only)
    return jsonify({
        'success': True,
        'data': [dict(zip(['id', 'name', 'specialty', 'contact_info', 'status'], trainer)) for trainer in trainers]
    })

@app.route('/api/trainers', methods=['POST'])
@handle_api_errors
def add_trainer():
    """添加新教练"""
    data = request.json
    success, message = db_ops.add_trainer(data['name'], data['specialty'], data['contact_info'])
    return jsonify({'success': success, 'message': message})

@app.route('/api/trainers/<int:trainer_id>', methods=['PUT'])
@handle_api_errors
def update_trainer(trainer_id):
    """更新教练信息"""
    data = request.json
    success, message = db_ops.update_trainer(trainer_id, data['name'], data['specialty'], data['contact_info'], data['status'])
    return jsonify({'success': success, 'message': message})

@app.route('/api/trainers/<int:trainer_id>', methods=['DELETE'])
@handle_api_errors
def delete_trainer(trainer_id):
    """删除教练（逻辑删除）"""
    success, message = db_ops.delete_trainer_logically(trainer_id)
    return jsonify({'success': success, 'message': message})

@app.route('/api/trainers/search', methods=['GET'])
@handle_api_errors
def search_trainers():
    """搜索教练"""
    search_term = request.args.get('term', '')
    trainers = db_ops.search_trainers(search_term)
    return jsonify({
        'success': True,
        'data': [dict(zip(['id', 'name', 'specialty', 'contact_info', 'status'], trainer)) for trainer in trainers]
    })

# 课程管理API
@app.route('/api/courses', methods=['GET'])
@handle_api_errors
def get_courses():
    """获取所有课程"""
    active_only = request.args.get('active_only', 'false').lower() == 'true'
    courses = db_ops.get_all_courses(active_only)
    return jsonify({
        'success': True,
        'data': [dict(zip(['id', 'name', 'description', 'default_duration_minutes', 'status'], course)) for course in courses]
    })

@app.route('/api/courses', methods=['POST'])
@handle_api_errors
def add_course():
    """添加新课程"""
    data = request.json
    success, message = db_ops.add_course(data['name'], data['description'], data.get('default_duration_minutes'))
    return jsonify({'success': success, 'message': message})

@app.route('/api/courses/<int:course_id>', methods=['PUT'])
@handle_api_errors
def update_course(course_id):
    """更新课程信息"""
    data = request.json
    success, message = db_ops.update_course(course_id, data['name'], data['description'], data.get('default_duration_minutes'), data['status'])
    return jsonify({'success': success, 'message': message})

@app.route('/api/courses/<int:course_id>', methods=['DELETE'])
@handle_api_errors
def delete_course(course_id):
    """删除课程（逻辑删除）"""
    success, message = db_ops.delete_course_logically(course_id)
    return jsonify({'success': success, 'message': message})

# 会员卡类型管理API
@app.route('/api/card-types', methods=['GET'])
@handle_api_errors
def get_card_types():
    """获取所有会员卡类型"""
    card_types = db_ops.get_all_card_types()
    return jsonify({
        'success': True,
        'data': [dict(zip(['id', 'name', 'price', 'duration_days', 'description'], card_type)) for card_type in card_types]
    })

@app.route('/api/card-types', methods=['POST'])
@handle_api_errors
def add_card_type():
    """添加新会员卡类型"""
    data = request.json
    success, message = db_ops.add_card_type(data['name'], data['price'], data['duration_days'], data['description'])
    return jsonify({'success': success, 'message': message})

@app.route('/api/card-types/<int:card_type_id>', methods=['PUT'])
@handle_api_errors
def update_card_type(card_type_id):
    """更新会员卡类型"""
    data = request.json
    success, message = db_ops.update_card_type(card_type_id, data['name'], data['price'], data['duration_days'], data['description'])
    return jsonify({'success': success, 'message': message})

@app.route('/api/card-types/<int:card_type_id>', methods=['DELETE'])
@handle_api_errors
def delete_card_type(card_type_id):
    """删除会员卡类型"""
    success, message = db_ops.delete_card_type(card_type_id)
    return jsonify({'success': success, 'message': message})

# 会员详细信息API
@app.route('/api/members/<int:member_id>/cards', methods=['GET'])
@handle_api_errors
def get_member_cards(member_id):
    """获取会员的所有卡"""
    cards = db_ops.get_cards_for_member(member_id)
    return jsonify({
        'success': True,
        'data': [dict(zip(['id', 'card_type_name', 'purchase_date', 'activation_date', 'expiry_date', 'status', 'notes', 'card_type_id'], card)) for card in cards]
    })

@app.route('/api/members/<int:member_id>/cards', methods=['POST'])
@handle_api_errors
def assign_card_to_member(member_id):
    """为会员办卡"""
    data = request.json
    success, message = db_ops.assign_card_to_member(
        member_id, data['card_type_id'], data['purchase_date'], 
        data.get('activation_date'), data['expiry_date'], data['status'], data.get('notes', '')
    )
    return jsonify({'success': success, 'message': message})

@app.route('/api/member-cards/<int:card_id>', methods=['PUT'])
@handle_api_errors
def update_member_card(card_id):
    """更新会员卡信息"""
    data = request.json
    success, message = db_ops.update_member_card_details(
        card_id, data['card_type_id'], data['purchase_date'], 
        data.get('activation_date'), data['expiry_date'], data['status'], data.get('notes', '')
    )
    return jsonify({'success': success, 'message': message})

@app.route('/api/member-cards/<int:card_id>', methods=['DELETE'])
@handle_api_errors
def delete_member_card(card_id):
    """删除会员卡"""
    success, message = db_ops.delete_member_card(card_id)
    return jsonify({'success': success, 'message': message})

@app.route('/api/members/<int:member_id>/enrollments', methods=['GET'])
@handle_api_errors
def get_member_enrollments(member_id):
    """获取会员的课程报名"""
    enrollments = db_ops.get_enrollments_for_member(member_id)
    return jsonify({
        'success': True,
        'data': [dict(zip(['id', 'course_name', 'enrollment_date', 'status', 'notes', 'course_id'], enrollment)) for enrollment in enrollments]
    })

@app.route('/api/members/<int:member_id>/enrollments', methods=['POST'])
@handle_api_errors
def enroll_member_in_course(member_id):
    """为会员报名课程"""
    data = request.json
    success, message = db_ops.enroll_member_in_course(
        member_id, data['course_id'], data['enrollment_date'], data.get('status', 'enrolled'), data.get('notes', '')
    )
    return jsonify({'success': success, 'message': message})

@app.route('/api/enrollments/<int:enrollment_id>', methods=['PUT'])
@handle_api_errors
def update_enrollment(enrollment_id):
    """更新课程报名信息"""
    data = request.json
    success, message = db_ops.update_enrollment_details(
        enrollment_id, data['course_id'], data['enrollment_date'], data['status'], data.get('notes', '')
    )
    return jsonify({'success': success, 'message': message})

@app.route('/api/enrollments/<int:enrollment_id>', methods=['DELETE'])
@handle_api_errors
def delete_enrollment(enrollment_id):
    """取消课程报名"""
    success, message = db_ops.unenroll_member_from_course(enrollment_id)
    return jsonify({'success': success, 'message': message})

@app.route('/api/members/<int:member_id>/assignments', methods=['GET'])
@handle_api_errors
def get_member_assignments(member_id):
    """获取会员的教练指派"""
    assignments = db_ops.get_assignments_for_member(member_id)
    return jsonify({
        'success': True,
        'data': [dict(zip(['id', 'trainer_name', 'assignment_date', 'assignment_type', 'notes', 'trainer_id'], assignment)) for assignment in assignments]
    })

@app.route('/api/members/<int:member_id>/assignments', methods=['POST'])
@handle_api_errors
def assign_trainer_to_member_api(member_id):
    """为会员指派教练"""
    data = request.json
    success, message = db_ops.assign_trainer_to_member(
        member_id, data['trainer_id'], data['assignment_date'], data.get('assignment_type', ''), data.get('notes', '')
    )
    return jsonify({'success': success, 'message': message})

@app.route('/api/assignments/<int:assignment_id>', methods=['PUT'])
@handle_api_errors
def update_assignment(assignment_id):
    """更新教练指派信息"""
    data = request.json
    success, message = db_ops.update_assignment_details(
        assignment_id, data['trainer_id'], data['assignment_date'], data.get('assignment_type', ''), data.get('notes', '')
    )
    return jsonify({'success': success, 'message': message})

@app.route('/api/assignments/<int:assignment_id>', methods=['DELETE'])
@handle_api_errors
def delete_assignment(assignment_id):
    """解除教练指派"""
    success, message = db_ops.unassign_trainer_from_member(assignment_id)
    return jsonify({'success': success, 'message': message})

if __name__ == '__main__':
    if not init_database():
        print("数据库初始化失败，程序退出")
        exit(1)
    
    print("Flask服务器启动中...")
    print("API地址：http://localhost:5000/api/")
    print("健康检查：http://localhost:5000/api/health")
    
    try:
        app.run(debug=True, host='0.0.0.0', port=5000)
    except Exception as e:
        print(f"服务器启动失败：{e}")
