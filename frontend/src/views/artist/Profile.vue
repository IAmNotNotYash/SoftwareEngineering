<template>
  <div>
    <ArtistNavbar />
    <div class="profile-page">
      <!-- Page Header -->
      <div class="header">
        <div class="brand-badge">Artist Profile</div>
        <template v-if="!isEditing">
          <h1>{{ profileData?.brand_name || 'Your Brand' }}</h1>
          <h2 class="name-subtitle">{{ profileData?.full_name || user?.name }}</h2>
        </template>
        <h1 v-else>Edit Your Identity</h1>
        <p>Manage your artisan identity and track your platform performance.</p>
      </div>

      <div class="profile-content">
        <!-- Banner Section -->
        <section class="profile-section banner-section">
          <div class="section-header">
            <div>
              <h2>Profile Banner</h2>
              <p class="section-desc">This wide image appears as your profile background for buyers.</p>
            </div>
            <button @click="$refs.coverInput.click()" class="upload-btn-lite" :disabled="uploadingCover">
              {{ uploadingCover ? 'Uploading...' : 'Update Banner' }}
            </button>
            <input type="file" ref="coverInput" @change="onCoverChange" hidden accept="image/*" />
          </div>
          
          <div class="banner-preview" :style="profileData?.cover_image_url ? { backgroundImage: `url(${getImageUrl(profileData.cover_image_url)})` } : { background: '#fcf9f7' }">
            <div v-if="!profileData?.cover_image_url" class="banner-placeholder">
              <i class="img-icon">🖼️</i>
              <span>No banner uploaded yet</span>
            </div>
          </div>
        </section>

        <!-- Avatar & Basic Identity Section -->
        <section class="profile-section avatar-section">
          <div class="avatar-container">
            <div v-if="profileData?.profile_image_url" class="avatar-large" :style="{ backgroundImage: `url(${getImageUrl(profileData.profile_image_url)})` }"></div>
            <div v-else class="avatar-large-placeholder">{{ (profileData?.brand_name || user?.name || 'A').charAt(0) }}</div>
            
            <div class="avatar-actions">
              <h2>{{ profileData?.brand_name || 'Brand Avatar' }}</h2>
              <p>This image will appear on your catalogues and store profile.</p>
              <div class="upload-controls">
                <button @click="$refs.fileInput.click()" class="upload-btn" :disabled="uploading">
                  {{ uploading ? 'Uploading...' : 'Change Avatar' }}
                </button>
                <input type="file" ref="fileInput" @change="onFileChange" hidden accept="image/*" />
              </div>
            </div>
          </div>
        </section>

        <!-- Brand Info Section (Includes About/Bio) -->
        <section class="profile-section">
          <div class="section-header">
            <h2>Brand Information</h2>
            <div class="action-buttons">
              <button v-if="!isEditing" @click="toggleEdit" class="edit-btn">Edit Details</button>
              <template v-else>
                <button @click="cancelEdit" class="cancel-btn">Cancel</button>
                <button @click="saveChanges" class="save-btn" :disabled="saving">
                  {{ saving ? 'Saving...' : 'Save Changes' }}
                </button>
              </template>
            </div>
          </div>

          <div class="info-grid">
            <div class="info-group">
              <label>Artist Real Name</label>
              <p v-if="!isEditing">{{ profileData?.full_name || user?.name || '—' }}</p>
              <input v-else v-model="editForm.full_name" type="text" class="edit-input" placeholder="Your full name" />
            </div>
            <div class="info-group">
              <label>Brand / Studio Name</label>
              <p v-if="!isEditing" class="brand-text">{{ profileData?.brand_name || '—' }}</p>
              <input v-else v-model="editForm.brand_name" type="text" class="edit-input" placeholder="Your studio name" />
            </div>
            <div class="info-group">
              <label>Location / City</label>
              <p v-if="!isEditing">{{ profileData?.location || '—' }}</p>
              <input v-else v-model="editForm.location" type="text" class="edit-input" placeholder="e.g. Pune, Maharashtra" />
            </div>
            <div class="info-group">
              <label>Verification Status</label>
              <p :class="['status-badge', verificationStatus]">
                {{ verificationStatus.toUpperCase() || 'LOADING...' }}
              </p>
            </div>
            
            <div class="info-group full-width">
              <label>About the Artist</label>
              <div v-if="!isEditing">
                <p v-if="profileData?.bio" class="about-text bio-content">{{ profileData.bio }}</p>
                <p v-else class="about-text placeholder-text">Tell buyers about your artistic journey and philosophy...</p>
              </div>
              <textarea v-else v-model="editForm.bio" class="edit-textarea" rows="4" placeholder="Describe your artisan journey, inspirations, and history..."></textarea>
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
              <div class="kpi-label">Followers</div>
              <div class="kpi-value">{{ profileData?.follower_count || 0 }}</div>
            </div>
          </div>
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
import { getProfile, uploadProfileImage, updateProfile } from '../../api/auth.js'

