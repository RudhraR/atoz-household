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
            role:""
        }
    },
    components: {
        Navbar
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
                        role: "customer"             
                    })
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