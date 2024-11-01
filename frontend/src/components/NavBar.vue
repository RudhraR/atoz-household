<template>
    <nav class="navbar navbar-expand-lg bg-body-tertiary sticky-top">
      <div class="container-fluid">
        <a class="navbar-brand" href="#">
            <button class="btn btn-info"><h4>A - Z</h4></button>
    </a>
        <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarText" aria-controls="navbarText" aria-expanded="false" aria-label="Toggle navigation">
          <span class="navbar-toggler-icon"></span>
        </button>
        <div class="collapse navbar-collapse" id="navbarText">
          <ul class="navbar-nav me-auto mb-2 mb-lg-0">
            <li class="nav-item mx-5">
              <router-link class="nav-link" to="/">Home</router-link>
            </li>
             <li class="nav-item"  v-if="this.isLoggedin && this.role === 'admin'">
              <router-link class="nav-link" to="/manage_users">Manage users</router-link>
            </li>
            <!-- <li class="nav-item"  v-if="this.isLoggedin && this.role === 'customer'">
              <router-link class="nav-link" to="/view_service_requests">My Service Requests</router-link>
            </li>  -->
            </ul>
          <ul class="navbar-nav ms-auto mb-2 mb-lg-0">
            
            <li class="nav-item"  v-if="!this.isLoggedin">
              <router-link class="nav-link" to="/professional_registration">
                <i>Register as Service professional</i></router-link>
            </li>
            
            <li class="nav-item"  v-if="this.isLoggedin">
              <a class="nav-link" @click="logout">Logout</a>
            </li>
           
          </ul>
        </div>
      </div>
    </nav>
    </template>
    
    <script>
    import userMixin from '@/mixins/userMixin';
    export default {
      name: 'NavBar',
      mixins: [userMixin],
    }
    </script>