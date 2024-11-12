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
import BookServiceRequest from '@/components/BookServiceRequest.vue'
import ViewServiceRequests from '@/components/ViewServiceRequests.vue'
import ProfilePage from '@/views/ProfilePage.vue'
import SearchPage from '@/views/SearchPage.vue'
import SummaryGraphs from '@/views/SummaryGraphs.vue'
import { getLoginDetails } from '@/utils/getLoginDetails.js';


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
    component: ProfessionalDashboard,
    meta: {requiresAuth: true,role: 'professional'}
  },
  {
    path: '/categories',
    name: 'categories',
    component: Categories,
    meta: {requiresAuth: true,role: 'admin'}    
  },
  {
    path: '/services',
    name: 'services',
    component: Services,
    meta: {requiresAuth: true,role: 'admin'}
  },
  {
    path: '/admin_dashboard',
    name: 'admin_dashboard',
    component: AdminDashboard,
    meta: {requiresAuth: true,role: 'admin'}
  },
  {
    path: '/customer_dashboard',
    name: 'customer_dashboard',
    component: CustomerDashboard,
    meta: {requiresAuth: true,role: 'customer'}
  },
  {
    path: '/manage_users',
    name: 'manage_users',
    component: Manage_users,
    meta: {requiresAuth: true, role: 'admin'}
  },
  {
    path: '/book_service_request',
    name: 'book_service_request',
    component: BookServiceRequest,
    meta: {requiresAuth: true, role: 'customer'}
  },
  {
    path: '/view_service_requests',
    name: 'view_service_requests',
    component: ViewServiceRequests,
    meta: {requiresAuth: true}
  },
  {
    path: '/profile',
    name: 'profile',
    component: ProfilePage,
    meta: {requiresAuth: true}
  },
  {
    path: '/search',
    name: 'search',
    component: SearchPage,
    meta: {requiresAuth: true}
  },
  {
    path: '/summary',
    name: 'summary',
    component: SummaryGraphs,
    meta: {requiresAuth: true}
  }
]

const router = createRouter({
  history: createWebHashHistory(),
  routes
})

router.beforeEach(async (to, from, next) => {
  try {
    const loginDetails = await getLoginDetails();
    
    if (to.matched.some((record) => record.meta.requiresAuth)) {
      if (!loginDetails || !loginDetails.isLoggedin) {
        next({ path: '/' });  // Redirect to login page
      } else if (to.meta.role && to.meta.role != loginDetails.role) {
        next({ path: '/' });  // Redirect if roles don't match
      } else {
        next();  // Proceed if everything checks out
      }
    } else {
      next();  // No auth required
    }
  } catch (error) {
    console.error("Error fetching login details:", error);
    next({ path: '/' });
  }
});


export default router
