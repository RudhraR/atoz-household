<template>
  <Navbar />
  <div v-if="isLoggedin" class="d-flex justify-content-center align-items-center" style="margin-top: 20px">
    <div class="card shadow">
      <h5 class="card-header text-white bg-secondary">Edit Profile Details</h5>
      <div class="card-body">
      <form @submit.prevent="update">        
        <!-- Username field -->
        <div class="form-group mb-3 row">
          <label for="username" class="col-sm-4 col-form-label">Name</label>
          <div class="col-sm-8">
            <input v-model="username" type="text" class="form-control" @blur="validateUsername" />
            <div v-if="usernameError" class="text-danger">{{ usernameError }}</div>
          </div>
        </div>

        <!-- Email field (disabled) -->
        <div class="form-group mb-3 row">
          <label for="email" class="col-sm-4 col-form-label">Email</label>
          <div class="col-sm-8">
            <input v-model="email" type="email" class="form-control" disabled />
          </div>
        </div>

        <!-- Password field -->
        <div class="form-group mb-3 row">
          <label for="password" class="col-sm-4 col-form-label">Password</label>
          <div class="col-sm-8">
            <input v-model="password" type="password" class="form-control" placeholder="Password" />
            
          </div>
        </div>

        <!-- Address field -->
        <div class="form-group mb-3 row">
          <label for="address" class="col-sm-4 col-form-label">Address</label>
          <div class="col-sm-8">
            <textarea class="form-control" v-model="address" name="address" rows="2" @blur="validateAddress"></textarea>
            <div v-if="addressError" class="text-danger">{{ addressError }}</div>
          </div>
        </div>

        <!-- Pincode field -->
        <div class="form-group mb-3 row">
          <label for="pincode" class="col-sm-4 col-form-label">Pincode</label>
          <div class="col-sm-8">
            <input v-model="pincode" type="text" class="form-control" @blur="validatePincode" />
            <div v-if="pincodeError" class="text-danger">{{ pincodeError }}</div>
          </div>
        </div>

        <!-- Mobile number field -->
        <div class="form-group mb-3 row">
          <label for="mobile" class="col-sm-4 col-form-label">Mobile</label>
          <div class="col-sm-8">
            <input v-model="mobile" type="tel" maxlength="10" class="form-control" @blur="validateMobile" />
            <div v-if="mobileError" class="text-danger">{{ mobileError }}</div>
          </div>
        </div>

        <button class="btn btn-primary w-100" type="submit">Update</button>
        </form>
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
      username: "",
      address: "",
      pincode: "",
      mobile: "",
      role: "",
      // Validation error messages
      usernameError: "",
      
      addressError: "",
      pincodeError: "",
      mobileError: ""
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
        if (!response.ok) {
          alert(data.error)
        } else {
          this.email = data.user.email
          // this.password = data.user.password
          this.username = data.user.username
          this.address = data.user.address
          this.pincode = data.user.pincode
          this.mobile = data.user.mobile
        }
      } catch (error) {
        console.log(error)
      }
    },

    // Validation methods
    validateUsername() {
      if (!this.username) {
        this.usernameError = "Username is required.";
      } else {
        this.usernameError = "";
      }
    },

    
    validateAddress() {
      if (!this.address) {
        this.addressError = "Address is required.";
      } else {
        this.addressError = "";
      }
    },

    validatePincode() {
      const pincodePattern = /^[1-9][0-9]{5}$/;
      if (!this.pincode) {
        this.pincodeError = "Pincode is required.";
      } else if (!pincodePattern.test(this.pincode)) {
        this.pincodeError = "Invalid pincode format.";
      } else {
        this.pincodeError = "";
      }
    },

    validateMobile() {
      const mobilePattern = /^[6-9][0-9]{9}$/;
      if (!this.mobile) {
        this.mobileError = "Mobile number is required.";
      } else if (!mobilePattern.test(this.mobile)) {
        this.mobileError = "Enter valid mobile number.";
      } else {
        this.mobileError = "";
      }
    },

    // Profile update logic
    async update() {
      // Validate the fields before proceeding with the update
      this.validateUsername();
    
      this.validateAddress();
      this.validatePincode();
      this.validateMobile();

      // If there are any validation errors, stop the form submission
      if (this.usernameError || this.addressError || this.pincodeError || this.mobileError) {
        return; // Stop form submission if any error exists
      }

      try {
        const formData = new FormData();
        formData.append('password', this.password);
        formData.append('username', this.username);
        formData.append('address', this.address);
        formData.append('pincode', this.pincode);
        formData.append('mobile', this.mobile);

        const response = await fetch('http://127.0.0.1:5000/updateProfile', {
          method: 'POST',
          headers: {
            'Authorization': `Bearer ${localStorage.getItem('access_token')}`
          },
          body: formData
        })

        const data = await response.json()
        if (!response.ok) {
          alert(data.error)
        } else {
          alert(data.message)
          this.$router.push('/')
        }
      } catch (error) {
        console.log(error)
      }
    }
  }
}
</script>

<style scoped></style>
