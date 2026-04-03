<template>
  <nav class="navbar">
    <div class="navbar-logo">
      <RouterLink to="/buyer/dashboard">
        <img src="../assets/logo1.png" alt="Kala Logo" class="logo-img" v-if="hasLogo" @error="hasLogo = false" />
        
        <span class="brand-text">Kala</span>
      </RouterLink>
    </div>
    <div class="navbar-links">
      <RouterLink to="/buyer/dashboard" active-class="router-link-active">Dashboard</RouterLink>
      <RouterLink to="/buyer/products" active-class="router-link-active">Products</RouterLink>
      <RouterLink to="/buyer/following" active-class="router-link-active">Following</RouterLink>
      <RouterLink to="/buyer/orders" active-class="router-link-active">Orders</RouterLink>
      <RouterLink to="/buyer/cart" active-class="router-link-active" class="cart-link">
        Cart <span class="cart-count" v-if="cartTotalItems > 0">{{ cartTotalItems }}</span>
      </RouterLink>
      <RouterLink to="/buyer/profile" active-class="router-link-active" class="profile-link">Profile</RouterLink>
      <a href="#" class="logout" @click.prevent="logout">Logout</a>
    </div>
  </nav>
</template>

<script setup>
import { computed, ref } from 'vue'
import { useCartStore } from '../stores/cart.js'
import { useAuthStore } from '../stores/auth.js'
import { useRouter } from 'vue-router'

const cartStore = useCartStore()
const authStore = useAuthStore()
const router = useRouter()

const cartTotalItems = computed(() =>
  cartStore.items.reduce((sum, item) => sum + item.quantity, 0)
)

function logout() {
  authStore.logout()
  router.push('/auth/login')
}

const hasLogo = ref(true)
</script>

<style scoped>
.navbar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 60px;
  height: 72px;
  background: var(--color-nav-bg);
  backdrop-filter: blur(16px);
  -webkit-backdrop-filter: blur(16px);
  border-bottom: 1px solid rgba(232, 224, 216, 0.4);
  box-shadow: 0 4px 30px rgba(0, 0, 0, 0.03);
  position: sticky;
  top: 0;
  z-index: 100;
  transition: all 0.3s ease;
}

.navbar-logo a {
  font-family: 'Playfair Display', serif;
  font-size: 22px;
  color: #C4622D;
  font-weight: 600;
  letter-spacing: 0.5px;
  text-decoration: none;
  display: flex;
  align-items: center;
  gap: 8px;
}

.logo-img {
  height: 28px;
  width: auto;
  border-radius: 4px; /* Soften edges if the logo background is solid */
  object-fit: contain;
}

.brand-text {
  font-style: italic;
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
  color: #666;
  font-family: 'DM Sans', sans-serif;
  position: relative;
  font-weight: 500;
  padding: 6px 0;
  transition: color 0.3s ease;
}

.navbar-links a::after {
  content: '';
  position: absolute;
  width: 0;
  height: 2px;
  bottom: 0;
  left: 50%;
  background-color: #C4622D;
  transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
  transform: translateX(-50%);
  border-radius: 2px;
}

.navbar-links a:hover {
  color: #1a1a1a;
}
.navbar-links a:hover::after,
.navbar-links a.router-link-active::after {
  width: 100%;
}

.navbar-links a.router-link-active {
  color: #1a1a1a;
  font-weight: 600;
}

.navbar-links .logout {
  color: #999;
}

.navbar-links .logout:hover {
  color: #1a1a1a;
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
  font-size: 10px;
  font-weight: 700;
  padding: 3px 7px;
  border-radius: 12px;
  box-shadow: 0 2px 6px rgba(196, 98, 45, 0.3);
}
</style>
