<template>
  <div class="form">
    <h3>{{ member ? '编辑会员' : '添加会员' }}</h3>
    <div class="form-group">
      <label for="memberName">姓名 *</label>
      <input 
        type="text" 
        id="memberName" 
        v-model="formData.name"
        required
      >
    </div>
    <div class="form-group">
      <label for="memberGender">性别</label>
      <select id="memberGender" v-model="formData.gender">
        <option value="">请选择</option>
        <option value="男">男</option>
        <option value="女">女</option>
        <option value="其他">其他</option>
      </select>
    </div>
    <div class="form-group">
      <label for="memberBirthDate">生日</label>
      <input 
        type="date" 
        id="memberBirthDate" 
        v-model="formData.birth_date"
      >
    </div>
    <div class="form-group">
      <label for="memberPhone">电话 *</label>
      <input 
        type="tel" 
        id="memberPhone" 
        v-model="formData.phone"
        required
      >
    </div>
    <div class="form-group">
      <label for="memberHealthNotes">健康备注</label>
      <textarea 
        id="memberHealthNotes" 
        v-model="formData.health_notes"
      ></textarea>
    </div>
    <div v-if="member" class="form-group">
      <label for="memberStatus">状态</label>
      <select id="memberStatus" v-model="formData.status">
        <option value="active">活跃</option>
        <option value="inactive">非活跃</option>
      </select>
    </div>
    <div class="form-actions">
      <button type="button" class="btn" @click="appStore.closeModal()">取消</button>
      <button type="button" class="btn btn-primary" @click="saveMember">
        {{ member ? '更新' : '添加' }}
      </button>
    </div>
  </div>
</template>

<script setup>
import { reactive } from 'vue'
import { useApi } from '@/composables/useApi'
import { useAppStore } from '@/stores/app'

const props = defineProps(['member', 'onSaved'])
const api = useApi()
const appStore = useAppStore()

const formData = reactive({
  name: props.member?.name || '',
  gender: props.member?.gender || '',
  birth_date: props.member?.birth_date || '',
  phone: props.member?.phone || '',
  health_notes: props.member?.health_notes || '',
  status: props.member?.status || 'active'
})

const saveMember = async () => {
  if (!formData.name || !formData.phone) {
    appStore.showMessage('姓名和电话不能为空', 'error')
    return
  }
  
  try {
    let response
    if (props.member) {
      response = await api.updateMember(props.member.id, formData)
    } else {
      response = await api.createMember(formData)
    }
    
    if (response.success) {
      appStore.showMessage(response.message, 'success')
      appStore.closeModal()
      if (props.onSaved) {
        props.onSaved()
      }
    } else {
      appStore.showMessage(response.message, 'error')
    }
  } catch (error) {
    appStore.showMessage('保存会员信息失败', 'error')
  }
}
</script>

<style scoped>
/* 表单样式 */
.form {
  background: white;
  padding: 2rem;
  border-radius: var(--radius-lg);
  max-width: 500px;
  width: 100%;
}

.form h3 {
  color: var(--gray-800);
  font-size: 1.5rem;
  font-weight: 600;
  margin-bottom: 1.5rem;
  text-align: center;
}

.form-group {
  margin-bottom: 1.5rem;
}

.form-group label {
  display: block;
  margin-bottom: 0.5rem;
  color: var(--gray-700);
  font-weight: 500;
  font-size: 0.9rem;
}

.form-group input,
.form-group select,
.form-group textarea {
  width: 100%;
  padding: 0.75rem;
  border: 2px solid var(--gray-200);
  border-radius: var(--radius);
  font-size: 1rem;
  transition: all 0.3s ease;
  background: var(--gray-50);
  color: var(--gray-800);
}

.form-group input:focus,
.form-group select:focus,
.form-group textarea:focus {
  outline: none;
  border-color: var(--primary-color);
  box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
  background: white;
}

.form-group textarea {
  resize: vertical;
  min-height: 80px;
}

.form-actions {
  display: flex;
  gap: 1rem;
  justify-content: flex-end;
  margin-top: 2rem;
  padding-top: 1rem;
  border-top: 1px solid var(--gray-200);
}
</style>
