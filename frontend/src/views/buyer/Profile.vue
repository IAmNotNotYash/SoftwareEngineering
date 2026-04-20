<template>
  <BuyerNavbar />
  <div class="profile-page">
    <div class="header">
      <h1>My Profile</h1>
      <p>Your account information on the Kala platform.</p>
    </div>

    <div v-if="loading" class="loading-state">
      <div class="spinner"></div>
      <p>Loading your profile...</p>
    </div>

    <div class="profile-content" v-else>
      <!-- Personal Info Section -->
      <section class="profile-section">
        <div class="section-header">
          <h2>Personal Information</h2>
          <button v-if="!isEditing" @click="startEditing" class="edit-btn">Edit Profile</button>
          <div v-else class="edit-actions">
            <button @click="cancelEditing" class="cancel-btn">Cancel</button>
            <button @click="saveProfile" class="save-btn" :disabled="saving">
              {{ saving ? 'Saving...' : 'Save Changes' }}
            </button>
          </div>
        </div>
        <div class="info-grid">
          <div class="info-group">
            <label>Full Name</label>
            <input v-if="isEditing" v-model="editForm.full_name" type="text" class="edit-input" />
            <p v-else>{{ user?.full_name || user?.name || '—' }}</p>
          </div>
          <div class="info-group">
            <label>Email Address</label>
            <p>{{ user?.email || '—' }}</p>
          </div>
          <div class="info-group">
            <label>Phone Number</label>
            <input v-if="isEditing" v-model="editForm.phone" type="tel" class="edit-input" placeholder="Enter phone number" />
            <p v-else>{{ user?.phone || '—' }}</p>
          </div>
          <div class="info-group">
            <label>Account Type</label>
            <p style="text-transform: capitalize;">{{ user?.role || '—' }}</p>
          </div>
          <div class="info-group">
            <label>Member Since</label>
            <p>{{ joinDateStr }}</p>
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
          <div class="kpi-card">
            <div class="kpi-label">Followed Artists</div>
            <div class="kpi-value">{{ followedArtists.length }}</div>
          </div>
        </div>
      </section>

      <!-- Following Section -->
      <section class="profile-section">
        <h2>Artists I Follow</h2>
        <div v-if="followedArtists.length === 0" class="empty-state">
          <p>You haven't followed any artists yet.</p>
        </div>
        <div v-else class="artist-list">
          <div v-for="artist in followedArtists" :key="artist.id" class="artist-chip">
            <img v-if="artist.profile_image_url" :src="getImageUrl(artist.profile_image_url)" alt="Avatar" />
            <div v-else class="avatar-placeholder small">{{ (artist.full_name || artist.name || 'A').charAt(0) }}</div>
            <div class="artist-info">
              <span class="artist-name">{{ artist.full_name || artist.name }}</span>
              <span class="artist-tagline">{{ artist.location || 'Artisan' }}</span>
            </div>
            <button @click="unfollow(artist.id)" class="unfollow-btn">Unfollow</button>
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

const user = ref(null)
const orderCount = ref(0)
const followedArtists = ref([])
const loading = ref(true)
const saving = ref(false)
const isEditing = ref(false)
const editForm = ref({
  full_name: '',
  email: '',
  phone: ''
})

const fetchProfile = async () => {
  try {
    const token = sessionStorage.getItem('token')
    
    // 1. Load Profile
    const res = await fetch('http://127.0.0.1:5000/api/auth/profile', {
      headers: { 'Authorization': `Bearer ${token}` }
    })
    if (res.ok) {
      user.value = await res.json()
    }
    
    // 2. Load Following List
    const followRes = await fetch('http://127.0.0.1:5000/api/social/following', {
      headers: { 'Authorization': `Bearer ${token}` }
    })
    if (followRes.ok) {
      followedArtists.value = await followRes.json()
    }
    
    // Load Cart count
    await cartStore.loadCart()

    // Load Order count
    const ordersData = await getOrders()
    const orders = Array.isArray(ordersData) ? ordersData : (ordersData.orders || [])
    orderCount.value = orders.length
  } catch (e) {
    console.error(e)
    user.value = authStore.user // fallback
  } finally {
    loading.value = false
  }
}

