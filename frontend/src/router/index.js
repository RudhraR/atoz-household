import { createRouter, createWebHashHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import LoginPage from '@/views/LoginPage.vue'
import Customer_Registration from '@/views/Customer_Registration.vue'
import Professional_Registration from '@/views/Professional_Registration.vue'
import Dashboard from '@/views/Dashboard.vue'
import Categories from '@/views/Categories.vue'
import Services from '@/views/Services.vue'
import AdminDashboard from '@/views/AdminDashboard.vue'
import CustomerDashboard from '@/views/CustomerDashboard.vue'
import Manage_users from '@/views/Manage_users.vue'

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
  },
  {
    path: '/categories',
    name: 'categories',
    component: Categories
  },
  {
    path: '/services',
    name: 'services',
    component: Services
  },
  {
    path: '/admin_dashboard',
    name: 'admin_dashboard',
    component: AdminDashboard
  },
  {
    path: '/customer_dashboard',
    name: 'customer_dashboard',
    component: CustomerDashboard
  },
  {
    path: '/manage_users',
    name: 'manage_users',
    component: Manage_users
  }
]

const router = createRouter({
  history: createWebHashHistory(),
  routes
})

export default router
