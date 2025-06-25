<template>
  <div class="container">
    <AppHeader />
    <main class="main">
      <router-view v-slot="{ Component }">
        <transition name="fade" mode="out-in">
          <component :is="Component" v-if="Component" />
        </transition>
      </router-view>
    </main>
    <AppModal />
    <MessageContainer />
  </div>
</template>

<script setup>
import AppHeader from './components/AppHeader.vue'
import AppModal from './components/AppModal.vue'
import MessageContainer from './components/MessageContainer.vue'
</script>

<style>
/* 确保全局样式生效 */
.container {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

.main {
  flex: 1;
  padding: 2rem;
  overflow-x: hidden;
}

/* 页面切换动画 */
.fade-enter-active,
.fade-leave-active {
  transition: all 0.3s ease;
}

.fade-enter-from {
  opacity: 0;
  transform: translateX(20px);
}

.fade-leave-to {
  opacity: 0;
  transform: translateX(-20px);
}

/* 确保路由视图正确显示 */
.router-view {
  width: 100%;
  min-height: 400px;
}

@media (max-width: 768px) {
  .main {
    padding: 1rem;
  }
}
</style>
