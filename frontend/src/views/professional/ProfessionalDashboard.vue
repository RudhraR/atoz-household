<template>
    <div v-if= "user">
      <div>
      <br><h5 style="text-align: left;">
        <i>&nbsp; Welcome, {{ this.user.username }}! </i>
      </h5><br> </div>
      <div class="container">
        <div class="card">
          <h5 class="card-header bg-secondary text-white">Your Service Requests</h5>
          <div class="card-body">
            <ViewServiceRequests />
          </div>
        </div>
        
    </div>
  </div>
  </template>
  
  <script>
import userMixin from '@/mixins/userMixin';
import ViewServiceRequests from '@/components/ViewServiceRequests.vue';
  export default {
    name: 'ProfessionalDashboard',
    mixins: [userMixin],
    components: {
      ViewServiceRequests
    }
  };
  </script>
  
  <style scoped>
  
  </style>
  