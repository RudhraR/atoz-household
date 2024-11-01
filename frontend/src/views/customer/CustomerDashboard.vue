<template>
  <div>
    <div v-if="user">
      <br>
      <h5 style="text-align: left;">
        <i>&nbsp; Welcome, {{ user.username }}! </i>
      </h5><br>
    </div>
    <div class="container">
      <!-- Loop through each category -->
      <div class="card shadow border-dark">
        <h5 class="card-header text-white bg-secondary">Looking for?</h5>
        <div class="card-body">
          <div class="row">
            <div v-for="category in categoriesWithServices" :key="category.id" class="col-sm-2">
              <div class="card" @click="setCurrentCategory(category)" style="cursor: pointer;" data-bs-toggle="modal"
                data-bs-target="#viewCategoryModal">
                <img class="card-img-top" :src="category.imagePath" width="100" height="150">
                <div class="card-body">
                  <h6 class="card-title">{{ category.name }}</h6>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Bootstrap Modal for viewing Category details-->
    <div class="modal fade" id="viewCategoryModal" tabindex="-1" aria-hidden="true">
      <div class="modal-dialog modal-lg">
        <div class="modal-content">
          <div class="modal-header" style="text-align: center; width: 100%;">
            <h5 class="modal-title">Available services in this category</h5>
            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
          </div>
          <div class="modal-body">
            <div class="row" v-if="currentCategoryServices.length > 0">
              <div v-for="service in currentCategoryServices" :key="service.id" class="col-sm-4">
                <div class="card">
                  <h5 class="card-header">{{ service.name }}</h5>
                  <div class="card-body">
                    <p class="card-text"><b>Price: </b> 
                      <i class="text-muted">Rs.{{ service.price }}</i></p>
                    <p class="card-text"><b>Time Required:</b> <br>
                      <i class="text-muted">{{ service.time_required }} </i></p>
                  </div>
                  <div class="card-footer">
                    <!-- Change: Updated click event to openBookingModal method -->
                    <button class="btn btn-primary" @click="openBookingModal(service)">Book Service</button>
                  </div>
                </div>
              </div>
            </div>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
          </div>
        </div>
      </div>
    </div>

    <!-- Change: New modal for Booking Service Request -->
    <div class="modal fade" id="bookServiceModal" tabindex="-1" aria-hidden="true">
      <div class="modal-dialog modal-lg">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">Book a Service</h5>
            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
          </div>
          <div class="modal-body">
            <BookServiceRequest 
              :serviceDetails="currentService" 
              :customerDetails="user" 
              v-if="isModalVisible" 
              @close="closeBookingModal"  
            />
          </div>
        </div>
      </div>
    </div>

    <br><br>
    <div class="container" v-if="user">
      <div class="card shadow">
        <h5 class="card-header bg-dark text-white" style="text-align: left;">Service History</h5>
        <div class="card-body">
      <ViewServiceRequests />
      </div>
      </div>
    </div>
    
  </div>
</template>

<script>
import userMixin from '@/mixins/userMixin';
import BookServiceRequest from './BookServiceRequest.vue';
import ViewServiceRequests from '@/components/ViewServiceRequests.vue';

export default {
  name: 'CustomerDashboard',
  mixins: [userMixin],
  components: {
    BookServiceRequest,
    ViewServiceRequests
  },
  data() {
    return {
      currentCategoryServices: [],
      categories: [],
      currentCategory: [],
      currentService: null, // To store the currently selected service
      isModalVisible: false, // State to control modal visibility
    };
  },
  computed: {
    // Computed property to filter categories with services
    categoriesWithServices() {
      return this.categories.filter(category => category.services && category.services.length > 0);
    }
  },
  async mounted() {
    await this.fetchCategories();
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
      } else {
        this.categories = data.categories.map(category => ({
          ...category,
          imagePath: `http://127.0.0.1:5000/images/${category.categoryImage}`
        }));
        console.log(this.categories)
      }
    },

    async setCurrentCategory(category) {
      this.currentCategory = category.name;
      try {
        const response = await fetch(`http://127.0.0.1:5000/categories/${category.id}/services`, {
          method: 'GET',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${localStorage.getItem('access_token')}`
          }
        });
        const data = await response.json();
        this.currentCategoryServices = data.services;
      }
      catch (error) {
        alert(error)
      }
    },

    openBookingModal(service) {
      this.currentService = service; // Set the selected service
      this.isModalVisible = true; // Open the booking modal
      $('#viewCategoryModal').modal('hide');
      $('#bookServiceModal').modal('show'); 
    },

    closeBookingModal() {
      this.isModalVisible = false; 
      $('#bookServiceModal').modal('hide'); 
      this.currentService = null;
      this.$router.go(0);
    },
  }
};
</script>

<style scoped></style>
