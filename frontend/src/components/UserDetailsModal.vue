<template>
    <div class="modal fade show" tabindex="-1" role="dialog" aria-labelledby="userDetailsModal" aria-modal="true">
      <div class="modal-dialog" role="document">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">
              {{ userType === 'customer' ? 'Customer Details' : 'Professional Details' }}
            </h5>
            <button type="button" class="btn-close" @click="$emit('close')"></button>
          </div>
          <div class="modal-body">
            <table style="text-align: left;">
            <tbody>
            <tr>
              <td><strong>ID:</strong></td> <td>{{ userDetails.id }}</td>
            </tr>
              <tr>
                <td><strong>Name:</strong></td> <td>{{ userDetails.username }}</td>
              </tr>
              <tr>
                <td><strong>Email:</strong></td> <td>{{ userDetails.email }}</td>
              </tr>
              <tr>
                <td><strong>Mobile:</strong></td> <td>{{ userDetails.mobile }}</td>
              </tr>
              <tr>
                <td><strong>Address:</strong></td> <td>{{ userDetails.address }}</td>
              </tr>
              <tr>
                <td><strong>Pincode:</strong></td> <td>{{ userDetails.pincode }}</td>
              </tr>
              
              <tr v-if="userType === 'professional'">
                <td><strong>Services Provided:</strong></td> <td> &nbsp;{{ userDetails.services_provided }}</td>
              </tr>
              <tr v-if="userType === 'professional'">
                <td><strong>Experience:</strong></td> <td> &nbsp;{{ userDetails.experience }}</td>
              </tr>
              <tr v-if="userType === 'professional'">
                <td><strong>Resume:</strong></td> 
                <td>
                    <a :href="`http://127.0.0.1:5000/view_resume/${userDetails.id}`" 
                            target="_blank">{{ userDetails.resume }}</a>
                </td>
              </tr>
            </tbody>
            </table>    
              <div class="modal-footer">
                <button type="button" class="btn btn-secondary" @click="$emit('close')">Close</button> 
              </div>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script>
 
  export default {
    name: 'UserDetailsModal',
    props: {
      userDetails: {
        type: Object,
        required: true,
      },
      userType: {
        type: String,
        required: true, // can be 'professional' or 'customer'
      },
    }
  };
  </script>
  
  <style scoped>
 .modal {
  display: none; /* Prevent direct block display */
  background: rgba(0, 0, 0, 0.5);
}
.show {
  display: block !important; /* Ensure modal is visible when 'show' class is added */
}
  
  </style>
  