// 加载会员卡列表
async function loadMemberCards(memberId) {
    const tbody = document.getElementById('memberCardsTableBody');
    tbody.innerHTML = '<tr><td colspan="7" class="loading">正在加载会员卡数据...</td></tr>';
    
    const response = await api.getMemberCards(memberId);
    
    if (response.success) {
        tbody.innerHTML = '';
        if (response.data.length === 0) {
            tbody.innerHTML = '<tr><td colspan="7">该会员暂无会员卡</td></tr>';
        } else {
            response.data.forEach(card => {
                const row = document.createElement('tr');
                row.innerHTML = `
                    <td>${card.id}</td>
                    <td>${card.card_type_name}</td>
                    <td>${formatDate(card.purchase_date)}</td>
                    <td>${formatDate(card.activation_date)}</td>
                    <td>${formatDate(card.expiry_date)}</td>
                    <td>${card.status}</td>
                    <td>
                        <button class="btn" onclick="editMemberCard(${card.id})">编辑</button>
                        <button class="btn btn-danger" onclick="deleteMemberCard(${card.id}, '${card.card_type_name}')">删除</button>
                    </td>
                `;
                tbody.appendChild(row);
            });
        }
    } else {
        tbody.innerHTML = `<tr><td colspan="7">加载失败: ${response.message}</td></tr>`;
    }
}

// 加载会员课程报名列表
async function loadMemberEnrollments(memberId) {
    const tbody = document.getElementById('memberCoursesTableBody');
    tbody.innerHTML = '<tr><td colspan="6" class="loading">正在加载课程报名数据...</td></tr>';
    
    const response = await api.getMemberEnrollments(memberId);
    
    if (response.success) {
        tbody.innerHTML = '';
        if (response.data.length === 0) {
            tbody.innerHTML = '<tr><td colspan="6">该会员暂未报名任何课程</td></tr>';
        } else {
            response.data.forEach(enrollment => {
                const row = document.createElement('tr');
                row.innerHTML = `
                    <td>${enrollment.id}</td>
                    <td>${enrollment.course_name}</td>
                    <td>${formatDate(enrollment.enrollment_date)}</td>
                    <td>${enrollment.status}</td>
                    <td>${enrollment.notes || ''}</td>
                    <td>
                        <button class="btn" onclick="editMemberEnrollment(${enrollment.id})">编辑</button>
                        <button class="btn btn-danger" onclick="deleteMemberEnrollment(${enrollment.id}, '${enrollment.course_name}')">取消</button>
                    </td>
                `;
                tbody.appendChild(row);
            });
        }
    } else {
        tbody.innerHTML = `<tr><td colspan="6">加载失败: ${response.message}</td></tr>`;
    }
}

// 加载会员教练指派列表
async function loadMemberAssignments(memberId) {
    const tbody = document.getElementById('memberTrainersTableBody');
    tbody.innerHTML = '<tr><td colspan="6" class="loading">正在加载教练指派数据...</td></tr>';
    
    const response = await api.getMemberAssignments(memberId);
    
    if (response.success) {
        tbody.innerHTML = '';
        if (response.data.length === 0) {
            tbody.innerHTML = '<tr><td colspan="6">该会员暂未指派任何教练</td></tr>';
        } else {
            response.data.forEach(assignment => {
                const row = document.createElement('tr');
                row.innerHTML = `
                    <td>${assignment.id}</td>
                    <td>${assignment.trainer_name}</td>
                    <td>${formatDate(assignment.assignment_date)}</td>
                    <td>${assignment.assignment_type || ''}</td>
                    <td>${assignment.notes || ''}</td>
                    <td>
                        <button class="btn" onclick="editMemberAssignment(${assignment.id})">编辑</button>
                        <button class="btn btn-danger" onclick="deleteMemberAssignment(${assignment.id}, '${assignment.trainer_name}')">解除</button>
                    </td>
                `;
                tbody.appendChild(row);
            });
        }
    } else {
        tbody.innerHTML = `<tr><td colspan="6">加载失败: ${response.message}</td></tr>`;
    }
}

