import { createRouter, createWebHistory } from 'vue-router'
import Dashboard from '@/views/Dashboard.vue'
import Members from '@/views/Members.vue'
import MemberDetail from '@/views/MemberDetail.vue'
import Trainers from '@/views/Trainers.vue'
import TrainerDetail from '@/views/TrainerDetail.vue'
import Courses from '@/views/Courses.vue'
import CardTypes from '@/views/CardTypes.vue'

const routes = [
  {
    path: '/',
    name: 'Dashboard',
    component: Dashboard,
    meta: { title: '首页' }
  },
  {
    path: '/members',
    name: 'Members',
    component: Members,
    meta: { title: '会员管理' }
  },
  {
    path: '/members/:id',
    name: 'MemberDetail',
    component: MemberDetail,
    props: true,
    meta: { title: '会员详情' }
  },
  {
    path: '/trainers',
    name: 'Trainers',
    component: Trainers,
    meta: { title: '教练管理' }
  },
  {
    path: '/trainers/:id',
    name: 'TrainerDetail',
    component: TrainerDetail,
    props: true,
    meta: { title: '教练详情' }
  },
  {
    path: '/courses',
    name: 'Courses',
    component: Courses,
    meta: { title: '课程管理' }
  },
  {
    path: '/card-types',
    name: 'CardTypes',
    component: CardTypes,
    meta: { title: '会员卡类型' }
  },
  {
    path: '/:pathMatch(.*)*',
    redirect: '/'
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
