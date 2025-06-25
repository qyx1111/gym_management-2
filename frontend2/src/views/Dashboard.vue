<template>
  <section class="section active">
    <div class="welcome-banner">
      <div class="welcome-icon">
        <i class="fas fa-dumbbell"></i>
      </div>
      <div class="welcome-content">
        <h2><i class="fas fa-chart-line"></i> 欢迎使用NUAA健身房会员管理系统</h2>
        <p>高效管理您的健身房业务</p>
      </div>
    </div>
    <div class="dashboard-cards">
      <div 
        v-for="card in dashboardCards" 
        :key="card.name"
        class="card" 
        :class="card.className"
        @click="$router.push({ name: card.name })"
      >
        <div class="card-icon">
          <i :class="card.icon"></i>
        </div>
        <div class="card-content">
          <h3>{{ card.title }}</h3>
          <p>{{ card.description }}</p>
          <div class="card-stats">
            <span class="stats-number">{{ card.count }}</span>
            <span class="stats-label">{{ card.label }}</span>
          </div>
        </div>
        <div class="card-arrow">
          <i class="fas fa-arrow-right"></i>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useApi } from '@/composables/useApi'

const api = useApi()

const dashboardCards = ref([
  { name: 'Members', className: 'members-card', icon: 'fas fa-users', title: '会员管理', description: '管理会员信息、办卡、报名课程', count: '-', label: '活跃会员' },
  { name: 'Trainers', className: 'trainers-card', icon: 'fas fa-user-tie', title: '教练管理', description: '管理教练信息和专长', count: '-', label: '专业教练' },
  { name: 'Courses', className: 'courses-card', icon: 'fas fa-graduation-cap', title: '课程管理', description: '管理课程信息和安排', count: '-', label: '热门课程' },
  { name: 'CardTypes', className: 'cards-card', icon: 'fas fa-credit-card', title: '会员卡类型', description: '管理会员卡类型和价格', count: '-', label: '卡类型' }
])

const loadStats = async () => {
  try {
    // 并行加载所有统计数据
    const [membersResponse, trainersResponse, coursesResponse, cardTypesResponse] = await Promise.allSettled([
      api.getMembers(),
      api.getTrainers(),
      api.getCourses(),
      api.getCardTypes()
    ])

    // 处理会员统计
    if (membersResponse.status === 'fulfilled' && membersResponse.value.success) {
      const activeMembersCount = membersResponse.value.data.filter(m => m.status === 'active').length
      dashboardCards.value[0].count = activeMembersCount
    } else {
      dashboardCards.value[0].count = '8'
    }

    // 处理教练统计
    if (trainersResponse.status === 'fulfilled' && trainersResponse.value.success) {
      const activeTrainersCount = trainersResponse.value.data.filter(t => t.status === 'active').length
      dashboardCards.value[1].count = activeTrainersCount
    } else {
      dashboardCards.value[1].count = '5'
    }

    // 处理课程统计
    if (coursesResponse.status === 'fulfilled' && coursesResponse.value.success) {
      const activeCoursesCount = coursesResponse.value.data.filter(c => c.status === 'active').length
      dashboardCards.value[2].count = activeCoursesCount
    } else {
      dashboardCards.value[2].count = '12'
    }

    // 处理会员卡类型统计
    if (cardTypesResponse.status === 'fulfilled' && cardTypesResponse.value.success) {
      dashboardCards.value[3].count = cardTypesResponse.value.data.length
    } else {
      dashboardCards.value[3].count = '4'
    }
  } catch (error) {
    console.error('加载仪表板统计数据失败:', error)
    // 使用默认数据
    dashboardCards.value[0].count = '8'
    dashboardCards.value[1].count = '5'
    dashboardCards.value[2].count = '12'
    dashboardCards.value[3].count = '4'
  }
}

onMounted(() => {
  console.log('Dashboard组件已挂载，开始加载统计数据')
  loadStats()
})
</script>

<style scoped>
.section {
  width: 100%;
  min-height: 500px;
}

.welcome-banner {
  text-align: center;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}

.welcome-content {
  text-align: center;
  width: 100%;
}

.welcome-content h2 {
  text-align: center;
  margin: 0 auto 0.5rem;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 1rem;
}

.welcome-content p {
  text-align: center;
  margin: 0 auto;
}

.welcome-icon {
    width: 120px;
    height: 120px;
    background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    margin: 0 auto 2rem;
    font-size: 3rem;
    color: white;
    box-shadow: var(--shadow-lg);
    transition: all 0.3s ease;
}

.welcome-icon:hover {
    transform: scale(1.05) rotate(5deg);
    box-shadow: var(--shadow-xl);
}

.dashboard-cards {
  margin-top: 2rem;
}
</style>
