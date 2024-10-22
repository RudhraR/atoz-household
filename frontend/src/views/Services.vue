<template>
  <div class="container" style="margin-top: 20px;">
    <div class="card shadow">
      <div class="card-header">
        <h5>
          All Services 
          <button type="button" style="float:right;" class="btn btn-sm btn-success" @click="openModal('add')">
            <i class="bi bi-plus-lg"></i> &nbsp; Add New Service
          </button>
        </h5>
      </div>
      <div class="card-body">
        <table class="table">
          <thead>
            <tr>
              <th>Category </th>
              <th>Service Name</th>
              <th>Price</th>
              <th>Time Required</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            <template v-for="(category, index) in categoriesWithServices" :key="category.id">
              <tr>
                <th>{{ category.name }}:</th>
                <td></td>
                <td></td>
                <td></td>
                <td></td>
              </tr>
              <tr v-for="(service, serviceIndex) in category.services" :key="service.id">
                <td>{{ serviceIndex + 1 }}</td>
                <td><a @click="openModal('view', service)" style="cursor: pointer; " class="text-secondary">
                  {{ service.name }}</a></td>
                <td>{{ service.price }}</td>
                <td>{{ service.time_required }}</td>
                <td class="btn-group">
                  <button class="btn btn-primary btn-sm" @click="openModal('edit', service)">Edit</button>
                  <!-- <button class="btn btn-secondary btn-sm" @click="openModal('view', service)">Details</button> -->
                  <button class="btn btn-danger btn-sm" @click="deleteService(service.id)">Delete</button>
                </td>
              </tr>
            </template>
          </tbody>
        </table>
      </div>
    </div>

    <!-- Reusable Modal for Add/Edit/View -->
    <ServiceModal
      v-if="isModalVisible"
      :service="selectedService"
      :mode="modalMode"
      :user="this.user"
      @close="isModalVisible = false"
      @save="saveService"
      :categories="categories"  
    />
  </div>
</template>

<script>
import ServiceModal from '@/components/ServiceModal.vue' // Import the reusable modal component
import userMixin from '@/mixins/userMixin';
export default {
  mixins: [userMixin],
  components: {
    ServiceModal,
  },
  data() {
    return {
      isModalVisible: false,
      selectedService: {
      name: '',
      description: '',
      price: 0,
      category_id: null,
      time_value: 0, // Initialize time value for new service
      time_unit: 'minutes', // Initialize time unit for new service
    },
      modalMode: 'add', // 'add', 'edit', or 'view'
      services: [],
      categories: [],
    };
  },
  computed: {
    categoriesWithServices() {
      const categoriesWithServices = [];
      for (let categoryId in this.categories) {
        const category = this.categories[categoryId];
        const servicesInCategory = this.services.filter(service => service.category_id == category.id);
        if (servicesInCategory.length > 0) {
          categoriesWithServices.push({ ...category, services: servicesInCategory });
        }
      }
      return categoriesWithServices;
    }
  },
  mounted() {
    this.fetchServices();
    this.fetchCategories();
  },
  methods: {
    openModal(mode, service = null) {
      this.modalMode = mode;
      if (mode === 'edit' || mode === 'view') {
        this.selectedService = { ...service }; // Clone the service object to avoid mutating the original one
      } else {
        this.selectedService = {
        name: '',
        description: '',
        price: 0,
        category_id: null,
        time_value: 0, // Reset for new service
        time_unit: 'minutes', // Reset for new service
      };
      }
      this.isModalVisible = true; // Show the modal
    },
    async fetchServices() {
      const response = await fetch('http://127.0.0.1:5000/services', {
        method: 'GET',
        headers: { 'Content-Type': 'application/json', 'Authorization': `Bearer ${localStorage.getItem('access_token')}` }
      });
      const data = await response.json();
      if (response.ok) {
        this.services = data.services;
      }
    },
    async fetchCategories() {
      const response = await fetch('http://127.0.0.1:5000/categories', {
        method: 'GET',
        headers: { 'Content-Type': 'application/json', 'Authorization': `Bearer ${localStorage.getItem('access_token')}` }
      });
      const data = await response.json();
      if (response.ok) {
        this.categories = data.categories;
      }
    },
    async saveService(serviceData) {
      if (this.modalMode === 'add') {
        await this.addService(serviceData);
      } else if (this.modalMode === 'edit') {
        await this.updateService(serviceData);
      }
      this.isModalVisible = false; // Hide modal after saving
    },
    async addService(serviceData) {
      const response = await fetch('http://127.0.0.1:5000/services', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', 'Authorization': `Bearer ${localStorage.getItem('access_token')}` },
        body: JSON.stringify(serviceData)
      });
      if (response.ok) {
        this.fetchServices(); // Refresh services list
      }
    },
    async updateService(serviceData) {
      const response = await fetch(`http://127.0.0.1:5000/services/${serviceData.id}`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json', 'Authorization': `Bearer ${localStorage.getItem('access_token')}` },
        body: JSON.stringify(serviceData)
      });
      if (response.ok) {
        this.fetchServices(); // Refresh services list
      }
    },
    async deleteService(id) {
      const response = await fetch(`http://127.0.0.1:5000/services/${id}`, {
        method: 'DELETE',
        headers: { 'Authorization': `Bearer ${localStorage.getItem('access_token')}` }
      });
      if (response.ok) {
        this.fetchServices(); // Refresh services list
      }
    },
  },
};
</script>

<style scoped>
/* Add your styles here */
</style>
