<template>
    <div class="d-flex justify-content-center" style="margin-top: 32px;">
    <div class="card text-center" style="width: 25rem">
      <div class="card-header">
        <ul class="nav nav-tabs card-header-tabs">
          <li class="nav-item">
            <a
              class="nav-link"
              :class="{ active: isLogin }"
              @click="showLogin"
              href="#"
            >User Login</a>
          </li>
          <li class="nav-item ms-auto">
            <a
              class="nav-link"
              :class="{ active: !isLogin }"
              @click="showRegister"
              href="#"
            >Register as new customer</a>
          </li>
        </ul>
      </div>
      <div class="card-body">   
        <!-- Conditional rendering of components -->
        <LoginPage v-if="isLogin" />
        <customer_registration v-else />
    </div>   
      </div>
    </div>
  </template>
  
  <script>
  import LoginPage from './LoginPage.vue';
  import customer_registration from './Customer_Registration.vue';
  
  export default {
    name: 'AuthCard',
    components: {
        LoginPage,
        customer_registration,
    },
    data() {
      return {
        isLogin: true, // Show login by default
      };
    },
    methods: {
      showLogin() {
        this.isLogin = true;
      },
      showRegister() {
        this.isLogin = false;
      },
    },
  };
  </script>
  
  <style scoped>

  </style>
  