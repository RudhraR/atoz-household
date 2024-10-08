<template>
    <NavBar />
    <div class="d-flex justify-content-center align-items-center vh-100">
    <div class="card shadow">
    <!-- <div class="card-header"><h5>Service Professional Registration</h5></div> -->
    <h5 class="card-header">Service Professional Registration</h5>
      <div class="card-body">
      <div class="form-group mb-3">
        <input v-model="username" type="text" class="form-control" placeholder="Name" required/>
      </div>
      <div class="form-group mb-3">
        <input v-model="email" type="email" class="form-control" placeholder="Email" required/>
      </div>
      <div class="form-group mb-3">
        <input v-model="password" type="password" class="form-control" placeholder="Password" required/>
      </div>
      <div class="form-group mb-3">
         <input v-model="services_provided" type="text" class="form-control" placeholder="Services Available (e.g., plumbing, electrical)" required/>
        </div>
        <div class="form-group mb-3">
        <!-- <label for="experience">Experience (in years)</label> -->
          <input v-model="experience" type="number" class="form-control" min="0" placeholder="Experience (in years)" required/>
        </div>

      <div class="form-group mb-3">
          <label for="address" style="text-align: left; display: block;">&nbsp;Address</label>
          <textarea class="form-control" v-model="address" name="address" rows="2" required></textarea>
      </div>
      <div class="form-group mb-3">
        <input v-model="pincode" type="text" class="form-control" placeholder="Pincode" required/>
      </div>
      <button class="btn btn-primary w-100" @click="register">Submit</button>
      
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
          services_provided:"",
          experience:"",
          role:""
      }
  },
  components: {
    NavBar
  },
  methods: {
      async register() {
          try {
              const response = await fetch('http://127.0.0.1:5000/register', {
                  method: 'POST',
                  headers: {
                      'Content-Type': 'application/json'
                  },
                  body: JSON.stringify({
                      email: this.email,
                      password: this.password,
                      username: this.username,
                      address: this.address,
                      pincode: this.pincode,
                      services_provided: this.services_provided,
                      experience: this.experience,
                      role: "professional"             
                  })
              })
              const data = await response.json()
              console.log("Data: ", data)
              if (!response.ok) {
                  alert(data.error)
              }
              else {
                  alert(data.message)
                  this.$router.push('/')
                //   window.location.reload();
              }
          }catch(error) {
              console.log(error)
          }
  }
}}
</script>

<style scoped></style>