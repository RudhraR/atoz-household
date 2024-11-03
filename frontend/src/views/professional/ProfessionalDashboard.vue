<template>
    <div v-if= "user">
      <div>
      <br><h5 style="text-align: left;">
        <i>&nbsp; Welcome, {{ this.user.username }}! </i>
      </h5><br> </div>
      <div class="container">
        <div class="card">
          <div class="card-header bg-secondary text-white"><h5>Your Service Requests</h5></div>
          <div class="card-body">
            <h5 style="text-align: left;">Open Service Requests: </h5>
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
  