<template>
  <section class="section">
    <div class="section-header">
      <div class="section-title">
        <i class="fas fa-user-tie section-icon"></i>
        <h2>教练管理</h2>
      </div>
      <button class="btn btn-primary" @click="showTrainerForm()">
        <i class="fas fa-plus"></i>
        <span>添加教练</span>
      </button>
    </div>
    
    <div class="search-bar">
      <div class="search-input-group">
        <i class="fas fa-search search-icon"></i>
        <input 
          type="text" 
          v-model="searchTerm"
          @input="handleSearch"
          placeholder="搜索教练姓名或专长..." 
        >
      </div>
      <button class="btn btn-refresh" @click="loadTrainers">
        <i class="fas fa-sync-alt"></i>
        <span>刷新</span>
      </button>
    </div>

    <div class="table-container">
      <table class="table">
        <thead>
          <tr>
            <th><i class="fas fa-hashtag"></i> ID</th>
            <th><i class="fas fa-user"></i> 姓名</th>
            <th><i class="fas fa-star"></i> 专长</th>
            <th><i class="fas fa-phone"></i> 联系方式</th>
            <th><i class="fas fa-signal"></i> 状态</th>
            <th><i class="fas fa-cogs"></i> 操作</th>
          </tr>
        </thead>
        <tbody>
          <tr v-if="loading">
            <td colspan="6" class="loading">正在加载教练数据...</td>
          </tr>
          <tr v-else-if="trainers.length === 0">
            <td colspan="6">暂无教练数据</td>
          </tr>
          <tr v-else v-for="trainer in trainers" :key="trainer.id">
            <td>{{ trainer.id }}</td>
            <td>{{ trainer.name }}</td>
            <td>{{ trainer.specialties || '' }}</td>
            <td>{{ trainer.contact_info || '' }}</td>
            <td>{{ getTrainerStatusText(trainer.status) }}</td>
            <td>
              <button class="btn btn-success" @click="showTrainerDetail(trainer)">查看详情</button>
              <button class="btn" @click="editTrainer(trainer)">编辑</button>
              <button class="btn btn-danger" @click="deleteTrainer(trainer)">删除</button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </section>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useApi } from '@/composables/useApi'
import { useAppStore } from '@/stores/app'
import TrainerForm from '@/components/forms/TrainerForm.vue'

const router = useRouter()
const api = useApi()
const appStore = useAppStore()

const trainers = ref([])
const loading = ref(false)
const error = ref('')
const searchTerm = ref('')

const getTrainerStatusText = (status) => {
  const statusMap = {
    'active': '活跃',
    'inactive': '非活跃'
  }
  return statusMap[status] || status
}

const loadTrainers = async () => {
  loading.value = true
  error.value = ''
  try {
    console.log('正在加载教练数据...')
    const response = await api.getTrainers()
    
    if (response && response.success) {
      trainers.value = response.data
    } else {
      trainers.value = getMockTrainers()
      if (response && response.message) {
        appStore.showMessage(`使用模拟数据: ${response.message}`, 'info')
      }
    }
  } catch (apiError) {
    console.error('API 错误:', apiError)
    trainers.value = getMockTrainers()
    appStore.showMessage('使用模拟数据展示', 'info')
  } finally {
    loading.value = false
  }
}

const getMockTrainers = () => {
  return [
    {
      id: 1,
      name: '刘教练',
      specialties: '力量训练，体能训练',
      contact_info: '13800138001',
      status: 'active'
    },
    {
      id: 2,
      name: '陈教练',
      specialties: '瑜伽，舞蹈',
      contact_info: '13800138002',
      status: 'active'
    },
    {
      id: 3,
      name: '王教练',
      specialties: '游泳，水中健身',
      contact_info: '13800138003',
      status: 'active'
    }
  ]
}

const handleSearch = async () => {
  if (!searchTerm.value.trim()) {
    await loadTrainers()
    return
  }
  
  loading.value = true
  try {
    const response = await api.searchTrainers(searchTerm.value.trim())
    if (response.success) {
      trainers.value = response.data
    } else {
      appStore.showMessage(`搜索失败: ${response.message}`, 'error')
    }
  } catch (error) {
    appStore.showMessage('搜索教练失败', 'error')
  } finally {
    loading.value = false
  }
}

const showTrainerForm = (trainer = null) => {
  appStore.openModal(TrainerForm, { 
    trainer,
    onSaved: loadTrainers
  })
}

const editTrainer = (trainer) => {
  showTrainerForm(trainer)
}

const deleteTrainer = (trainer) => {
  if (confirm(`确定要删除教练 "${trainer.name}" 吗？`)) {
    performDelete(trainer.id)
  }
}

const performDelete = async (id) => {
  try {
    const response = await api.deleteTrainer(id)
    if (response.success) {
      appStore.showMessage(response.message, 'success')
      await loadTrainers()
    } else {
      appStore.showMessage(response.message, 'error')
    }
  } catch (error) {
    appStore.showMessage('删除教练失败', 'error')
  }
}

const showTrainerDetail = (trainer) => {
  router.push({ name: 'TrainerDetail', params: { id: trainer.id } })
}

onMounted(() => {
  console.log('Trainers组件已挂载，开始加载数据')
  loadTrainers()
})
</script>

<style scoped>
.section {
  width: 100%;
  min-height: 500px;
}

.loading, .no-data {
  text-align: center;
  padding: 2rem;
  color: var(--gray-500);
  font-style: italic;
}
</style>
