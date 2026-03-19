<template>
  <div>
    <BuyerNavbar />
    <div class="page-container">
      <h1 class="page-title">Your Cart</h1>

      <div class="cart-layout" v-if="cartState.items.length > 0">
        <!-- Cart Items List -->
        <div class="cart-items">
          <div v-for="item in cartState.items" :key="item.id" class="cart-card">
            <div class="item-img" :style="{ backgroundImage: `url(${item.image})` }"></div>
            <div class="item-details">
              <h3 class="item-title">{{ item.title }}</h3>
              <p class="item-artist">{{ item.artist }}</p>
              <div class="item-actions">
                <div class="quantity-controls">
                  <button @click="cartState.updateQuantity(item.id, -1)">-</button>
                  <span>{{ item.quantity }}</span>
                  <button @click="cartState.updateQuantity(item.id, 1)">+</button>
                </div>
                <button class="remove-btn" @click="cartState.removeItem(item.id)">Remove</button>
              </div>
            </div>
            <div class="item-price">
              ₹{{ (item.price * item.quantity).toLocaleString('en-IN') }}
            </div>
          </div>
        </div>

        <!-- Order Summary -->
        <div class="order-summary">
          <h2>Order Summary</h2>
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
            <span>Total</span>
            <span>₹{{ cartTotal.toLocaleString('en-IN') }}</span>
          </div>
          <RouterLink to="/buyer/checkout" class="checkout-btn" style="display:block; text-decoration:none; text-align:center;">Proceed to Checkout</RouterLink>
          
          <div class="secure-badge">
            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="11" width="18" height="11" rx="2" ry="2"></rect><path d="M7 11V7a5 5 0 0 1 10 0v4"></path></svg>
            Secure Checkout
          </div>
        </div>
      </div>

      <!-- Empty State -->
      <div v-else class="empty-cart">
        <div class="empty-icon">🛒</div>
        <h2>Your cart is empty</h2>
        <p>Looks like you haven't added anything to your cart yet.</p>
        <RouterLink to="/buyer/products" class="continue-shopping">Browse Catalogue</RouterLink>
      </div>

    </div>
  </div>
</template>

<script setup>
import BuyerNavbar from '../../components/BuyerNavbar.vue'
import { cartState, cartSubtotal, cartTotal } from '../../store/cart.js'
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

.cart-layout {
  display: flex;
  gap: 40px;
  align-items: flex-start;
}

.cart-items {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.cart-card {
  display: flex;
  background: #ffffff;
  border-radius: 8px;
  padding: 20px;
  border: 1px solid #e8e0d8;
  gap: 24px;
}

.item-img {
  width: 120px;
  height: 120px;
  border-radius: 6px;
  background-size: cover;
  background-position: center;
  flex-shrink: 0;
}

.item-details {
  flex: 1;
  display: flex;
  flex-direction: column;
}

.item-artist {
  font-size: 11px;
  color: #888;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  margin-bottom: 6px;
}

.item-title {
  font-family: 'Playfair Display', serif;
  font-size: 18px;
  font-weight: 600;
  color: #000;
  margin-bottom: 24px;
  margin-top:0;
}

.item-actions {
  display: flex;
  align-items: center;
  gap: 16px;
  margin-top: auto;
}

.quantity-controls {
  display: flex;
  align-items: center;
  gap: 12px;
}

.quantity-controls button {
  background: white;
  border: 1px solid #ccc;
  width: 28px;
  height: 28px;
  border-radius: 4px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  font-size: 14px;
}

.quantity-controls button:hover {
  border-color: #C4622D;
  color: #C4622D;
}

.quantity-controls span {
  font-weight: 600;
  font-size: 14px;
}

.remove-btn {
  font-family: 'DM Sans', sans-serif;
  background: transparent;
  border: none;
  font-size: 13px;
  color: #d94242;
  cursor: pointer;
  margin-left: 16px;
  font-weight: 500;
  padding: 0;
}

.remove-btn:hover {
  text-decoration: underline;
}

.item-price {
  text-align: right;
  font-family: 'Playfair Display', serif;
  font-size: 20px;
  font-weight: 600;
  color: #000;
  display: flex;
  flex-direction: column;
  align-items: flex-end;
}

/* Summary Styles */
.order-summary {
  width: 360px;
  background: #fdfaf8;
  border-radius: 8px;
  padding: 32px;
  border: 1px solid #f0e6e0;
  position: sticky;
  top: 80px;
}

.order-summary h2 {
  font-family: 'Playfair Display', serif;
  font-size: 22px;
  font-weight: 600;
  color: #000;
  margin-bottom: 24px;
  margin-top:0;
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

.checkout-btn {
  width: 100%;
  background: #C4622D;
  color: white;
  border: none;
  padding: 14px;
  border-radius: 6px;
  font-family: 'DM Sans', sans-serif;
  font-size: 15px;
  font-weight: 600;
  cursor: pointer;
  transition: background 0.2s;
  margin-bottom: 16px;
}

.checkout-btn:hover {
  background: #a95224;
}

.secure-badge {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  font-size: 12px;
  color: #888;
}

/* Empty State */
.empty-cart {
  text-align: center;
  padding: 80px 0;
}

.empty-icon {
  font-size: 48px;
  margin-bottom: 16px;
  opacity: 0.5;
}

.empty-cart h2 {
  font-family: 'Playfair Display', serif;
  font-size: 24px;
  color: #000;
  margin-bottom: 12px;
}

.empty-cart p {
  color: #666;
  margin-bottom: 32px;
}

.continue-shopping {
  display: inline-block;
  background: #C4622D;
  color: white;
  text-decoration: none;
  padding: 12px 24px;
  border-radius: 4px;
  font-weight: 600;
  transition: background 0.2s;
}

.continue-shopping:hover {
  background: #a95224;
}
</style>
