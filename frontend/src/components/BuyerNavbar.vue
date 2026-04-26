<template>
  <nav class="navbar">
    <div class="navbar-logo">
      <RouterLink to="/buyer/dashboard">
        <img src="../assets/logo1.png" alt="Kala Logo" class="logo-img" v-if="hasLogo" @error="hasLogo = false" />
        
        <span class="brand-text">Kala</span>
      </RouterLink>
    </div>
    <div class="navbar-links" v-if="authStore.user">
      <RouterLink to="/buyer/dashboard" active-class="router-link-active">Dashboard</RouterLink>
      <RouterLink to="/buyer/explore" active-class="router-link-active">Explore</RouterLink>
      <RouterLink to="/buyer/following" active-class="router-link-active">Following</RouterLink>
      <RouterLink to="/buyer/orders" active-class="router-link-active">Orders</RouterLink>
      <RouterLink to="/buyer/cart" active-class="router-link-active" class="cart-link">
        Cart <span class="cart-badge" v-if="cartTotalItems > 0">{{ cartTotalItems }}</span>
      </RouterLink>
      <RouterLink to="/buyer/profile" active-class="router-link-active" class="profile-link">
        <div v-if="authStore.user?.profile_image_url" class="nav-avatar" :style="{ backgroundImage: `url(${getImageUrl(authStore.user.profile_image_url)})` }"></div>
        <div v-else class="nav-avatar-placeholder">{{ (authStore.user?.name || 'U').charAt(0) }}</div>
        Profile
      </RouterLink>
      <a href="#" class="logout" @click.prevent="logout">Logout</a>
    </div>
    <div class="navbar-links" v-else>
      <RouterLink to="/auth/login" class="login-btn">Login</RouterLink>
      <RouterLink to="/auth/register" class="signup-btn">Sign Up</RouterLink>
    </div>
  </nav>
</template>

<script setup>
import { computed, ref, onMounted } from 'vue'
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

const getImageUrl = (url) => {
  if (!url) return ''
  return url.startsWith('http') ? url : `http://127.0.0.1:5000${url}`
}

onMounted(() => {
  authStore.refreshUser()
})
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

.signup-btn {
  background: #C4622D !important;
  color: white !important;
  padding: 8px 16px !important;
  border-radius: 6px;
}

.signup-btn::after {
  display: none;
}

.login-btn {
  color: #666 !important;
}

.login-btn:hover {
  color: #C4622D !important;
}

.profile-link {
  display: flex;
  align-items: center;
  gap: 8px;
}

.nav-avatar {
  width: 24px;
  height: 24px;
  border-radius: 50%;
  background-size: cover;
  background-position: center;
  border: 1px solid #e8e0d8;
}

.nav-avatar-placeholder {
  width: 24px;
  height: 24px;
  border-radius: 50%;
  background: #fdf2ed;
  color: #C4622D;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 11px;
  font-weight: 700;
  border: 1px solid #e8e0d8;
}
.cart-badge {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  background: #C4622D;
  color: #fff;
  font-size: 10px;
  font-weight: 700;
  min-width: 18px;
  height: 18px;
  padding: 0 4px;
  border-radius: 10px;
  margin-left: 6px;
  vertical-align: middle;
  transition: transform 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275);
}

.cart-link:hover .cart-badge {
  transform: scale(1.1);
}
</style>
