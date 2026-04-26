<template>
  <div>
    <BuyerNavbar />
    <div class="page-container">
      <div v-if="orderPlaced" class="success-state">
        <div class="success-icon">✓</div>
        <h1 class="page-title">Order Confirmed!</h1>
        <p class="success-text">Thank you for supporting independent artists. Your order has been placed successfully.</p>
        <RouterLink to="/buyer/orders" class="success-btn">View My Orders</RouterLink>
      </div>

      <div v-else class="checkout-layout">
        <!-- Left Column: Forms -->
        <div class="checkout-forms">
          <h1 class="page-title">Secure Checkout</h1>
          
          <!-- Shipping Address -->
          <div class="form-section">
            <h2 class="section-title">1. Shipping Address</h2>
            <div class="address-options">
              <label class="radio-card" :class="{ active: selectedAddress === 'home' }">
                <input type="radio" v-model="selectedAddress" value="home" name="address" />
                <div class="card-content">
                  <div class="card-title">Home Address</div>
                  <div class="card-desc">
                    123 Artisan Valley<br/>
                    Craft District, Sector 4<br/>
                    Mumbai, Maharashtra
                  </div>
                </div>
              </label>
              
              <label class="radio-card" :class="{ active: selectedAddress === 'new' }">
                <input type="radio" v-model="selectedAddress" value="new" name="address" />
                <div class="card-content">
                  <div class="card-title">+ Add New Address</div>
                  <div class="card-desc">Ship to a different location</div>
                </div>
              </label>
            </div>

            <!-- New Address Form (Conditional) -->
            <div v-if="selectedAddress === 'new'" class="new-address-form">
              <input type="text" v-model="newAddress.fullAddress" placeholder="Complete Address" class="form-input" />
              <div class="input-row">
                <input type="text" v-model="newAddress.city" placeholder="City" class="form-input" />
                <input type="text" v-model="newAddress.state" placeholder="State" class="form-input" />
                <input type="text" v-model="newAddress.pinCode" placeholder="PIN Code" class="form-input" />
              </div>
            </div>
          </div>

          <!-- Payment Info -->
          <div class="form-section">
            <h2 class="section-title">2. Payment Method</h2>
            <div class="payment-info-card">
              <div class="card-content">
                <div class="card-title">Secure Online Payment</div>
                <div class="card-desc">
                  You will be redirected to our secure payment gateway (Razorpay) to pay via 
                  <strong>UPI, Cards, Netbanking or Wallets</strong>.
                </div>
              </div>
            </div>
          </div>

        </div>

        <!-- Right Column: Order Summary -->
        <div class="order-summary">
          <h2>Order Summary</h2>
          <div class="cart-preview">
            <div v-for="item in cartStore.items" :key="item.id" class="preview-item">
              <span>{{ item.quantity }}x {{ item.title }}</span>
              <span>₹{{ (item.price * item.quantity).toLocaleString('en-IN') }}</span>
            </div>
          </div>
          
          <div class="summary-divider"></div>

          <div class="summary-row">
            <span>Subtotal</span>
            <span>₹{{ cartStore.subtotal.toLocaleString('en-IN') }}</span>
          </div>
          <div class="summary-row">
            <span>Shipping</span>
            <span>₹{{ cartStore.shipping.toLocaleString('en-IN') }}</span>
          </div>
          <div class="summary-divider"></div>
          <div class="summary-row total-row">
            <span>Amount Payable</span>
            <span>₹{{ cartStore.total.toLocaleString('en-IN') }}</span>
          </div>
          
          <p v-if="statusMessage" style="color:#d94242; font-size:14px; margin-bottom:12px;">{{ statusMessage }}</p>
          <button class="place-order-btn" @click="handleCheckout" :disabled="cartStore.items.length === 0">
            Pay &amp; Place Order
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import BuyerNavbar from '../../components/BuyerNavbar.vue'
import { useCartStore } from '../../stores/cart.js'
import { useAuthStore } from '../../stores/auth.js'
import { placeOrder, verifyPayment } from '../../api/commerce.js'

const router = useRouter()
const cartStore = useCartStore()
const authStore = useAuthStore()

const selectedAddress = ref('home')
const orderPlaced = ref(false)
const statusMessage = ref('')

// New address form fields
const newAddress = ref({ fullAddress: '', city: '', state: '', pinCode: '' })

// Razorpay Script Loading
onMounted(() => {
  const script = document.createElement('script');
  script.src = 'https://checkout.razorpay.com/v1/checkout.js';
  script.async = true;
  document.body.appendChild(script);
})

