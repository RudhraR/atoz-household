<template>
    <NavBar />
    <div v-if="this.role" class="container mt-5">
      <!-- Search Input Section -->
      <div class="search-box d-flex align-items-center mb-3">
        <label class="me-2 flex-shrink-0">Search by:</label>
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
      <table class="table table-striped" v-if="results.length > 0">
        <thead>
          <tr>
            <!-- Conditional headers based on role -->
            <th v-if="this.role === 'customer'">Service Name</th>
            <th v-if="this.role === 'customer'">Category</th>
            <th v-if="this.role === 'customer'">Book Service</th>
  
            <th v-if="this.role === 'professional'">Service Request</th>
            <th v-if="this.role === 'professional'">Date Booked</th>
            <th v-if="this.role === 'professional'">Date Closed</th>
  
            <th v-if="this.role === 'admin'">Name</th>
            <th v-if="this.role === 'admin'">Email</th>
            <th v-if="this.role === 'admin'">Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="item in results" :key="item.id">
            <!-- Customer Role: Book Service Button to Open Modal -->
            <td v-if="this.role === 'customer'">{{ item.service_name }}</td>
            <td v-if="this.role === 'customer'">{{ item.category }}</td>
            <td v-if="this.role === 'customer'">
              <button @click="openBookingModal(item)" class="btn btn-primary">Book Service</button>
            </td>
  
            <!-- Professional Role: Show Service Requests -->
            <td v-if="this.role === 'professional'">{{ item.service_request }}</td>
            <td v-if="this.role === 'professional'">{{ item.date_booked }}</td>
            <td v-if="this.role === 'professional'">{{ item.date_closed }}</td>
  
            <!-- Admin Role: Show Details with Delete Function -->
            <td v-if="this.role === 'admin'">{{ item.name }}</td>
            <td v-if="this.role === 'admin'">{{ item.email }}</td>
            <td v-if="this.role === 'admin'">
              <button @click="deleteUser(item.id, item.role)" class="btn btn-danger">Delete</button>
            </td>
          </tr>
        </tbody>
      </table>
  
      <p v-if ="invalidSearch" class="text-muted"><i>Enter a valid search query.</i></p>
      <!-- Book Service Modal -->
      <BookServiceRequest v-if="isModalOpen" :service="selectedService" @close="isModalOpen = false" />
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
        isModalOpen: false,
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
              { value: 'date_booked', text: 'Date Booked' },
              { value: 'date_closed', text: 'Date Closed' },
              { value: 'location', text: 'Location' },
              { value: 'pincode', text: 'Pincode' },
            ];
          } else if (this.role === 'admin') {
            return [
              { value: 'id', text: 'User ID' },
              { value: 'email', text: 'User Email' },
              { value: 'name', text: 'User Name' },
              { value: 'status', text: 'Service Request Status' },
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
            Authorization: "Bearer " + localStorage.getItem("access_token")
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
      
      const response = await fetch('http://127.0.0.1:5000/search/professionals', {
        method: 'POST',  
        headers: {
            Authorization: "Bearer " + localStorage.getItem("access_token")
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
            Authorization: `Bearer  + localStorage.getItem("access_token")`
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
        this.isModalOpen = true;
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
  