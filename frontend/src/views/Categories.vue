<template>
    <!-- <NavBar /> -->
    <div class="container"  style="margin-top: 20px;">
      <div class="card shadow">
        <h5 class="card-header">All Categories</h5> 
        <div class="card-body">
          <!-- <div style=" float:right; display: flex;"> -->
            <div class="row">
              <div class="col-6">
            <input v-model="categoryName" placeholder="Category Name"  required/></div>
            <div class="col-6"><button @click="addCategory" class="btn btn-sm btn-success" >
               Add Category</button></div>
          </div><br>

            <table class = "table">
            <thead>
            <tr>
                <th scope="col">#</th>
                <th scope="col">Category Name</th>
                <th scope="col" v-if = "role == 'admin'">Actions</th>
            </tr>
            </thead>
            <tbody>
            <tr v-for="(category, index) in categories" :key="category.id">
                <th scope="row">{{index+1}}</th>
                <td>{{category.name}}</td>
                <td v-if = "role == 'admin'" class = "btn-group">
                    <button type="button" class="btn btn-sm btn-primary" @click="editCategory(category.id)">Edit</button>
                    <button type="button" class="btn btn-sm btn-danger" @click="deleteCategory(category.id)">Delete</button>
                </td>
            </tr>
            </tbody>
            </table>

    </div></div></div>
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