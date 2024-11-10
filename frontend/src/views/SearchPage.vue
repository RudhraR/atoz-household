<template>
    <NavBar />
    <div v-if="this.role" class="container mt-5">
      <!-- Search Input Section -->
      <div class="search-box d-flex align-items-center mb-3">
        <label v-if = "this.role === 'customer' || this.role === 'admin'" class="me-2 flex-shrink-0">Search by:</label>
        <label v-else = "this.role === 'professional'" class="me-2 flex-shrink-0">Search Service Request by:</label>
        <select v-model="searchType" class="form-select me-2">
          <option v-for="option in searchOptions" :key="option.value" :value="option.value">
            {{ option.text }}
          </option>
        </select>
        <input 
          v-model="searchQuery" 
          type="text" 
          class="form-control" 
          placeholder="Enter search text" 
        />
        <button @click="performSearch" class="btn btn-primary ms-2">Search</button>
      </div>
  
      <!-- Results Table -->
      <table class="table table-striped" v-if="results && results.length > 0">
        <thead>
          <tr>
            <!-- Conditional headers based on role -->

            <template v-if="this.role === 'customer'">
              <th>Service Name</th>
              <th>Category</th>
              <th>Price</th>
              <th>Time Required</th>
              <th>Actions</th>
            </template>

            <template v-if="this.role === 'professional'">
              <th>Req. #</th>
              <th>Service Name</th>
              <th>Category</th>
              <th>Customer Name</th>
              <th>Address</th>
              <th>Pincode</th>
              <th>Date Booked</th>
              <th>Date Closed</th>
              <th>Status</th>
            </template>
            <template v-if ="this.role === 'admin'">
              <template v-if="searchType != 'status'">
                <th>Name</th>
                <th>Email</th>
                <th>Actions</th>
              </template>
              <template v-else>
                <th>ID</th>
                <th>Service Name</th>
                <th>Category</th>
                <th>Customer Name</th>
                <th>Assigned Professional</th>
                <th>Booked on</th>
                <th>Completed on</th>
                <th>Status</th>
              </template>
            </template>
          </tr>
        </thead>
        <tbody>
          <tr v-for="item in results" :key="item.id">
      
            <!-- Customer Role: Book Service Button to Open Modal -->
            <template v-if="this.role === 'customer'">
              <td>{{ item.name }}</td>
              <td>{{ item.category }}</td>
              <td>{{ item.price }}</td>
              <td>{{ item.time_required }}</td>
              <td>
                <button @click="openBookingModal(item)" class="btn btn-primary">Book Service</button>
              </td>
            </template>

            <!-- Professional Role: Show Service Requests -->
            <template v-if="this.role === 'professional'">
              <td>{{ item.id }}</td>
              <td>{{ item.service_name }}</td>
              <td>{{ item.category }}</td>
              <td>{{ item.customer_name }}</td>
              <td>{{ item.address }}</td>
              <td>{{ item.pincode }}</td>
              <td>{{ item.date_booked }}</td>
              <td>{{ item.date_closed }}</td>
              <td>{{ item.status }}</td>
            </template>
             
            <!-- Admin Role: Show Details -->
            <template v-if="this.role === 'admin'">
              <template v-if="searchType != 'status'">
                <!-- Show customer/professional Details with Delete Function -->
                <td>{{ item.name }}</td>
                <td>{{ item.email }}</td>
                <td>
                  <button @click="deleteUser(item.id, item.role)" class="btn btn-danger">Delete</button>
                </td>
              </template>
              <template v-else>
                <td>{{ item.id }}</td>
                <td>{{ item.service_name }}</td>
                <td>{{ item.category }}</td>
                <td>{{ item.customer_name }}</td>
                <td>{{ item.assigned_professional }}</td>
                <td>{{ item.date_booked }}</td>
                <td>{{ item.date_closed }}</td>
                <td>{{ item.status }}</td>
              </template>
            </template>
          </tr>
        </tbody>
      </table>
    
      <p v-if ="invalidSearch" class="text-muted"><i>Enter a valid search query.</i></p>
    
      <!-- Modal for Booking Service Request -->
    <div class="modal fade" id="bookServiceModal" tabindex="-1" aria-hidden="true">
      <div class="modal-dialog modal-lg">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">Book a Service</h5>
            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
          </div>
          <div class="modal-body">
            <BookServiceRequest 
              :serviceDetails="selectedService" 
              :customerDetails="user" 
              :rebooked=false
              v-if="isModalVisible" 
              @close="closeBookingModal"  
            />
          </div>
        </div>
      </div>
    </div>


    </div>
  </template>
  
  <script>
  import BookServiceRequest from '@/components/BookServiceRequest.vue';
  import userMixin from '@/mixins/userMixin';
  import NavBar from '@/components/NavBar.vue';
  export default {
    name: "SearchPage",
    components: {
      BookServiceRequest,
      NavBar
    },
    mixins: [userMixin],
    data() {
      return {
        searchType: '',
        searchQuery: '',
        results: [],
        isModalVisible: false,
        selectedService: null,
        searchOptions: [], // Options dynamically change based on role
        invalidSearch: false
      };
    },

    computed: {
        searchOptions() {
          if (this.role === 'customer') {
            return [
              { value: 'service_name', text: 'Service Name' },
              { value: 'location', text: 'Location' },
              { value: 'pincode', text: 'Pincode' },
            ];
          } else if (this.role === 'professional') {
            return [
              { value: 'date_booked', text: 'Date Booked(yyyy-mm-dd)' },
              { value: 'date_closed', text: 'Date Closed(yyyy-mm-dd)' },
              { value: 'location', text: 'Location' },
              { value: 'pincode', text: 'Pincode' },
              { value: 'status', text: 'Status(requested/accepted/completed/cancelled/rejected)' }
            ];
          } else if (this.role === 'admin') {
            return [
              { value: 'id', text: 'User ID' },
              { value: 'email', text: 'User Email' },
              { value: 'name', text: 'User Name' },
              { value: 'status', text: 'Service Request Status(requested/accepted/completed/cancelled/rejected)' },
            ];
          }
        }
    },
    methods: { 

  async performSearch() {
    this.invalidSearch = false;
    const formData = new FormData();
    formData.append('query', this.searchQuery);
    formData.append('type', this.searchType);

    if (this.role === 'customer') {
      await this.fetchCustomerResults(formData);
    } else if (this.role === 'professional') {
      await this.fetchProfessionalResults(formData);
    } else if (this.role === 'admin') {
      await this.fetchAdminResults(formData);
    }
  },

  async fetchCustomerResults(formData) {
    try {
      
      const response = await fetch('http://127.0.0.1:5000/search/customers', {
        method: 'POST',  
        headers: {
            'Authorization': `Bearer ${localStorage.getItem('access_token')}`
        },
        body: formData,  // Send the FormData object
      });
      const data = await response.json();
      this.results = data.results
    } catch (error) {
      console.error("Error fetching customer search results:", error);
    }
  },

  async fetchProfessionalResults(formData) {
    try {
      formData.append('user_id', this.user.id)
      const response = await fetch('http://127.0.0.1:5000/search/professionals', {
        method: 'POST',  
        headers: {
            'Authorization': `Bearer ${localStorage.getItem('access_token')}`
        },
        body: formData,  // Send the FormData object
      });
      const data = await response.json();
      this.results = data.results
    } catch (error) {
      console.error("Error fetching professional search results:", error);
    }
  },

  async fetchAdminResults(formData) {
    try {
      
      const response = await fetch('http://127.0.0.1:5000/search/admin', {
        method: 'POST',  
        headers: {
            'Authorization': `Bearer ${localStorage.getItem('access_token')}`
        },
        body: formData,  // Send the FormData object
      });
      const data = await response.json();
      console.log(data)
      if(!response.ok) {
        this.results = []
          this.invalidSearch = true
      }
      else{
          this.results = data.results
      }
      
    } catch (error) {
      console.error("Error fetching admin search results:", error);
    }
  },

      openBookingModal(service) {
        this.selectedService = service;
        this.isModalVisible = true;
        $('#bookServiceModal').modal('show'); 
      },
      closeBookingModal() {
      this.isModalVisible = false; 
      $('#bookServiceModal').modal('hide'); 
      this.selectedService = null;
    },
      async deleteUser(id, role) {
        try {
                url = (role==='customer')?`http://127.0.0.1:5000/customers/${id}`:`http://127.0.0.1:5000/professionals/${id}`
                const response = await fetch(url, 
                { 
                    method: 'DELETE',
                    headers: {
                     'Authorization': `Bearer ${localStorage.getItem('access_token')}`
                    }
                 });
                const data = await response.json();
                if (!response.ok) {
                    alert(data.error);
                }
                else{
                    alert(data.message);
                }
                this.performSearch();
            } catch (error) {
          console.error("Error deleting user:", error);
        }
      },
    },
  };
  </script>
  
  <style scoped>
  .search-box {
    display: flex;
    align-items: center;
    margin-bottom: 20px;
  }
  .search-box label {
    font-weight: bold;
  }
  </style>
  