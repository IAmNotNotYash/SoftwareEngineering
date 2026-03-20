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
              <input type="text" placeholder="Full Name" class="form-input" />
              <textarea placeholder="Complete Address" class="form-input" rows="3"></textarea>
              <div class="input-row">
                <input type="text" placeholder="City" class="form-input" />
                <input type="text" placeholder="PIN Code" class="form-input" />
              </div>
            </div>
          </div>

          <!-- Payment Options -->
          <div class="form-section">
            <h2 class="section-title">2. Payment Method</h2>
            <div class="payment-options">
              <label class="radio-card" :class="{ active: selectedPayment === 'card' }">
                <input type="radio" v-model="selectedPayment" value="card" name="payment" />
                <div class="card-content">
                  <div class="card-title">Credit / Debit Card</div>
                  <div class="card-desc">Visa, MasterCard, RuPay</div>
                </div>
              </label>

              <label class="radio-card" :class="{ active: selectedPayment === 'upi' }">
                <input type="radio" v-model="selectedPayment" value="upi" name="payment" />
                <div class="card-content">
                  <div class="card-title">UPI</div>
                  <div class="card-desc">Google Pay, PhonePe, Paytm</div>
                </div>
              </label>
            </div>

            <!-- Card Form (Conditional) -->
            <div v-if="selectedPayment === 'card'" class="new-address-form">
              <input type="text" placeholder="Card Number" class="form-input" />
              <div class="input-row">
                <input type="text" placeholder="MM/YY" class="form-input" />
                <input type="text" placeholder="CVV" class="form-input" />
              </div>
            </div>
            <!-- UPI Form (Conditional) -->
            <div v-if="selectedPayment === 'upi'" class="new-address-form">
              <input type="text" placeholder="Enter UPI ID (e.g., name@bank)" class="form-input" />
            </div>
          </div>
        </div>

        <!-- Right Column: Order Summary -->
        <div class="order-summary">
          <h2>Order Summary</h2>
          <div class="cart-preview">
            <div v-for="item in cartState.items" :key="item.id" class="preview-item">
              <span>{{ item.quantity }}x {{ item.title }}</span>
              <span>₹{{ (item.price * item.quantity).toLocaleString('en-IN') }}</span>
            </div>
          </div>
          
          <div class="summary-divider"></div>

          <div class="summary-row">
            <span>Subtotal</span>
            <span>₹{{ cartSubtotal.toLocaleString('en-IN') }}</span>
          </div>
          <div class="summary-row">
            <span>Shipping</span>
            <span>₹{{ cartState.shipping.toLocaleString('en-IN') }}</span>
          </div>
          <div class="summary-divider"></div>
          <div class="summary-row total-row">
            <span>Amount Payable</span>
            <span>₹{{ cartTotal.toLocaleString('en-IN') }}</span>
          </div>
          
          <button class="place-order-btn" @click="handleCheckout" :disabled="cartState.items.length === 0">
            Pay & Place Order
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import BuyerNavbar from '../../components/BuyerNavbar.vue'
import { cartState, cartSubtotal, cartTotal } from '../../store/cart.js'

const selectedAddress = ref('home')
const selectedPayment = ref('card')
const orderPlaced = ref(false)

const handleCheckout = () => {
  if (cartState.items.length > 0) {
    // Simulate placing order
    setTimeout(() => {
      cartState.clearCart()
      orderPlaced.value = true
    }, 800)
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

.radio-card {
  display: flex;
  align-items: flex-start;
  gap: 16px;
  padding: 20px;
  border: 1px solid #e8e0d8;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.2s;
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
