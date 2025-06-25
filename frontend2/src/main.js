import { createApp } from 'vue'
import { createPinia } from 'pinia'
import App from './App.vue'
import router from './router'
import './assets/styles/main.css'

const app = createApp(App)
const pinia = createPinia()

app.use(pinia)
app.use(router)

// 添加全局错误处理
app.config.errorHandler = (err, vm, info) => {
  console.error('Vue error:', err, info)
}

// 添加路由守卫进行调试
router.beforeEach((to, from, next) => {
  console.log(`路由从 ${from.name || '/'} 切换到 ${to.name}`)
  next()
})

router.afterEach((to, from) => {
  console.log(`路由切换完成: ${to.name}`)
  // 确保页面标题更新
  document.title = `${to.meta?.title || to.name || '页面'} - NUAA健身房管理系统`
})

app.mount('#app')
