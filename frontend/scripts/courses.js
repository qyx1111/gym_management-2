// 加载课程列表
async function loadCourses() {
    const tbody = document.getElementById('coursesTableBody');
    tbody.innerHTML = '<tr><td colspan="6" class="loading">正在加载课程数据...</td></tr>';
    
    const response = await api.getCourses();
    
    if (response.success) {
        tbody.innerHTML = '';
        response.data.forEach(course => {
            const row = document.createElement('tr');
            row.innerHTML = `
                <td>${course.id}</td>
                <td>${course.name}</td>
                <td>${course.description || ''}</td>
                <td>${course.default_duration_minutes || ''}</td>
                <td>${course.status}</td>
                <td>
                    <button class="btn" onclick="editCourse(${course.id})">编辑</button>
                    <button class="btn btn-danger" onclick="deleteCourse(${course.id}, '${course.name}')">删除</button>
                </td>
            `;
            tbody.appendChild(row);
        });
    } else {
        tbody.innerHTML = `<tr><td colspan="6">加载失败: ${response.message}</td></tr>`;
    }
}

// 显示课程表单
function showCourseForm(course = null) {
    currentEditingItem = course;
    const title = course ? '编辑课程' : '添加课程';
    
    const formContent = `
        <div class="form">
            <h3>${title}</h3>
            <div class="form-group">
                <label for="courseName">课程名称 *</label>
                <input type="text" id="courseName" value="${course ? course.name : ''}" required>
            </div>
            <div class="form-group">
                <label for="courseDescription">课程描述</label>
                <textarea id="courseDescription">${course ? course.description || '' : ''}</textarea>
            </div>
            <div class="form-group">
                <label for="courseDuration">默认时长(分钟)</label>
                <input type="number" id="courseDuration" value="${course ? course.default_duration_minutes || '' : ''}" min="1" max="480">
            </div>
            ${course ? `
            <div class="form-group">
                <label for="courseStatus">状态</label>
                <select id="courseStatus">
                    <option value="active" ${course.status === 'active' ? 'selected' : ''}>活动</option>
                    <option value="inactive" ${course.status === 'inactive' ? 'selected' : ''}>非活动</option>
                </select>
            </div>
            ` : ''}
            <div class="form-actions">
                <button type="button" class="btn" onclick="closeModal()">取消</button>
                <button type="button" class="btn btn-primary" onclick="saveCourse()">${course ? '更新' : '添加'}</button>
            </div>
        </div>
    `;
    
    showModal(formContent);
}

// 保存课程
async function saveCourse() {
    const courseData = {
        name: document.getElementById('courseName').value.trim(),
        description: document.getElementById('courseDescription').value.trim(),
        default_duration_minutes: parseInt(document.getElementById('courseDuration').value) || null
    };
    
    if (currentEditingItem) {
        courseData.status = document.getElementById('courseStatus').value;
    }
    
    if (!courseData.name) {
        showMessage('课程名称不能为空', 'error');
        return;
    }
    
    let response;
    if (currentEditingItem) {
        response = await api.updateCourse(currentEditingItem.id, courseData);
    } else {
        response = await api.createCourse(courseData);
    }
    
    if (response.success) {
        showMessage(response.message, 'success');
        closeModal();
        loadCourses();
    } else {
        showMessage(response.message, 'error');
    }
}

// 编辑课程
async function editCourse(id) {
    const response = await api.getCourses();
    if (response.success) {
        const course = response.data.find(c => c.id === id);
        if (course) {
            showCourseForm(course);
        } else {
            showMessage('未找到课程信息', 'error');
        }
    } else {
        showMessage('无法加载课程信息', 'error');
    }
}

// 删除课程
async function deleteCourse(id, name) {
    confirmAction(`确定要删除课程 "${name}" 吗？`, async () => {
        const response = await api.deleteCourse(id);
        if (response.success) {
            showMessage(response.message, 'success');
            loadCourses();
        } else {
            showMessage(response.message, 'error');
        }
    });
}
