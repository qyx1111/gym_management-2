// 教练状态转换函数
function getTrainerStatusText(status) {
    const statusMap = {
        'active': '活跃',
        'inactive': '非活跃'
    };
    return statusMap[status] || status;
}

// 加载教练列表
async function loadTrainers() {
    const tbody = document.getElementById('trainersTableBody');
    tbody.innerHTML = '<tr><td colspan="6" class="loading">正在加载教练数据...</td></tr>';
    
    const response = await api.getTrainers();
    
    if (response.success) {
        tbody.innerHTML = '';
        response.data.forEach(trainer => {
            const row = document.createElement('tr');
            row.innerHTML = `
                <td>${trainer.id}</td>
                <td>${trainer.name}</td>
                <td>${trainer.specialty || ''}</td>
                <td>${trainer.contact_info || ''}</td>
                <td>${getTrainerStatusText(trainer.status)}</td>
                <td>
                    <button class="btn btn-success" onclick="showTrainerDetail(${trainer.id}, '${trainer.name}')">查看详情</button>
                    <button class="btn" onclick="editTrainer(${trainer.id})">编辑</button>
                    <button class="btn btn-danger" onclick="deleteTrainer(${trainer.id}, '${trainer.name}')">删除</button>
                </td>
            `;
            tbody.appendChild(row);
        });
    } else {
        tbody.innerHTML = `<tr><td colspan="6">加载失败: ${response.message}</td></tr>`;
    }
}

// 搜索教练
async function searchTrainers() {
    const searchTerm = document.getElementById('trainerSearch').value.trim();
    if (!searchTerm) {
        loadTrainers();
        return;
    }
    
    const tbody = document.getElementById('trainersTableBody');
    tbody.innerHTML = '<tr><td colspan="6" class="loading">搜索中...</td></tr>';
    
    const response = await api.searchTrainers(searchTerm);
    
    if (response.success) {
        tbody.innerHTML = '';
        if (response.data.length === 0) {
            tbody.innerHTML = '<tr><td colspan="6">未找到匹配的教练</td></tr>';
        } else {
            response.data.forEach(trainer => {
                const row = document.createElement('tr');
                row.innerHTML = `
                    <td>${trainer.id}</td>
                    <td>${trainer.name}</td>
                    <td>${trainer.specialty || ''}</td>
                    <td>${trainer.contact_info || ''}</td>
                    <td>${getTrainerStatusText(trainer.status)}</td>
                    <td>
                        <button class="btn btn-success" onclick="showTrainerDetail(${trainer.id}, '${trainer.name}')">查看详情</button>
                        <button class="btn" onclick="editTrainer(${trainer.id})">编辑</button>
                        <button class="btn btn-danger" onclick="deleteTrainer(${trainer.id}, '${trainer.name}')">删除</button>
                    </td>
                `;
                tbody.appendChild(row);
            });
        }
    } else {
        tbody.innerHTML = `<tr><td colspan="6">搜索失败: ${response.message}</td></tr>`;
    }
}

// 显示教练表单
function showTrainerForm(trainer = null) {
    currentEditingItem = trainer;
    const title = trainer ? '编辑教练' : '添加教练';
    
    const formContent = `
        <div class="form">
            <h3>${title}</h3>
            <div class="form-group">
                <label for="trainerName">姓名 *</label>
                <input type="text" id="trainerName" value="${trainer ? trainer.name : ''}" required>
            </div>
            <div class="form-group">
                <label for="trainerSpecialty">专长</label>
                <input type="text" id="trainerSpecialty" value="${trainer ? trainer.specialty || '' : ''}" placeholder="如：瑜伽、健身、游泳等">
            </div>
            <div class="form-group">
                <label for="trainerContact">联系方式</label>
                <input type="text" id="trainerContact" value="${trainer ? trainer.contact_info || '' : ''}" placeholder="电话或邮箱">
            </div>
            ${trainer ? `
            <div class="form-group">
                <label for="trainerStatus">状态</label>
                <select id="trainerStatus">
                    <option value="active" ${trainer.status === 'active' ? 'selected' : ''}>活跃</option>
                    <option value="inactive" ${trainer.status === 'inactive' ? 'selected' : ''}>非活跃</option>
                </select>
            </div>
            ` : ''}
            <div class="form-actions">
                <button type="button" class="btn" onclick="closeModal()">取消</button>
                <button type="button" class="btn btn-primary" onclick="saveTrainer()">${trainer ? '更新' : '添加'}</button>
            </div>
        </div>
    `;
    
    showModal(formContent);
}

// 保存教练
async function saveTrainer() {
    const trainerData = {
        name: document.getElementById('trainerName').value.trim(),
        specialty: document.getElementById('trainerSpecialty').value.trim(),
        contact_info: document.getElementById('trainerContact').value.trim()
    };
    
    if (currentEditingItem) {
        trainerData.status = document.getElementById('trainerStatus').value;
    }
    
    if (!trainerData.name) {
        showMessage('教练姓名不能为空', 'error');
        return;
    }
    
    let response;
    if (currentEditingItem) {
        response = await api.updateTrainer(currentEditingItem.id, trainerData);
    } else {
        response = await api.createTrainer(trainerData);
    }
    
    if (response.success) {
        showMessage(response.message, 'success');
        closeModal();
        loadTrainers();
    } else {
        showMessage(response.message, 'error');
    }
}

// 编辑教练
async function editTrainer(id) {
    const response = await api.getTrainers();
    if (response.success) {
        const trainer = response.data.find(t => t.id === id);
        if (trainer) {
            showTrainerForm(trainer);
        } else {
            showMessage('未找到教练信息', 'error');
        }
    } else {
        showMessage('无法加载教练信息', 'error');
    }
}

// 删除教练
async function deleteTrainer(id, name) {
    confirmAction(`确定要删除教练 "${name}" 吗？`, async () => {
        const response = await api.deleteTrainer(id);
        if (response.success) {
            showMessage(response.message, 'success');
            loadTrainers();
        } else {
            showMessage(response.message, 'error');
        }
    });
}

// 显示教练详情
function showTrainerDetail(id, name) {
    currentTrainerId = id;
    document.getElementById('trainerDetailTitle').textContent = `教练详情 - ${name} (ID: ${id})`;
    showSection('trainer-detail');
    showTrainerTab('trainer-courses');
    loadTrainerCourses(id);
}
