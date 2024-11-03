<template>
    <div class="container" style="margin-top: 20px;" v-if="filteredServiceRequests.length > 0">
          <table class="table border">
            <thead>
              <tr>      
                <th>Request #</th>              
                <th>Category</th>
                <th>Service Name</th>
                <th v-if="user.role != 'customer'">Customer Name</th>
                <th v-if="user.role != 'professional'">Assigned Professional</th>
                <th>Booked on</th>
                <th>Status</th>
                <th v-if="user.role != 'admin'">Actions</th>
              </tr>
            </thead>
            <tbody>
              <template v-for="(request) in filteredServiceRequests" :key="request.id">
                <tr>
                  <th>{{ request.id }}</th>
                  <td>{{ request.category }}</td>
                  <td>{{ request.service_name }}</td>
                  <td v-if="user.role != 'customer'">{{ request.customer_name }}</td>
                  <td v-if="user.role != 'professional'">{{ request.assigned_professional }}</td>
                  <td>{{ request.booked_on }}</td>
                  <td>{{ request.status }}</td>

                  <td v-if="user.role == 'professional'">
                    <button v-if ="request.status === 'requested'" class="btn btn-primary btn-sm" @click="updateRequest(request.id, 'accepted')">Accept</button>
                    <button class="btn btn-danger btn-sm" @click="updateRequest(request.id, 'rejected')">Reject</button>
                  </td>
                  <td v-if="user.role == 'customer'">
                    <button v-if ="request.status === 'rejected'"class="btn btn-primary btn-sm" @click="reopenRequest(request.id, request.professional_id)">Reopen</button>
                    <button v-if ="request.status === 'accepted'" class="btn btn-success btn-sm" @click="customerUpdateRequest(request.id, 'completed')">Complete</button>
                    <button v-if ="request.status === 'requested' || request.status === 'accepted'" class="btn btn-danger btn-sm" @click="customerUpdateRequest(request.id, 'cancelled')">Cancel</button>
                    <p v-if="request.status === 'completed' || request.status === 'cancelled'">N/A</p>
                  </td>
                </tr>
                
              </template>
            </tbody>
          </table>
    </div>
    <div class="container" style="margin-top: 20px;" v-else>
      <p class="text-muted"><i>No service requests found.</i></p>
    </div>

    <!-- Display closed requests -->
    <div class="container" style="margin-top: 20px;" v-if="closedRequests.length > 0 && user.role == 'professional'">
          <table class="table caption-top border">
            <caption><h5>Closed Requests: </h5></caption>
            <thead>
              <tr>      
                <th>Request #</th>              
                <th>Category</th>
                <th>Service Name</th>
                <th>Customer Name</th>
                <th>Closed on</th>
                <th>Status</th>
              </tr>
            </thead>
            <tbody>
              <template v-for="(request) in closedRequests" :key="request.id">
                <tr>
                  <th>{{ request.id }}</th>
                  <td>{{ request.category }}</td>
                  <td>{{ request.service_name }}</td>
                  <td>{{ request.customer_name }}</td>
                  <td>{{ request.closed_on }}</td>
                  <td>{{ request.status }}</td>
                </tr>
                
              </template>
            </tbody>
          </table>
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
            request => request.assigned_professional === this.user.username && request.status === 'requested' || request.status === 'accepted'
            );
        }
    }
    },
    closedRequests() {
      return this.serviceRequests.filter(
    request =>
      request.assigned_professional === this.user.username &&
      (request.status === 'closed' || request.status === 'rejected')
  );
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

        async updateRequest(requestId, status) {
          try {
            const response = await fetch(`http://127.0.0.1:5000/service_requests/${requestId}/${status}`, {
              method: 'PUT',
              headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${localStorage.getItem('access_token')}`
              },
              body: JSON.stringify({ status }),
            });
            if (!response.ok) {
              throw new Error('Failed to update request');
            }
            const data = await response.json(); 
            console.log(data);
            this.fetchServiceRequests();
          } catch (error) {
            console.error(error);
          }
      },

      async customerUpdateRequest(requestId, status) {
        try {
          const response = await fetch(`http://127.0.0.1:5000/service_requests/customer/${requestId}/${status}`, {
            method: 'PUT',
            headers: {
              'Content-Type': 'application/json',
              'Authorization': `Bearer ${localStorage.getItem('access_token')}`
            },
            body: JSON.stringify({ status }),
          });
          if (!response.ok) {
            throw new Error('Failed to update request');
          }
          const data = await response.json(); 
          console.log(data);
          this.fetchServiceRequests();
        } catch (error) {
          console.error(error); 
        }
      },
      async reopenRequest(requestId, professional_id) {
        try {
          const response = await fetch(`http://127.0.0.1:5000/service_requests/reopen/${requestId}/${professional_id}`, {
            method: 'PUT',
            headers: {
              'Content-Type': 'application/json',
              'Authorization': `Bearer ${localStorage.getItem('access_token')}`
            },
            body: JSON.stringify({ professional_id }),
          });
          if (!response.ok) {
            throw new Error('Failed to reopen request');
          }
          const data = await response.json(); 
          console.log(data);
          this.fetchServiceRequests();
        } catch (error) {
          console.error(error); 
        }
      }}
    };
</script>
  