// 加载会员卡类型列表
async function loadCardTypes() {
    const tbody = document.getElementById('cardTypesTableBody');
    tbody.innerHTML = '<tr><td colspan="6" class="loading">正在加载会员卡类型数据...</td></tr>';
    
    const response = await api.getCardTypes();
    
    if (response.success) {
        tbody.innerHTML = '';
        response.data.forEach(cardType => {
            const row = document.createElement('tr');
            row.innerHTML = `
                <td>${cardType.id}</td>
                <td>${cardType.name}</td>
                <td>¥${cardType.price}</td>
                <td>${cardType.duration_days}</td>
                <td>${cardType.description || ''}</td>
                <td>
                    <button class="btn" onclick="editCardType(${cardType.id})">编辑</button>
                    <button class="btn btn-danger" onclick="deleteCardType(${cardType.id}, '${cardType.name}')">删除</button>
                </td>
            `;
            tbody.appendChild(row);
        });
    } else {
        tbody.innerHTML = `<tr><td colspan="6">加载失败: ${response.message}</td></tr>`;
    }
}

// 显示会员卡类型表单
function showCardTypeForm(cardType = null) {
    currentEditingItem = cardType;
    const title = cardType ? '编辑会员卡类型' : '添加会员卡类型';
    
    const formContent = `
        <div class="form">
            <h3>${title}</h3>
            <div class="form-group">
                <label for="cardTypeName">类型名称 *</label>
                <input type="text" id="cardTypeName" value="${cardType ? cardType.name : ''}" required placeholder="如：月卡、年卡、次卡等">
            </div>
            <div class="form-group">
                <label for="cardTypePrice">价格(元) *</label>
                <input type="number" id="cardTypePrice" value="${cardType ? cardType.price : ''}" required min="0" step="0.01">
            </div>
            <div class="form-group">
                <label for="cardTypeDuration">有效期(天) *</label>
                <input type="number" id="cardTypeDuration" value="${cardType ? cardType.duration_days : ''}" required min="1">
            </div>
            <div class="form-group">
                <label for="cardTypeDescription">描述</label>
                <textarea id="cardTypeDescription">${cardType ? cardType.description || '' : ''}</textarea>
            </div>
            <div class="form-actions">
                <button type="button" class="btn" onclick="closeModal()">取消</button>
                <button type="button" class="btn btn-primary" onclick="saveCardType()">${cardType ? '更新' : '添加'}</button>
            </div>
        </div>
    `;
    
    showModal(formContent);
}

// 保存会员卡类型
async function saveCardType() {
    const cardTypeData = {
        name: document.getElementById('cardTypeName').value.trim(),
        price: parseFloat(document.getElementById('cardTypePrice').value),
        duration_days: parseInt(document.getElementById('cardTypeDuration').value),
        description: document.getElementById('cardTypeDescription').value.trim()
    };
    
    if (!cardTypeData.name) {
        showMessage('类型名称不能为空', 'error');
        return;
    }
    
    if (!cardTypeData.price || cardTypeData.price <= 0) {
        showMessage('价格必须大于0', 'error');
        return;
    }
    
    if (!cardTypeData.duration_days || cardTypeData.duration_days <= 0) {
        showMessage('有效期必须大于0天', 'error');
        return;
    }
    
    let response;
    if (currentEditingItem) {
        response = await api.updateCardType(currentEditingItem.id, cardTypeData);
    } else {
        response = await api.createCardType(cardTypeData);
    }
    
    if (response.success) {
        showMessage(response.message, 'success');
        closeModal();
        loadCardTypes();
    } else {
        showMessage(response.message, 'error');
    }
}

// 编辑会员卡类型
async function editCardType(id) {
    const response = await api.getCardTypes();
    if (response.success) {
        const cardType = response.data.find(ct => ct.id === id);
        if (cardType) {
            showCardTypeForm(cardType);
        } else {
            showMessage('未找到会员卡类型信息', 'error');
        }
    } else {
        showMessage('无法加载会员卡类型信息', 'error');
    }
}

// 删除会员卡类型
async function deleteCardType(id, name) {
    confirmAction(`确定要删除会员卡类型 "${name}" 吗？\n注意：删除后相关的会员卡可能会受到影响。`, async () => {
        const response = await api.deleteCardType(id);
        if (response.success) {
            showMessage(response.message, 'success');
            loadCardTypes();
        } else {
            showMessage(response.message, 'error');
        }
    });
}
