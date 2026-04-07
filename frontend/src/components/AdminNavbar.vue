<template>
  <nav class="navbar">
    <div class="navbar-logo">
      <RouterLink to="/admin/dashboard">
        <img src="../assets/logo1.png" alt="Kala Logo" class="logo-img" v-if="hasLogo" @error="hasLogo = false" />
        <span class="brand-text">Kala</span>
      </RouterLink>
    </div>
    <div class="navbar-links">
      <RouterLink to="/admin/dashboard" active-class="router-link-active">Dashboard</RouterLink>
      <RouterLink to="/admin/verification" active-class="router-link-active">Verification</RouterLink>
      <RouterLink to="/admin/artists" active-class="router-link-active">Artists</RouterLink>
      <RouterLink to="/admin/buyers" active-class="router-link-active">Buyers</RouterLink>
      <RouterLink to="/admin/orders" active-class="router-link-active">Orders</RouterLink>
      <RouterLink to="/admin/analytics" active-class="router-link-active">Analytics</RouterLink>
      <a href="#" class="logout" @click.prevent="handleLogout">Logout</a>
    </div>
  </nav>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth.js'

const hasLogo = ref(true)
const router = useRouter()
const authStore = useAuthStore()

function handleLogout() {
  authStore.logout()
  router.push('/auth/login')
}
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
  border-radius: 4px;
  object-fit: contain;
}

.brand-text {
  font-style: italic;
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
</style>