<template>
    <div class="container" style="float:left;">
        <form @submit.prevent="submitServiceRequest">

            <!-- Service Name (prepopulated and disabled) -->
            <div class="form-group mb-3 row">
                <label for="serviceName" class="col-sm-6 col-form-label left-align">Service Name</label>
                <div class="col-sm-6">
                    <input type="text" id="serviceName" class="form-control" v-model="serviceName" disabled />
                </div>
            </div>

            <!-- Customer Address (prepopulated and disabled) -->
            <div class="form-group mb-3 row">
                <label for="address" class="col-sm-6 col-form-label">Your Address</label>
                <div class="col-sm-6">
                    <input type="text" id="address" class="form-control" v-model="customerAddress" disabled />
                </div>
            </div>

            <!-- Customer Pincode (prepopulated and disabled) -->
            <div class="form-group mb-3 row">
                <label for="pincode" class="col-sm-6 col-form-label">Your Pincode</label>
                <div class="col-sm-6">
                    <input type="text" id="pincode" class="form-control" v-model="customerPincode" disabled />
                </div>
            </div>

            <!-- Customer Contact Number -->
            <div class="form-group mb-3 row">
                <label for="contactNumber" class="col-sm-6 col-form-label">Your Contact Number</label>
                <div class="col-sm-6">
                    <input type="tel" id="contactNumber" class="form-control" v-model="contactNumber" disabled />
                </div>
            </div>

            <!-- Date of Request (prepopulated and disabled) -->
            <div class="form-group mb-3 row">
                <label for="dateOfRequest" class="col-sm-6 col-form-label">Date of Request</label>
                <div class="col-sm-6">
                    <input type="datetime-local" id="dateOfRequest" class="form-control" v-model="dateOfRequest" />
                </div>
            </div>

            <!-- Select Available Professional -->
            <div class="form-group mb-3 row">
                <label for="professional" class="col-sm-6 col-form-label">Available Professionals</label>
                <div class="col-sm-6">
                    <select id="professional" class="form-control" v-model="selectedProfessional">
                        <option v-for="user in professionals" :key="user.id" :value="user.id">
                            {{ user.username }} &nbsp;&nbsp;
                            {{ user.rating ? `(Rating: ${user.rating}/5)` : '(No ratings yet)' }}
                        </option>
                    </select>
                </div>
            </div>

            <!-- Submit Button -->
            <button type="submit" class="btn btn-primary">Book Service</button>
            
        </form>
    </div>
</template>

<script>
export default {
    name: "BookServiceRequest",
    props: {
        serviceDetails: {
            type: Object,
            required: true,
        },
        customerDetails: {
            type: Object,
            required: true,
        },
        rebooked: {
            type: Boolean,
            default: false,
        },
    },
    data() {
        return {
            serviceName: '', // Initialized empty
            customerAddress: '', // Initialized empty
            customerPincode: '', // Initialized empty
            dateOfRequest: '', // Initialized empty
            professionals: [], // List of available professionals
            selectedProfessional: null, // Selected professional's user ID
            contactNumber: "", // Customer's contact number
            remarks: "", // Optional remarks
        };
    },
    watch: {
        serviceDetails: {
            immediate: true,
            handler(newValue) {
                this.resetForm(); // Reset form when serviceDetails changes
            },
        },
        customerDetails: {
            immediate: true,
            handler(newValue) {
                this.resetForm(); // Reset form when customerDetails changes
            },
        },

    },
    methods: {
        resetForm() {
            // Reset all form fields
            this.serviceName = this.serviceDetails?.name || '';
            this.customerAddress = this.customerDetails?.address || '';
            this.customerPincode = this.customerDetails?.pincode || '';
            this.dateOfRequest = null; //new Date().toLocaleDateString(); // Reset to today
            this.selectedProfessional = null; // Reset selection
            this.contactNumber = this.customerDetails?.mobile || ""; // Clear contact number
            this.remarks = ""; // Clear remarks
            this.fetchProfessionals(); // Fetch professionals each time
        },
        async fetchProfessionals() {
            try {
                const categoryId = this.serviceDetails?.category_id; // Get the category ID from service details
                if (!categoryId) {
                    console.error("No category ID found in service details.");
                    return;
                }
                const response = await fetch(`http://127.0.0.1:5000/professionals_by_category/${categoryId}`, {
                    headers: {
                        Authorization: `Bearer ${localStorage.getItem("access_token")}`,
                    },
                }); 
                const data = await response.json();
                this.professionals = data.professionals; // Assign the filtered professionals to the list
                console.log(this.professionals);
            } catch (error) {
                console.error("Error fetching professionals:", error);
            }
        },
        async submitServiceRequest() {
            const requestData = {
                service_id: this.serviceDetails.id, // Use the service ID passed via props
                customer_id: this.customerDetails.id, // Use the customer ID passed via props
                professional_id: this.selectedProfessional,
                date_of_request: this.dateOfRequest,
                status: "requested",
            };
            console.log('Request Data:', requestData); // Log the request data for debugging
            console.log("from rebooked:", this.rebooked)
            console.log("serviceid:", this.serviceDetails.serviceRequest_id)
            try {
                const response = await fetch(`http://127.0.0.1:5000/service_requests`, {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json",
                        Authorization: `Bearer ${localStorage.getItem("access_token")}`,
                    },
                    body: JSON.stringify(requestData),
                });

                if (!response.ok) {
                    const errorData = await response.json(); // Parse the error response
                    alert(`Error booking service: ${errorData.error || 'Unknown error'}`); // Show specific error
                    return; // Exit the method
                }
                alert("Service booked successfully!");
                if (this.rebooked && this.serviceDetails.hasOwnProperty('serviceRequest_id')) {
                    console.log("from rebooked:", this.serviceDetails.serviceRequest_id)
                    const response = await fetch(`http://127.0.0.1:5000/service_requests/rebook/${this.serviceDetails.serviceRequest_id}`, {
                        method: "PUT",
                        headers: {
                            "Content-Type": "application/json",
                            Authorization: `Bearer ${localStorage.getItem("access_token")}`,
                        },
                        body: JSON.stringify({ status: "booked" }),
                    });
                    if (!response.ok) {
                        const errorData = await response.json(); // Parse the error response
                        alert(`Error updating existing service: ${errorData.error || 'Unknown error'}`); // Show specific error
                        return; // Exit the method
                    }
                }
                this.$emit('close');
            } catch (error) {
                console.error("Error booking service: ${error.message}");
                alert("An error occurred while booking the service.");
            }


        },
    },
    mounted() {
        this.fetchProfessionals(); // Fetch professionals on component mount
        this.resetForm();
    },
};
</script>

<style scoped>
.container {
    max-width: 600px;
    margin: auto;
}
</style>