<template>
  <section class="section">
    <div class="section-header">
      <div class="section-title">
        <i class="fas fa-user-circle section-icon"></i>
        <h2>会员详情 - {{ memberName }} (ID: {{ id }})</h2>
      </div>
      <button class="btn btn-back" @click="$router.push({ name: 'Members' })">
        <i class="fas fa-arrow-left"></i>
        <span>返回会员列表</span>
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

    <div v-if="activeTab === 'cards'" class="tab-content active">
      <div class="section-header">
        <h3>会员卡管理</h3>
        <button class="btn btn-primary" @click="showMemberCardForm()">办理新卡</button>
      </div>
      <div class="table-container">
        <table class="table">
          <thead>
            <tr>
              <th>卡ID</th>
              <th>卡类型</th>
              <th>购买日期</th>
              <th>激活日期</th>
              <th>失效日期</th>
              <th>状态</th>
              <th>操作</th>
            </tr>
          </thead>
          <tbody>
            <tr v-if="cardsLoading">
              <td colspan="7" class="loading">正在加载会员卡数据...</td>
            </tr>
            <tr v-else-if="memberCards.length === 0">
              <td colspan="7">该会员暂无会员卡</td>
            </tr>
            <tr v-else v-for="card in memberCards" :key="card.id">
              <td>{{ card.id }}</td>
              <td>{{ card.card_type_name }}</td>
              <td>{{ formatDate(card.purchase_date) }}</td>
              <td>{{ formatDate(card.activation_date) }}</td>
              <td>{{ formatDate(card.expiry_date) }}</td>
              <td>{{ getCardStatusText(card.status) }}</td>
              <td>
                <button class="btn" @click="editMemberCard(card)">编辑</button>
                <button class="btn btn-danger" @click="deleteMemberCard(card)">删除</button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <div v-if="activeTab === 'courses'" class="tab-content active">
      <div class="section-header">
        <h3>已报课程</h3>
        <button class="btn btn-primary" @click="showMemberCourseForm()">报名新课程</button>
      </div>
      <div class="table-container">
        <table class="table">
          <thead>
            <tr>
              <th>报名ID</th>
              <th>课程名称</th>
              <th>报名日期</th>
              <th>状态</th>
              <th>备注</th>
              <th>操作</th>
            </tr>
          </thead>
          <tbody>
            <tr v-if="coursesLoading">
              <td colspan="6" class="loading">正在加载课程报名数据...</td>
            </tr>
            <tr v-else-if="memberEnrollments.length === 0">
              <td colspan="6">该会员暂未报名任何课程</td>
            </tr>
            <tr v-else v-for="enrollment in memberEnrollments" :key="enrollment.id">
              <td>{{ enrollment.id }}</td>
              <td>{{ enrollment.course_name }}</td>
              <td>{{ formatDate(enrollment.enrollment_date) }}</td>
              <td>{{ enrollment.status }}</td>
              <td>{{ enrollment.notes || '' }}</td>
              <td>
                <button class="btn" @click="editMemberEnrollment(enrollment)">编辑</button>
                <button class="btn btn-danger" @click="deleteMemberEnrollment(enrollment)">取消</button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <div v-if="activeTab === 'trainers'" class="tab-content active">
      <div class="section-header">
        <h3>指派教练</h3>
        <button class="btn btn-primary" @click="showMemberTrainerForm()">指派新教练</button>
      </div>
      <div class="table-container">
        <table class="table">
          <thead>
            <tr>
              <th>指派ID</th>
              <th>教练姓名</th>
              <th>指派日期</th>
              <th>指派类型</th>
              <th>备注</th>
              <th>操作</th>
            </tr>
          </thead>
          <tbody>
            <tr v-if="trainersLoading">
              <td colspan="6" class="loading">正在加载教练指派数据...</td>
            </tr>
            <tr v-else-if="memberAssignments.length === 0">
              <td colspan="6">该会员暂未指派任何教练</td>
            </tr>
            <tr v-else v-for="assignment in memberAssignments" :key="assignment.id">
              <td>{{ assignment.id }}</td>
              <td>{{ assignment.trainer_name }}</td>
              <td>{{ formatDate(assignment.assignment_date) }}</td>
              <td>{{ getAssignmentTypeText(assignment.assignment_type) }}</td>
              <td>{{ assignment.notes || '' }}</td>
              <td>
                <button class="btn" @click="editMemberAssignment(assignment)">编辑</button>
                <button class="btn btn-danger" @click="deleteMemberAssignment(assignment)">解除</button>
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

const activeTab = ref('cards')
const memberName = ref('')
const memberCards = ref([])
const memberEnrollments = ref([])
const memberAssignments = ref([])
const cardsLoading = ref(false)
const coursesLoading = ref(false)
const trainersLoading = ref(false)

const tabs = [
  { key: 'cards', label: '会员卡', icon: 'fas fa-credit-card' },
  { key: 'courses', label: '已报课程', icon: 'fas fa-graduation-cap' },
  { key: 'trainers', label: '指派教练', icon: 'fas fa-user-tie' }
]

