<template>
  <NavBar />
  <!-- <div v-if="user" class="home mt-5">
      <h1>Welcome {{ this.user.username }}</h1>
  </div> -->
  <div>
    <CustomerDashboard v-if="user && user.role == 'customer' && user.is_active " />
    <AdminDashboard v-else-if="user && user.role == 'admin'"/>
    <ProfessionalDashboard v-else-if="user && user.role == 'professional' && user.is_active"/>
    <AuthCard v-else />
  </div>
</template>

<script>
import userMixin from '@/mixins/userMixin';
import NavBar from '@/components/NavBar.vue'
import AuthCard from './AuthCard.vue';
import ProfessionalDashboard from './professional/ProfessionalDashboard.vue';
import AdminDashboard from './admin/AdminDashboard.vue';
import CustomerDashboard from './customer/CustomerDashboard.vue';

export default {
  name: 'HomeView',
  components: {
    AuthCard,
    ProfessionalDashboard,
    NavBar,
    AdminDashboard,
    CustomerDashboard
  },
  mixins: [userMixin],
}
</script>