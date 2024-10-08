<template>
    <div>
      <h1>Manage Services</h1>
      <input v-model="serviceName" placeholder="Service Name" />
      <input v-model="serviceDescription" placeholder="Description" />
      <input v-model.number="servicePrice" type="number" placeholder="Price" />
      
      <!-- Time Required -->
      <input v-model.number="timeValue" type="number" placeholder="Time Value" />
      <select v-model="timeUnit">
        <option value="minutes">Minutes</option>
        <option value="hours">Hours</option>
      </select>
      
      <select v-model="selectedCategoryId">
        <option v-for="category in categories" :key="category.id" :value="category.id">
          {{ category.name }}
        </option>
      </select>
      
      <button @click="addService">Add Service</button>
  
      <ul>
        <li v-for="service in services" :key="service.id">
          {{ service.name }} - {{ service.description }} - ${{ service.price }} - 
          {{ service.time_value }} {{ service.time_unit }}
          <button @click="deleteService(service.id)">Delete</button>
        </li>
      </ul>
    </div>
  </template>
  
  <script>
  export default {
    data() {
      return {
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
    methods: {
      async fetchServices() {
        const response = await fetch('/services');
        this.services = await response.json();
      },
      async fetchCategories() {
        const response = await fetch('/categories');
        this.categories = await response.json();
      },
      async addService() {
        await fetch('/services', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({
            name: this.serviceName,
            description: this.serviceDescription,
            price: this.servicePrice,
            time_value: this.timeValue,
            time_unit: this.timeUnit,
            category_id: this.selectedCategoryId
          })
        });
        this.resetForm();
        this.fetchServices();
      },
      async deleteService(id) {
        await fetch(`/services/${id}`, { method: 'DELETE' });
        this.fetchServices();
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
    mounted() {
      this.fetchServices();
      this.fetchCategories();
    }
  };
  </script>
  