// 会员卡状态转换函数
function getCardStatusText(status) {
    const statusMap = {
        'pending_activation': '待激活',
        'active': '活跃',
        'frozen': '冻结',
        'expired': '过期',
        'cancelled': '已取消'
    };
    return statusMap[status] || status;
}

// 课程报名状态转换函数
function getEnrollmentStatusText(status) {
    const statusMap = {
        '已报名': '已报名',
        '进行中': '进行中',
        '已完成': '已完成',
        '已取消': '已取消'
    };
    return statusMap[status] || status;
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
                    <td>${getCardStatusText(card.status)}</td>
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
                    <td>${getEnrollmentStatusText(enrollment.status)}</td>
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
                    <td>${getAssignmentTypeText(assignment.assignment_type)}</td>
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
                    <option value="active" ${card && card.status === 'active' ? 'selected' : ''}>活跃</option>
                    <option value="frozen" ${card && card.status === 'frozen' ? 'selected' : ''}>冻结</option>
                    <option value="expired" ${card && card.status === 'expired' ? 'selected' : ''}>过期</option>
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

// 显示课程报名表单
async function showMemberCourseForm(enrollmentId = null) {
    const courses = await api.getCourses();
    if (!courses.success) {
        showMessage('无法加载课程列表', 'error');
        return;
    }
    
    let enrollment = null;
    if (enrollmentId) {
        const enrollmentsResponse = await api.getMemberEnrollments(currentMemberId);
        if (enrollmentsResponse.success) {
            enrollment = enrollmentsResponse.data.find(e => e.id === enrollmentId);
        }
    }
    
    const title = enrollment ? '编辑课程报名' : '新课程报名';
    const courseOptions = courses.data.map(course => 
        `<option value="${course.id}" ${enrollment && enrollment.course_id === course.id ? 'selected' : ''}>${course.name}</option>`
    ).join('');
    
    const formContent = `
        <div class="form">
            <h3>${title}</h3>
            <div class="form-group">
                <label for="memberCourse">课程 *</label>
                <select id="memberCourse" required>
                    <option value="">请选择课程</option>
                    ${courseOptions}
                </select>
            </div>
            <div class="form-group">
                <label for="memberEnrollmentDate">报名日期 *</label>
                <input type="date" id="memberEnrollmentDate" value="${enrollment ? enrollment.enrollment_date.split(' ')[0] : getTodayDate()}" required>
            </div>
            <div class="form-group">
                <label for="memberEnrollmentStatus">状态</label>
                <select id="memberEnrollmentStatus">
                    <option value="已报名" ${enrollment && enrollment.status === '已报名' ? 'selected' : ''}>已报名</option>
                    <option value="进行中" ${enrollment && enrollment.status === '进行中' ? 'selected' : ''}>进行中</option>
                    <option value="已完成" ${enrollment && enrollment.status === '已完成' ? 'selected' : ''}>已完成</option>
                    <option value="已取消" ${enrollment && enrollment.status === '已取消' ? 'selected' : ''}>已取消</option>
                </select>
            </div>
            <div class="form-group">
                <label for="memberEnrollmentNotes">备注</label>
                <textarea id="memberEnrollmentNotes">${enrollment ? enrollment.notes || '' : ''}</textarea>
            </div>
            <div class="form-actions">
                <button type="button" class="btn" onclick="closeModal()">取消</button>
                <button type="button" class="btn btn-primary" onclick="saveMemberEnrollment(${enrollmentId || 'null'})">${enrollment ? '更新' : '报名'}</button>
            </div>
        </div>
    `;
    
    showModal(formContent);
}

// 保存课程报名
async function saveMemberEnrollment(enrollmentId) {
    const enrollmentData = {
        course_id: parseInt(document.getElementById('memberCourse').value),
        enrollment_date: document.getElementById('memberEnrollmentDate').value,
        status: document.getElementById('memberEnrollmentStatus').value,
        notes: document.getElementById('memberEnrollmentNotes').value.trim()
    };
    
    if (!enrollmentData.course_id) {
        showMessage('请选择课程', 'error');
        return;
    }
    
    if (!enrollmentData.enrollment_date) {
        showMessage('报名日期不能为空', 'error');
        return;
    }
    
    let response;
    if (enrollmentId) {
        response = await api.updateMemberEnrollment(enrollmentId, enrollmentData);
    } else {
        response = await api.enrollMemberInCourse(currentMemberId, enrollmentData);
    }
    
    if (response.success) {
        showMessage(response.message, 'success');
        closeModal();
        loadMemberEnrollments(currentMemberId);
    } else {
        showMessage(response.message, 'error');
    }
}

// 显示教练指派表单
async function showMemberTrainerForm(assignmentId = null) {
    const trainers = await api.getTrainers();
    if (!trainers.success) {
        showMessage('无法加载教练列表', 'error');
        return;
    }
    
    let assignment = null;
    if (assignmentId) {
        const assignmentsResponse = await api.getMemberAssignments(currentMemberId);
        if (assignmentsResponse.success) {
            assignment = assignmentsResponse.data.find(a => a.id === assignmentId);
        }
    }
    
    const title = assignment ? '编辑教练指派' : '指派教练';
    const trainerOptions = trainers.data.map(trainer => 
        `<option value="${trainer.id}" ${assignment && assignment.trainer_id === trainer.id ? 'selected' : ''}>${trainer.name}</option>`
    ).join('');
    
    const formContent = `
        <div class="form">
            <h3>${title}</h3>
            <div class="form-group">
                <label for="memberTrainer">教练 *</label>
                <select id="memberTrainer" required>
                    <option value="">请选择教练</option>
                    ${trainerOptions}
                </select>
            </div>
            <div class="form-group">
                <label for="memberAssignmentDate">指派日期 *</label>
                <input type="date" id="memberAssignmentDate" value="${assignment ? assignment.assignment_date.split(' ')[0] : getTodayDate()}" required>
            </div>
            <div class="form-group">
                <label for="memberAssignmentType">指派类型</label>
                <select id="memberAssignmentType">
                    <option value="">请选择类型</option>
                    <option value="personal" ${assignment && assignment.assignment_type === 'personal' ? 'selected' : ''}>私教</option>
                    <option value="group" ${assignment && assignment.assignment_type === 'group' ? 'selected' : ''}>团体课</option>
                    <option value="consultation" ${assignment && assignment.assignment_type === 'consultation' ? 'selected' : ''}>咨询</option>
                    <option value="assessment" ${assignment && assignment.assignment_type === 'assessment' ? 'selected' : ''}>体能评估</option>
                </select>
            </div>
            <div class="form-group">
                <label for="memberAssignmentNotes">备注</label>
                <textarea id="memberAssignmentNotes">${assignment ? assignment.notes || '' : ''}</textarea>
            </div>
            <div class="form-actions">
                <button type="button" class="btn" onclick="closeModal()">取消</button>
                <button type="button" class="btn btn-primary" onclick="saveMemberAssignment(${assignmentId || 'null'})">${assignment ? '更新' : '指派'}</button>
            </div>
        </div>
    `;
    
    showModal(formContent);
}

// 保存教练指派
async function saveMemberAssignment(assignmentId) {
    const assignmentData = {
        trainer_id: parseInt(document.getElementById('memberTrainer').value),
        assignment_date: document.getElementById('memberAssignmentDate').value,
        assignment_type: document.getElementById('memberAssignmentType').value,
        notes: document.getElementById('memberAssignmentNotes').value.trim()
    };
    
    if (!assignmentData.trainer_id) {
        showMessage('请选择教练', 'error');
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
        response = await api.assignTrainerToMember(currentMemberId, assignmentData);
    }
    
    if (response.success) {
        showMessage(response.message, 'success');
        closeModal();
        loadMemberAssignments(currentMemberId);
    } else {
        showMessage(response.message, 'error');
    }
}

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

function editMemberEnrollment(enrollmentId) {
    showMemberCourseForm(enrollmentId);
}

function deleteMemberEnrollment(enrollmentId, courseName) {
    confirmAction(`确定要取消 "${courseName}" 课程报名吗？`, async () => {
        const response = await api.deleteMemberEnrollment(enrollmentId);
        if (response.success) {
            showMessage(response.message, 'success');
            loadMemberEnrollments(currentMemberId);
        } else {
            showMessage(response.message, 'error');
        }
    });
}

function editMemberAssignment(assignmentId) {
    showMemberTrainerForm(assignmentId);
}

function deleteMemberAssignment(assignmentId, trainerName) {
    confirmAction(`确定要解除与教练 "${trainerName}" 的指派关系吗？`, async () => {
        const response = await api.deleteMemberAssignment(assignmentId);
        if (response.success) {
            showMessage(response.message, 'success');
            loadMemberAssignments(currentMemberId);
        } else {
            showMessage(response.message, 'error');
        }
    });
}
