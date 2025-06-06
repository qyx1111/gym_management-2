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
                    <td>${assignment.course_type || ''}</td>
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
                    <td>${assignment.assignment_type || ''}</td>
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
