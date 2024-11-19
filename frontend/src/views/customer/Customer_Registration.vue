<template>
  <div class="card shadow">
    <div class="card-body">
      <!-- Username field -->
      <div class="form-group mb-3">
        <input v-model="username" type="text" class="form-control" placeholder="Name" required />
        <div v-if="usernameError" class="text-danger">{{ usernameError }}</div>
      </div>

      <!-- Email field -->
      <div class="form-group mb-3">
        <input v-model="email" type="email" class="form-control" placeholder="Email" required />
        <div v-if="emailError" class="text-danger">{{ emailError }}</div>
      </div>

      <!-- Password field -->
      <div class="form-group mb-4">
        <input v-model="password" type="password" class="form-control" placeholder="Password" required />
      </div>

      <!-- Address field -->
      <div class="form-group mb-3">
        <label for="address" style="text-align: left; display: block;">&nbsp;Address</label>
        <textarea class="form-control" v-model="address" name="address" rows="2" required></textarea>
      </div>

      <!-- Pincode field -->
      <div class="form-group mb-3">
        <input v-model="pincode" type="text" class="form-control" placeholder="Pincode" required />
        <div v-if="pincodeError" class="text-danger">{{ pincodeError }}</div>
      </div>

      <!-- Mobile field -->
      <div class="form-group mb-3">
        <input v-model="mobile" type="tel" class="form-control" placeholder="Mobile number" required />
        <div v-if="mobileError" class="text-danger">{{ mobileError }}</div>
      </div>

      <button class="btn btn-primary w-100" @click="register">Submit</button>
    </div>
  </div>
</template>

<script>
import Navbar from '@/components/NavBar.vue'

export default {
  name: "customer_registration",
  data() {
    return {
      email: "",
      password: "",
      username: "",
      address: "",
      pincode: "",
      mobile: "",
      role: "",
      // Error messages
      emailError: "",
      usernameError: "",
      pincodeError: "",
      mobileError: ""
    }
  },
  components: {
    Navbar
  },
  methods: {
    // Method to validate the email address
    validateEmail() {
      const emailPattern = /^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,6}$/;
      if (!this.email) {
        this.emailError = "Email is required.";
      } else if (!emailPattern.test(this.email)) {
        this.emailError = "Invalid email format.";
      } else {
        this.emailError = "";
      }
    },

    // Method to validate the username
    validateUsername() {
      if (!this.username) {
        this.usernameError = "Username is required.";
      } else if (this.username.length < 3) {
        this.usernameError = "Username must be at least 3 characters.";
      } else {
        this.usernameError = "";
      }
    },

    // Method to validate the pincode
    validatePincode() {
      const pincodePattern = /^[1-9][0-9]{5}$/; // 6-digit Indian pincode
      if (!this.pincode) {
        this.pincodeError = "Pincode is required.";
      } else if (!pincodePattern.test(this.pincode)) {
        this.pincodeError = "Invalid pincode format.";
      } else {
        this.pincodeError = "";
      }
    },

    // Method to validate the mobile number
    validateMobile() {
      const mobilePattern = /^[6-9][0-9]{9}$/; // 10-digit mobile number starting with 6-9
      if (!this.mobile) {
        this.mobileError = "Mobile number is required.";
      } else if (!mobilePattern.test(this.mobile)) {
        this.mobileError = "Invalid mobile number.";
      } else {
        this.mobileError = "";
      }
    },

    // Method to check all validations before submitting
    validateForm() {
      this.validateEmail();
      this.validateUsername();
      this.validatePincode();
      this.validateMobile();
      return !this.emailError && !this.usernameError && !this.pincodeError && !this.mobileError;
    },

    async register() {
      if (!this.validateForm()) {
        return; // Stop form submission if there are validation errors
      }
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
        } else {
          alert(data.message)
          window.location.href = "/";
        }
      } catch (error) {
        console.log(error)
      }
    }
  }
}
</script>

<style scoped>
.text-danger {
  font-size: 0.875rem;
  color: #dc3545;
}
</style>