const authStore = useAuthStore()
const user = computed(() => authStore.user)
const profileData = ref(null)

const isEditing = ref(false)
const saving = ref(false)
const uploading = ref(false)
const uploadingCover = ref(false)
const fileInput = ref(null)
const coverInput = ref(null)

const editForm = ref({
  full_name: '',
  brand_name: '',
  location: '',
  bio: ''
})

const verificationStatus = ref('approved')
const stats = ref({
  products: 0,
  orders: 0,
  catalogues: 0
})

const fetchProfileData = async () => {
  try {
    const data = await getProfile()
    profileData.value = data
    verificationStatus.value = data.verification_status || 'approved'
  } catch (e) {
    console.error(e)
  }
}

onMounted(async () => {
  await fetchProfileData()
  try {
    const productsData = await getProducts()
    const artistProducts = Array.isArray(productsData) ? productsData : productsData.products || []
    stats.value.products = artistProducts.length

    const ordersData = await getOrders()
    const artistOrders = Array.isArray(ordersData) ? ordersData : ordersData.orders || []
    stats.value.orders = artistOrders.length

    const cataloguesData = await getCatalogues({ status: 'live' })
    const artistCatalogues = cataloguesData.catalogues || []
    stats.value.catalogues = artistCatalogues.length
  } catch (err) {
    console.error("Failed to load artist stats", err)
  }
})

function toggleEdit() {
  editForm.value = {
    full_name: profileData.value?.full_name || '',
    brand_name: profileData.value?.brand_name || '',
    location: profileData.value?.location || '',
    bio: profileData.value?.bio || ''
  }
  isEditing.value = true
}

function cancelEdit() {
  isEditing.value = false
}

async function saveChanges() {
  saving.value = true
  try {
    await updateProfile(editForm.value)
    await fetchProfileData()
    if (authStore.user) {
      authStore.user.name = editForm.value.full_name
      authStore.user.brandName = editForm.value.brand_name
    }
    isEditing.value = false
    alert('Brand profile updated successfully!')
  } catch (err) {
    alert('Failed to update profile: ' + err.message)
  } finally {
    saving.value = false
  }
}

const onFileChange = async (event) => {
  const file = event.target.files[0]
  if (!file) return
  uploading.value = true
  try {
    await uploadProfileImage(file, 'profile')
    await fetchProfileData()
    alert('Avatar updated!')
  } catch (err) {
    alert('Failed to upload avatar: ' + err.message)
  } finally {
    uploading.value = false
  }
}

const onCoverChange = async (event) => {
  const file = event.target.files[0]
  if (!file) return
  uploadingCover.value = true
  try {
    await uploadProfileImage(file, 'cover')
    await fetchProfileData()
    alert('Banner updated!')
  } catch (err) {
    alert('Failed to upload banner: ' + err.message)
  } finally {
    uploadingCover.value = false
  }
}

const getImageUrl = (url) => {
  if (!url) return ''
  return url.startsWith('http') ? url : `http://127.0.0.1:5000${url}`
}
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
  margin-bottom: 4px;
}

.name-subtitle {
  font-size: 18px;
  color: #666;
  font-weight: 500;
  margin-bottom: 20px;
}

