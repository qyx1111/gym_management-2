<template>
  <section class="section">
    <div class="section-header">
      <div class="section-title">
        <i class="fas fa-credit-card section-icon"></i>
        <h2>会员卡类型管理</h2>
      </div>
      <button class="btn btn-primary" @click="showCardTypeForm()">
        <i class="fas fa-plus"></i>
        <span>添加卡类型</span>
      </button>
    </div>
    
    <div class="search-bar">
      <div class="search-input-group">
        <i class="fas fa-search search-icon"></i>
        <input 
          type="text" 
          v-model="searchTerm"
          @input="handleSearch"
          placeholder="搜索卡类型名称或描述..." 
        >
      </div>
      <button class="btn btn-refresh" @click="loadCardTypes">
        <i class="fas fa-sync-alt"></i>
        <span>刷新</span>
      </button>
    </div>
    
    <div class="table-container">
      <table class="table">
        <thead>
          <tr>
            <th><i class="fas fa-hashtag"></i> ID</th>
            <th><i class="fas fa-credit-card"></i> 类型名称</th>
            <th><i class="fas fa-money-bill"></i> 价格(元)</th>
            <th><i class="fas fa-calendar-day"></i> 有效期(天)</th>
            <th><i class="fas fa-info-circle"></i> 描述</th>
            <th><i class="fas fa-cogs"></i> 操作</th>
          </tr>
        </thead>
        <tbody>
          <tr v-if="loading">
            <td colspan="6" class="loading">正在加载会员卡类型数据...</td>
          </tr>
          <tr v-else-if="cardTypes.length === 0">
            <td colspan="6">暂无会员卡类型数据</td>
          </tr>
          <tr v-else v-for="cardType in cardTypes" :key="cardType.id">
            <td>{{ cardType.id }}</td>
            <td>{{ cardType.name }}</td>
            <td>¥{{ cardType.price }}</td>
            <td>{{ cardType.duration_days }}</td>
            <td>{{ cardType.description || '' }}</td>
            <td>
              <button class="btn" @click="editCardType(cardType)">编辑</button>
              <button class="btn btn-danger" @click="deleteCardType(cardType)">删除</button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </section>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useApi } from '@/composables/useApi'
import { useAppStore } from '@/stores/app'
import CardTypeForm from '@/components/forms/CardTypeForm.vue'

const api = useApi()
const appStore = useAppStore()

const cardTypes = ref([])
const loading = ref(false)
const searchTerm = ref('')

const loadCardTypes = async () => {
  loading.value = true
  try {
    console.log('正在加载会员卡类型数据...')
    const response = await api.getCardTypes()
    
    if (response && response.success) {
      cardTypes.value = response.data
    } else {
      cardTypes.value = getMockCardTypes()
      if (response && response.message) {
        appStore.showMessage(`使用模拟数据: ${response.message}`, 'info')
      }
    }
  } catch (error) {
    cardTypes.value = getMockCardTypes()
    appStore.showMessage('使用模拟数据展示', 'info')
  } finally {
    loading.value = false
  }
}

const getMockCardTypes = () => {
  return [
    {
      id: 1,
      name: '月卡',
      price: 200,
      duration_days: 30,
      description: '30天有效期，适合短期健身'
    },
    {
      id: 2,
      name: '季卡',
      price: 500,
      duration_days: 90,
      description: '90天有效期，性价比较高'
    },
    {
      id: 3,
      name: '年卡',
      price: 1800,
      duration_days: 365,
      description: '365天有效期，最优惠价格'
    },
    {
      id: 4,
      name: '次卡',
      price: 50,
      duration_days: 365,
      description: '单次使用，一年内有效'
    }
  ]
}

const handleSearch = async () => {
  if (!searchTerm.value.trim()) {
    await loadCardTypes()
    return
  }
  
  loading.value = true
  try {
    const response = await api.searchCardTypes(searchTerm.value.trim())
    if (response.success) {
      cardTypes.value = response.data
    } else {
      appStore.showMessage(`搜索失败: ${response.message}`, 'error')
    }
  } catch (error) {
    appStore.showMessage('搜索会员卡类型失败', 'error')
  } finally {
    loading.value = false
  }
}

const showCardTypeForm = (cardType = null) => {
  appStore.openModal(CardTypeForm, { 
    cardType,
    onSaved: loadCardTypes
  })
}

const editCardType = (cardType) => {
  showCardTypeForm(cardType)
}

const deleteCardType = (cardType) => {
  if (confirm(`确定要删除会员卡类型 "${cardType.name}" 吗？\n注意：删除后相关的会员卡可能会受到影响。`)) {
    performDelete(cardType.id)
  }
}

const performDelete = async (id) => {
  try {
    const response = await api.deleteCardType(id)
    if (response.success) {
      appStore.showMessage(response.message, 'success')
      await loadCardTypes()
    } else {
      appStore.showMessage(response.message, 'error')
    }
  } catch (error) {
    appStore.showMessage('删除会员卡类型失败', 'error')
  }
}

onMounted(() => {
  console.log('CardTypes组件已挂载，开始加载数据')
  loadCardTypes()
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
