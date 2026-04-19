<template>
  <div class="catalogues-page">
    <ArtistNavbar />

    <main class="page-container">
      <div class="page-header">
        <div>
          <h1 class="page-title">Catalogues</h1>
          <p class="subtitle">Manage and track your active and past product catalogues.</p>
        </div>
        <router-link to="/artist/newcatalogue" class="btn primary-btn">+ New Catalogue</router-link>
      </div>

      <div class="catalogues-grid" v-if="!loading">
        <div class="catalogue-card" v-for="c in catalogues" :key="c.id">
          <div class="catalogue-bg" :style="{ backgroundImage: `url(${getImageUrl(c.cover_photo_url)})` }">
            <div class="catalogue-overlay">
              
              <!-- Top bar: Status & Actions -->
              <div class="card-top">
                <div class="status-badge" :class="c.status.toLowerCase()">{{ c.status }}</div>
                <div class="actions">
                  <router-link :to="`/artist/edit-catalogue/${c.id}`" class="icon-btn edit-btn" title="Edit">✎</router-link>
                  <button class="icon-btn end-btn" title="End Catalogue">⏹</button>
                </div>
              </div>
              
              <!-- Bottom bar: Title & Stats -->
              <div class="card-bottom">
                <h3>{{ c.title }}</h3>
                <div class="catalogue-stats">
                  <div class="stat-item" title="Revenue"><span class="stat-icon">₹</span> {{ formatPrice(c.stats?.total_revenue) }}</div>
                  <div class="stat-item" title="Orders"><span class="stat-icon">📦</span> {{ c.stats?.total_orders || 0 }}</div>
                  <div class="stat-item" title="Products"><span class="stat-icon">🖼</span> {{ c.product_count || 0 }}</div>
                  <div class="stat-item" title="Views"><span class="stat-icon">👁</span> {{ c.stats?.total_views || 0 }}</div>
                  <div class="stat-item" title="Likes"><span class="stat-icon">❤</span> {{ c.stats?.total_likes || 0 }}</div>
                </div>
              </div>

            </div>
          </div>
        </div>
      </div>

      <div class="loading-state" v-else>
        <p>Loading your collections...</p>
      </div>

      <div class="empty-state" v-if="!loading && catalogues.length === 0">
        <p>You haven't created any catalogues yet.</p>
        <router-link to="/artist/newcatalogue" class="btn primary-btn">Create Your First Catalogue</router-link>
      </div>

      <!-- Stories Management Section -->
      <div class="stories-mgmt-section" v-if="!loading">
        <div class="section-header">
          <h2 class="section-title">Your Stories & Insights</h2>
          <router-link to="/artist/story" class="btn secondary-btn">+ New Story</router-link>
        </div>
        
        <div class="stories-mgmt-grid" v-if="stories.length > 0">
          <div class="story-mgmt-card" v-for="s in stories" :key="s.id">
            <div class="story-mgmt-img" :style="{ backgroundImage: `url(${getImageUrl(s.cover_image_url)})` }"></div>
            <div class="story-mgmt-info">
              <div class="story-mgmt-meta">
                <span class="type-badge">{{ s.type }}</span>
                <span class="date">{{ new Date(s.created_at).toLocaleDateString() }}</span>
              </div>
              <h4 class="story-mgmt-title">{{ s.title }}</h4>
              <div class="story-mgmt-actions">
                <button class="text-btn danger" @click="handleDeletePost(s.id)">Delete</button>
              </div>
            </div>
          </div>
        </div>
        <div class="empty-mgmt-state" v-else>
          <p>Shared your process or inspiration recently? Write a story to engage your audience.</p>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import ArtistNavbar from '../../components/ArtistNavbar.vue'
import { getCatalogues } from '../../api/catalogue'
import { getPosts, deletePost } from '../../api/social'
import { useAuthStore } from '../../stores/auth'

const authStore = useAuthStore()
const catalogues = ref([])
const stories = ref([])
const loading = ref(true)

const fetchCatalogues = async () => {
  try {
    const user_id = authStore.user?.id
    if (!user_id) return
    
    // Fetch all statuses for the artist: live, draft, ended
    const [resLive, resDraft, resEnded] = await Promise.all([
      getCatalogues({ status: 'live', user_id }),
      getCatalogues({ status: 'draft', user_id }),
      getCatalogues({ status: 'ended', user_id })
    ])
    
    catalogues.value = [
      ...(Array.isArray(resLive) ? resLive : (resLive.catalogues || [])),
      ...(Array.isArray(resDraft) ? resDraft : (resDraft.catalogues || [])),
      ...(Array.isArray(resEnded) ? resEnded : (resEnded.catalogues || []))
    ]

    // Fetch Stories specifically for this artist
    const artistId = authStore.user?.artistId
    if (artistId) {
      stories.value = await getPosts({ artist_id: artistId })
    }
  } catch (err) {
    console.error("Failed to fetch catalogues:", err)
  } finally {
    loading.value = false
  }
}

const handleDeletePost = async (id) => {
  if (!confirm("Are you sure you want to delete this story?")) return
  try {
    await deletePost(id)
    stories.value = stories.value.filter(s => s.id !== id)
  } catch (err) {
    alert(err.message)
  }
}

onMounted(fetchCatalogues)

const formatPrice = (val) => {
  return new Intl.NumberFormat('en-IN', {
    maximumFractionDigits: 0
  }).format(val || 0)
}

const getImageUrl = (url) => {
  if (!url) return '' // Remove placeholder
  if (url.startsWith('http')) return url
  return `http://localhost:5000${url}`
}
</script>

<style scoped>
.catalogues-page {
  min-height: 100vh;
  background: var(--color-bg-page);
  font-family: var(--font-body);
}

