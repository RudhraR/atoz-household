<template>
  <div class="container" style="margin-top: 20px;" v-if="filteredServiceRequests && filteredServiceRequests.length > 0">
    <table class="table caption-top border">
      <caption>
        <h5>Open Requests: </h5>
      </caption>
      <thead>
        <tr>
          <th>Request #</th>
          <th>Category</th>
          <th>Service Name</th>
          <th v-if="role != 'customer'">Customer Name</th>
          <th v-if="role != 'professional'">Assigned Professional</th>
          <th>Booked on</th>
          <th>Status</th>
          <th v-if="role != 'admin'">Actions</th>
        </tr>
      </thead>
      <tbody>
        <tr v-if="filteredServiceRequests && filteredServiceRequests.length > 0" 
          v-for="(request) in filteredServiceRequests" :key="request.id">
          
            <th>{{ request.id }}</th>
            <td>{{ request.category }}</td>
            <td>{{ request.service_name }}</td>
            <td v-if="role != 'customer'">{{ request.customer_name }}</td>
            <td v-if="role != 'professional'">{{ request.assigned_professional }}</td>
            <td>{{ request.booked_on }}</td>
            <td>{{ request.status }}</td>

            <td v-if="role == 'professional'">
              <button v-if="request.status === 'requested'" class="btn btn-primary btn-sm"
                @click="updateRequest(request.id, 'accepted')">Accept</button>
              <button class="btn btn-danger btn-sm" @click="updateRequest(request.id, 'rejected')">Reject</button>
              <button v-if="request.status === 'accepted'" class="btn btn-success btn-sm"
                @click="updateRequest(request.id, 'completed')">Complete</button>
            </td>
            <td v-if="role == 'customer'">

              <button v-if="request.status === 'accepted'" class="btn btn-success btn-sm"
                @click="completeRequest(request)">Complete</button>
              <span v-if="request.status === 'requested' || request.status === 'accepted'">
              <button class="btn btn-warning btn-sm" 
              @click="openRescheduleModal(request)">Reschedule</button>
              <button class="btn btn-danger btn-sm" 
              @click="customerUpdateRequest(request.id, 'cancelled')">Cancel</button>
              </span>
                <p v-if="request.status === 'completed' || request.status === 'cancelled'">N/A</p>
            </td>
          </tr>

      </tbody>
    </table>
  </div>
  <div v-else>
    <p class="text-muted text-center"><i>No service requests found</i></p>
  </div>


  <!-- Display closed requests -->
  <div class="container" style="margin-top: 20px;" v-if="closedRequests && closedRequests.length > 0">
    <table class="table caption-top border">
      <caption>
        <h5>Closed Requests: </h5>
      </caption>
      <thead>
        <tr>
          <th>Request #</th>
          <th>Category</th>
          <th>Service Name</th>
          <th v-if="user.role != 'customer'">Customer Name</th>
          <th v-if="user.role != 'professional'">Professional Name</th>
          <th>Closed on</th>
          <th>Status</th>
          <th v-if="user.role == 'customer'">Actions</th>
        </tr>
      </thead>
      <tbody>
        <template v-for="(request) in closedRequests" :key="request.id">
          <tr>
            <th>{{ request.id }}</th>
            <td>{{ request.category }}</td>
            <td>{{ request.service_name }}</td>
            <td v-if="user.role != 'customer'">{{ request.customer_name }}</td>
            <td v-if="user.role != 'professional'">{{ request.assigned_professional }}</td>
            <td>{{ request.closed_on }}</td>
            <td>{{ request.status }}</td>
            <td v-if="user.role == 'customer'">
              <button v-if="request.status === 'rejected' && request.rebooked == false" class="btn btn-primary btn-sm"
                @click="handleRetryClick(request)">Retry booking</button>
              <p v-else style="margin: 0%;">N/A</p>
            </td>

          </tr>

        </template>
      </tbody>
    </table>
  </div>
  
  <!-- Reschedule service request Modal -->
  <div class="modal fade" id="rescheduleServiceModal" tabindex="-1" aria-hidden="true" ref="rescheduleServiceModal">
    <div class="modal-dialog">
      <div class="modal-content">
        <div class="modal-header">
          <h5 class="modal-title">Reschedule Request</h5>
          <button type="button" class="btn-close" data-bs-dismiss="modal"
            aria-label="Close"></button>
        </div>
        <div class="modal-body">
          <div class="form row mb-3">
            <label class="col-sm-6 col-form-label">Request ID</label>
            <div class="col-sm-6">
              <input type="text" class="form-control" v-model="selectedRequest.id" disabled>
            </div>
          </div>
          <div class="form row mb-3">
            <label class="col-sm-6 col-form-label">Service name</label>
            <div class="col-sm-6">
              <input type="text" class="form-control" v-model="selectedRequest.service_name" disabled>
            </div>
          </div>
          <div class="form row mb-3">
            <label class="col-sm-6 col-form-label">Booked on</label>
            <div class="col-sm-6">
              <input type="text" class="form-control" v-model="selectedRequest.booked_on" disabled>
            </div>
          </div>
          <div class="form row mb-3">
            <label class="col-sm-6 col-form-label">Reschedule to: </label>
            <div class="col-sm-6">
              <input type="datetime-local" class="form-control" v-model="rescheduledDate" >
            </div>
          </div>
        </div>
        <div class="modal-footer">
          <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cancel</button>
          <button type="button" class="btn btn-primary" @click="rescheduleRequest(selectedRequest.id, rescheduledDate)">
            Reschedule Request</button>
        </div>
      </div>
    </div>
  </div>

  <!-- Complete service request Modal -->
  <div class="modal fade" id="serviceRemarksModal" tabindex="-1" aria-hidden="true" ref="serviceRemarksModal">
    <div class="modal-dialog">
      <div class="modal-content">
        <div class="modal-header">
          <h5 class="modal-title">Service Remarks</h5>
          <button type="button" class="btn-close" @click="resetForm()" data-bs-dismiss="modal"
            aria-label="Close"></button>
        </div>
        <div class="modal-body">
          <div class="form row mb-3">
            <label class="col-sm-6 col-form-label">Request ID</label>
            <div class="col-sm-6">
              <input type="text" class="form-control" v-model="selectedRequest.id" disabled>
            </div>
          </div>

          <div class="form row mb-3">
            <label class="col-sm-6 col-form-label">Service Name</label>
            <div class="col-sm-6">
              <input type="text" class="form-control" v-model="selectedRequest.service_name" disabled>
            </div>
          </div>

          <div class="form row mb-3">
            <label class="col-sm-6 col-form-label">Assigned Professional</label>
            <div class="col-sm-6">
              <input type="text" class="form-control" v-model="selectedRequest.assigned_professional" disabled>
            </div>
          </div>

          <div class="card shadow">
            <div class="card-header">Give us your feedback:</div>
            <div class="card-body">
              <div class="form-group row">
                <label class="col-form-label col-sm-6">Rate the service: &nbsp;</label>
                <div class="col-sm-6" style="text-align: left;">
                  <span v-for="(star, index) in 5" :key="index" @click="setRating(index + 1)"
                    style="cursor: pointer; text-align: left;">
                    <i :class="index < serviceRating ? 'fas fa-star text-danger' : 'far fa-star text-secondary'"></i>
                  </span>
                </div>
              </div>

              <div class="form-group row" style="text-align: center;">
                <label class="col-sm-6 col-form-label">Remarks (if any):</label>
                <span class="col-sm-6"><textarea class="form-control" v-model="remarks" rows="3"
                    placeholder="Enter any additional remarks here"></textarea>
                </span>
              </div>
            </div>
          </div>

        </div>
        <div class="modal-footer">
          <button type="button" class="btn btn-secondary" @click="resetForm()"
            data-bs-dismiss="modal">Cancel</button>
          <button type="button" class="btn btn-primary" @click="customerUpdateRequest(selectedRequest.id, 'completed')">Submit &
            Close Request</button>
        </div>
      </div>
    </div>
  </div>


