<template>
  <BuyerNavbar />
  <div class="profile-page">
    <div class="header">
      <h1>My Profile</h1>
      <p>Manage your personal information and shipping details.</p>
    </div>

    <div v-if="loading" class="loading-state">
      <div class="spinner"></div>
      <p>Loading your profile...</p>
    </div>

    <div v-else class="profile-content">
      <!-- Personal Info Section -->
      <section class="profile-section">
        <h2>Personal Information</h2>
        <div class="info-grid">
          <div class="info-group">
            <label>Full Name</label>
            <p>{{ profile.name }}</p>
          </div>
          <div class="info-group">
            <label>Email Address</label>
            <p>{{ profile.email }}</p>
          </div>
          <div class="info-group">
            <label>Phone Number</label>
            <p>{{ profile.phone }}</p>
          </div>
          <div class="info-group">
            <label>Member Since</label>
            <p>{{ profile.joinDate }}</p>
          </div>
        </div>
      </section>

      <!-- Stats Section -->
      <section class="profile-section">
        <h2>My Activity</h2>
        <div class="kpi-grid">
          <div class="kpi-card">
            <div class="kpi-label">Followed Artists</div>
            <div class="kpi-value">{{ stats.followedArtists || 0 }}</div>
          </div>
          <div class="kpi-card">
            <div class="kpi-label">Favorite Products</div>
            <div class="kpi-value">{{ stats.favoriteProducts || 0 }}</div>
          </div>
          <div class="kpi-card">
            <div class="kpi-label">Recent Orders</div>
            <div class="kpi-value">{{ stats.recentOrders || 0 }}</div>
          </div>
          <div class="kpi-card">
            <div class="kpi-label">Upcoming Deliveries</div>
            <div class="kpi-value text-highlight">{{ stats.upcomingDeliveries || 0 }}</div>
          </div>
        </div>
      </section>

      <!-- Shipping Address Section -->
      <section class="profile-section">
        <div class="section-header">
          <h2>Default Shipping Address</h2>
          <button class="edit-btn">Edit</button>
        </div>
        <div class="address-card">
          <p>{{ profile.shipping.address }}</p>
          <p>{{ profile.shipping.city }}, {{ profile.shipping.state }} {{ profile.shipping.zip }}</p>
          <p>{{ profile.shipping.country }}</p>
        </div>
      </section>

      <!-- Payment Method Section -->
      <section class="profile-section">
        <div class="section-header">
          <h2>Payment Method</h2>
          <button class="edit-btn">Edit</button>
        </div>
        <div class="payment-card">
          <div class="card-icon">💳</div>
          <div class="card-details">
            <p class="card-number">{{ profile.payment.cardType }} ending in •••• {{ profile.payment.last4 }}</p>
            <p class="card-expiry">Expires {{ profile.payment.expiry }}</p>
          </div>
        </div>
      </section>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { getBuyerProfile, getDashboardStats } from '../../api/buyer.js'
import BuyerNavbar from '../../components/BuyerNavbar.vue'

const profile = ref(null)
const stats = ref(null)
const loading = ref(true)

onMounted(async () => {
  const [profileData, statsData] = await Promise.all([
    getBuyerProfile(),
    getDashboardStats()
  ])
  profile.value = profileData
  stats.value = statsData
  loading.value = false
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
