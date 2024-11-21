<template>
    <div class="container" style="float:left;">
        <form @submit.prevent="openPaymentModal">
            <div class="form-group mb-3 row">
                <label for="serviceName" class="col-sm-6 col-form-label left-align">Service Name</label>
                <div class="col-sm-6">
                    <input type="text" id="serviceName" class="form-control" v-model="serviceName" disabled />
                </div>
            </div>

            <div class="form-group mb-3 row">
                <label for="address" class="col-sm-6 col-form-label">Your Address</label>
                <div class="col-sm-6">
                    <input type="text" id="address" class="form-control" v-model="customerAddress" disabled />
                </div>
            </div>

            <div class="form-group mb-3 row">
                <label for="pincode" class="col-sm-6 col-form-label">Your Pincode</label>
                <div class="col-sm-6">
                    <input type="text" id="pincode" class="form-control" v-model="customerPincode" disabled />
                </div>
            </div>

            <div class="form-group mb-3 row">
                <label for="contactNumber" class="col-sm-6 col-form-label">Your Contact Number</label>
                <div class="col-sm-6">
                    <input type="tel" id="contactNumber" class="form-control" v-model="contactNumber" disabled />
                </div>
            </div>

            <div class="form-group mb-3 row">
                <label for="dateOfRequest" class="col-sm-6 col-form-label">Date of Request</label>
                <div class="col-sm-6">
                    <input type="datetime-local" id="dateOfRequest" class="form-control" v-model="dateOfRequest" required />
                    <span v-if="errors.dateOfRequest" class="text-danger">{{ errors.dateOfRequest }}</span>
                </div>
            </div>

            <div class="form-group mb-3 row">
                <label for="professional" class="col-sm-6 col-form-label">Available Professionals</label>
                <div class="col-sm-6">
                    <select id="professional" class="form-control" v-model="selectedProfessional" required>
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
                <h5>Price: </h5>
                <p>Rs. {{ price }}</p>

                <!-- Payment Method -->
                <div>
                    <label>
                        <input type="radio" value="card" v-model="paymentMethod" /> Card Payment
                    </label>
                    <label>
                        <input type="radio" value="upi" v-model="paymentMethod" /> UPI Payment
                    </label>
                </div>

                <!-- Validation Errors -->
                <p v-if="errorMessage" class="error text-danger">{{ errorMessage }}</p>

                <!-- Card Payment Fields -->
                <div v-if="paymentMethod === 'card'" class="mt-3">
                    <div class="form-group">
                        <label for="cardNumber">Card Number</label>
                        <input type="text" id="cardNumber" v-model="cardDetails.cardNumber" class="form-control"
                            placeholder="Enter 16-digit card number" />
                        <p v-if="errors.cardNumber" class="error text-danger">{{ errors.cardNumber }}</p>
                    </div>
                    <div class="form-group">
                        <label for="expiryDate">Expiry Date</label>
                        <input type="text" id="expiryDate" v-model="cardDetails.expiryDate" class="form-control"
                            placeholder="MM/YY" />
                        <p v-if="errors.expiryDate" class="error text-danger">{{ errors.expiryDate }}</p>
                    </div>

                    <div class="form-group">
                        <label for="cvv">CVV</label>
                        <input type="password" id="cvv" v-model="cardDetails.cvv" class="form-control"
                            placeholder="Enter 3-digit CVV" />
                        <p v-if="errors.cvv" class="error text-danger">{{ errors.cvv }}</p>
                    </div>
                </div>

                <!-- UPI Payment Field -->
                <div v-if="paymentMethod === 'upi'" class="mt-3">
                    <div class="form-group">
                        <label for="upiId">UPI ID</label>
                        <input type="text" id="upiId" v-model="upiId" class="form-control" placeholder="example@upi" />
                        <p v-if="errors.upiId" class="error text-danger">{{ errors.upiId }}</p>
                    </div>
                </div>

                <!-- Action Buttons -->
                <div class="mt-3">
                    <button class="btn btn-success" @click="validatePayment">Complete Payment</button>
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
            serviceName: '',
            customerAddress: '',
            customerPincode: '',
            dateOfRequest: '',
            professionals: [],
            selectedProfessional: null,
            contactNumber: "", // Customer's contact number
            remarks: "",
            price: 0,
            showPaymentModal: false, // Payment modal visibility
            paymentMethod: '', // Selected payment method ('card' or 'upi')
            cardDetails: { // Card payment fields
                cardNumber: '',
                expiryDate: '',
                cvv: '',
            },
            upiId: '', // UPI ID
            errors: {}, // For payment validation errors
            errorMessage: "",
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
            const selectedDate = new Date(this.dateOfRequest);
            const currentDate = new Date();

            if (selectedDate <= currentDate) {
                this.errors.dateOfRequest = "The date and time must be in the future.";
                return;
            }
            else{
                this.showPaymentModal = true; // Show payment modal
            }
        },
        closePaymentModal() {
            this.showPaymentModal = false; // Hide modal
        },
        async validatePayment() {
            this.errors = {}; // Reset errors
            let valid = true;

            // Validate card details if payment method is "card"
            if (this.paymentMethod === "card") {
                if (!/^\d{16}$/.test(this.cardDetails.cardNumber)) {
                    this.errors.cardNumber = "Card number must be 16 digits.";
                    valid = false;
                }
                if (!/^\d{2}\/\d{2}$/.test(this.cardDetails.expiryDate)) {
                    this.errors.expiryDate = "Expiry date must be in MM/YY format.";
                    valid = false;
                } else {
                    const [month, year] = this.cardDetails.expiryDate.split("/").map(Number);
                    const currentYear = new Date().getFullYear() % 100; // Get last two digits of the current year
                    const currentMonth = new Date().getMonth() + 1; // Months are zero-based
                    
                    if (month < 1 || month > 12) {
                        this.errors.expiryDate = "Month must be between 01 and 12.";
                        valid = false;
                    } else if (year < currentYear || (year === currentYear && month < currentMonth)) {
                        this.errors.expiryDate = "Expiry date cannot be in the past.";
                        valid = false;
                    }
                }
                if (!/^\d{3}$/.test(this.cardDetails.cvv)) {
                    this.errors.cvv = "CVV must be 3 digits.";
                    valid = false;
                }
            } else if (this.paymentMethod === "upi") {
                // Validate UPI ID if payment method is "upi"
                if (!/^[a-zA-Z0-9.\-_]+@[a-zA-Z]+$/.test(this.upiId)) {
                    this.errors.upiId = "Invalid UPI ID format.";
                    valid = false;
                }
            } else {
                this.errorMessage = "Please select a payment method.";
                valid = false;
            }

            if (!valid) return;

            // Simulate payment success
            alert("Payment successful!");
            this.closePaymentModal();
            this.submitServiceRequest();
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