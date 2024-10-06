import { createRouter, createWebHashHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import LoginPage from '@/views/LoginPage.vue'
import Customer_Registration from '@/views/Customer_Registration.vue'
import Professional_Registration from '@/views/Professional_Registration.vue'
import Dashboard from '@/views/Dashboard.vue'

const routes = [
  {
    path: '/',
    name: 'home',
    component: HomeView
  },
  {
    path: '/login',
    name: 'login',
    component: LoginPage
  },
  {
    path: '/customer_registration',
    name: 'customer_registration',
    component: Customer_Registration
  },
  {
    path: '/professional_registration',
    name: 'professional_registration',
    component: Professional_Registration
  },
  {
    path: '/dashboard',
    name: 'dashboard',
    component: Dashboard
  }
]

const router = createRouter({
  history: createWebHashHistory(),
  routes
})

export default router
