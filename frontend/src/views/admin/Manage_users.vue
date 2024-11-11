<template>
    <NavBar />
    <div class="container" style="margin-top: 20px;" v-if="role == 'admin' && isLoggedin">
        <div class="row">
            
            <div class="col-3">
                <div class="card shadow ">
                    <h5 class="card-header text-white bg-secondary">All Customers</h5>
                    <div class="card-body">
                        <table class="table">
                            <thead>
                                <tr>
                                    <th scope="col">#</th>
                                    <th scope="col">Name</th>
                                    <th scope="col">Actions</th>
                                </tr>
                            </thead>
                            <tbody>
                                <tr v-for="(customer, index) in all_customers" v-if="all_customers && all_customers.length > 0"
                                    :key="customer.id">
                                    <th scope="row">{{ index + 1 }}</th>
                                    <td><a @click="openModal('customer', customer)" style="cursor: pointer;"
                                            class="text-secondary">
                                            {{ customer.username }}</a>
                                    </td>
                                   

                                    <td v-if="role == 'admin'" class="btn-group">                                     
                                        <button type="button" class="btn btn-sm btn-danger"
                                            @click="deleteCustomer(customer.id)"> Delete </button>
                                    </td>
                                </tr>
                                <tr v-else>
                                    <td colspan="4" class="text-muted"><i>No customers found</i></td>
                                </tr>
                            </tbody>
                        </table>
                    </div>
                </div>
            </div>
            <!-- Show list of active professionals -->
            <div class="col-4">
                <div class="card shadow ">
                    <h5 class="card-header text-white bg-secondary">Available professionals</h5>
                    <div class="card-body">
                        <table class="table">
                            <thead>
                                <tr>
                                    <th scope="col">#</th>
                                    <th scope="col">Name</th>
                                    <th scope="col">Service provided</th>
                                    <th scope="col">Actions</th>
                                </tr>
                            </thead>
                            <tbody>
                                <tr v-for="(professional, index) in available_professionals"
                                    v-if="available_professionals && available_professionals.length > 0" :key="professional.id">
                                    <th scope="row">{{ index + 1 }}</th>
                                    <td><a @click="openModal('professional', professional)" style="cursor: pointer;"
                                            class="text-secondary">
                                            {{ professional.username }}</a>
                                    </td>
                                    <td>{{ professional.services_provided }}</td>

                                    <td v-if="role == 'admin'" class="btn-group">
                                        <button type="button" class="btn btn-sm btn-danger"
                                            @click="updateProfessional(professional.id, 'reject')"> Delete </button>
                                    </td>
                                </tr>
                                <tr v-else>
                                    <td colspan="5" class="text-muted"><i>No new professional requests found</i></td>
                                </tr>
                            </tbody>
                        </table>
                    </div>
                </div>
            </div>
            
            <div class="col-5">
                <div class="card shadow">
                    <h5 class="card-header text-white bg-secondary">New professionals - Requests</h5>
                    <div class="card-body">
                        <table class="table">
                            <thead>
                                <tr>
                                    <th scope="col">#</th>
                                    <th scope="col">Name</th>
                                    
                                    <th scope="col">Resume</th>
                                    <th scope="col">Actions</th>
                                </tr>
                            </thead>
                            <tbody>
                                <tr v-for="(professional, index) in new_professionals"
                                    v-if="new_professionals && new_professionals.length > 0" :key="professional.id">
                                    <th scope="row">{{ index + 1 }}</th>
                                    <td>
                                        <a @click="openModal('professional', professional)" style="cursor: pointer;"
                                            class="text-secondary">
                                            {{ professional.username }}</a>
                                    </td>
                                    
                                    <td><a :href="`http://127.0.0.1:5000/view_resume/${professional.id}`"
                                            target="_blank">{{ professional.resume }}</a></td>

                                    <td v-if="role == 'admin'" class="btn-group">
                                        <button type="button" class="btn btn-sm btn-success"
                                            @click="updateProfessional(professional.id, 'approve')"> Approve </button>
                                        <button type="button" class="btn btn-sm btn-danger"
                                            @click="updateProfessional(professional.id, 'reject')"> Reject </button>
                                    </td>
                                </tr>
                                <tr v-else>
                                    <td colspan="5" class="text-muted"><i>No new professional requests found</i></td>
                                </tr>
                            </tbody>
                        </table>
                    </div>
                </div>
           </div>
        </div> 
        <br>
            
                <div class="card shadow">
                    <h5 class="card-header text-white bg-secondary">Service Requests</h5>
                    <div class="card-body">
                        <ViewServiceRequests />
                    </div>
                </div>
           

        <UserDetailsModal v-if="isModalVisible" :userDetails="userDetails" :userType="userType"
            @close="isModalVisible = false" />
    </div>
