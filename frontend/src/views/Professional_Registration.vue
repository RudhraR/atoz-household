<template>
    <NavBar />
    <div class="d-flex justify-content-center align-items-center vh-100">
    <div class="card shadow" style="width: 40rem;">
    <h5 class="card-header">Service Professional Registration</h5>
      <div class="card-body">
      <div class="form-group mb-3 row">
        <label for="username" class="col-sm-3 col-form-label">Name</label>
        <div class="col-sm-9">
        <input v-model="username" type="text" id="username" class="form-control" placeholder="Your Name"/>
        </div>
      </div>
      <div class="form-group mb-3 row">
        <label for="email" class="col-sm-3 col-form-label">Email</label>
        <div class="col-sm-9">
        <input v-model="email" type="email" id="email" class="form-control" placeholder="Email" required/>
        </div>
      </div>
      <div class="form-group mb-3 row">
        <label for="password" class="col-sm-3 col-form-label">Password</label>
        <div class="col-sm-9">
        <input v-model="password" type="password" class="form-control" id="Password" placeholder="Password" required/>
      </div>
      </div>
      <div class="form-group mb-3 row">
        <label for="services_provided" class="col-sm-3 col-form-label">Service Provided</label>
        <div class="col-sm-9">
         <select id="categorySelect" class="form-control" v-model="services_provided" required>
                  <option value="" disabled>Select a category</option>
                  <option v-for="category in categories" :key="category.id" :value="category.id">
                    {{ category.name }}
                  </option>
                </select>
          </div>
        </div>
        <div class="form-group mb-3 row">
        <label for="experience" class="col-sm-3 col-form-label">Experience</label>
        <div class="col-sm-9">
          <input v-model="experience" type="number" class="form-control" min="0" max="60" id="experience" placeholder="Experience (in years)" required/>
        </div>
      </div>
      <div class="form-group mb-3 row">
        <label for="role" class="col-sm-3 col-form-label">Resume(in .pdf)</label>
        <div class="col-sm-9">
          <input type="file" id="resume" class="form-control" accept=".pdf" @change="handleResumeUpload" required/>
        </div>
      </div>
      <div class="form-group mb-3 row">
          <label for="address" class="col-sm-3 col-form-label">&nbsp;Address</label>
          <div class="col-sm-9">
          <textarea class="form-control" v-model="address" name="address" rows="2" required></textarea>
           </div> 
        </div>
      <div class="form-group mb-3 row">
        <label for="pincode" class="col-sm-3 col-form-label">Pincode</label>
        <div class="col-sm-9">
        <input v-model="pincode" type="text" class="form-control" placeholder="Pincode" required/>
      </div>
      </div>
      <button class="btn btn-primary" @click="register">Submit</button>
      
  </div></div>
    </div>

</template>

<script>
import NavBar from '../components/NavBar.vue'
export default {
  name: "professional_registration",
  data() {
      return {
          email: "",
          password: "",
          username:"",
          address:"",
          pincode:"",
          services_provided:null,
          experience:"",
          role:"", 
          resume: null,
          categories: []
      }
  },
  components: {
    NavBar
  },
  mounted() {
    this.fetchCategories();
  },
  methods: {
    handleResumeUpload(event) {
      console.log(event.target.files[0])
      this.resume = event.target.files[0];
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
      async register() {
          try {
              const formData = new FormData()
              formData.append('email', this.email)
              formData.append('password', this.password)
              formData.append('username', this.username)
              formData.append('address', this.address)
              formData.append('pincode', this.pincode)
              formData.append('experience', this.experience)
              formData.append('resume', this.resume)
              formData.append('services_provided', this.services_provided)
              formData.append('role', "professional")
              
              const response = await fetch('http://127.0.0.1:5000/register', {
                  method: 'POST',
                  body: formData
        
              })
              console.log("Formdata: ", formData)
              const data = await response.json()
              console.log("Data: ", data)
              if (!response.ok) {
                  alert(data.error)
              }
              else {
                  alert(data.message)
                  this.$router.push('/')
              }
          }catch(error) {
              console.log(error)
          }
  }
}}
</script>

<style scoped></style>