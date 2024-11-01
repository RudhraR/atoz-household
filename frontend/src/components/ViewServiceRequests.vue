<template>
    <div class="container" style="margin-top: 20px;" v-if="filteredServiceRequests.length > 0">
          <table class="table">
            <thead>
              <tr>      
                <th>Request #</th>              
                <th>Category</th>
                <th>Service Name</th>
                <th v-if="user.role != 'customer'">Customer Name</th>
                <th>Assigned Professional</th>
                <th>Booked on</th>
                <th>Status</th>
              </tr>
            </thead>
            <tbody>
              <template v-for="(request) in filteredServiceRequests" :key="request.id">
                <tr>
                  <th>{{ request.id }}</th>
  
                  <td>{{ request.category }}</td>
                  <td>{{ request.service_name }}</td>
                  <td v-if="user.role != 'customer'">{{ request.customer_name }}</td>
                  <td>{{ request.assigned_professional }}</td>
                  <td>{{ request.booked_on }}</td>
                  <td>{{ request.status }}</td>
                </tr>
                
              </template>
            </tbody>
          </table>
    </div>
    <div class="container" style="margin-top: 20px;" v-else>
      <p class="text-muted"><i>No service requests found.</i></p>
    </div>
  </template>

<script>

import userMixin from '@/mixins/userMixin';
    export default {
      name: 'ViewServiceRequests',
      mixins: [userMixin],
     
      data() {
        return {
          serviceRequests: [],
        };
      },
      computed: {
     filteredServiceRequests() {
      // Filtering logic based on role
      if (this.serviceRequests.length === 0) {
        return [];
      }
      else{
        if (this.user.role === "admin") {
            return this.serviceRequests;
        } else if (this.user.role === "customer") {
            return this.serviceRequests.filter(
            request => request.customer_id === this.user.id
        );
        } else if (this.user.role === "professional") {
            return this.serviceRequests.filter(
            request => request.assigned_professional === this.user.username
            );
        }
    }
    }
  },
      async mounted() {
        await this.fetchServiceRequests();
      },
      methods: {
        async fetchServiceRequests() {
          try {
            const response = await fetch('http://127.0.0.1:5000/service_requests',
              {
                method: 'GET',
                headers: {
                  'Content-Type': 'application/json',
                  'Authorization': `Bearer ${localStorage.getItem('access_token')}`
                }
              });
              if (!response.ok) {
              throw new Error('Failed to fetch service requests');
            }
            const data = await response.json();
            this.serviceRequests = data.service_requests;
            console.log(this.serviceRequests);            
          } catch (error) {
            console.error(error);
          }
        },
      },
    };
</script>
  