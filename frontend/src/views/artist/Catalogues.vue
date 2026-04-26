<template>
  <div class="catalogues-page">
    <ArtistNavbar />

    <main class="page-container">
      <div class="page-header">
        <div>
          <h1 class="page-title">Catalogues & Stories</h1>
          <p class="subtitle">Manage and track your active collections and standalone narratives.</p>
        </div>
        <div class="header-actions">
          <router-link to="/artist/newcatalogue" class="btn primary-btn" v-if="activeTab === 'catalogues'">+ New Catalogue</router-link>
          <router-link to="/artist/story" class="btn primary-btn" v-else>+ Post Story</router-link>
        </div>
      </div>

      <!-- Tab Switcher -->
      <div class="tab-switcher">
        <button class="tab-btn" :class="{active: activeTab === 'catalogues'}" @click="activeTab = 'catalogues'">My Catalogues</button>
        <button class="tab-btn" :class="{active: activeTab === 'stories'}" @click="activeTab = 'stories'">My Stories</button>
      </div>

      <div v-if="activeTab === 'catalogues'">
        <div class="catalogues-grid" v-if="!loading">
          <div class="catalogue-card" v-for="c in catalogues" :key="c.id">
            <div class="catalogue-bg" :style="{ backgroundImage: `url(${getImageUrl(c.cover_photo_url)})` }">
              <div class="catalogue-overlay">
                <div class="card-top">
                  <div class="status-badge" :class="c.status.toLowerCase()">{{ c.status }}</div>
                  <div class="actions">
                    <router-link :to="`/artist/edit-catalogue/${c.id}`" class="icon-btn edit-btn" title="Edit">✎</router-link>
                    <button class="icon-btn end-btn" title="End Catalogue">⏹</button>
                  </div>
                </div>
                <div class="card-bottom">
                  <h3>{{ c.title }}</h3>
                  <div class="catalogue-stats">
                    <div class="stat-item" title="Revenue"><span class="stat-icon">₹</span> {{ formatPrice(c.stats?.total_revenue) }}</div>
                    <div class="stat-item" title="Orders"><span class="stat-icon">📦</span> {{ c.stats?.total_orders || 0 }}</div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
        <div class="empty-state" v-if="!loading && catalogues.length === 0">
          <p>You haven't created any catalogues yet.</p>
          <router-link to="/artist/newcatalogue" class="btn primary-btn">Create Your First Catalogue</router-link>
        </div>
      </div>

      <div v-else-if="activeTab === 'stories'">
        <div class="stories-grid" v-if="!loading">
          <div class="story-card" v-for="s in stories" :key="s.id">
            <div class="story-image" :style="{ backgroundImage: `url(${s.cover_image_url})` }"></div>
            <div class="story-info">
              <div class="story-type">{{ s.type }}</div>
              <h3 class="story-title">{{ s.title }}</h3>
              <div class="story-meta">
                <span>❤ {{ s.likes_count || 0 }}</span>
                <span>💬 {{ s.comments_count || 0 }}</span>
              </div>
              <div class="story-actions">
                <button class="btn edit-action-btn" @click="editStory(s.id)">✎ Edit</button>
                <button class="btn delete-action-btn" @click="handleDeletePost(s.id)">🗑 Delete</button>
              </div>
            </div>
          </div>
        </div>
        <div class="empty-state" v-if="!loading && stories.length === 0">
          <p>You haven't posted any stories yet.</p>
          <router-link to="/artist/story" class="btn primary-btn">Post Your First Story</router-link>
        </div>
      </div>

      <div class="loading-state" v-if="loading">
        <p>Loading your narratives...</p>
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import ArtistNavbar from '../../components/ArtistNavbar.vue'
import { getCatalogues } from '../../api/catalogue'
import { getPosts, deletePost } from '../../api/social'
import { useAuthStore } from '../../stores/auth'

const authStore = useAuthStore()
const router = useRouter()
const catalogues = ref([])
const stories = ref([])
const loading = ref(true)
const activeTab = ref('catalogues')

