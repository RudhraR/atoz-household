<template>
    <div>
      <div v-if= "user">
      <br><h5 style="text-align: left;">
        <i>&nbsp; Welcome, {{ this.user.username }}! Explore all our services. </i>
      </h5><br> </div>
      <div class="container">
        <div  v-for="(category) in categoriesWithServices" :key="category.id">
      <!-- Loop through each category -->
        <!-- Category Card -->
        <div class="card" v-if="category.services.length > 0">
          <h5 class="card-header text-white bg-secondary">{{ category.name }}</h5>
          <div class="card-body">
            <div class="row">
            <!-- Loop through services under each category -->
            <div v-for="service in category.services" :key="service.id" class="col-sm-2">
              <div class="card"  style="cursor: pointer;" @click="openModal('view', service)">
                <img class="card-img-top" src="../assets/default_image.jpg" >
              <div class="card-body">
                <h6 class="card-title">{{ service.name }}</h6>
                <p class="card-text">Price: ${{ service.price }}</p>
                <p class="card-text text-muted small"><i>Click to book service</i></p>
              </div>
            </div>
          </div>
          
        </div>
      </div>
    </div>
    </div>
  </div>
  
  <service-modal
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
import userMixin from '@/mixins/userMixin';
import ServiceModal from '@/components/ServiceModal.vue'
  export default {
    name: 'Category_Services',
    mixins: [userMixin],
    components: {
      ServiceModal
    },
    data() {
    return {
      services: [],
      categories: [],
      isModalVisible: false,
      selectedService: {
      name: '',
      description: '',
      price: 0,
      category_id: null,
      time_value: 0, // Initialize time value for new service
      time_unit: 'minutes', // Initialize time unit for new service
    },
      modalMode:'view'
    };
  },
  computed: {
    // Group services by category
    categoriesWithServices() {
      const categoriesWithServices = [];

      // Loop over each category and gather services that belong to it
      this.categories.forEach(category => {
        const servicesInCategory = this.services.filter(service => service.category_id === category.id);

        // Push category with its services into the final array
        categoriesWithServices.push({
          ...category,
          services: servicesInCategory
        });
      });

      return categoriesWithServices;
    }
  },
  created() {
    this.fetchCategories();
    this.fetchServices();
  },
  methods: {
    async fetchCategories() {
      const response = await fetch('http://127.0.0.1:5000/categories', {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${localStorage.getItem('access_token')}`
        }
      });
        const data = await response.json()
        
        if (!response.ok) {
            alert(data.error)
        }
        else {
        this.categories = data.categories
        }
    },
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
    },

    openModal(mode, service = null) {
      this.modalMode = mode;
      this.selectedService = { ...service }; // Clone the service object to avoid mutating the original one
      this.isModalVisible = true; // Show the modal
    }
  } 
  };
  </script>
  
  <style scoped>
  </style>
  