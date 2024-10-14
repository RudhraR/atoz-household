<template>
  <NavBar />
  <!-- <div v-if="user" class="home mt-5">
      <h1>Welcome {{ this.user.username }}</h1>
  </div> -->
  <div>
    <CustomerDashboard v-if="user && user.role == 'customer'" />
    <AdminDashboard v-else-if="user && user.role == 'admin'"/>
    <Dashboard v-else-if="user && user.role == 'professional' && user.is_active"/>
    <AuthCard v-else />
  </div>
</template>

<script>
import userMixin from '@/mixins/userMixin';
import NavBar from '@/components/NavBar.vue'
import AuthCard from './AuthCard.vue';
import Dashboard from './Dashboard.vue';
import AdminDashboard from './AdminDashboard.vue';
import CustomerDashboard from './CustomerDashboard.vue';

export default {
  name: 'HomeView',
  components: {
    AuthCard,
    Dashboard,
    NavBar,
    AdminDashboard,
    CustomerDashboard
  },
  mixins: [userMixin],
}
</script>