// 显示会员卡表单
async function showMemberCardForm(cardId = null) {
    const cardTypes = await api.getCardTypes();
    if (!cardTypes.success) {
        showMessage('无法加载会员卡类型', 'error');
        return;
    }
    
    let card = null;
    if (cardId) {
        // 这里需要获取具体卡的信息，暂时从列表中查找
        const cardsResponse = await api.getMemberCards(currentMemberId);
        if (cardsResponse.success) {
            card = cardsResponse.data.find(c => c.id === cardId);
        }
    }
    
    const title = card ? '编辑会员卡' : '办理新会员卡';
    const cardTypeOptions = cardTypes.data.map(ct => 
        `<option value="${ct.id}" ${card && card.card_type_id === ct.id ? 'selected' : ''}>${ct.name}</option>`
    ).join('');
    
    const formContent = `
        <div class="form">
            <h3>${title}</h3>
            <div class="form-group">
                <label for="memberCardType">卡类型 *</label>
                <select id="memberCardType" required>
                    <option value="">请选择卡类型</option>
                    ${cardTypeOptions}
                </select>
            </div>
            <div class="form-group">
                <label for="memberCardPurchaseDate">购买日期 *</label>
                <input type="date" id="memberCardPurchaseDate" value="${card ? card.purchase_date.split(' ')[0] : getTodayDate()}" required>
            </div>
            <div class="form-group">
                <label for="memberCardActivationDate">激活日期</label>
                <input type="date" id="memberCardActivationDate" value="${card && card.activation_date ? card.activation_date : ''}">
            </div>
            <div class="form-group">
                <label for="memberCardExpiryDate">失效日期 *</label>
                <input type="date" id="memberCardExpiryDate" value="${card ? card.expiry_date : ''}" required>
            </div>
            <div class="form-group">
                <label for="memberCardStatus">状态</label>
                <select id="memberCardStatus">
                    <option value="pending_activation" ${card && card.status === 'pending_activation' ? 'selected' : ''}>待激活</option>
                    <option value="active" ${card && card.status === 'active' ? 'selected' : ''}>活动</option>
                    <option value="frozen" ${card && card.status === 'frozen' ? 'selected' : ''}>冻结</option>
                    <option value="expired" ${card && card.status === 'expired' ? 'selected' : ''}>过期</option>
                    <option value="cancelled" ${card && card.status === 'cancelled' ? 'selected' : ''}>取消</option>
                </select>
            </div>
            <div class="form-group">
                <label for="memberCardNotes">备注</label>
                <textarea id="memberCardNotes">${card ? card.notes || '' : ''}</textarea>
            </div>
            <div class="form-actions">
                <button type="button" class="btn" onclick="closeModal()">取消</button>
                <button type="button" class="btn btn-primary" onclick="saveMemberCard(${cardId || 'null'})">${card ? '更新' : '办理'}</button>
            </div>
        </div>
    `;
    
    showModal(formContent);
}

// 保存会员卡
async function saveMemberCard(cardId) {
    const cardData = {
        card_type_id: parseInt(document.getElementById('memberCardType').value),
        purchase_date: document.getElementById('memberCardPurchaseDate').value,
        activation_date: document.getElementById('memberCardActivationDate').value || null,
        expiry_date: document.getElementById('memberCardExpiryDate').value,
        status: document.getElementById('memberCardStatus').value,
        notes: document.getElementById('memberCardNotes').value.trim()
    };
    
    if (!cardData.card_type_id) {
        showMessage('请选择卡类型', 'error');
        return;
    }
    
    if (!cardData.purchase_date || !cardData.expiry_date) {
        showMessage('购买日期和失效日期不能为空', 'error');
        return;
    }
    
    let response;
    if (cardId) {
        response = await api.updateMemberCard(cardId, cardData);
    } else {
        response = await api.assignCardToMember(currentMemberId, cardData);
    }
    
    if (response.success) {
        showMessage(response.message, 'success');
        closeModal();
        loadMemberCards(currentMemberId);
    } else {
        showMessage(response.message, 'error');
    }
}

// 其他会员详情相关函数
function editMemberCard(cardId) {
    showMemberCardForm(cardId);
}

function deleteMemberCard(cardId, cardTypeName) {
    confirmAction(`确定要删除这张 "${cardTypeName}" 吗？`, async () => {
        const response = await api.deleteMemberCard(cardId);
        if (response.success) {
            showMessage(response.message, 'success');
            loadMemberCards(currentMemberId);
        } else {
            showMessage(response.message, 'error');
        }
    });
}

// 类似地实现课程和教练的表单函数...
function showMemberCourseForm() {
    showMessage('课程报名功能开发中...', 'warning');
}

function showMemberTrainerForm() {
    showMessage('教练指派功能开发中...', 'warning');
}

function editMemberEnrollment(enrollmentId) {
    showMessage('编辑功能开发中...', 'warning');
}

function deleteMemberEnrollment(enrollmentId, courseName) {
    showMessage('取消功能开发中...', 'warning');
}

function editMemberAssignment(assignmentId) {
    showMessage('编辑功能开发中...', 'warning');
}

function deleteMemberAssignment(assignmentId, trainerName) {
    showMessage('解除功能开发中...', 'warning');
}
