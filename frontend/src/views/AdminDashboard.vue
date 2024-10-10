<template>
    <!-- <NavBar /> -->
    <div class="container">
        <div class="row">
            <div class="col-8">
                <Services />
            </div>
            <div class="col-4">
                <Categories />
            </div>
        </div>
    </div>  
    
</template>
  
  <script>
  import userMixin from '@/mixins/userMixin';
  import NavBar from '@/components/NavBar.vue'
  import Categories from './Categories.vue';
  import Services from './Services.vue';

  
  export default {
    name: 'AdminDashboard',
    components: {
      Categories,
      Services,
      NavBar
    },
    mixins: [userMixin],
  }
  </script>