</template>

<script>
import userMixin from '@/mixins/userMixin';
import NavBar from '@/components/NavBar.vue'
import UserDetailsModal from '@/components/UserDetailsModal.vue';
import ViewServiceRequests from '@/components/ViewServiceRequests.vue';

export default {
    name: "Manage_users",
    components: {
        NavBar,
        UserDetailsModal,
        ViewServiceRequests
    },
    mixins: [userMixin],
    data() {
        return {
            isModalVisible: false,
            userType: '',
            userDetails: {
                'id': 0,
                'username': '',
                'email': '',
                'services_provided': '',
                'resume': '',
                'experience': 0,
                'address': '',
                'pincode': ''
            },
            new_professionals: [],
            available_professionals: [],
            all_customers: [],
        };
    },
    async mounted() {
        this.getAllProfessionals();
        this.getAllCustomers();
    },
    methods: {
        openModal(userType, userDetails) {
            this.userType = userType;
            this.userDetails = { ...userDetails }; // Clone the service object to avoid mutating the original one  
            this.isModalVisible = true; // Show the modal
        },
        async getAllProfessionals() {
            const response = await fetch('http://127.0.0.1:5000/professionals', {
                method: 'GET',
                headers: {
                    'Authorization': `Bearer ${localStorage.getItem('access_token')}`
                }
            });
            const data = await response.json();
            if (!response.ok) {
                alert(data.error);
            } else {
                this.new_professionals = data.new_professionals;
                this.available_professionals = data.available_professionals;
                console.log(data.available_professionals)
            }
        },
        async getAllCustomers() {
            const response = await fetch('http://127.0.0.1:5000/customers', {
                method: 'GET',
                headers: {
                    'Authorization': `Bearer ${localStorage.getItem('access_token')}`
                }
            });
            const data = await response.json();
            if (!response.ok) {
                alert(data.error);
            } else {
                this.all_customers = data.customers;
            }    
        },

        async deleteCustomer(id) {
            const response = await fetch(`http://127.0.0.1:5000/customers/${id}`, {
                method: 'DELETE',
                headers: {
                    'Authorization': `Bearer ${localStorage.getItem('access_token')}`
                }
            });
            const data = await response.json();
            if (!response.ok) {
                alert(data.error);
            } else {
                alert(data.message);
                this.getAllCustomers();
            }  
        },
        async updateProfessional(id, action) {
            if (action === 'approve') {
                const response = await fetch(`http://127.0.0.1:5000/professionals/${id}`, {
                    method: 'PUT',
                    headers: {
                        'Content-Type': 'application/json',
                        'Authorization': `Bearer ${localStorage.getItem('access_token')}`
                    },
                    body: JSON.stringify({ professional_id: id })
                });
                const data = await response.json();
                if (!response.ok) {
                    alert(data.error);
                } else {
                    alert(data.message);
                    this.getAllProfessionals();
                }
            }

            else if (action === 'reject') {
                const response = await fetch(`http://127.0.0.1:5000/professionals/${id}`, {
                    method: 'DELETE',
                    headers: {
                        'Content-Type': 'application/json',
                        'Authorization': `Bearer ${localStorage.getItem('access_token')}`
                    },
                });
                const data = await response.json();
                if (!response.ok) {
                    alert(data.error);
                } else {
                    alert(data.message);
                    this.getAllProfessionals();
                }
            }
        }
    }
}
</script>