.header p {
  color: #666;
  font-size: 16px;
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

.banner-section {
  padding-bottom: 40px;
}

.section-desc {
  font-size: 14px;
  color: #888;
  margin-top: 4px;
}

.banner-preview {
  margin-top: 24px;
  height: 240px;
  border-radius: 12px;
  background-size: cover;
  background-position: center;
  position: relative;
  overflow: hidden;
  display: flex;
  align-items: center;
  justify-content: center;
  border: 1px dashed #e8e0d8;
}

.banner-placeholder {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 12px;
  color: #c9c0b8;
}

.img-icon {
  font-size: 40px;
}

.upload-btn-lite {
  background: #fcf9f7;
  color: #C4622D;
  border: 1px solid #e8e0d8;
  padding: 8px 16px;
  border-radius: 6px;
  font-size: 13px;
  font-weight: 600;
  cursor: pointer;
}

.upload-btn-lite:hover {
  background: #fdf2ed;
}

.avatar-section {
  background: linear-gradient(to right, #ffffff, #faf8f6);
}

.avatar-container {
  display: flex;
  align-items: center;
  gap: 32px;
}

.avatar-large {
  width: 100px;
  height: 100px;
  border-radius: 50%;
  background-size: cover;
  background-position: center;
  border: 4px solid #fff;
  box-shadow: 0 4px 15px rgba(0,0,0,0.1);
}

.avatar-large-placeholder {
  width: 100px;
  height: 100px;
  border-radius: 50%;
  background: #fdf2ed;
  color: #C4622D;
  display: flex;
  align-items: center;
  justify-content: center;
  font-family: 'Playfair Display', serif;
  font-size: 40px;
  font-weight: 700;
  border: 4px solid #fff;
  box-shadow: 0 4px 15px rgba(0,0,0,0.05);
}

.avatar-actions h2 {
  font-size: 20px;
  margin-bottom: 4px;
  font-family: 'Playfair Display', serif;
}

.avatar-actions p {
  color: #888;
  font-size: 14px;
  margin-bottom: 16px;
}

.upload-btn {
  background: white;
  border: 1px solid #e8e0d8;
  padding: 8px 20px;
  border-radius: 6px;
  font-size: 13px;
  font-weight: 600;
  color: #C4622D;
  cursor: pointer;
  transition: all 0.2s;
}

.upload-btn:hover {
  background: #C4622D;
  color: white;
  border-color: #C4622D;
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

.action-buttons {
  display: flex;
  gap: 12px;
}

.edit-btn, .save-btn, .cancel-btn {
  padding: 10px 24px;
  border-radius: 6px;
  font-weight: 600;
  font-size: 14px;
  cursor: pointer;
  transition: all 0.2s;
}

.edit-btn {
  background: transparent;
  border: 1px solid #e8e0d8;
  color: #C4622D;
}

.edit-btn:hover {
  background: #fdf2ed;
  border-color: #C4622D;
}

.save-btn {
  background: #C4622D;
  color: white;
  border: none;
}

.save-btn:hover {
  background: #a95224;
}

.cancel-btn {
  background: #f5f5f5;
  color: #666;
  border: none;
}

.info-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 32px 48px;
}

.full-width {
  grid-column: span 2;
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

.edit-input {
  width: 100%;
  padding: 12px;
  border: 1px solid #e8e0d8;
  border-radius: 6px;
  font-family: 'DM Sans', sans-serif;
  font-size: 16px;
  outline: none;
}

.edit-input:focus {
  border-color: #C4622D;
  box-shadow: 0 0 0 3px rgba(196, 98, 45, 0.1);
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
  margin-top: 10px;
}

.bio-content {
  font-style: normal;
  white-space: pre-line;
}

.placeholder-text {
  font-style: italic;
  color: #999;
}

.edit-textarea {
  width: 100%;
  padding: 16px;
  border: 1px solid #e8e0d8;
  border-radius: 8px;
  font-family: 'DM Sans', sans-serif;
  font-size: 16px;
  line-height: 1.6;
  outline: none;
  resize: vertical;
}

.edit-textarea:focus {
  border-color: #C4622D;
  box-shadow: 0 0 0 3px rgba(196, 98, 45, 0.1);
}
</style>
