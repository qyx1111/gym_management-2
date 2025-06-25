<template>
  <section class="section">
    <div class="section-header">
      <div class="section-title">
        <i class="fas fa-user-tie section-icon"></i>
        <h2>教练详情 - {{ trainerName }} (ID: {{ id }})</h2>
      </div>
      <button class="btn btn-back" @click="$router.push({ name: 'Trainers' })">
        <i class="fas fa-arrow-left"></i>
        <span>返回教练列表</span>
      </button>
    </div>
    
    <div class="tabs">
      <button 
        v-for="tab in tabs" 
        :key="tab.key"
        class="tab-btn" 
        :class="{ active: activeTab === tab.key }"
        @click="activeTab = tab.key"
      >
        <i :class="tab.icon"></i>
        <span>{{ tab.label }}</span>
      </button>
    </div>

    <div v-if="activeTab === 'courses'" class="tab-content active">
      <div class="section-header">
        <h3>教学课程管理</h3>
        <button class="btn btn-primary" @click="showTrainerCourseForm()">分配新课程</button>
      </div>
      <div class="table-container">
        <table class="table">
          <thead>
            <tr>
              <th>分配ID</th>
              <th>课程名称</th>
              <th>分配日期</th>
              <th>课程类型</th>
              <th>备注</th>
              <th>操作</th>
            </tr>
          </thead>
          <tbody>
            <tr v-if="coursesLoading">
              <td colspan="6" class="loading">正在加载教练课程数据...</td>
            </tr>
            <tr v-else-if="trainerCourses.length === 0">
              <td colspan="6">该教练暂无分配课程</td>
            </tr>
            <tr v-else v-for="assignment in trainerCourses" :key="assignment.id">
              <td>{{ assignment.id }}</td>
              <td>{{ assignment.course_name }}</td>
              <td>{{ formatDate(assignment.assignment_date) }}</td>
              <td>{{ getCourseTypeText(assignment.course_type) }}</td>
              <td>{{ assignment.notes || '' }}</td>
              <td>
                <button class="btn" @click="editTrainerCourse(assignment)">编辑</button>
                <button class="btn btn-danger" @click="deleteTrainerCourse(assignment)">取消</button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <div v-if="activeTab === 'members'" class="tab-content active">
      <div class="section-header">
        <h3>指派会员</h3>
        <button class="btn btn-primary" @click="showTrainerMemberForm()">指派新会员</button>
      </div>
      <div class="table-container">
        <table class="table">
          <thead>
            <tr>
              <th>指派ID</th>
              <th>会员姓名</th>
              <th>指派日期</th>
              <th>指派类型</th>
              <th>备注</th>
              <th>操作</th>
            </tr>
          </thead>
          <tbody>
            <tr v-if="membersLoading">
              <td colspan="6" class="loading">正在加载教练会员数据...</td>
            </tr>
            <tr v-else-if="trainerMembers.length === 0">
              <td colspan="6">该教练暂无指派会员</td>
            </tr>
            <tr v-else v-for="assignment in trainerMembers" :key="assignment.id">
              <td>{{ assignment.id }}</td>
              <td>{{ assignment.member_name }}</td>
              <td>{{ formatDate(assignment.assignment_date) }}</td>
              <td>{{ getAssignmentTypeText(assignment.assignment_type) }}</td>
              <td>{{ assignment.notes || '' }}</td>
              <td>
                <button class="btn" @click="editTrainerMember(assignment)">编辑</button>
                <button class="btn btn-danger" @click="deleteTrainerMember(assignment)">解除</button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </section>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { useRoute } from 'vue-router'
import { useApi } from '@/composables/useApi'
import { useAppStore } from '@/stores/app'

const props = defineProps(['id'])
const route = useRoute()
const api = useApi()
const appStore = useAppStore()

const activeTab = ref('courses')
const trainerName = ref('')
const trainerCourses = ref([])
const trainerMembers = ref([])
const coursesLoading = ref(false)
const membersLoading = ref(false)