const fetchCatalogues = async () => {
  try {
    const user_id = authStore.user?.id
    if (!user_id) return
    
    // Fetch all statuses for the artist: live, draft, ended
    const resLive = await getCatalogues({ status: 'live', user_id })
    const resDraft = await getCatalogues({ status: 'draft', user_id })
    const resEnded = await getCatalogues({ status: 'ended', user_id })
    
    catalogues.value = [
      ...resLive.catalogues,
      ...resDraft.catalogues,
      ...resEnded.catalogues
    ]

    // Fetch all stories for this artist (backend will filter by logged-in artist)
    const resPosts = await getPosts({ user_id })
    stories.value = resPosts
  } catch (err) {
    console.error("Failed to fetch catalogues:", err)
  } finally {
    loading.value = false
  }
}

onMounted(fetchCatalogues)

const editStory = (id) => {
  router.push(`/artist/edit-story/${id}`)
}

const handleDeletePost = async (id) => {
  if (!confirm("Are you sure you want to delete this story? This cannot be undone.")) return
  try {
    await deletePost(id)
    stories.value = stories.value.filter(s => s.id !== id)
  } catch (err) {
    alert("Delete failed: " + err.message)
  }
}

const formatPrice = (val) => {
  return new Intl.NumberFormat('en-IN', {
    maximumFractionDigits: 0
  }).format(val || 0)
}

const getImageUrl = (url) => {
  if (!url) return 'https://images.unsplash.com/photo-1544816155-12df9643f363?w=800'
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

/* Tab Switcher */
.tab-switcher {
  display: flex;
  gap: 8px;
  margin-bottom: 40px;
  border-bottom: 1px solid #e8e0d8;
  padding-bottom: 1px;
}

.tab-btn {
  background: none;
  border: none;
  padding: 12px 24px;
  font-size: 15px;
  font-weight: 600;
  color: #888;
  cursor: pointer;
  position: relative;
  transition: all 0.2s;
}

.tab-btn.active {
  color: #C4622D;
}

.tab-btn.active::after {
  content: '';
  position: absolute;
  bottom: -1px;
  left: 0;
  right: 0;
  height: 2px;
  background: #C4622D;
}

/* Stories Grid */
.stories-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 32px;
}

.story-card {
  background: #fff;
  border-radius: 12px;
  border: 1px solid #e8e0d8;
  overflow: hidden;
  box-shadow: 0 4px 12px rgba(0,0,0,0.03);
  transition: transform 0.2s;
}

.story-card:hover { transform: translateY(-4px); }

.story-image {
  height: 180px;
  background-size: cover;
  background-position: center;
}

.story-info {
  padding: 20px;
}

.story-type {
  font-size: 10px;
  text-transform: uppercase;
  color: #C4622D;
  font-weight: 700;
  letter-spacing: 0.5px;
  margin-bottom: 8px;
}

.story-title {
  margin: 0 0 12px 0;
  font-family: var(--font-heading);
  font-size: 18px;
  color: #1a1a1a;
  line-height: 1.3;
}

.story-meta {
  display: flex;
  gap: 16px;
  font-size: 13px;
  color: #888;
  margin-bottom: 20px;
}

.story-actions {
  display: flex;
  gap: 12px;
  margin-top: 8px;
}

.story-actions .btn {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 6px;
  border-radius: 8px;
  padding: 10px 0;
  font-size: 13px;
  font-weight: 600;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.edit-action-btn {
  background: #fdf2ed;
  color: #C4622D;
  border: 1px solid rgba(196, 98, 45, 0.2);
}

.edit-action-btn:hover {
  background: #C4622D;
  color: #fff;
  border-color: #C4622D;
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(196, 98, 45, 0.2);
}

.delete-action-btn {
  background: #fff;
  color: #888;
  border: 1px solid #eee;
}

.delete-action-btn:hover {
  background: #fff5f5;
  color: #e53e3e;
  border-color: #feb2b2;
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(229, 62, 62, 0.08);
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