</template>

<script>

import userMixin from '@/mixins/userMixin';
export default {
  name: 'ViewServiceRequests',
  mixins: [userMixin],
  props: ['serviceRequest'],
  emits: ['retry-booking'],
  data() {
    return {
      serviceRequests: [],
      selectedRequest: [],        // Stores the request details to complete and give remarks
      serviceRating: 0,        // Stores the selected service rating
      remarks: '',             // Stores the remarks
      professionals: [],                 // List of professionals for the category
      selectedCategoryId: null,         // Stores the selected category ID
      rescheduledDate: ''
    };
  },
  computed: {
    filteredServiceRequests() {
      // Filtering logic based on role
      if (this.serviceRequests.length === 0) {
        return [];
      }
      else {
        if (this.user && this.user.role === "admin") {
          return this.serviceRequests.filter(
            request => request.status === 'requested' || request.status === 'accepted');
        } else if (this.user && this.user.role === "customer") {
          return this.serviceRequests.filter(
            request => request.customer_id === this.user.id && request.status === 'requested' || request.status === 'accepted'
          );
        } else if (this.user&& this.user.role === "professional") {
          return this.serviceRequests.filter(
            request => request.assigned_professional === this.user.username && request.status === 'requested' || request.status === 'accepted'
          );
        }
      }
    },
    closedRequests() {
      if (this.serviceRequests.length === 0) {
        return [];
      }
      else {
        if (this.user && this.user.role === "customer") {
          return this.serviceRequests.filter(
            request =>
              request.customer_id === this.user.id &&
              (request.status === 'cancelled' || request.status === 'completed' || request.status === 'rejected')
          )
        }
        else if (this.user && this.user.role === "professional") {
          return this.serviceRequests.filter(
            request =>
              request.assigned_professional === this.user.username &&
              (request.status === 'closed' || request.status === 'rejected' || request.status === 'completed')
          );
        }
        else if(this.user && this.user.role === "admin") {
          return this.serviceRequests.filter(
            request =>
              request.status === 'closed' || request.status === 'rejected' || 
              request.status === 'completed' || request.status === 'cancelled'
          )
        }
      }
    }
  },
  async mounted() {
    await this.fetchServiceRequests();
  },
  methods: {
    setRating(rating) {
      this.serviceRating = rating; // Update the service rating based on the selected star
    },
    resetForm() {
      this.remarks = '';
      this.serviceRating = 0;
      this.selectedRequest = [];
      this.rescheduledDate = '';
    },
    async openRescheduleModal(request) {
      this.selectedRequest = request;
      const rescheduledModal = new bootstrap.Modal(this.$refs.rescheduleServiceModal);   // Initialize Bootstrap Modal
      rescheduledModal.show();
    },
    async rescheduleRequest(requestId, rescheduledDate) {
     try{
      const formData = new FormData();
      formData.append('rescheduled_date', rescheduledDate);
      const response = await fetch(`http://127.0.0.1:5000/service_requests/${requestId}/reschedule`, {
        method: 'PUT',
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('access_token')}`
        },
        body: formData
      });
        if (!response.ok) {
          throw new Error('Failed to reschedule request');
        }
        const data = await response.json();
        alert(data.message);
        // close the modal
        const rescheduledModal = bootstrap.Modal.getInstance(this.$refs.rescheduleServiceModal);
        rescheduledModal.hide();
        this.fetchServiceRequests();
      } catch (error) {
          console.error(error);
        } 
    },
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
      const formData = new FormData();
      formData.append('status', status);
      if(status === 'completed') {
        formData.append('rating', this.serviceRating);
        formData.append('remarks', this.remarks);
        const serviceRemarksModal = bootstrap.Modal.getInstance(this.$refs.serviceRemarksModal);   // Initialize Bootstrap Modal
      serviceRemarksModal.hide();
      }
      for (let [key, value] of formData.entries()) {
    console.log(`${key}: ${value}`);
}
      try {
        const response = await fetch(`http://127.0.0.1:5000/service_requests/customer/${requestId}/${status}`, {
          method: 'PUT',
          headers: {
            'Authorization': `Bearer ${localStorage.getItem('access_token')}`
          },
          body: formData
        });
        if (!response.ok) {
          throw new Error('Failed to close request');
        }
        const data = await response.json();
        console.log(data);
        this.fetchServiceRequests();
      } catch (error) {
        console.error(error);
      }
      if(status == "completed") {
        this.resetForm();
      }
    },
    async completeRequest(request) {
      this.selectedRequest = request;
      const serviceRemarksModal = new bootstrap.Modal(this.$refs.serviceRemarksModal);   // Initialize Bootstrap Modal
      serviceRemarksModal.show();
    },
    async fetchProfessionals(categoryId) {
      try {
        const response = await fetch(`http://127.0.0.1:5000/professionals_by_category/${categoryId}`,
          {
            method: 'GET',
            headers: {
              'Content-Type': 'application/json',
              'Authorization': `Bearer ${localStorage.getItem('access_token')}`
            }
          }
        );
        if (!response.ok) {
          throw new Error('Failed to fetch professionals');
        }

        const data = await response.json();
        this.professionals = data.professionals;   // Assign professionals to dropdown
      } catch (error) {
        console.error("Error fetching professionals:", error);
      }
    },
    async handleRetryClick(serviceRequest) {
      // Emit the event to the parent
      
      const response = await fetch(`http://127.0.0.1:5000/service/${serviceRequest.service_id}`, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${localStorage.getItem('access_token')}`
        }
      });
      const data = await response.json();
      data.service.serviceRequest_id = serviceRequest.id;
      this.$emit('retry-booking', data.service);
    }

  }
};
</script>
