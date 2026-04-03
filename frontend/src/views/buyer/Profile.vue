<template>
  <BuyerNavbar />
  <div class="profile-page">
    <div class="header">
      <h1>My Profile</h1>
      <p>Your account information on the Kala platform.</p>
    </div>

    <div class="profile-content">
      <!-- Personal Info Section -->
      <section class="profile-section">
        <h2>Personal Information</h2>
        <div class="info-grid">
          <div class="info-group">
            <label>Full Name</label>
            <p>{{ user?.name || '—' }}</p>
          </div>
          <div class="info-group">
            <label>Email Address</label>
            <p>{{ user?.email || '—' }}</p>
          </div>
          <div class="info-group">
            <label>Account Type</label>
            <p style="text-transform: capitalize;">{{ user?.role || '—' }}</p>
          </div>
        </div>
      </section>

      <!-- Stats Section -->
      <section class="profile-section">
        <h2>My Activity</h2>
        <div class="kpi-grid">
          <div class="kpi-card">
            <div class="kpi-label">Items in Cart</div>
            <div class="kpi-value">{{ cartStore.items.length }}</div>
          </div>
          <div class="kpi-card">
            <div class="kpi-label">Total Orders</div>
            <div class="kpi-value">{{ orderCount }}</div>
          </div>
        </div>
      </section>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import BuyerNavbar from '../../components/BuyerNavbar.vue'
import { useAuthStore } from '../../stores/auth.js'
import { useCartStore } from '../../stores/cart.js'
import { getOrders } from '../../api/commerce.js'

const authStore = useAuthStore()
const cartStore = useCartStore()

const user = computed(() => authStore.user)
const orderCount = ref('—')


onMounted(async () => {
  await cartStore.loadCart()
  try {
    const data = await getOrders()
    const orders = Array.isArray(data) ? data : (data.orders || [])
    orderCount.value = orders.length
  } catch {
    orderCount.value = 0
  }
})
</script>

<style scoped>
.profile-page {
  padding: 40px;
  max-width: 900px;
  margin: 0 auto;
  font-family: 'DM Sans', sans-serif;
}

.header {
  margin-bottom: 40px;
}

.header h1 {
  font-family: 'Playfair Display', serif;
  font-size: 36px;
  color: #2D2A26;
  margin-bottom: 12px;
}

.header p {
  color: #666;
  font-size: 16px;
}

.loading-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 80px 0;
  color: #666;
}

.spinner {
  width: 40px;
  height: 40px;
  border: 3px solid #f3f3f3;
  border-top: 3px solid #C4622D;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin-bottom: 16px;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.profile-content {
  display: flex;
  flex-direction: column;
  gap: 32px;
}

.profile-section {
  background: white;
  border-radius: 12px;
  padding: 32px;
  border: 1px solid #eee;
  box-shadow: 0 4px 12px rgba(0,0,0,0.02);
}

.profile-section h2 {
  font-family: 'Playfair Display', serif;
  font-size: 24px;
  color: #2D2A26;
  margin-bottom: 24px;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
}

.section-header h2 {
  margin-bottom: 0;
}

.edit-btn {
  background: none;
  border: none;
  color: #C4622D;
  font-weight: 600;
  font-family: 'DM Sans', sans-serif;
  cursor: pointer;
  font-size: 14px;
}

.edit-btn:hover {
  text-decoration: underline;
}

.info-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 28px;
}

.info-group label {
  display: block;
  font-size: 12px;
  font-weight: 600;
  color: #888;
  margin-bottom: 8px;
  text-transform: uppercase;
  letter-spacing: 0.8px;
}

.info-group p {
  font-size: 16px;
  color: #2D2A26;
  font-weight: 500;
}

.address-card, .payment-card {
  background: #fcfcfc;
  padding: 24px;
  border-radius: 8px;
  border: 1px solid #eee;
}

.address-card p {
  color: #444;
  line-height: 1.6;
  margin-bottom: 4px;
}

.address-card p:last-child {
  margin-bottom: 0;
}

.payment-card {
  display: flex;
  align-items: center;
  gap: 20px;
}

.card-icon {
  font-size: 32px;
}

.card-number {
  font-weight: 600;
  color: #2D2A26;
  margin-bottom: 6px;
  font-size: 16px;
}

.card-expiry {
  font-size: 14px;
  color: #888;
}

.text-highlight {
  color: #C4622D;
}

.kpi-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 20px;
}

.kpi-card {
  background: #faf8f5;
  border-radius: 8px;
  padding: 20px;
  border: 1px solid #f0f0f0;
  text-align: center;
}

.kpi-label {
  font-family: 'DM Sans', sans-serif;
  font-size: 11px;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  color: #888;
  margin-bottom: 8px;
  font-weight: 600;
}

.kpi-value {
  font-family: 'Playfair Display', serif;
  font-size: 28px;
  color: #2D2A26;
  font-weight: 600;
}

@media (max-width: 768px) {
  .info-grid {
    grid-template-columns: 1fr;
  }
  .kpi-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}
</style>