.page-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 60px 40px;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-end;
  margin-bottom: 48px;
}

.page-title {
  font-family: var(--font-heading);
  font-size: 34px;
  font-weight: 700;
  color: #1a1a1a;
  margin: 0 0 8px 0;
}

.subtitle {
  font-size: 16px;
  color: #666;
  margin: 0;
}

.btn {
  padding: 10px 20px;
  border-radius: 6px;
  font-size: 14px;
  font-weight: 600;
  text-decoration: none;
  transition: all 0.2s ease;
  cursor: pointer;
}

.primary-btn {
  background: #C4622D;
  color: #fff;
  border: none;
}
.primary-btn:hover { background: #a85427; }

/* Grid matching Buyer aesthetic (large cards) */
.catalogues-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 32px;
}

.catalogue-card {
  position: relative;
  height: 320px;
  border-radius: 16px;
  overflow: hidden;
  box-shadow: 0 4px 24px rgba(0,0,0,0.06);
  transition: transform 0.3s ease, box-shadow 0.3s ease;
  cursor: pointer;
}

.catalogue-card:hover {
  transform: translateY(-6px);
  box-shadow: 0 12px 32px rgba(0,0,0,0.12);
}

.catalogue-bg {
  position: absolute;
  inset: 0;
  background-size: cover;
  background-position: center;
  transition: transform 0.4s ease;
}

.catalogue-card:hover .catalogue-bg {
  transform: scale(1.05);
}

.catalogue-overlay {
  position: absolute;
  inset: 0;
  background: linear-gradient(
    rgba(0,0,0,0.5) 0%, 
    rgba(0,0,0,0.1) 40%, 
    rgba(0,0,0,0.2) 60%, 
    rgba(0,0,0,0.85) 100%
  );
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  padding: 24px;
}

.card-top {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
}

.status-badge {
  font-size: 11px;
  font-weight: 700;
  padding: 6px 14px;
  border-radius: 20px;
  text-transform: uppercase;
  letter-spacing: 0.8px;
  backdrop-filter: blur(8px);
}
.status-badge.live { background: rgba(22, 163, 74, 0.85); color: #fff; }
.status-badge.draft { background: rgba(107, 114, 128, 0.85); color: #fff; }
.status-badge.ended { background: rgba(220, 38, 38, 0.85); color: #fff; }

.actions {
  display: flex;
  gap: 10px;
  opacity: 0;
  transform: translateY(-10px);
  transition: all 0.3s ease;
}

.catalogue-card:hover .actions {
  opacity: 1;
  transform: translateY(0);
}

.icon-btn {
  background: rgba(255,255,255,0.2);
  backdrop-filter: blur(8px);
  color: #fff;
  border: 1px solid rgba(255,255,255,0.4);
  width: 36px;
  height: 36px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  font-size: 16px;
  transition: all 0.2s;
}

.icon-btn:hover {
  background: #fff;
  color: #1a1a1a;
  border-color: #fff;
}
.end-btn { font-size: 14px; }
.end-btn:hover { color: #F59E0B; } /* Amber warn color for ending */

.card-bottom h3 {
  font-family: var(--font-heading);
  font-size: 26px;
  font-weight: 700;
  color: #ffffff;
  margin: 0 0 16px 0;
  text-shadow: 0 2px 8px rgba(0,0,0,0.5);
}

.catalogue-stats {
  display: flex;
  gap: 20px;
  background: rgba(0,0,0,0.4);
  backdrop-filter: blur(8px);
  padding: 12px 20px;
  border-radius: 8px;
  border: 1px solid rgba(255,255,255,0.15);
}

.stat-item {
  color: #fff;
  font-size: 14px;
  font-weight: 600;
  display: flex;
  align-items: center;
  gap: 8px;
  letter-spacing: 0.5px;
}

.stat-icon {
  font-size: 16px;
  opacity: 0.8;
}

/* Stories Mgmt Styles */
.stories-mgmt-section {
  margin-top: 80px;
}

.stories-mgmt-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 24px;
}

.story-mgmt-card {
  background: white;
  border: 1px solid #e8e0d8;
  border-radius: 12px;
  overflow: hidden;
  display: flex;
  flex-direction: column;
}

.story-mgmt-img {
  height: 140px;
  background-size: cover;
  background-position: center;
}

.story-mgmt-info {
  padding: 16px;
}

.story-mgmt-meta {
  display: flex;
  justify-content: space-between;
  margin-bottom: 8px;
}

.type-badge {
  font-size: 10px;
  text-transform: uppercase;
  font-weight: 700;
  color: #C4622D;
  background: #fdf2ed;
  padding: 2px 8px;
  border-radius: 4px;
}

.date {
  font-size: 11px;
  color: #888;
}

.story-mgmt-title {
  font-size: 16px;
  font-weight: 600;
  margin: 0 0 12px 0;
  line-height: 1.4;
  height: 44px;
  overflow: hidden;
}

.story-mgmt-actions {
  display: flex;
  justify-content: flex-end;
}

.text-btn {
  background: none;
  border: none;
  font-size: 13px;
  font-weight: 600;
  cursor: pointer;
  padding: 4px 0;
}

.danger {
  color: #dc2626;
}

.empty-mgmt-state {
  padding: 40px;
  background: #fdfaf8;
  border-radius: 12px;
  text-align: center;
  color: #888;
  font-size: 14px;
}
</style>
.loading-state, .empty-state {
  text-align: center;
  padding: 100px 20px;
  background: #fff;
  border-radius: 16px;
  border: 2px dashed #eee;
  margin-top: 20px;
}
.loading-state p, .empty-state p {
  font-size: 18px;
  color: #666;
  margin-bottom: 24px;
}
