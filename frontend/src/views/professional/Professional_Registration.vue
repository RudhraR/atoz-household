<template>
  <NavBar />
  <div class="d-flex justify-content-center align-items-center" style="margin-top: 20px">
    <div class="card shadow" style="width: 40rem;">
      <h5 class="card-header">Service Professional Registration</h5>
      <div class="card-body">
        <form @submit.prevent="register">
        <!-- Username field -->
        <div class="form-group mb-3 row">
          <label for="username" class="col-sm-3 col-form-label">Name</label>
          <div class="col-sm-9">
            <input v-model="username" type="text" id="username" class="form-control" placeholder="Your Name" required/>
            <div v-if="usernameError" class="text-danger">{{ usernameError }}</div>
          </div>
        </div>

        <!-- Email field -->
        <div class="form-group mb-3 row">
          <label for="email" class="col-sm-3 col-form-label">Email</label>
          <div class="col-sm-9">
            <input v-model="email" type="email" id="email" class="form-control" placeholder="Email" required/>
            <div v-if="emailError" class="text-danger">{{ emailError }}</div>
          </div>
        </div>

        <!-- Password field -->
        <div class="form-group mb-3 row">
          <label for="password" class="col-sm-3 col-form-label">Password</label>
          <div class="col-sm-9">
            <input v-model="password" type="password" class="form-control" id="Password" placeholder="Password" required/>
            <div v-if="passwordError" class="text-danger">{{ passwordError }}</div>
          </div>
        </div>

        <!-- Service Provided field -->
        <div class="form-group mb-3 row">
          <label for="services_provided" class="col-sm-3 col-form-label">Service Provided</label>
          <div class="col-sm-9">
            <select id="categorySelect" class="form-control" v-model="services_provided" required>
              <option value="" disabled>Select a category</option>
              <option v-for="category in categories" :key="category.id" :value="category.id">
                {{ category.name }}
              </option>
            </select>
            <div v-if="servicesError" class="text-danger">{{ servicesError }}</div>
          </div>
        </div>

        <!-- Experience field -->
        <div class="form-group mb-3 row">
          <label for="experience" class="col-sm-3 col-form-label">Experience</label>
          <div class="col-sm-9">
            <input v-model="experience" type="number" class="form-control" min="0" max="60" id="experience" placeholder="Experience (in years)" required/>
            <div v-if="experienceError" class="text-danger">{{ experienceError }}</div>
          </div>
        </div>

        <!-- Resume upload field -->
        <div class="form-group mb-3 row">
          <label for="role" class="col-sm-3 col-form-label">Resume (in .pdf)</label>
          <div class="col-sm-9">
            <input type="file" id="resume" class="form-control" accept=".pdf" @change="handleResumeUpload" required/>
            <div v-if="resumeError" class="text-danger">{{ resumeError }}</div>
          </div>
        </div>

        <!-- Address field -->
        <div class="form-group mb-3 row">
          <label for="address" class="col-sm-3 col-form-label">&nbsp;Address</label>
          <div class="col-sm-9">
            <textarea class="form-control" v-model="address" name="address" rows="2" required></textarea>
            <div v-if="addressError" class="text-danger">{{ addressError }}</div>
          </div>
        </div>

        <!-- Pincode field -->
        <div class="form-group mb-3 row">
          <label for="pincode" class="col-sm-3 col-form-label">Pincode</label>
          <div class="col-sm-9">
            <input v-model="pincode" type="text" class="form-control" placeholder="Pincode" required/>
            <div v-if="pincodeError" class="text-danger">{{ pincodeError }}</div>
          </div>
        </div>

        <!-- Mobile number field -->
        <div class="form-group mb-3 row">
          <label for="mobile" class="col-sm-3 col-form-label">Mobile</label>
          <div class="col-sm-9">
            <input v-model="mobile" type="tel" id="mobile" min="10" max="10" class="form-control" placeholder="Mobile number" required/>
            <div v-if="mobileError" class="text-danger">{{ mobileError }}</div>
          </div>
        </div>

        <button class="btn btn-primary" type="submit">Submit</button>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
import NavBar from '@/components/NavBar.vue'

export default {
  name: "professional_registration",
  data() {
    return {
      email: "",
      password: "",
      username: "",
      address: "",
      pincode: "",
      services_provided: null,
      experience: "",
      mobile: "",
      role: "",
      resume: null,
      categories: [],
      // Validation error messages
      emailError: "",
      usernameError: "",
      passwordError: "",
      servicesError: "",
      experienceError: "",
      resumeError: "",
      addressError: "",
      pincodeError: "",
      mobileError: ""
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

    // Validation methods
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

    validateUsername() {
      if (!this.username) {
        this.usernameError = "Username is required.";
      } else {
        this.usernameError = "";
      }
    },

    validatePassword() {
      if (!this.password) {
        this.passwordError = "Password is required.";
      } else {
        this.passwordError = "";
      }
    },

    validateServices() {
      if (!this.services_provided) {
        this.servicesError = "Service category is required.";
      } else {
        this.servicesError = "";
      }
    },

    validateExperience() {
      if (!this.experience || this.experience < 0 || this.experience > 60) {
        this.experienceError = "Experience should be between 0 and 60 years.";
      } else {
        this.experienceError = "";
      }
    },

    validateResume() {
      if (!this.resume) {
        this.resumeError = "Resume is required.";
      } else if (this.resume.type !== "application/pdf") {
        this.resumeError = "Only PDF files are allowed.";
      } else {
        this.resumeError = "";
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
        this.mobileError = "Mobile number must be 10 digits.";
      } else {
        this.mobileError = "";
      }
    },

    // Final registration logic
    async register() {
      this.validateEmail();
      this.validateUsername();
      this.validatePassword();
      this.validateServices();
      this.validateExperience();
      this.validateResume();
      this.validateAddress();
      this.validatePincode();
      this.validateMobile();

      if (
        this.emailError ||
        this.usernameError ||
        this.passwordError ||
        this.servicesError ||
        this.experienceError ||
        this.resumeError ||
        this.addressError ||
        this.pincodeError ||
        this.mobileError
      ) {
        return; // Do not submit if validation fails
      }

      try {
        const formData = new FormData();
        formData.append('email', this.email);
        formData.append('password', this.password);
        formData.append('username', this.username);
        formData.append('address', this.address);
        formData.append('pincode', this.pincode);
        formData.append('mobile', this.mobile);
        formData.append('experience', this.experience);
        formData.append('resume', this.resume);
        formData.append('services_provided', this.services_provided);
        formData.append('role', "professional");

        const response = await fetch('http://127.0.0.1:5000/register', {
          method: 'POST',
          body: formData
        });

        const data = await response.json();
        if (!response.ok) {
          alert(data.error);
        } else {
          alert(data.message);
          this.$router.push('/');
        }
      } catch (error) {
        console.log(error);
      }
    }
  }
}
</script>
