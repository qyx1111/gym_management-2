<template>
  <div class="form">
    <h3>{{ course ? '编辑课程' : '添加课程' }}</h3>
    <div class="form-group">
      <label for="courseName">课程名称 *</label>
      <input 
        type="text" 
        id="courseName" 
        v-model="formData.name"
        required
      >
    </div>
    <div class="form-group">
      <label for="courseDescription">课程描述</label>
      <textarea 
        id="courseDescription" 
        v-model="formData.description"
      ></textarea>
    </div>
    <div class="form-group">
      <label for="courseDuration">默认时长(分钟)</label>
      <input 
        type="number" 
        id="courseDuration" 
        v-model="formData.default_duration_minutes" 
        min="1" 
        max="480"
      >
    </div>
    <div v-if="course" class="form-group">
      <label for="courseStatus">状态</label>
      <select id="courseStatus" v-model="formData.status">
        <option value="active">活跃</option>
        <option value="inactive">非活跃</option>
      </select>
    </div>
    <div class="form-actions">
      <button type="button" class="btn" @click="appStore.closeModal()">取消</button>
      <button type="button" class="btn btn-primary" @click="saveCourse">
        {{ course ? '更新' : '添加' }}
      </button>
    </div>
  </div>
</template>

<script setup>
import { reactive } from 'vue'
import { useApi } from '@/composables/useApi'
import { useAppStore } from '@/stores/app'

const props = defineProps(['course', 'onSaved'])
const api = useApi()
const appStore = useAppStore()

const formData = reactive({
  name: props.course?.name || '',
  description: props.course?.description || '',
  default_duration_minutes: props.course?.default_duration_minutes || null,
  status: props.course?.status || 'active'
})

const saveCourse = async () => {
  if (!formData.name) {
    appStore.showMessage('课程名称不能为空', 'error')
    return
  }
  
  try {
    let response
    if (props.course) {
      response = await api.updateCourse(props.course.id, formData)
    } else {
      response = await api.createCourse(formData)
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
    appStore.showMessage('保存课程信息失败', 'error')
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
