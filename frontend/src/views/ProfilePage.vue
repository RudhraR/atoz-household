<template>
    <Navbar />
    <div v-if="isLoggedin" class="d-flex justify-content-center align-items-center" style="margin-top: 20px">
    <div class="card shadow">
      <h5 class="card-header text-white bg-secondary">Edit Profile Details </h5>
      <div class="card-body">
       
      <div class="form-group mb-3 row">
        <label for="username" class="col-sm-4 col-form-label">Name</label>
        <div class="col-sm-8">
        <input v-model="username" type="text" class="form-control" />
        </div>
      </div>
      <div class="form-group mb-3 row">
        <label for="email" class="col-sm-4 col-form-label">Email</label>
        <div class="col-sm-8">
        <input v-model="email" type="email" class="form-control" disabled/>
      </div></div>
      <div class="form-group mb-3 row">
        <label for="password" class="col-sm-4 col-form-label">Password</label>
        <div class="col-sm-8">
        <input v-model="password" type="password" class="form-control" placeholder="Password"/>
      </div></div>
      <div class="form-group mb-3 row">
          <label for="address" class="col-sm-4 col-form-label">&nbsp;Address</label>
          <div class="col-sm-8">
          <textarea class="form-control" v-model="address" name="address" rows="2" ></textarea>
      </div></div>
      <div class="form-group mb-3 row">
        <label for="pincode" class="col-sm-4 col-form-label">Pincode</label>
        <div class="col-sm-8">
        <input v-model="pincode" type="text" class="form-control" />
      </div></div>
      <div class="form-group mb-3 row">
        <label for="mobile" class="col-sm-4 col-form-label">Mobile</label>
        <div class="col-sm-8">
        <input v-model="mobile" type="tel" maxlength="10" class="form-control" />
      </div></div>
      <button class="btn btn-primary w-100" @click="update">Update</button>
  </div>
    </div>
</div>
</template>

<script>
import Navbar from '@/components/NavBar.vue'
import userMixin from '@/mixins/userMixin';
export default {
  name: "ProfilePage",
  mixins: [userMixin],
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
  async mounted() {
      await this.getProfile()
  },
  methods: {
      async getProfile() {
        try {
            const response = await fetch('http://127.0.0.1:5000/getuserdata', {
                method: 'GET',
                headers: {
                    'Authorization': `Bearer ${localStorage.getItem('access_token')}`
                },
            })
            const data = await response.json()
            console.log("Data: ", data)
            if (!response.ok) {
                alert(data.error)
            }
            else {
                this.email = data.user.email
                this.password = data.user.password
                this.username = data.user.username
                this.address = data.user.address
                this.pincode = data.user.pincode
                this.mobile = data.user.mobile
      }
    } catch (error) {
        console.log(error)
    }
    },
      async update() {
          try {
           
            const formData = new FormData()
            // formData.append('email', this.email)
            formData.append('password', this.password)
            formData.append('username', this.username)
            formData.append('address', this.address)
            formData.append('pincode', this.pincode)
            formData.append('mobile', this.mobile)
           
            const response = await fetch('http://127.0.0.1:5000/updateProfile', {
                method: 'POST',
                headers: {
                    'Authorization': `Bearer ${localStorage.getItem('access_token')}`
                },
                body: formData
      })
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