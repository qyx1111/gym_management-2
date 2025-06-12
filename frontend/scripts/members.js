// 会员状态转换函数
function getMemberStatusText(status) {
    const statusMap = {
        'active': '活跃',
        'inactive': '非活跃',
        'frozen': '冻结'
    };
    return statusMap[status] || status;
}

// 加载会员列表
async function loadMembers() {
    const tbody = document.getElementById('membersTableBody');
    tbody.innerHTML = '<tr><td colspan="7" class="loading">正在加载会员数据...</td></tr>';
    
    const response = await api.getMembers();
    
    if (response.success) {
        tbody.innerHTML = '';
        response.data.forEach(member => {
            const row = document.createElement('tr');
            row.innerHTML = `
                <td>${member.id}</td>
                <td>${member.name}</td>
                <td>${member.gender || ''}</td>
                <td>${member.phone}</td>
                <td>${formatDate(member.join_date)}</td>
                <td>${getMemberStatusText(member.status)}</td>
                <td>
                    <button class="btn btn-success" onclick="showMemberDetail(${member.id}, '${member.name}')">查看详情</button>
                    <button class="btn" onclick="editMember(${member.id})">编辑</button>
                    <button class="btn btn-danger" onclick="deleteMember(${member.id}, '${member.name}')">删除</button>
                </td>
            `;
            tbody.appendChild(row);
        });
    } else {
        tbody.innerHTML = `<tr><td colspan="7">加载失败: ${response.message}</td></tr>`;
    }
}

// 搜索会员
async function searchMembers() {
    const searchTerm = document.getElementById('memberSearch').value.trim();
    if (!searchTerm) {
        loadMembers();
        return;
    }
    
    const tbody = document.getElementById('membersTableBody');
    tbody.innerHTML = '<tr><td colspan="7" class="loading">搜索中...</td></tr>';
    
    const response = await api.searchMembers(searchTerm);
    
    if (response.success) {
        tbody.innerHTML = '';
        if (response.data.length === 0) {
            tbody.innerHTML = '<tr><td colspan="7">未找到匹配的会员</td></tr>';
        } else {
            response.data.forEach(member => {
                const row = document.createElement('tr');
                row.innerHTML = `
                    <td>${member.id}</td>
                    <td>${member.name}</td>
                    <td>${member.gender || ''}</td>
                    <td>${member.phone}</td>
                    <td>${formatDate(member.join_date)}</td>
                    <td>${getMemberStatusText(member.status)}</td>
                    <td>
                        <button class="btn btn-success" onclick="showMemberDetail(${member.id}, '${member.name}')">查看详情</button>
                        <button class="btn" onclick="editMember(${member.id})">编辑</button>
                        <button class="btn btn-danger" onclick="deleteMember(${member.id}, '${member.name}')">删除</button>
                    </td>
                `;
                tbody.appendChild(row);
            });
        }
    } else {
        tbody.innerHTML = `<tr><td colspan="7">搜索失败: ${response.message}</td></tr>`;
    }
}

// 显示会员表单
function showMemberForm(member = null) {
    currentEditingItem = member;
    const title = member ? '编辑会员' : '添加会员';
    
    const formContent = `
        <div class="form">
            <h3>${title}</h3>
            <div class="form-group">
                <label for="memberName">姓名 *</label>
                <input type="text" id="memberName" value="${member ? member.name : ''}" required>
            </div>
            <div class="form-group">
                <label for="memberGender">性别</label>
                <select id="memberGender">
                    <option value="">请选择</option>
                    <option value="男" ${member && member.gender === '男' ? 'selected' : ''}>男</option>
                    <option value="女" ${member && member.gender === '女' ? 'selected' : ''}>女</option>
                    <option value="其他" ${member && member.gender === '其他' ? 'selected' : ''}>其他</option>
                </select>
            </div>
            <div class="form-group">
                <label for="memberBirthDate">生日</label>
                <input type="date" id="memberBirthDate" value="${member ? member.birth_date : ''}">
            </div>
            <div class="form-group">
                <label for="memberPhone">电话 *</label>
                <input type="tel" id="memberPhone" value="${member ? member.phone : ''}" required>
            </div>
            <div class="form-group">
                <label for="memberHealthNotes">健康备注</label>
                <textarea id="memberHealthNotes">${member ? member.health_notes || '' : ''}</textarea>
            </div>
            ${member ? `
            <div class="form-group">
                <label for="memberStatus">状态</label>
                <select id="memberStatus">
                    <option value="active" ${member.status === 'active' ? 'selected' : ''}>活跃</option>
                    <option value="inactive" ${member.status === 'inactive' ? 'selected' : ''}>非活跃</option>
                </select>
            </div>
            ` : ''}
            <div class="form-actions">
                <button type="button" class="btn" onclick="closeModal()">取消</button>
                <button type="button" class="btn btn-primary" onclick="saveMember()">${member ? '更新' : '添加'}</button>
            </div>
        </div>
    `;
    // 显示模态框
    showModal(formContent);
}

// 保存会员
async function saveMember() {
    const memberData = {
        name: document.getElementById('memberName').value.trim(),
        gender: document.getElementById('memberGender').value,
        birth_date: document.getElementById('memberBirthDate').value,
        phone: document.getElementById('memberPhone').value.trim(),
        health_notes: document.getElementById('memberHealthNotes').value.trim(),
        // 为兼容后端，提供空字符串默认值
        emergency_contact_name: '',
        emergency_contact_phone: ''
    };
    
    if (currentEditingItem) {
        memberData.status = document.getElementById('memberStatus').value;
    }
    
    if (!memberData.name || !memberData.phone) {
        showMessage('姓名和电话不能为空', 'error');
        return;
    }
    
    let response;
    if (currentEditingItem) {
        response = await api.updateMember(currentEditingItem.id, memberData);
    } else {
        response = await api.createMember(memberData);
    }
    
    if (response.success) {
        showMessage(response.message, 'success');
        closeModal();
        loadMembers();
    } else {
        showMessage(response.message, 'error');
    }
}

// 编辑会员
async function editMember(id) {
    const response = await api.getMember(id);
    if (response.success) {
        showMemberForm(response.data);
    } else {
        showMessage('无法加载会员信息', 'error');
    }
}

// 删除会员
async function deleteMember(id, name) {
    confirmAction(`确定要删除会员 "${name}" 吗？`, async () => {
        const response = await api.deleteMember(id);
        if (response.success) {
            showMessage(response.message, 'success');
            loadMembers();
        } else {
            showMessage(response.message, 'error');
        }
    });
}

// 显示会员详情
function showMemberDetail(id, name) {
    currentMemberId = id;
    document.getElementById('memberDetailTitle').textContent = `会员详情 - ${name} (ID: ${id})`;
    showSection('member-detail');
    showTab('member-cards');
    loadMemberCards(id);
}
