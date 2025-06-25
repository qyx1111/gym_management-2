<template>
  <section class="section">
    <div class="section-header">
      <div class="section-title">
        <i class="fas fa-graduation-cap section-icon"></i>
        <h2>课程管理</h2>
      </div>
      <button class="btn btn-primary" @click="showCourseForm()">
        <i class="fas fa-plus"></i>
        <span>添加课程</span>
      </button>
    </div>
    
    <div class="search-bar">
      <div class="search-input-group">
        <i class="fas fa-search search-icon"></i>
        <input 
          type="text" 
          v-model="searchTerm"
          @input="handleSearch"
          placeholder="搜索课程名称或描述..." 
        >
      </div>
      <button class="btn btn-refresh" @click="loadCourses">
        <i class="fas fa-sync-alt"></i>
        <span>刷新</span>
      </button>
    </div>
    
    <div class="table-container">
      <table class="table">
        <thead>
          <tr>
            <th><i class="fas fa-hashtag"></i> ID</th>
            <th><i class="fas fa-graduation-cap"></i> 课程名称</th>
            <th><i class="fas fa-info-circle"></i> 描述</th>
            <th><i class="fas fa-clock"></i> 默认时长(分钟)</th>
            <th><i class="fas fa-signal"></i> 状态</th>
            <th><i class="fas fa-cogs"></i> 操作</th>
          </tr>
        </thead>
        <tbody>
          <tr v-if="loading">
            <td colspan="6" class="loading">正在加载课程数据...</td>
          </tr>
          <tr v-else-if="courses.length === 0">
            <td colspan="6">暂无课程数据</td>
          </tr>
          <tr v-else v-for="course in courses" :key="course.id">
            <td>{{ course.id }}</td>
            <td>{{ course.name }}</td>
            <td>{{ course.description || '' }}</td>
            <td>{{ course.default_duration_minutes || '' }}</td>
            <td>{{ getCourseStatusText(course.status) }}</td>
            <td>
              <button class="btn" @click="editCourse(course)">编辑</button>
              <button class="btn btn-danger" @click="deleteCourse(course)">删除</button>
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
import CourseForm from '@/components/forms/CourseForm.vue'

const api = useApi()
const appStore = useAppStore()

const courses = ref([])
const loading = ref(false)
const searchTerm = ref('')

const getCourseStatusText = (status) => {
  const statusMap = {
    'active': '活跃',
    'inactive': '非活跃'
  }
  return statusMap[status] || status
}

const loadCourses = async () => {
  loading.value = true
  try {
    console.log('正在加载课程数据...')
    const response = await api.getCourses()
    
    if (response && response.success) {
      courses.value = response.data
    } else {
      courses.value = getMockCourses()
      if (response && response.message) {
        appStore.showMessage(`使用模拟数据: ${response.message}`, 'info')
      }
    }
  } catch (error) {
    courses.value = getMockCourses()
    appStore.showMessage('使用模拟数据展示', 'info')
  } finally {
    loading.value = false
  }
}

const getMockCourses = () => {
  return [
    {
      id: 1,
      name: '力量训练',
      description: '增强肌肉力量和耐力',
      default_duration_minutes: 60,
      status: 'active'
    },
    {
      id: 2,
      name: '瑜伽课程',
      description: '提高身体柔韧性和平衡性',
      default_duration_minutes: 90,
      status: 'active'
    },
    {
      id: 3,
      name: '游泳训练',
      description: '游泳技能训练和水中健身',
      default_duration_minutes: 45,
      status: 'active'
    }
  ]
}

const handleSearch = async () => {
  if (!searchTerm.value.trim()) {
    await loadCourses()
    return
  }
  
  loading.value = true
  try {
    const response = await api.searchCourses(searchTerm.value.trim())
    if (response.success) {
      courses.value = response.data
    } else {
      appStore.showMessage(`搜索失败: ${response.message}`, 'error')
    }
  } catch (error) {
    appStore.showMessage('搜索课程失败', 'error')
  } finally {
    loading.value = false
  }
}

const showCourseForm = (course = null) => {
  appStore.openModal(CourseForm, { 
    course,
    onSaved: loadCourses
  })
}

const editCourse = (course) => {
  showCourseForm(course)
}

const deleteCourse = (course) => {
  if (confirm(`确定要删除课程 "${course.name}" 吗？`)) {
    performDelete(course.id)
  }
}

const performDelete = async (id) => {
  try {
    const response = await api.deleteCourse(id)
    if (response.success) {
      appStore.showMessage(response.message, 'success')
      await loadCourses()
    } else {
      appStore.showMessage(response.message, 'error')
    }
  } catch (error) {
    appStore.showMessage('删除课程失败', 'error')
  }
}

onMounted(() => {
  console.log('Courses组件已挂载，开始加载数据')
  loadCourses()
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
