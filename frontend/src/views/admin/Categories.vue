<template>
  <div class="container" style="margin-top: 20px;">
    <div class="card shadow">
      <h5 class="card-header">All Categories
        <button @click="addCategory" style="float:right;" class="btn btn-sm btn-success" 
            data-bs-toggle="modal" data-bs-target="#addCategoryModal">
            <i class="bi bi-plus-lg"></i> &nbsp;Add Category
            </button>
      </h5>
      <div class="card-body">
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
                <button type="button" class="btn btn-sm btn-primary" data-bs-toggle="modal"
                  data-bs-target="#editCategoryModal" @click="setCurrentCategory(category)">
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
    
    <!-- Bootstrap Modal for adding Category -->
    <div class="modal fade" id="addCategoryModal" tabindex="-1" aria-hidden="true">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">Add Category</h5>
            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
          </div>
          <div class="modal-body">
            <div class="form-group mb-3 row">
              <label for="categoryName" class="col-sm-3 col-form-label">Category Name</label>
              <div class="col-sm-9">
                <input v-model="categoryName" class="form-control" placeholder="Category Name" />
              </div>
            </div>
            <div class="form-group mb-3 row">
              <label for="categoryImage" class="col-sm-3 col-form-label">Category Image</label>
              <div class="col-sm-9">
                <input type="file" id="categoryImage" class="form-control" accept=".jpg" @change="handleImageUpload"
                  required />
              </div>
            </div>
            <div class="modal-footer">
              <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
              <button type="button" class="btn btn-success" @click="addCategory">Add category</button>
            </div>
          </div>
        </div>
      </div>
      </div>

      <!-- Bootstrap Modal for Editing Category -->
      <div class="modal fade" id="editCategoryModal" tabindex="-1" aria-labelledby="editCategoryModalLabel"
        aria-hidden="true">
        <div class="modal-dialog">
          <div class="modal-content">
            <div class="modal-header">
              <h5 class="modal-title" id="editCategoryModalLabel">Edit Category</h5>
              <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
            </div>
            <div class="modal-body">              
              <div class="form-group mb-3 row">
              <label for="currentCategoryName" class="col-sm-3 col-form-label">Category Name</label>
              <div class="col-sm-9">
                <input v-model="currentCategoryName" class="form-control" placeholder="Category Name" />
              </div>
            </div>
            <div class="form-group mb-3 row">
              <label for="currentCategoryImage" class="col-sm-3 col-form-label">Category Image</label>
              <div class="col-sm-9">
                <input type="file" id="currentCategoryImage" class="form-control" accept=".jpg" 
                @change="handleImageUpload" />
                <i class="text-muted">Current image: 
                  <span v-if="currentCategoryImagePath">
                  <img :src="currentCategoryImagePath" width="50" height="50">
                </span>
                <span v-else>
                  Default image
                </span>

                </i>
              </div>
            </div>
            </div>
            <div class="modal-footer">
              <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
              <button type="button" class="btn btn-primary" @click="updateCategory">Save changes</button>
            </div>
          </div>
        </div>
      </div>

      <!-- Bootstrap Modal for viewing Category details-->
      <div class="modal fade" id="viewCategoryModal" tabindex="-1" aria-labelledby="viewCategoryModalLabel"
        aria-hidden="true">
        <div class="modal-dialog">
          <div class="modal-content">
            <div class="modal-header">
              <h5 class="modal-title" id="viewCategoryModalLabel">Category Details</h5>
              <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
            </div>
            <div class="modal-body">
              <div style="float:left"><strong>Name:</strong> {{ currentCategoryName }}</div><br><br>
              <div style="float:left"><strong>Image:</strong> &nbsp;
                <span v-if="currentCategoryImage">
                  <img :src="currentCategoryImagePath" width="50" height="50">
                </span>
                <span v-else>
                  <i>None. Default image will be shown</i>
                </span>
                </div><br><br><br>
              <div style="float:left"><strong>Available Services:</strong></div><br>
              <div style="float:left" v-if="currentCategoryServices.length > 0">
                <ul>
                  <li v-for="service in currentCategoryServices" :key="service.id">
                    {{ service.name.trim() }}
                  </li>
                </ul>
              </div>
              <div style="float:left" class="text-muted" v-else>
                <i>None</i>
              </div>
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
      categoryImage: null,
      currentCategory: [],
      currentCategoryId: null,
      currentCategoryName: '',
      currentCategoryImage: null,
      currentCategoryImagePath: null,
      currentCategoryServices: [],
    };
  },
  methods: {
    async handleImageUpload(event) {
      console.log(event.target.files[0])
      this.categoryImage = event.target.files[0];
      this.currentCategoryImage = event.target.files[0];

    },
    async fetchCategories() {
      const response = await fetch('http://127.0.0.1:5000/categories', {
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('access_token')}`
        }
      });
      const data = await response.json();

      if (!response.ok) {
        alert(data.error);
      } else {
        this.categories = data.categories.map(category => ({
    ...category,
    imagePath: `http://127.0.0.1:5000/images/${category.categoryImage}`
}));
      }
    },
    async addCategory() {
      if (!this.categoryName) return;
      try{
        const formData = new FormData();
        formData.append('categoryImage', this.categoryImage);
        formData.append('name', this.categoryName);
        const response = await fetch('http://127.0.0.1:5000/categories', {
          method: 'POST',
          headers: {
            'Authorization': `Bearer ${localStorage.getItem('access_token')}`
          },
          body: formData
        });
        const data = await response.json();
        if (!response.ok) {
          alert(data.error);
        } else {
          this.categoryName = '';
          this.categoryImage = null;
          // Close the modal programmatically after saving
          const modalElement = document.getElementById('addCategoryModal');
          const modal = bootstrap.Modal.getInstance(modalElement); // Get the modal instance
          modal.hide(); // Hide the modal

          this.fetchCategories();
        }
      } catch (error) {
        console.log(error);
      }
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
      this.currentCategoryImage = category.categoryImage
      this.currentCategoryImagePath = category.imagePath
      const data = await fetch(`http://127.0.0.1:5000/categories/${category.id}/services`).then(response => response.json());
      this.currentCategoryServices = data.services;
      console.log(this.currentCategoryId, this.currentCategoryName, this.currentCategoryImage, this.currentCategoryServices);
    },
    async updateCategory() {
      if (!this.currentCategoryName) return;
      const formData = new FormData();
      formData.append('categoryImage', this.currentCategoryImage);
      formData.append('name', this.currentCategoryName);
      await fetch(`http://127.0.0.1:5000/categories/${this.currentCategoryId}`, {
        method: 'PUT',
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('access_token')}`
        },
        body: formData
      });

      // Close the modal programmatically after saving
      
      this.currentCategoryImage = null;
      this.currentCategoryName = '';
      this.currentCategoryImagePath = null;
      const modalElement = document.getElementById('editCategoryModal');
      const modal = bootstrap.Modal.getInstance(modalElement); // Get the modal instance
      modal.hide(); // Hide the modal

      // Fetch categories again to refresh the list
      this.fetchCategories();
      window.location.href = "/";
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
