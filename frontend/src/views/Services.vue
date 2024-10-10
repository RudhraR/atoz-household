<template>
  <div  class="container" style="margin-top: 20px;">
    <div class="card shadow">
      <div class="card-header">
        <h5>All Services 
        <button type="button" style="float:right;" class="btn btn-sm btn-success" data-bs-toggle="modal" data-bs-target="#addServiceModal">
        <i class="bi bi-plus-lg"></i> &nbsp; Add New Service
        </button></h5>
      </div>
      <div class="card-body">
        
      <!-- Table to display categories with their respective services -->
      <table class="table" >
      <thead>
        <tr>
          <th scope="col" style="width: 20%;" class="text-muted">Category</th>
          <th scope="col" style="width: 5%;">#</th>  
          <th scope="col" style="width: 20%;">Service Name</th>
          <th scope="col" style="width: 15%;">Price</th>
          <th scope="col" style="width: 20%;">Time Required</th>
          <th scope="col" style="width: 20%;">Actions</th>
        </tr>
        </thead>
        <tbody>
        <template v-if = "categoriesWithServices.length > 0 " 
          v-for="category in categoriesWithServices" :key="category.id">      
                 
                 <th class="text-muted">{{ category.name }}:</th>
                 <td></td>
                 <td></td>
                 <td></td>
                 <td></td>
                 
                 <tr v-for="(service, serviceIndex) in category.services" :key="service.id">
                   <td></td>
                   <td> {{ serviceIndex + 1 }}</td>
                   <td>{{ service.name }}</td>
                   <td>Rs. {{ service.price }}</td>
                   <td>{{ service.time_required }}</td>
                   <td class = "btn-group">
                    <button type="button" class="btn btn-sm btn-primary" @click="editService(service.id)">Edit</button>
                    <button type="button" class="btn btn-sm btn-danger" @click="deleteService(service.id)">Delete</button>
                  </td>
                 </tr>         
        </template>
        <template v-else>
          <tr>
            <td colspan="6" class="text-center">No Services Available</td>
          </tr>
        </template>
        </tbody>
      </table>
  </div></div>

   <!-- Modal for Adding New Service -->
   <div class="modal fade" id="addServiceModal" tabindex="-1" role="dialog" aria-labelledby="addServiceModalLabel" aria-hidden="true">
    <div class="modal-dialog" role="document">
      <div class="modal-content">
        <div class="modal-header">
          <h5 class="modal-title">Add New Service</h5>
            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
        </div>
        <div class="modal-body text-start">
          <div class="mb-3 row">
            <label for="serviceName" class="col-sm-3 col-form-label">Name</label>
            <div class="col-sm-9"><input class="form-control" v-model="serviceName" placeholder="Service Name" /></div>
          </div>
          <div class="mb-3 row">
            <label for="serviceDescription" class="col-sm-3 col-form-label">Description</label>
            <div class="col-sm-9"><input class="form-control" v-model="serviceDescription" placeholder="Description" /></div>
          </div>
          <div class="mb-3 row">
            <label for="servicePrice" class="col-sm-3 col-form-label">Price</label>
            <div class="col-sm-9"><input class="form-control" v-model="servicePrice" placeholder="Price" /></div>
          </div>
          <div class="mb-3 row">
            <label for="serviceTime" class="col-sm-4 col-form-label">Time Required</label>
            <div class="col-sm-8">
              <div class="row">
                <div class = "col-sm-6">
                <input v-model="timeValue" type="number" class="form-control" placeholder="Time Value" />
                </div>
                <div class = "col-sm-6">
                <select v-model="timeUnit" class="form-select">
                <option value="minutes">Minutes</option>
                <option value="hours">Hours</option>
              </select>
                </div>
              </div>
            </div>
          </div>
          <div class="mb-3 row">
            <label for="serviceCategory" class="col-sm-3 col-form-label">Category</label>
            <div class="col-sm-9">
              <select v-model="selectedCategoryId" class="form-select">

                <option v-for="category in categories" :key="category.id" :value="category.id">
                {{ category.name }}</option>
             </select>
            </div>
          </div>
    </div>
        <div class="modal-footer">
          <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
          <button type="button" class="btn btn-primary" @click="addService">Add Service</button>
        </div>
      </div>
    </div>
  </div>  
</div>
</template>

<script>
import userMixin from '@/mixins/userMixin';
export default {
  name: 'Services',
  mixins: [userMixin],
  data() {
    return {
      showServiceModal: false,  // To control the visibility of the Add Service modal
      services: [],
      serviceName: '',
      serviceDescription: '',
      servicePrice: 0,
      timeValue: 0,  // Time value (numeric)
      timeUnit: 'minutes',  // Time unit (minutes or hours)
      categories: [],
      selectedCategoryId: null
    };
  },
  mounted() {
    this.fetchServices();
    this.fetchCategories();
  },
  computed: {
    // Group services by category
    categoriesWithServices() {
      const categoriesWithServices = [];
      for (let categoryId in this.categories) {
        const category = this.categories[categoryId];
        const servicesInCategory = this.services.filter(service => service.category_id == category.id);
        if (servicesInCategory.length > 0) {
          categoriesWithServices.push({
          ...category,
          services: servicesInCategory });
        }
      }
      return categoriesWithServices;
    }
  },
  methods: {
    async fetchServices() {
      const response = await fetch('http://127.0.0.1:5000/services',
        {
          method: 'GET',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${localStorage.getItem('access_token')}`
          }
        }
      );
      const data = await response.json();
      if (!response.ok) {
        alert(data.error);
      }
      else {
        this.services = data.services;
      }
      console.log("Services: ", this.services);
    },
    async fetchCategories() {
      const response = await fetch('http://127.0.0.1:5000/categories', {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${localStorage.getItem('access_token')}`
        }
      });
      const data = await response.json();
      if (!response.ok) {
        alert(data.error);
      }
      else {
        this.categories = data.categories;
        console.log(this.categories)
      }
    },
  async addService() {
    if (this.serviceName && this.serviceDescription && this.servicePrice && this.timeValue && this.selectedCategoryId) {
      try {
        const newService = {
          name: this.serviceName,
          description: this.serviceDescription,
          price: this.servicePrice,
          time_required: `${this.timeValue} ${this.timeUnit}`,
          category_id: this.selectedCategoryId
        };

        const response = await fetch('http://127.0.0.1:5000/services', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${localStorage.getItem('access_token')}`
          },
          body: JSON.stringify(newService)
        });

        if (response.ok) {
          this.fetchServices();
          this.resetForm();
          $('#addServiceModal').modal('hide'); // Close the modal
        } else {
          console.error('Error adding service:', response.statusText);
        }
      } catch (error) {
        console.error('Error adding service:', error);
      }
    } else {
      alert("Please fill out all fields.");
    }
  },
    async deleteService(id) {
      const response = await fetch(`http://127.0.0.1:5000/services/${id}`, { 
        method: 'DELETE' ,
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('access_token')}`
        }
      });
      const data = await response.json();
      if (!response.ok) {
        alert(data.error);
      }
      else {
        this.fetchServices();
      }
    },
    resetForm() {
      this.serviceName = '';
      this.serviceDescription = '';
      this.servicePrice = 0;
      this.timeValue = 0;
      this.timeUnit = 'minutes';
      this.selectedCategoryId = null;
    }
  },
  
};

</script>

<style scoped>

</style>
