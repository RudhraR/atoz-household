<template>
    <NavBar />

    <div class="container">
    <h3>All Categories</h3>
    <div class="form-group" style=" float:right; display: flex;">
        <input v-model="categoryName" placeholder="Category Name" required/>
      <button @click="addCategory" class="btn btn-sm btn-primary" style="margin-left: -20px;">Add Category</button>
    </div>
    <table class = "table">
        <thead>
            <tr>
                <th scope="col">#</th>
                <th scope="col">Category Name</th>
                <th scope="col">Actions</th>
            </tr>
        </thead>
        <tbody>
            <tr v-for="category in categories" :key="category.id">
                <th scope="row">{{category.id}}</th>
                <td>{{category.name}}</td>
                <td v-if = "role == 'admin'" class = "btn-group">
                    <button type="button" class="btn btn-primary" @click="editCategory(category.id)">Edit</button>
                    <button type="button" class="btn btn-danger" @click="deleteCategory(category.id)">Delete</button>
                </td>
            </tr>
        </tbody>
    </table>

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
        categoryName: ''
      };
    },
    methods: {
      async fetchCategories() {
        const response = await fetch('http://127.0.0.1:5000/categories');
        const data = await response.json()
        
        if (!response.ok) {
            alert(data.error)
        }
        else {
        this.categories = data.categories
        }
      },
      async addCategory() {
        if (!this.categoryName) return;
        else{
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
      }},
      async deleteCategory(id) {
        await fetch(`http://127.0.0.1:5000/categories/${id}`, { 
            method: 'DELETE',
            headers: {
              'Authorization': `Bearer ${localStorage.getItem('access_token')}`
            }
         });
        this.fetchCategories();
      },
      async editCategory(id) {
        // await fetch(`http://127.0.0.1:5000/categories/${id}`, { method: 'PUT' });
        this.fetchCategories();
      }
    },
    mounted() {
      this.fetchCategories();
    }
  };
  </script>