const tabs = [
  { key: 'courses', label: '教学课程', icon: 'fas fa-graduation-cap' },
  { key: 'members', label: '指派会员', icon: 'fas fa-users' }
]

const trainerId = computed(() => props.id || route.params.id)

const formatDate = (dateString) => {
  if (!dateString) return ''
  const date = new Date(dateString)
  return date.toLocaleDateString('zh-CN')
}

const getCourseTypeText = (type) => {
  const typeMap = {
    'regular': '常规课程',
    'special': '特色课程',
    'private': '私教课程',
    'group': '团体课程'
  }
  return typeMap[type] || type
}

const getAssignmentTypeText = (type) => {
  const typeMap = {
    'personal': '私教',
    'group': '团体课',
    'consultation': '咨询',
    'assessment': '体能评估'
  }
  return typeMap[type] || type
}

const loadTrainerInfo = async () => {
  try {
    const response = await api.getTrainers()
    if (response.success) {
      const trainer = response.data.find(t => t.id == trainerId.value)
      if (trainer) {
        trainerName.value = trainer.name
      }
    }
  } catch (error) {
    console.error('Failed to load trainer info:', error)
  }
}

const loadTrainerCourses = async () => {
  coursesLoading.value = true
  try {
    const response = await api.getTrainerCourses(trainerId.value)
    if (response.success) {
      trainerCourses.value = response.data
    } else {
      appStore.showMessage(`加载失败: ${response.message}`, 'error')
    }
  } catch (error) {
    appStore.showMessage('加载教练课程数据失败', 'error')
  } finally {
    coursesLoading.value = false
  }
}

const loadTrainerMembers = async () => {
  membersLoading.value = true
  try {
    const response = await api.getTrainerMembers(trainerId.value)
    if (response.success) {
      trainerMembers.value = response.data
    } else {
      appStore.showMessage(`加载失败: ${response.message}`, 'error')
    }
  } catch (error) {
    appStore.showMessage('加载教练会员数据失败', 'error')
  } finally {
    membersLoading.value = false
  }
}

const showTrainerCourseForm = () => {
  appStore.showMessage('课程分配表单功能待实现', 'warning')
}

const editTrainerCourse = (assignment) => {
  appStore.showMessage('编辑课程分配功能待实现', 'warning')
}

const deleteTrainerCourse = (assignment) => {
  if (confirm(`确定要取消教练对 "${assignment.course_name}" 课程的分配吗？`)) {
    performDeleteCourse(assignment.id)
  }
}

const performDeleteCourse = async (assignmentId) => {
  try {
    const response = await api.deleteTrainerCourse(assignmentId)
    if (response.success) {
      appStore.showMessage(response.message, 'success')
      await loadTrainerCourses()
    } else {
      appStore.showMessage(response.message, 'error')
    }
  } catch (error) {
    appStore.showMessage('取消课程分配失败', 'error')
  }
}

const showTrainerMemberForm = () => {
  appStore.showMessage('会员指派表单功能待实现', 'warning')
}

const editTrainerMember = (assignment) => {
  appStore.showMessage('编辑会员指派功能待实现', 'warning')
}

const deleteTrainerMember = (assignment) => {
  if (confirm(`确定要解除教练与会员 "${assignment.member_name}" 的指派关系吗？`)) {
    performDeleteMember(assignment.id)
  }
}

const performDeleteMember = async (assignmentId) => {
  try {
    const response = await api.deleteTrainerMember(assignmentId)
    if (response.success) {
      appStore.showMessage(response.message, 'success')
      await loadTrainerMembers()
    } else {
      appStore.showMessage(response.message, 'error')
    }
  } catch (error) {
    appStore.showMessage('解除会员指派失败', 'error')
  }
}

watch(activeTab, (newTab) => {
  switch (newTab) {
    case 'courses':
      loadTrainerCourses()
      break
    case 'members':
      loadTrainerMembers()
      break
  }
})

onMounted(() => {
  loadTrainerInfo()
  loadTrainerCourses()
})
</script>
