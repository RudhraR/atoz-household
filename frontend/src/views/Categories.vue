<template>
  <div class="container" style="margin-top: 20px;">
    <div class="card shadow">
      <h5 class="card-header">All Categories</h5>
      <div class="card-body">
        <div class="row">
          <div class="col-6">
            <input v-model="categoryName" placeholder="Category Name" required />
          </div>
          <div class="col-6">
            <button @click="addCategory" class="btn btn-sm btn-success">
              Add Category
            </button>
          </div>
        </div>
        <br />

        <table class="table">
          <thead>
            <tr>
              <th scope="col">#</th>
              <th scope="col">Category Name</th>
              <th scope="col" v-if="role == 'admin'">Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(category, index) in categories" :key="category.id">
              <th scope="row">{{ index + 1 }}</th>
              <td>
                <a @click="setCurrentCategory(category)" style="cursor: pointer;" class="text-secondary"
                data-bs-toggle="modal" data-bs-target="#viewCategoryModal">
                  {{ category.name }}</a>
              </td>
              <td v-if="role == 'admin'" class="btn-group">
                <button type="button" class="btn btn-sm btn-primary" 
                        data-bs-toggle="modal" 
                        data-bs-target="#editCategoryModal"
                        @click="setCurrentCategory(category)">
                  Edit
                </button>
                <button type="button" class="btn btn-sm btn-danger" @click="deleteCategory(category.id)">
                  Delete
                </button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- Bootstrap Modal for Editing Category -->
    <div class="modal fade" id="editCategoryModal" tabindex="-1" aria-labelledby="editCategoryModalLabel" aria-hidden="true">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title" id="editCategoryModalLabel">Edit Category</h5>
            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
          </div>
          <div class="modal-body">
            <input v-model="currentCategoryName" class="form-control" placeholder="Category Name" />
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
            <button type="button" class="btn btn-primary" @click="updateCategory">Save changes</button>
          </div>
        </div>
      </div>
    </div>

    <!-- Bootstrap Modal for viewing Category details-->
    <div class="modal fade" id="viewCategoryModal" tabindex="-1" aria-labelledby="viewCategoryModalLabel" aria-hidden="true">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title" id="viewCategoryModalLabel">Category Details</h5>
            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
          </div>
          <div class="modal-body">
            <div style="float:left"><strong>Name:</strong> {{ currentCategoryName }}</div><br><br>
            <div style="float:left"><strong>Available Services:</strong></div><br>
            <div style="float:left">
            <ul>
              <li v-for="service in currentCategoryServices" :key="service.id">
                {{service.name.trim()}}
              </li>
            </ul></div>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
          </div>
        </div>
      </div>
    </div>


  </div>
</template>

<script>
import NavBar from '@/components/NavBar.vue';
import userMixin from '@/mixins/userMixin';

export default {
  name: 'Categories',
  mixins: [userMixin],
  components: {
    NavBar
  },
  data() {
    return {
      categories: [],
      categoryName: '',
      currentCategoryId: null,
      currentCategoryName: '',
      currentCategoryServices: [],};
  },
  methods: {
    async fetchCategories() {
      const response = await fetch('http://127.0.0.1:5000/categories');
      const data = await response.json();

      if (!response.ok) {
        alert(data.error);
      } else {
        this.categories = data.categories;        
      }
    },
    async addCategory() {
      if (!this.categoryName) return;

      await fetch('http://127.0.0.1:5000/categories', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${localStorage.getItem('access_token')}`
        },
        body: JSON.stringify({ name: this.categoryName })
      });
      this.categoryName = '';
      this.fetchCategories();
    },
    async deleteCategory(id) {
      await fetch(`http://127.0.0.1:5000/categories/${id}`, {
        method: 'DELETE',
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('access_token')}`
        }
      });
      this.fetchCategories();
    },
    async setCurrentCategory(category) {
      
      this.currentCategoryId = category.id;
      this.currentCategoryName = category.name; 
      const data = await fetch(`http://127.0.0.1:5000/categories/${category.id}/services`).then(response => response.json());
      this.currentCategoryServices = data.services;
      console.log(this.currentCategoryId, this.currentCategoryName, this.currentCategoryServices);
    },
    async updateCategory() {
      if (!this.currentCategoryName) return;

      await fetch(`http://127.0.0.1:5000/categories/${this.currentCategoryId}`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${localStorage.getItem('access_token')}`
        },
        body: JSON.stringify({ name: this.currentCategoryName })
      });

       // Close the modal programmatically after saving
       const modalElement = document.getElementById('editCategoryModal');
      const modal = bootstrap.Modal.getInstance(modalElement); // Get the modal instance
      modal.hide(); // Hide the modal

      // Fetch categories again to refresh the list
      this.fetchCategories();
    }
  },
  mounted() {
    this.fetchCategories();
  }
};
</script>

<style scoped>
/* Add any custom styles if necessary */
</style>
