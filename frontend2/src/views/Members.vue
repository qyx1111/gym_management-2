<template>
  <section class="section">
    <div class="section-header">
      <div class="section-title">
        <i class="fas fa-users section-icon"></i>
        <h2>会员管理</h2>
      </div>
      <button class="btn btn-primary" @click="showMemberForm()">
        <i class="fas fa-plus"></i>
        <span>添加会员</span>
      </button>
    </div>
    
    <div class="search-bar">
      <div class="search-input-group">
        <i class="fas fa-search search-icon"></i>
        <input 
          type="text" 
          v-model="searchTerm"
          @input="handleSearch"
          placeholder="搜索会员姓名或电话..." 
        >
      </div>
      <button class="btn btn-refresh" @click="loadMembers">
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
            <th><i class="fas fa-venus-mars"></i> 性别</th>
            <th><i class="fas fa-phone"></i> 电话</th>
            <th><i class="fas fa-calendar"></i> 入会日期</th>
            <th><i class="fas fa-signal"></i> 状态</th>
            <th><i class="fas fa-cogs"></i> 操作</th>
          </tr>
        </thead>
        <tbody>
          <tr v-if="loading">
            <td colspan="7" class="loading">正在加载会员数据...</td>
          </tr>
          <tr v-else-if="error">
            <td colspan="7" class="error">{{ error }}</td>
          </tr>
          <tr v-else-if="members.length === 0">
            <td colspan="7" class="no-data">暂无会员数据</td>
          </tr>
          <tr v-else v-for="member in members" :key="member.id">
            <td>{{ member.id }}</td>
            <td>{{ member.name }}</td>
            <td>{{ member.gender || '-' }}</td>
            <td>{{ member.phone }}</td>
            <td>{{ formatDate(member.join_date) }}</td>
            <td>{{ getMemberStatusText(member.status) }}</td>
            <td>
              <button class="btn btn-success" @click="showMemberDetail(member)">查看详情</button>
              <button class="btn" @click="editMember(member)">编辑</button>
              <button class="btn btn-danger" @click="deleteMember(member)">删除</button>
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
import MemberForm from '@/components/forms/MemberForm.vue'

const router = useRouter()
const api = useApi()
const appStore = useAppStore()

const members = ref([])
const loading = ref(false)
const error = ref('')
const searchTerm = ref('')

const getMemberStatusText = (status) => {
  const statusMap = {
    'active': '活跃',
    'inactive': '非活跃',
    'frozen': '冻结'
  }
  return statusMap[status] || status
}

const formatDate = (dateString) => {
  if (!dateString) return ''
  const date = new Date(dateString)
  return date.toLocaleDateString('zh-CN')
}

const loadMembers = async () => {
  loading.value = true
  error.value = ''
  try {
    console.log('正在加载会员数据...')
    const response = await api.getMembers()
    
    if (response && response.success) {
      members.value = response.data
      console.log('会员数据加载成功:', response.data)
    } else {
      console.log('API 调用失败，使用模拟数据')
      members.value = getMockMembers()
      if (response && response.message) {
        appStore.showMessage(`使用模拟数据: ${response.message}`, 'info')
      }
    }
  } catch (apiError) {
    console.error('API 错误:', apiError)
    members.value = getMockMembers()
    error.value = 'API连接失败，显示模拟数据'
    appStore.showMessage('使用模拟数据展示', 'info')
  } finally {
    loading.value = false
  }
}

// 添加模拟数据函数
const getMockMembers = () => {
  return [
    {
      id: 1,
      name: '张三',
      gender: '男',
      phone: '13812345678',
      join_date: '2024-01-15',
      status: 'active'
    },
    {
      id: 2,
      name: '李四',
      gender: '女',
      phone: '13987654321',
      join_date: '2024-02-20',
      status: 'active'
    },
    {
      id: 3,
      name: '王五',
      gender: '男',
      phone: '13765432109',
      join_date: '2024-03-10',
      status: 'inactive'
    }
  ]
}

const handleSearch = async () => {
  if (!searchTerm.value.trim()) {
    await loadMembers()
    return
  }
  
  loading.value = true
  try {
    const response = await api.searchMembers(searchTerm.value.trim())
    if (response.success) {
      members.value = response.data
    } else {
      appStore.showMessage(`搜索失败: ${response.message}`, 'error')
    }
  } catch (error) {
    appStore.showMessage('搜索会员失败', 'error')
  } finally {
    loading.value = false
  }
}

const showMemberForm = (member = null) => {
  appStore.openModal(MemberForm, { 
    member,
    onSaved: loadMembers
  })
}

const editMember = async (member) => {
  try {
    const response = await api.getMember(member.id)
    if (response.success) {
      showMemberForm(response.data)
    } else {
      appStore.showMessage('无法加载会员信息', 'error')
    }
  } catch (error) {
    appStore.showMessage('加载会员信息失败', 'error')
  }
}

const deleteMember = (member) => {
  if (confirm(`确定要删除会员 "${member.name}" 吗？`)) {
    performDelete(member.id)
  }
}

const performDelete = async (id) => {
  try {
    const response = await api.deleteMember(id)
    if (response.success) {
      appStore.showMessage(response.message, 'success')
      await loadMembers()
    } else {
      appStore.showMessage(response.message, 'error')
    }
  } catch (error) {
    appStore.showMessage('删除会员失败', 'error')
  }
}

const showMemberDetail = (member) => {
  router.push({ name: 'MemberDetail', params: { id: member.id } })
}

// 确保组件挂载时立即加载数据
onMounted(() => {
  console.log('Members组件已挂载，开始加载数据')
  loadMembers()
})
</script>

<style scoped>
.section {
  width: 100%;
  min-height: 500px;
}

.loading, .error, .no-data {
  text-align: center;
  padding: 2rem;
  color: var(--gray-500);
  font-style: italic;
}

.error {
  color: var(--danger-color);
}
</style>