const memberId = computed(() => props.id || route.params.id)

const formatDate = (dateString) => {
  if (!dateString) return ''
  const date = new Date(dateString)
  return date.toLocaleDateString('zh-CN')
}

const getCardStatusText = (status) => {
  const statusMap = {
    'pending_activation': '待激活',
    'active': '活跃',
    'frozen': '冻结',
    'expired': '过期',
    'cancelled': '已取消'
  }
  return statusMap[status] || status
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

const loadMemberInfo = async () => {
  try {
    const response = await api.getMember(memberId.value)
    if (response.success) {
      memberName.value = response.data.name
    }
  } catch (error) {
    console.error('Failed to load member info:', error)
  }
}

const loadMemberCards = async () => {
  cardsLoading.value = true
  try {
    const response = await api.getMemberCards(memberId.value)
    if (response.success) {
      memberCards.value = response.data
    } else {
      appStore.showMessage(`加载失败: ${response.message}`, 'error')
    }
  } catch (error) {
    appStore.showMessage('加载会员卡数据失败', 'error')
  } finally {
    cardsLoading.value = false
  }
}

const loadMemberEnrollments = async () => {
  coursesLoading.value = true
  try {
    const response = await api.getMemberEnrollments(memberId.value)
    if (response.success) {
      memberEnrollments.value = response.data
    } else {
      appStore.showMessage(`加载失败: ${response.message}`, 'error')
    }
  } catch (error) {
    appStore.showMessage('加载课程报名数据失败', 'error')
  } finally {
    coursesLoading.value = false
  }
}

const loadMemberAssignments = async () => {
  trainersLoading.value = true
  try {
    const response = await api.getMemberAssignments(memberId.value)
    if (response.success) {
      memberAssignments.value = response.data
    } else {
      appStore.showMessage(`加载失败: ${response.message}`, 'error')
    }
  } catch (error) {
    appStore.showMessage('加载教练指派数据失败', 'error')
  } finally {
    trainersLoading.value = false
  }
}

const showMemberCardForm = () => {
  // TODO: 实现会员卡表单
  appStore.showMessage('会员卡表单功能待实现', 'warning')
}

const editMemberCard = (card) => {
  appStore.showMessage('编辑会员卡功能待实现', 'warning')
}

const deleteMemberCard = (card) => {
  if (confirm(`确定要删除这张 "${card.card_type_name}" 吗？`)) {
    performDeleteCard(card.id)
  }
}

const performDeleteCard = async (cardId) => {
  try {
    const response = await api.deleteMemberCard(cardId)
    if (response.success) {
      appStore.showMessage(response.message, 'success')
      await loadMemberCards()
    } else {
      appStore.showMessage(response.message, 'error')
    }
  } catch (error) {
    appStore.showMessage('删除会员卡失败', 'error')
  }
}

const showMemberCourseForm = () => {
  appStore.showMessage('课程报名表单功能待实现', 'warning')
}

const editMemberEnrollment = (enrollment) => {
  appStore.showMessage('编辑课程报名功能待实现', 'warning')
}

const deleteMemberEnrollment = (enrollment) => {
  if (confirm(`确定要取消 "${enrollment.course_name}" 课程报名吗？`)) {
    performDeleteEnrollment(enrollment.id)
  }
}

const performDeleteEnrollment = async (enrollmentId) => {
  try {
    const response = await api.deleteMemberEnrollment(enrollmentId)
    if (response.success) {
      appStore.showMessage(response.message, 'success')
      await loadMemberEnrollments()
    } else {
      appStore.showMessage(response.message, 'error')
    }
  } catch (error) {
    appStore.showMessage('取消课程报名失败', 'error')
  }
}

const showMemberTrainerForm = () => {
  appStore.showMessage('教练指派表单功能待实现', 'warning')
}

const editMemberAssignment = (assignment) => {
  appStore.showMessage('编辑教练指派功能待实现', 'warning')
}

const deleteMemberAssignment = (assignment) => {
  if (confirm(`确定要解除与教练 "${assignment.trainer_name}" 的指派关系吗？`)) {
    performDeleteAssignment(assignment.id)
  }
}

const performDeleteAssignment = async (assignmentId) => {
  try {
    const response = await api.deleteMemberAssignment(assignmentId)
    if (response.success) {
      appStore.showMessage(response.message, 'success')
      await loadMemberAssignments()
    } else {
      appStore.showMessage(response.message, 'error')
    }
  } catch (error) {
    appStore.showMessage('解除教练指派失败', 'error')
  }
}

watch(activeTab, (newTab) => {
  switch (newTab) {
    case 'cards':
      loadMemberCards()
      break
    case 'courses':
      loadMemberEnrollments()
      break
    case 'trainers':
      loadMemberAssignments()
      break
  }
})

onMounted(() => {
  loadMemberInfo()
  loadMemberCards()
})
</script>
