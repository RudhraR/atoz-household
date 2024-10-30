<template>
      <div class="card shadow">
        <div class="card-body">
        <div class="form-group mb-3">
          <input v-model="username" type="text" class="form-control" placeholder="Name" required/>
        </div>
        <div class="form-group mb-3">
          <input v-model="email" type="email" class="form-control" placeholder="Email" required/>
        </div>
        <div class="form-group mb-4">
          <input v-model="password" type="password" class="form-control" placeholder="Password" required/>
        </div>
        <div class="form-group mb-3">
            <label for="address" style="text-align: left; display: block;">&nbsp;Address</label>
            <textarea class="form-control" v-model="address" name="address" rows="2" required></textarea>
        </div>
        <div class="form-group mb-3">
          <input v-model="pincode" type="text" class="form-control" placeholder="Pincode" required/>
        </div>
        <div class="form-group mb-3">
          <input v-model="mobile" type="tel" min="10" max="10" class="form-control" placeholder="Mobile number" required/>
        </div>
        <button class="btn btn-primary w-100" @click="register">Submit</button>
        
    </div>
      </div>

</template>

<script>
import Navbar from '../components/NavBar.vue'
export default {
    name: "customer_registration",
    data() {
        return {
            email: "",
            password: "",
            username:"",
            address:"",
            pincode:"",
            mobile:"",
            role:""
        }
    },
    components: {
        Navbar
    },
    methods: {
        async register() {
            try {
                const formData = new FormData()
              formData.append('email', this.email)
              formData.append('password', this.password)
              formData.append('username', this.username)
              formData.append('address', this.address)
              formData.append('pincode', this.pincode)
              formData.append('mobile', this.mobile)
              formData.append('role', "customer")
              
              const response = await fetch('http://127.0.0.1:5000/register', {
                  method: 'POST',
                  body: formData
        })
                const data = await response.json()
                console.log("Data: ", data)
                if (!response.ok) {
                    alert(data.error)
                }
                else {
                    alert(data.message)
                    // this.$router.push('/')
                    window.location.href = "/";
                }
            }catch(error) {
                console.log(error)
            }
    }
}}
</script>

<style scoped></style>