<template>
  <div class="form">
    <h3>{{ trainer ? '编辑教练' : '添加教练' }}</h3>
    <div class="form-group">
      <label for="trainerName">姓名 *</label>
      <input 
        type="text" 
        id="trainerName" 
        v-model="formData.name"
        required
      >
    </div>
    <div class="form-group">
      <label for="trainerSpecialties">专长</label>
      <textarea 
        id="trainerSpecialties" 
        v-model="formData.specialties"
        placeholder="请输入教练的专长领域，如：力量训练、瑜伽、游泳等"
      ></textarea>
    </div>
    <div class="form-group">
      <label for="trainerContact">联系方式</label>
      <input 
        type="text" 
        id="trainerContact" 
        v-model="formData.contact_info"
        placeholder="电话、邮箱等联系方式"
      >
    </div>
    <div v-if="trainer" class="form-group">
      <label for="trainerStatus">状态</label>
      <select id="trainerStatus" v-model="formData.status">
        <option value="active">活跃</option>
        <option value="inactive">非活跃</option>
      </select>
    </div>
    <div class="form-actions">
      <button type="button" class="btn" @click="appStore.closeModal()">取消</button>
      <button type="button" class="btn btn-primary" @click="saveTrainer">
        {{ trainer ? '更新' : '添加' }}
      </button>
    </div>
  </div>
</template>

<script setup>
import { reactive } from 'vue'
import { useApi } from '@/composables/useApi'
import { useAppStore } from '@/stores/app'

const props = defineProps(['trainer', 'onSaved'])
const api = useApi()
const appStore = useAppStore()

const formData = reactive({
  name: props.trainer?.name || '',
  specialties: props.trainer?.specialties || '',
  contact_info: props.trainer?.contact_info || '',
  status: props.trainer?.status || 'active'
})

const saveTrainer = async () => {
  if (!formData.name) {
    appStore.showMessage('姓名不能为空', 'error')
    return
  }
  
  try {
    let response
    if (props.trainer) {
      response = await api.updateTrainer(props.trainer.id, formData)
    } else {
      response = await api.createTrainer(formData)
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
    appStore.showMessage('保存教练信息失败', 'error')
  }
}
</script>

<style scoped>
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
