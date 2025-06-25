const express = require('express');
const cors = require('cors');
const bodyParser = require('body-parser');

const app = express();
const PORT = 5000;

// 中间件
app.use(cors());
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: true }));

// 模拟数据
let members = [
  {
    id: 1,
    name: '张三',
    gender: '男',
    birth_date: '1990-05-15',
    phone: '13812345678',
    join_date: '2024-01-15',
    health_notes: '无',
    status: 'active'
  },
  {
    id: 2,
    name: '李四',
    gender: '女',
    birth_date: '1988-08-20',
    phone: '13987654321',
    join_date: '2024-02-20',
    health_notes: '轻微高血压',
    status: 'active'
  },
  {
    id: 3,
    name: '王五',
    gender: '男',
    birth_date: '1995-12-10',
    phone: '13765432109',
    join_date: '2024-03-10',
    health_notes: '无',
    status: 'inactive'
  }
];

let trainers = [
  {
    id: 1,
    name: '刘教练',
    specialties: '力量训练，体能训练',
    contact_info: '13800138001',
    status: 'active'
  },
  {
    id: 2,
    name: '陈教练',
    specialties: '瑜伽，舞蹈',
    contact_info: '13800138002',
    status: 'active'
  },
  {
    id: 3,
    name: '王教练',
    specialties: '游泳，水中健身',
    contact_info: '13800138003',
    status: 'active'
  }
];

let courses = [
  {
    id: 1,
    name: '力量训练',
    description: '增强肌肉力量和耐力',
    default_duration_minutes: 60,
    status: 'active'
  },
  {
    id: 2,
    name: '瑜伽课程',
    description: '提高身体柔韧性和平衡性',
    default_duration_minutes: 90,
    status: 'active'
  },
  {
    id: 3,
    name: '游泳训练',
    description: '游泳技能训练和水中健身',
    default_duration_minutes: 45,
    status: 'active'
  }
];

let cardTypes = [
  {
    id: 1,
    name: '月卡',
    price: 200,
    duration_days: 30,
    description: '30天有效期，适合短期健身'
  },
  {
    id: 2,
    name: '季卡',
    price: 500,
    duration_days: 90,
    description: '90天有效期，性价比较高'
  },
  {
    id: 3,
    name: '年卡',
    price: 1800,
    duration_days: 365,
    description: '365天有效期，最优惠价格'
  }
];

// 会员相关路由
app.get('/api/members', (req, res) => {
  res.json({ success: true, data: members, message: '获取会员列表成功' });
});

app.get('/api/members/:id', (req, res) => {
  const id = parseInt(req.params.id);
  const member = members.find(m => m.id === id);
  if (member) {
    res.json({ success: true, data: member, message: '获取会员信息成功' });
  } else {
    res.status(404).json({ success: false, message: '会员不存在' });
  }
});

app.get('/api/members/search', (req, res) => {
  const term = req.query.term || '';
  const filtered = members.filter(member => 
    member.name.includes(term) || member.phone.includes(term)
  );
  res.json({ success: true, data: filtered, message: '搜索成功' });
});

app.post('/api/members', (req, res) => {
  const newMember = {
    id: Math.max(...members.map(m => m.id)) + 1,
    ...req.body,
    join_date: new Date().toISOString().split('T')[0]
  };
  members.push(newMember);
  res.json({ success: true, data: newMember, message: '添加会员成功' });
});

app.put('/api/members/:id', (req, res) => {
  const id = parseInt(req.params.id);
  const index = members.findIndex(m => m.id === id);
  if (index !== -1) {
    members[index] = { ...members[index], ...req.body };
    res.json({ success: true, data: members[index], message: '更新会员信息成功' });
  } else {
    res.status(404).json({ success: false, message: '会员不存在' });
  }
});

app.delete('/api/members/:id', (req, res) => {
  const id = parseInt(req.params.id);
  const index = members.findIndex(m => m.id === id);
  if (index !== -1) {
    members.splice(index, 1);
    res.json({ success: true, message: '删除会员成功' });
  } else {
    res.status(404).json({ success: false, message: '会员不存在' });
  }
});

// 教练相关路由
app.get('/api/trainers', (req, res) => {
  const activeOnly = req.query.active_only === 'true';
  const filtered = activeOnly ? trainers.filter(t => t.status === 'active') : trainers;
  res.json({ success: true, data: filtered, message: '获取教练列表成功' });
});

app.get('/api/trainers/search', (req, res) => {
  const term = req.query.term || '';
  const filtered = trainers.filter(trainer => 
    trainer.name.includes(term) || trainer.specialties.includes(term)
  );
  res.json({ success: true, data: filtered, message: '搜索成功' });
});

app.post('/api/trainers', (req, res) => {
  const newTrainer = {
    id: Math.max(...trainers.map(t => t.id)) + 1,
    ...req.body
  };
  trainers.push(newTrainer);
  res.json({ success: true, data: newTrainer, message: '添加教练成功' });
});

app.put('/api/trainers/:id', (req, res) => {
  const id = parseInt(req.params.id);
  const index = trainers.findIndex(t => t.id === id);
  if (index !== -1) {
    trainers[index] = { ...trainers[index], ...req.body };
    res.json({ success: true, data: trainers[index], message: '更新教练信息成功' });
  } else {
    res.status(404).json({ success: false, message: '教练不存在' });
  }
});

app.delete('/api/trainers/:id', (req, res) => {
  const id = parseInt(req.params.id);
  const index = trainers.findIndex(t => t.id === id);
  if (index !== -1) {
    trainers.splice(index, 1);
    res.json({ success: true, message: '删除教练成功' });
  } else {
    res.status(404).json({ success: false, message: '教练不存在' });
  }
});