async function handleCheckout() {
  if (cartStore.items.length === 0) return

  // Build shipping address snapshot
  let shipping_address_snapshot
  if (selectedAddress.value === 'home') {
    shipping_address_snapshot = {
      label: 'Home',
      full_address: '123 Artisan Valley, Craft District, Sector 4',
      city: 'Mumbai',
      state: 'Maharashtra',
      pin_code: '400032',
      country: 'India',
    }
  } else {
    if (!newAddress.value.fullAddress || !newAddress.value.city || !newAddress.value.pinCode) {
      statusMessage.value = 'Please fill in all address fields.'
      return
    }
    shipping_address_snapshot = {
      label: 'New Address',
      full_address: newAddress.value.fullAddress,
      city: newAddress.value.city,
      state: newAddress.value.state,
      pin_code: newAddress.value.pinCode,
      country: 'India',
    }
  }

  statusMessage.value = 'Preparing secure checkout...'
  
  try {
    // 1. Create order on backend to get Razorpay Order ID
    const orderData = await placeOrder({ 
      shipping_address: shipping_address_snapshot, 
      payment: { method: 'razorpay' } // Backend now expects this
    })

    if (!orderData.razorpay_order_id) {
      throw new Error("Could not initialize payment gateway.")
    }

    // 2. Open Razorpay Checkout Modal
    const options = {
      key: orderData.razorpay_key_id,
      amount: orderData.amount_paise,
      currency: "INR",
      name: "Kala Marketplace",
      description: "Payment for your artisanal order",
      order_id: orderData.razorpay_order_id,
      handler: async function (response) {
        // This runs if payment is successful at Razorpay level
        statusMessage.value = 'Verifying payment...'
        try {
          await verifyPayment(orderData.id, {
            razorpay_payment_id: response.razorpay_payment_id,
            razorpay_order_id: response.razorpay_order_id,
            razorpay_signature: response.razorpay_signature
          })
          
          await cartStore.clearCart()
          orderPlaced.value = true
        } catch (vErr) {
          statusMessage.value = "Payment verification failed. Please contact support."
          console.error(vErr)
        }
      },
      prefill: {
        name: authStore.user?.full_name || "",
        email: authStore.user?.email || "",
      },
      theme: {
        color: "#C4622D"
      },
      modal: {
        ondismiss: function() {
          statusMessage.value = "Checkout cancelled."
        }
      }
    };

    const rzp = new window.Razorpay(options);
    rzp.open();

  } catch (err) {
    statusMessage.value = err.message
    console.error("Checkout Error:", err)
  }
}
</script>

<style scoped>
.page-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 40px;
  font-family: 'DM Sans', sans-serif;
}

.page-title {
  font-family: 'Playfair Display', serif;
  font-size: 32px;
  font-weight: 600;
  color: #000;
  margin-bottom: 40px;
}

.checkout-layout {
  display: flex;
  gap: 60px;
  align-items: flex-start;
}

.checkout-forms {
  flex: 1.5;
}

.form-section {
  margin-bottom: 60px;
}

.section-title {
  font-family: 'Playfair Display', serif;
  font-size: 22px;
  font-weight: 600;
  color: #000;
  margin-bottom: 24px;
  border-bottom: 1px solid #e8e0d8;
  padding-bottom: 12px;
}

/* Radio Cards */
.address-options, .payment-options {
  display: flex;
  flex-direction: column;
  gap: 16px;
  margin-bottom: 24px;
}

.radio-card, .payment-info-card {
  display: flex;
  align-items: flex-start;
  gap: 16px;
  padding: 20px;
  border: 1px solid #e8e0d8;
  border-radius: 8px;
  transition: all 0.2s;
}

.radio-card {
  cursor: pointer;
}

.radio-card:hover {
  border-color: #C4622D;
}

.radio-card.active {
  border-color: #C4622D;
  background: #fdfaf8;
}

.radio-card input[type="radio"] {
  margin-top: 4px;
  accent-color: #C4622D;
}

.card-title {
  font-weight: 600;
  font-size: 16px;
  color: #000;
  margin-bottom: 6px;
}

.card-desc {
  font-size: 14px;
  color: #666;
  line-height: 1.5;
}

/* Forms */
.new-address-form {
  background: #f9f9f9;
  padding: 24px;
  border-radius: 8px;
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.form-input {
  width: 100%;
  padding: 12px 16px;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-family: 'DM Sans', sans-serif;
  font-size: 15px;
}

.form-input:focus {
  outline: none;
  border-color: #C4622D;
}

.input-row {
  display: flex;
  gap: 16px;
}

/* Summary Box */
.order-summary {
  flex: 1;
  background: #fdfaf8;
  border-radius: 8px;
  padding: 32px;
  border: 1px solid #f0e6e0;
  position: sticky;
  top: 40px;
}

.order-summary h2 {
  font-family: 'Playfair Display', serif;
  font-size: 22px;
  margin-bottom: 24px;
}

.cart-preview {
  display: flex;
  flex-direction: column;
  gap: 12px;
  margin-bottom: 20px;
}

.preview-item {
  display: flex;
  justify-content: space-between;
  font-size: 14px;
  color: #555;
}

.summary-row {
  display: flex;
  justify-content: space-between;
  margin-bottom: 16px;
  font-size: 14px;
  color: #555;
}

.summary-divider {
  height: 1px;
  background: #e8e0d8;
  margin: 20px 0;
}

.total-row {
  font-size: 18px;
  font-weight: 600;
  color: #000;
  margin-bottom: 32px;
}

.place-order-btn {
  width: 100%;
  background: #C4622D;
  color: white;
  border: none;
  padding: 16px;
  border-radius: 6px;
  font-family: 'DM Sans', sans-serif;
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
  transition: background 0.2s;
}

.place-order-btn:hover {
  background: #a95224;
}

.place-order-btn:disabled {
  background: #ccc;
  cursor: not-allowed;
}

/* Success State */
.success-state {
  text-align: center;
  padding: 100px 0;
}

.success-icon {
  width: 80px;
  height: 80px;
  border-radius: 50%;
  background: #d4edda;
  color: #155724;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 40px;
  margin: 0 auto 32px auto;
}

.success-text {
  font-size: 18px;
  color: #555;
  margin-bottom: 40px;
}

.success-btn {
  display: inline-block;
  background: #C4622D;
  color: white;
  text-decoration: none;
  padding: 14px 28px;
  border-radius: 4px;
  font-weight: 600;
  font-size: 16px;
}

.success-btn:hover {
  background: #a95224;
}
</style>
