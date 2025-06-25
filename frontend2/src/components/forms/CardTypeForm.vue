<template>
  <div class="form">
    <h3>{{ cardType ? '编辑会员卡类型' : '添加会员卡类型' }}</h3>
    <div class="form-group">
      <label for="cardTypeName">类型名称 *</label>
      <input 
        type="text" 
        id="cardTypeName" 
        v-model="formData.name"
        required
        placeholder="如：月卡、年卡、次卡等"
      >
    </div>
    <div class="form-group">
      <label for="cardTypePrice">价格(元) *</label>
      <input 
        type="number" 
        id="cardTypePrice" 
        v-model="formData.price"
        required 
        min="0" 
        step="0.01"
      >
    </div>
    <div class="form-group">
      <label for="cardTypeDuration">有效期(天) *</label>
      <input 
        type="number" 
        id="cardTypeDuration" 
        v-model="formData.duration_days"
        required 
        min="1"
      >
    </div>
    <div class="form-group">
      <label for="cardTypeDescription">描述</label>
      <textarea 
        id="cardTypeDescription" 
        v-model="formData.description"
      ></textarea>
    </div>
    <div class="form-actions">
      <button type="button" class="btn" @click="appStore.closeModal()">取消</button>
      <button type="button" class="btn btn-primary" @click="saveCardType">
        {{ cardType ? '更新' : '添加' }}
      </button>
    </div>
  </div>
</template>

<script setup>
import { reactive } from 'vue'
import { useApi } from '@/composables/useApi'
import { useAppStore } from '@/stores/app'

const props = defineProps(['cardType', 'onSaved'])
const api = useApi()
const appStore = useAppStore()

const formData = reactive({
  name: props.cardType?.name || '',
  price: props.cardType?.price || '',
  duration_days: props.cardType?.duration_days || '',
  description: props.cardType?.description || ''
})

const saveCardType = async () => {
  if (!formData.name) {
    appStore.showMessage('类型名称不能为空', 'error')
    return
  }
  
  if (!formData.price || formData.price <= 0) {
    appStore.showMessage('价格必须大于0', 'error')
    return
  }
  
  if (!formData.duration_days || formData.duration_days <= 0) {
    appStore.showMessage('有效期必须大于0天', 'error')
    return
  }
  
  try {
    let response
    if (props.cardType) {
      response = await api.updateCardType(props.cardType.id, formData)
    } else {
      response = await api.createCardType(formData)
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
    appStore.showMessage('保存会员卡类型失败', 'error')
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

@media (max-width: 768px) {
  .form {
    padding: 1.5rem;
  }
  
  .form-actions {
    flex-direction: column;
  }
  
  .form-actions .btn {
    width: 100%;
  }
}
</style>