// 课程相关路由
app.get('/api/courses', (req, res) => {
  const activeOnly = req.query.active_only === 'true';
  const filtered = activeOnly ? courses.filter(c => c.status === 'active') : courses;
  res.json({ success: true, data: filtered, message: '获取课程列表成功' });
});

app.get('/api/courses/search', (req, res) => {
  const term = req.query.term || '';
  const filtered = courses.filter(course => 
    course.name.includes(term) || course.description.includes(term)
  );
  res.json({ success: true, data: filtered, message: '搜索成功' });
});

app.post('/api/courses', (req, res) => {
  const newCourse = {
    id: Math.max(...courses.map(c => c.id)) + 1,
    ...req.body
  };
  courses.push(newCourse);
  res.json({ success: true, data: newCourse, message: '添加课程成功' });
});

app.put('/api/courses/:id', (req, res) => {
  const id = parseInt(req.params.id);
  const index = courses.findIndex(c => c.id === id);
  if (index !== -1) {
    courses[index] = { ...courses[index], ...req.body };
    res.json({ success: true, data: courses[index], message: '更新课程信息成功' });
  } else {
    res.status(404).json({ success: false, message: '课程不存在' });
  }
});

app.delete('/api/courses/:id', (req, res) => {
  const id = parseInt(req.params.id);
  const index = courses.findIndex(c => c.id === id);
  if (index !== -1) {
    courses.splice(index, 1);
    res.json({ success: true, message: '删除课程成功' });
  } else {
    res.status(404).json({ success: false, message: '课程不存在' });
  }
});

// 会员卡类型相关路由
app.get('/api/card-types', (req, res) => {
  res.json({ success: true, data: cardTypes, message: '获取会员卡类型列表成功' });
});

app.get('/api/card-types/search', (req, res) => {
  const term = req.query.term || '';
  const filtered = cardTypes.filter(cardType => 
    cardType.name.includes(term) || cardType.description.includes(term)
  );
  res.json({ success: true, data: filtered, message: '搜索成功' });
});

app.post('/api/card-types', (req, res) => {
  const newCardType = {
    id: Math.max(...cardTypes.map(ct => ct.id)) + 1,
    ...req.body
  };
  cardTypes.push(newCardType);
  res.json({ success: true, data: newCardType, message: '添加会员卡类型成功' });
});

app.put('/api/card-types/:id', (req, res) => {
  const id = parseInt(req.params.id);
  const index = cardTypes.findIndex(ct => ct.id === id);
  if (index !== -1) {
    cardTypes[index] = { ...cardTypes[index], ...req.body };
    res.json({ success: true, data: cardTypes[index], message: '更新会员卡类型成功' });
  } else {
    res.status(404).json({ success: false, message: '会员卡类型不存在' });
  }
});

app.delete('/api/card-types/:id', (req, res) => {
  const id = parseInt(req.params.id);
  const index = cardTypes.findIndex(ct => ct.id === id);
  if (index !== -1) {
    cardTypes.splice(index, 1);
    res.json({ success: true, message: '删除会员卡类型成功' });
  } else {
    res.status(404).json({ success: false, message: '会员卡类型不存在' });
  }
});

// 会员详情相关路由（模拟数据）
app.get('/api/members/:id/cards', (req, res) => {
  res.json({ 
    success: true, 
    data: [
      {
        id: 1,
        card_type_name: '年卡',
        purchase_date: '2024-01-15',
        activation_date: '2024-01-15',
        expiry_date: '2025-01-15',
        status: 'active'
      }
    ], 
    message: '获取会员卡信息成功' 
  });
});

app.get('/api/members/:id/enrollments', (req, res) => {
  res.json({ 
    success: true, 
    data: [
      {
        id: 1,
        course_name: '力量训练',
        enrollment_date: '2024-01-20',
        status: 'active',
        notes: '每周三次'
      }
    ], 
    message: '获取课程报名信息成功' 
  });
});

app.get('/api/members/:id/assignments', (req, res) => {
  res.json({ 
    success: true, 
    data: [
      {
        id: 1,
        trainer_name: '刘教练',
        assignment_date: '2024-01-25',
        assignment_type: 'personal',
        notes: '私教课程'
      }
    ], 
    message: '获取教练指派信息成功' 
  });
});

// 教练详情相关路由（模拟数据）
app.get('/api/trainers/:id/courses', (req, res) => {
  res.json({ 
    success: true, 
    data: [
      {
        id: 1,
        course_name: '力量训练',
        assignment_date: '2024-01-10',
        course_type: 'regular',
        notes: '主要负责器械指导'
      }
    ], 
    message: '获取教练课程信息成功' 
  });
});

app.get('/api/trainers/:id/members', (req, res) => {
  res.json({ 
    success: true, 
    data: [
      {
        id: 1,
        member_name: '张三',
        assignment_date: '2024-01-25',
        assignment_type: 'personal',
        notes: '私教学员'
      }
    ], 
    message: '获取教练会员信息成功' 
  });
});

// 启动服务器
app.listen(PORT, () => {
  console.log(`服务器运行在 http://localhost:${PORT}`);
  console.log('API 端点:');
  console.log('- GET /api/members - 获取会员列表');
  console.log('- GET /api/trainers - 获取教练列表');
  console.log('- GET /api/courses - 获取课程列表');
  console.log('- GET /api/card-types - 获取会员卡类型列表');
});
