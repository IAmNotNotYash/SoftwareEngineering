<template>
  <nav class="navbar">
    <div class="navbar-logo">
      <RouterLink to="/buyer/dashboard"><i>Kala</i> <span class="badge">BUYER</span></RouterLink>
    </div>
    <div class="navbar-links">
      <RouterLink to="/buyer/dashboard" active-class="router-link-active">Dashboard</RouterLink>
      <RouterLink to="/buyer/products" active-class="router-link-active">Products</RouterLink>
      <RouterLink to="/buyer/orders" active-class="router-link-active">Orders</RouterLink>
      <RouterLink to="/buyer/cart" active-class="router-link-active" class="cart-link">
        Cart <span class="cart-count" v-if="cartTotalItems > 0">{{ cartTotalItems }}</span>
      </RouterLink>
      <a href="#" class="logout">Logout</a>
    </div>
  </nav>
</template>

<script setup>
import { computed } from 'vue'
import { cartState } from '../store/cart.js'

const cartTotalItems = computed(() => {
  return cartState.items.reduce((sum, item) => sum + item.quantity, 0)
})
</script>

<style scoped>
.navbar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 40px;
  height: 56px;
  background: #ffffff;
  border-bottom: 1px solid #e8e0d8;
  position: sticky;
  top: 0;
  z-index: 100;
}

.navbar-logo a {
  font-family: 'Playfair Display', serif;
  font-size: 22px;
  color: #C4622D;
  font-weight: 600;
  letter-spacing: 0.5px;
  text-decoration: none;
  display: flex;
  align-items: baseline;
  gap: 8px;
}

.badge {
  font-family: 'DM Sans', sans-serif;
  font-size: 10px;
  font-weight: 600;
  background: #fdf2ed;
  color: #C4622D;
  padding: 2px 6px;
  border-radius: 4px;
  letter-spacing: 0.5px;
  vertical-align: middle;
}

.navbar-links {
  display: flex;
  align-items: center;
  gap: 28px;
}

.navbar-links a {
  text-decoration: none;
  font-size: 14px;
  color: #555;
  font-family: 'DM Sans', sans-serif;
}

.navbar-links a:hover {
  color: #C4622D;
}

.navbar-links a.router-link-active {
  color: #C4622D;
  font-weight: 600;
}

.navbar-links .logout {
  color: #888;
}

.navbar-links .logout:hover {
  color: #C4622D;
}

.cart-link {
  position: relative;
  display: flex;
  align-items: center;
  gap: 6px;
}

.cart-count {
  background: #C4622D;
  color: white;
  font-size: 11px;
  font-weight: 600;
  padding: 2px 6px;
  border-radius: 10px;
}
</style>
