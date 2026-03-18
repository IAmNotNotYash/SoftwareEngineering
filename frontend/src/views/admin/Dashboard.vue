<template>
  <div>
    <AdminNavbar />
    <div class="page-container">
      <h1 class="page-title">Platform Overview</h1>

      <div class="alert-banner" v-if="stats.pendingVerifications > 0">
        <span>{{ stats.pendingVerifications }} artist(s) awaiting verification.</span>
        <RouterLink to="/admin/verification" class="alert-link">Review Now</RouterLink>
      </div>

      <div class="kpi-grid">
        <div class="kpi-card">
          <div class="kpi-label">Total Revenue</div>
          <div class="kpi-value">₹{{ stats.totalRevenue?.toLocaleString('en-IN') }}</div>
        </div>
        <div class="kpi-card">
          <div class="kpi-label">Total Orders</div>
          <div class="kpi-value">{{ stats.totalOrders }}</div>
        </div>
        <div class="kpi-card">
          <div class="kpi-label">Registered Artists</div>
          <div class="kpi-value">{{ stats.registeredArtists }}</div>
        </div>
        <div class="kpi-card">
          <div class="kpi-label">Registered Buyers</div>
          <div class="kpi-value">{{ stats.registeredBuyers }}</div>
        </div>
        <div class="kpi-card">
          <div class="kpi-label">Pending Verifications</div>
          <div class="kpi-value">{{ stats.pendingVerifications }}</div>
        </div>
        <div class="kpi-card">
          <div class="kpi-label">Active Stories</div>
          <div class="kpi-value">{{ stats.activeStories }}</div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import AdminNavbar from '../../components/AdminNavbar.vue'
import { getDashboardStats } from '../../api/admin.js'

const stats = ref({})

onMounted(async () => {
  stats.value = await getDashboardStats()
})
</script>

<style scoped>
.alert-banner {
  display: flex;
  align-items: center;
  justify-content: space-between;
  background: #fef3cd;
  border: 1px solid #e8d89a;
  border-radius: 8px;
  padding: 14px 20px;
  margin-bottom: 32px;
  font-size: 14px;
  color: #7a5c00;
}

.alert-link {
  text-decoration: none;
  background: #ffffff;
  color: #1A1A1A;
  border: 1px solid #ccc;
  padding: 6px 14px;
  border-radius: 6px;
  font-size: 13px;
  font-weight: 500;
  transition: background 0.2s;
}

.alert-link:hover {
  background: #f5f5f5;
}

.kpi-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 20px;
}

.kpi-card {
  background: #ffffff;
  border-radius: 10px;
  padding: 24px;
  box-shadow: 0 1px 4px rgba(0, 0, 0, 0.07);
}

.kpi-label {
  font-size: 11px;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  color: #888;
  margin-bottom: 12px;
}

.kpi-value {
  font-family: 'Playfair Display', serif;
  font-size: 32px;
  color: #1A1A1A;
}
</style>