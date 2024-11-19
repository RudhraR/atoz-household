<template>
  
        <div class="card shadow p-4 border rounded-3 ">
        <!-- <h3 class="card-title text-center mb-4">Login</h3> -->
        <form @submit.prevent="login">
        <div class="form-group mb-3">
            <input v-model="email" type="email" class="form-control" placeholder="Email" required/>
          </div>
          <div class="form-group mb-4">
            <input v-model="password" type="password" class="form-control" placeholder="Password" required/>
          </div>
          <button type="submit" class="btn btn-primary w-100">Submit</button>
        </form>  
      </div>
   
</template>

<script>

import NavBar from '@/components/NavBar.vue'
export default {
    components: {
        NavBar
    }, 
    name: "LoginPage",
    data() {
        return {
            email: '',
            password: ''
        }
    },
    methods: {
        async login() {
            const response = await fetch('http://127.0.0.1:5000/login', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    email: this.email,
                    password: this.password
                })
                
            })
            const data = await response.json()
            console.log(data)
            if (!response.ok) {
                alert(data.error)
            }
            else {
                alert(data.message)
                // storing an item in local storage
                localStorage.setItem('access_token', data.access_token)
                
                // this.$router.push('/')
                window.location.href = "/";
                
            }
        }
    }
}

</script>