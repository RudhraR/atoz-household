<template>
    <div class="modal fade show" tabindex="-1" role="dialog"  aria-labelledby="serviceModalLabel" aria-modal="true">
      <div class="modal-dialog" role="document">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">
              {{ mode === 'add' ? 'Add New Service' : (mode === 'edit' ? 'Edit Service' : 'Service Details') }}
            </h5>
            <button type="button" class="btn-close" @click="$emit('close')"></button>
          </div>
          <div class="modal-body">
            <form @submit.prevent="handleSubmit">
              <div class="form-group mb-3 row">
                <label for="serviceName" class="col-sm-3 col-form-label">Name</label>
                <div class="col-sm-9">
                  <input type="text" class="form-control" id="serviceName" v-model="service.name"
                  :readonly="mode === 'view'" placeholder="Service Name" required/>
                </div>
              </div>
              <div class="form-group mb-3 row">
                <label for="serviceDescription" class="col-sm-3 col-form-label">Description</label>
                <div class="col-sm-9">
                  <input class="form-control" id="serviceDescription" v-model="service.description" 
                  :readonly="mode === 'view'" placeholder="Description" required/>
                </div>                
              </div>
              <div class="form-group mb-3 row">
                <label for="servicePrice" class="col-sm-3 col-form-label">Price</label>
                <div class="col-sm-9">
                  <input type="number" class="form-control" id="servicePrice" max="10000"
                  v-model.number="service.price" :readonly="mode === 'view'" required />
                </div>
              </div>
              <div class="form-group mb-3 row">
                <label for="timeRequired" class="col-sm-4 col-form-label">Time Required</label>
                <div class="col-sm-8">
                  <div class="row">
                    <div class = "col-sm-6">
                      <input type="number" class="form-control" id="timeValue" v-model.number="timeValue"
                    :readonly="mode === 'view'" required />
                    </div>
                    <div class = "col-sm-6">
                      <select class="form-select" v-model="timeUnit" :disabled="mode === 'view'" required >
                        <option value="minutes">Minutes</option>
                        <option value="hours">Hours</option>
                      </select>
                    </div></div>
              </div></div>
              <div class="form-group mb-3 row">
                <label for="categorySelect" class="col-sm-3 col-form-label">Category</label>
                <div class="col-sm-9">
                <select id="categorySelect" class="form-control" v-model="service.category_id"
                  :disabled="mode === 'view'" required>
                  <option value="" disabled>Select a category</option>
                  <option v-for="category in categories" :key="category.id" :value="category.id">
                    {{ category.name }}
                  </option>
                </select></div>
              </div>
              <div class="modal-footer">
                <button type="button" class="btn btn-secondary" @click="$emit('close')">Close</button>
                <button type="submit" class="btn btn-primary" v-if="mode === 'add' || mode === 'edit'">
                  <span v-if="mode === 'add'">Add Service</span>
                  <span v-else>Edit Service</span>
                </button>
                <button type="submit" class="btn btn-primary" v-else-if="mode === 'view' && user.role === 'customer'">
                  Book service
              </button>
              </div>
            </form>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script>
 
  export default {
    name: 'ServiceModal',
    props: {
      service: {
        type: Object,
        required: true,
      },
      mode: {
        type: String,
        required: true, // can be 'add', 'edit', or 'view'
      },
      categories: {
        type: Array,
        required: true,
      },
      user: {
        type: Object,
        required: true,
      }
    },
    data() {
      return {
        
        timeValue: this.service.time_required ? this.service.time_required.split(" ")[0] : 0, // Initialize time value
        timeUnit: this.service.time_required ? this.service.time_required.split(" ")[1] : 'minutes', // Initialize time unit
      };
    },
    methods: {
      handleSubmit() {
        // Prepare the service data to emit
        const serviceData = {
          ...this.service,
          time_required: `${this.timeValue} ${this.timeUnit}`, // Combine time value and unit
        };
        this.$emit('save', serviceData); // Emit save event with the service data
      },
    },
    watch: {
      service: {
        handler(newService) {
          if (this.mode === 'edit' || this.mode === 'view') {
            this.timeValue = newService.time_required.split(" ")[0];
            this.timeUnit = newService.time_required.split(" ")[1];
            
          } else {
            // Reset timeValue and timeUnit for add mode
            this.timeValue = 0;
            this.timeUnit = 'minutes';
            
          }
        },
        immediate: true,
      },
    },
  };
  </script>
  
  <style scoped>
 .modal {
  display: none; /* Prevent direct block display */
  background: rgba(0, 0, 0, 0.5);
}
.show {
  display: block !important; /* Ensure modal is visible when 'show' class is added */
}
  
  </style>
  