<template>
  <div>
    <ArtistNavbar />
    <div class="profile-page">
      <div class="header">
        <div class="brand-badge">Artist Profile</div>
        <h1>{{ user?.brandName || user?.name }}</h1>
        <p>Manage your artisan identity and track your platform performance.</p>
      </div>

      <div class="profile-content">
        <!-- Brand Info Section -->
        <section class="profile-section">
          <div class="section-header">
            <h2>Brand Information</h2>
            <button class="edit-btn">Edit Details</button>
          </div>
          <div class="info-grid">
            <div class="info-group">
              <label>Artist Name</label>
              <p>{{ user?.name || '—' }}</p>
            </div>
            <div class="info-group">
              <label>Brand / Studio Name</label>
              <p class="brand-text">{{ user?.brandName || '—' }}</p>
            </div>
            <div class="info-group">
              <label>Email Address</label>
              <p>{{ user?.email || '—' }}</p>
            </div>
            <div class="info-group">
              <label>Verification Status</label>
              <p :class="['status-badge', verificationStatus]">
                {{ verificationStatus.toUpperCase() || 'LOADING...' }}
              </p>
            </div>
          </div>
        </section>

        <!-- Stats Section -->
        <section class="profile-section">
          <h2>Business Performance</h2>
          <div class="kpi-grid">
            <div class="kpi-card">
              <div class="kpi-label">Active Products</div>
              <div class="kpi-value">{{ stats.products }}</div>
            </div>
            <div class="kpi-card">
              <div class="kpi-label">Total Orders</div>
              <div class="kpi-value">{{ stats.orders }}</div>
            </div>
            <div class="kpi-card">
              <div class="kpi-label">Live Catalogues</div>
              <div class="kpi-value">{{ stats.catalogues }}</div>
            </div>
            <div class="kpi-card">
              <div class="kpi-label">Member Since</div>
              <div class="kpi-value" style="font-size: 16px; margin-top: 10px;">April 2024</div>
            </div>
          </div>
        </section>

        <!-- About Section -->
        <section class="profile-section">
          <h2>About the Artist</h2>
          <p class="about-text">
            This section describes your artistic journey and the philosophy behind your craft.
            Click 'Edit Details' above to update your public biography.
          </p>
        </section>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import ArtistNavbar from '../../components/ArtistNavbar.vue'
import { useAuthStore } from '../../stores/auth.js'
import { getProducts, getOrders } from '../../api/commerce.js'
import { getCatalogues } from '../../api/catalogue.js'

const authStore = useAuthStore()
const user = computed(() => authStore.user)

const verificationStatus = ref('approved') // Dummy for now, would come from backend
const stats = ref({
  products: 0,
  orders: 0,
  catalogues: 0
})

onMounted(async () => {
  try {
    // Fetch Artist Stats
    // 1. Products count
    const productsData = await getProducts()
    // getProducts returns all but the API often handles filtering by artist_id in backend if needed
    // or we can filter locally for the artist dashboard feel
    const artistProducts = Array.isArray(productsData) ? productsData : productsData.products || []
    stats.value.products = artistProducts.length

    // 2. Orders count
    const ordersData = await getOrders()
    const artistOrders = Array.isArray(ordersData) ? ordersData : ordersData.orders || []
    stats.value.orders = artistOrders.length

    // 3. Catalogues count
    const cataloguesData = await getCatalogues({ status: 'live' })
    const artistCatalogues = cataloguesData.catalogues || []
    stats.value.catalogues = artistCatalogues.length
  } catch (err) {
    console.error("Failed to load artist stats", err)
  }
})
</script>

<style scoped>
.profile-page {
  padding: 60px 40px;
  max-width: 1000px;
  margin: 0 auto;
  font-family: 'DM Sans', sans-serif;
}

.header {
  margin-bottom: 48px;
}

.brand-badge {
  display: inline-block;
  padding: 4px 12px;
  background: #fdf2ed;
  color: #C4622D;
  border-radius: 4px;
  font-size: 12px;
  font-weight: 600;
  margin-bottom: 16px;
  letter-spacing: 1px;
  text-transform: uppercase;
}

.header h1 {
  font-family: 'Playfair Display', serif;
  font-size: 42px;
  color: #1A1A1A;
  margin-bottom: 12px;
}

.header p {
  color: #666;
  font-size: 18px;
  max-width: 600px;
}

.profile-content {
  display: flex;
  flex-direction: column;
  gap: 32px;
}

.profile-section {
  background: white;
  border-radius: 12px;
  padding: 40px;
  border: 1px solid #f0f0f0;
  box-shadow: 0 4px 20px rgba(0,0,0,0.02);
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 32px;
}

.profile-section h2 {
  font-family: 'Playfair Display', serif;
  font-size: 24px;
  color: #1A1A1A;
  margin: 0;
}

.edit-btn {
  background: transparent;
  border: 1px solid #e8e0d8;
  color: #C4622D;
  padding: 8px 20px;
  border-radius: 6px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
}

.edit-btn:hover {
  background: #fdf2ed;
  border-color: #C4622D;
}

.info-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 32px;
}

.info-group label {
  display: block;
  font-size: 12px;
  font-weight: 600;
  color: #999;
  margin-bottom: 8px;
  text-transform: uppercase;
  letter-spacing: 1px;
}

.info-group p {
  font-size: 17px;
  color: #333;
  font-weight: 500;
}

.brand-text {
  color: #C4622D !important;
  font-weight: 600 !important;
}

.status-badge {
  display: inline-block;
  padding: 4px 10px;
  border-radius: 20px;
  font-size: 11px;
  font-weight: 700;
}

.status-badge.approved {
  background: #e6f9f0;
  color: #10B981;
}

.kpi-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 24px;
  margin-top: 24px;
}

.kpi-card {
  background: #fafafa;
  padding: 24px;
  border-radius: 8px;
  border: 1px solid #f0f0f0;
}

.kpi-label {
  font-size: 11px;
  color: #888;
  text-transform: uppercase;
  font-weight: 600;
  letter-spacing: 0.5px;
  margin-bottom: 8px;
}

.kpi-value {
  font-family: 'Playfair Display', serif;
  font-size: 32px;
  font-weight: 700;
  color: #1A1A1A;
}

.about-text {
  font-size: 16px;
  line-height: 1.8;
  color: #555;
  font-style: italic;
}
</style>
