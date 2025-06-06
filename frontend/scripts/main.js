// 全局变量
let currentMemberId = null;
let currentTrainerId = null;
let currentEditingItem = null;

// 显示指定区域
function showSection(sectionId) {
    // 隐藏所有区域
    document.querySelectorAll('.section').forEach(section => {
        section.classList.remove('active');
    });
    
    // 显示指定区域
    document.getElementById(sectionId).classList.add('active');
    
    // 根据区域加载数据
    switch(sectionId) {
        case 'members':
            loadMembers();
            break;
        case 'trainers':
            loadTrainers();
            break;
        case 'courses':
            loadCourses();
            break;
        case 'card-types':
            loadCardTypes();
            break;
    }
}

// 显示标签页
function showTab(tabId) {
    // 隐藏所有标签内容
    document.querySelectorAll('.tab-content').forEach(content => {
        content.classList.remove('active');
    });
    
    // 移除所有标签按钮的active类
    document.querySelectorAll('.tab-btn').forEach(btn => {
        btn.classList.remove('active');
    });
    
    // 显示指定标签内容
    document.getElementById(tabId).classList.add('active');
    
    // 激活对应的标签按钮
    event.target.classList.add('active');
    
    // 根据标签加载数据
    if (currentMemberId) {
        switch(tabId) {
            case 'member-cards':
                loadMemberCards(currentMemberId);
                break;
            case 'member-courses':
                loadMemberEnrollments(currentMemberId);
                break;
            case 'member-trainers':
                loadMemberAssignments(currentMemberId);
                break;
        }
    }
}

// 显示教练标签页
function showTrainerTab(tabId) {
    // 隐藏所有标签内容
    document.querySelectorAll('.tab-content').forEach(content => {
        content.classList.remove('active');
    });
    
    // 移除所有标签按钮的active类
    document.querySelectorAll('.tab-btn').forEach(btn => {
        btn.classList.remove('active');
    });
    
    // 显示指定标签内容
    document.getElementById(tabId).classList.add('active');
    
    // 激活对应的标签按钮
    event.target.classList.add('active');
    
    // 根据标签加载数据
    if (currentTrainerId) {
        switch(tabId) {
            case 'trainer-courses':
                loadTrainerCourses(currentTrainerId);
                break;
            case 'trainer-members':
                loadTrainerMembers(currentTrainerId);
                break;
        }
    }
}

// 显示模态框
function showModal(content) {
    document.getElementById('modalBody').innerHTML = content;
    document.getElementById('modal').style.display = 'block';
}

// 关闭模态框
function closeModal() {
    document.getElementById('modal').style.display = 'none';
    currentEditingItem = null;
}

// 显示消息
function showMessage(message, type = 'success') {
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${type}`;
    messageDiv.textContent = message;
    
    // 插入到当前活动区域的顶部
    const activeSection = document.querySelector('.section.active');
    activeSection.insertBefore(messageDiv, activeSection.firstChild);
    
    // 3秒后自动移除
    setTimeout(() => {
        messageDiv.remove();
    }, 3000);
}

// 确认对话框
function confirmAction(message, callback) {
    if (confirm(message)) {
        callback();
    }
}

// 格式化日期
function formatDate(dateString) {
    if (!dateString) return '';
    const date = new Date(dateString);
    return date.toLocaleDateString('zh-CN');
}

// 格式化日期时间
function formatDateTime(dateString) {
    if (!dateString) return '';
    const date = new Date(dateString);
    return date.toLocaleString('zh-CN');
}

// 获取今天的日期（YYYY-MM-DD格式）
function getTodayDate() {
    const today = new Date();
    return today.toISOString().split('T')[0];
}

// 点击模态框外部关闭
window.onclick = function(event) {
    const modal = document.getElementById('modal');
    if (event.target === modal) {
        closeModal();
    }
}

// 页面加载完成后初始化
document.addEventListener('DOMContentLoaded', function() {
    showSection('dashboard');
});