onMounted(fetchProfile)

const startEditing = () => {
  editForm.value = {
    full_name: user.value?.full_name || '',
    email: user.value?.email || '',
    phone: user.value?.phone || ''
  }
  isEditing.value = true
}

const cancelEditing = () => {
  isEditing.value = false
}

const unfollow = async (artistId) => {
  try {
    const res = await fetch(`http://127.0.0.1:5000/api/social/follows/${artistId}`, {
      method: 'DELETE',
      headers: { 'Authorization': `Bearer ${sessionStorage.getItem('token')}` }
    })
    if (res.ok) {
      followedArtists.value = followedArtists.value.filter(a => a.id !== artistId)
    }
  } catch (e) {
    console.error(e)
  }
}

const saveProfile = async () => {
  saving.value = true
  try {
    const res = await fetch('http://127.0.0.1:5000/api/auth/profile', {
      method: 'PATCH',
      headers: { 
        'Authorization': `Bearer ${sessionStorage.getItem('token')}`,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(editForm.value)
    })
    
    if (res.ok) {
      await fetchProfile()
      isEditing.value = false
      alert('Profile updated successfully!')
    } else {
      const err = await res.json()
      alert(err.error || 'Failed to update profile')
    }
  } catch (e) {
    console.error(e)
    alert('An error occurred while saving.')
  } finally {
    saving.value = false
  }
}

const joinDateStr = computed(() => {
  if (!user.value?.created_at) return 'Recently'
  return new Date(user.value.created_at).toLocaleDateString('en-IN', { year: 'numeric', month: 'long', day: 'numeric' })
})

const getImageUrl = (url) => {
  if (!url) return ''
  return url.startsWith('http') ? url : `http://localhost:5000${url}`
}
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
  background: #C4622D;
  color: white;
  padding: 8px 16px;
  border-radius: 6px;
  border: none;
  font-weight: 600;
  font-family: 'DM Sans', sans-serif;
  cursor: pointer;
  transition: background 0.2s;
}

.edit-btn:hover {
  background: #a35225;
}

.edit-actions {
  display: flex;
  gap: 12px;
}

.save-btn {
  background: #2D2A26;
  color: white;
  padding: 8px 16px;
  border-radius: 6px;
  border: none;
  font-weight: 600;
  cursor: pointer;
}

.cancel-btn {
  background: #eee;
  color: #666;
  padding: 8px 16px;
  border-radius: 6px;
  border: none;
  font-weight: 600;
  cursor: pointer;
}

.edit-input {
  width: 100%;
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 6px;
  font-family: 'DM Sans', sans-serif;
  font-size: 15px;
  outline: none;
}

.edit-input:focus {
  border-color: #C4622D;
}

.empty-state {
  text-align: center;
  padding: 20px;
  color: #888;
  font-style: italic;
}

.artist-list {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.artist-chip {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 12px;
  background: #fdfdfd;
  border: 1px solid #f0f0f0;
  border-radius: 8px;
}

.artist-chip img {
  width: 48px;
  height: 48px;
  border-radius: 50%;
  object-fit: cover;
}

.artist-info {
  flex-grow: 1;
  display: flex;
  flex-direction: column;
}

.artist-name {
  font-weight: 600;
  color: #2D2A26;
}

.artist-tagline {
  font-size: 13px;
  color: #888;
}

.unfollow-btn {
  background: none;
  border: 1px solid #ddd;
  padding: 6px 12px;
  border-radius: 4px;
  font-size: 12px;
  cursor: pointer;
  color: #666;
}

.unfollow-btn:hover {
  background: #fff5f0;
  color: #C4622D;
  border-color: #C4622D;
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
