<template>
    <div class="container" style="float:left;">
        <form @submit.prevent="openPaymentModal">

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
            <button type="submit" class="btn btn-primary">Proceed to payment</button>
            
        </form>

        <!-- Payment Modal -->
        <div v-if="showPaymentModal" class="payment-modal">
            <div class="payment-content">
                <h4>Payment Details</h4><br>
                <h5>Price: </h5><p>Rs. {{price}}</p>
                <!-- Payment Method -->
                <div>
                    <label>
                        <input type="radio" value="card" v-model="paymentMethod" /> Card Payment
                    </label>
                    <label>
                        <input type="radio" value="upi" v-model="paymentMethod" /> UPI Payment
                    </label>
                </div>

                <!-- Card Payment Fields -->
                <div v-if="paymentMethod === 'card'" class="mt-3">
                    <div class="form-group">
                        <label for="cardNumber">Card Number</label>
                        <input type="text" id="cardNumber" v-model="cardDetails.cardNumber" class="form-control" />
                    </div>
                    <div class="form-group">
                        <label for="expiryDate">Expiry Date</label>
                        <input type="text" id="expiryDate" v-model="cardDetails.expiryDate" class="form-control" placeholder="MM/YY" />
                    </div>
                    <div class="form-group">
                        <label for="cvv">CVV</label>
                        <input type="password" id="cvv" v-model="cardDetails.cvv" class="form-control" />
                    </div>
                </div>

                <!-- UPI Payment Field -->
                <div v-if="paymentMethod === 'upi'" class="mt-3">
                    <div class="form-group">
                        <label for="upiId">UPI ID</label>
                        <input type="text" id="upiId" v-model="upiId" class="form-control" placeholder="example@upi" />
                    </div>
                </div>

                <!-- Action Buttons -->
                <div class="mt-3">
                    <button class="btn btn-success" @click="simulatePayment">Complete Payment</button>
                    <button class="btn btn-danger" @click="closePaymentModal">Cancel</button>
                </div>
            </div>
        </div>
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
            price: 0,
            showPaymentModal: false, // Payment modal visibility
            paymentMethod: '', // Selected payment method ('card' or 'upi')
            cardDetails: { // Card payment fields
                cardNumber: '',
                expiryDate: '',
                cvv: '',
            },
            upiId: '', // UPI ID
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
            this.dateOfRequest = null; 
            this.selectedProfessional = null; // Reset selection
            this.contactNumber = this.customerDetails?.mobile || ""; 
            this.remarks = ""; // Clear remarks
            this.price = this.serviceDetails?.price || 0;
            this.fetchProfessionals(); // Fetch professionals each time
        },
        openPaymentModal() {
            this.showPaymentModal = true; // Show payment modal
        },
        closePaymentModal() {
            this.showPaymentModal = false; // Hide modal
        },
        async simulatePayment() {
            // Simulate payment validation
            if (this.paymentMethod === 'card') {
                if (!this.cardDetails.cardNumber || !this.cardDetails.expiryDate || !this.cardDetails.cvv) {
                    alert("Please fill in all card details.");
                    return;
                }
                
            } else if (this.paymentMethod === 'upi') {
                if (!this.upiId) {
                    alert("Please enter your UPI ID.");
                    return;
                }
            } else {
                alert("Please select a payment method.");
                return;
            }

            // Simulate success
            alert("Payment successful!");
            this.closePaymentModal();
            await this.submitServiceRequest();
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
.payment-modal {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background-color: rgba(0, 0, 0, 0.5);
    display: flex;
    align-items: center;
    justify-content: center;
}

.payment-content {
    background: #fff;
    padding: 20px;
    border-radius: 5px;
    width: 400px;
    box-shadow: 0 0 10px rgba(0, 0, 0, 0.2);
    text-align: left;
}

.payment-content h4 {
    margin-bottom: 15px;
    text-align: center;
}

.payment-content .form-group {
    margin-bottom: 10px;
}

.payment-content .btn {
    margin: 5px 0;
    width: 100%;
}
</style>