<template>
  <header class="header">
    <div class="header-content">
      <div class="logo-section">
        <i class="fas fa-dumbbell header-icon"></i>
        <h1>NUAA健身房会员管理系统</h1>
      </div>
    </div>
    <nav class="nav">
      <router-link 
        v-for="item in navItems" 
        :key="item.name"
        :to="{ name: item.name }"
        class="nav-btn"
        :class="{ active: $route.name === item.name }"
      >
        <i :class="item.icon"></i>
        <span>{{ item.label }}</span>
      </router-link>
    </nav>
  </header>
</template>

<script setup>
const navItems = [
  { name: 'Dashboard', label: '首页', icon: 'fas fa-home' },
  { name: 'Members', label: '会员管理', icon: 'fas fa-users' },
  { name: 'Trainers', label: '教练管理', icon: 'fas fa-user-tie' },
  { name: 'Courses', label: '课程管理', icon: 'fas fa-graduation-cap' },
  { name: 'CardTypes', label: '会员卡类型', icon: 'fas fa-credit-card' }
]
</script>

