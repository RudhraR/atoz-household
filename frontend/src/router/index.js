import { createRouter, createWebHashHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import LoginPage from '@/views/LoginPage.vue'
import Customer_Registration from '@/views/customer/Customer_Registration.vue'
import Professional_Registration from '@/views/professional/Professional_Registration.vue'
import ProfessionalDashboard from '@/views/professional/ProfessionalDashboard.vue'
import Categories from '@/views/admin/Categories.vue'
import Services from '@/views/admin/Services.vue'
import AdminDashboard from '@/views/admin/AdminDashboard.vue'
import CustomerDashboard from '@/views/customer/CustomerDashboard.vue'
import Manage_users from '@/views/admin/Manage_users.vue'
import BookServiceRequest from '@/views/customer/BookServiceRequest.vue'
import ViewServiceRequests from '@/components/ViewServiceRequests.vue'

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
    path: '/professional_dashboard',
    name: 'professional_dashboard',
    component: ProfessionalDashboard
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
  },
  {
    path: '/book_service_request',
    name: 'book_service_request',
    component: BookServiceRequest
  },
  {
    path: '/view_service_requests',
    name: 'view_service_requests',
    component: ViewServiceRequests
  }
]

const router = createRouter({
  history: createWebHashHistory(),
  routes
})

export default router
