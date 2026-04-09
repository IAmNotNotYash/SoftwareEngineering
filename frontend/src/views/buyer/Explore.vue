<template>
  <div>
    <BuyerNavbar />
    <div class="page-container">
      <div class="header-section">
        <h1 class="page-title">Explore</h1>
        <div class="search-container">
          <div class="search-flex-input">
            <select v-model="searchType" class="search-type-select">
              <option value="all">All</option>
              <option value="catalogue">Catalogues</option>
              <option value="artist">Artists</option>
            </select>
            <div class="input-wrapper">
              <input 
                type="text" 
                v-model="searchQuery" 
                :placeholder="searchPlaceholder" 
                class="search-input" 
              />
              <span class="search-icon">🔍</span>
            </div>
          </div>
        </div>
      </div>

      <!-- Catalogues Section -->
      <div class="section-container" v-if="searchType === 'all' || searchType === 'catalogue'">
        <div class="section-header">
          <h2 class="section-title">Catalogues</h2>
          <button v-if="!showAllCatalogues && filteredCatalogues.length > 3" class="more-btn" @click="showAllCatalogues = true">View More</button>
          <button v-if="showAllCatalogues" class="more-btn" @click="showAllCatalogues = false">Show Less</button>
        </div>
        <div class="grid-container">
          <div v-for="catalogue in displayedCatalogues" :key="catalogue.id" class="catalogue-card">
            <div class="catalogue-image" :style="{ backgroundImage: `url(${catalogue.cover})` }">
              <div class="catalogue-overlay">
                <div class="catalogue-date">{{ catalogue.date }}</div>
                <h3 class="catalogue-title">{{ catalogue.title }}</h3>
                <div class="catalogue-artist">by {{ catalogue.artist }}</div>
                <RouterLink :to="`/buyer/catalogue/${catalogue.id}`" class="explore-btn">Explore</RouterLink>
              </div>
            </div>
          </div>
        </div>
        <div v-if="filteredCatalogues.length === 0" class="no-results">No catalogues found.</div>
      </div>

      <!-- Artists Section -->
      <div class="section-container" v-if="searchType === 'all' || searchType === 'artist'">
        <div class="section-header">
          <h2 class="section-title">Artists</h2>
          <button v-if="!showAllArtists && filteredArtists.length > 4" class="more-btn" @click="showAllArtists = true">View More</button>
          <button v-if="showAllArtists" class="more-btn" @click="showAllArtists = false">Show Less</button>
        </div>
        <div class="artists-grid">
          <div v-for="artist in displayedArtists" :key="artist.id" class="artist-card">
            <RouterLink :to="`/buyer/artist/${artist.id}`" class="artist-avatar" :style="{ backgroundImage: `url(${artist.avatar})` }"></RouterLink>
            <div class="artist-info">
              <RouterLink :to="`/buyer/artist/${artist.id}`" class="artist-name">{{ artist.name }}</RouterLink>
              <div class="artist-meta">{{ artist.category }} • {{ artist.followers }} Followers</div>
            </div>
            <button 
              class="follow-btn" 
              :class="{ 'is-following': followingIds.has(artist.id) }" 
              @click="handleFollow(artist.id)"
            >
              {{ followingIds.has(artist.id) ? 'Following' : 'Follow' }}
            </button>
          </div>
        </div>
        <div v-if="filteredArtists.length === 0" class="no-results">No artists found.</div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import BuyerNavbar from '../../components/BuyerNavbar.vue'
import { getAllCatalogues, getAllArtists } from '../../api/buyer.js'
import { followArtist, unfollowArtist, checkFollowStatus, getFollowing } from '../../api/social.js'

const searchQuery = ref('')
const searchType = ref('all')
const catalogues = ref([])
const artists = ref([])
const followingIds = ref(new Set())

const showAllCatalogues = ref(false)
const showAllArtists = ref(false)

const searchPlaceholder = computed(() => {
  if (searchType.value === 'catalogue') return 'Search catalogues...'
  if (searchType.value === 'artist') return 'Search artists...'
  return 'Search for anything...'
})

onMounted(async () => {
  catalogues.value = await getAllCatalogues()
  artists.value = await getAllArtists()
  
  // Check which artists are already followed
  try {
    const followed = await getFollowing()
    followed.forEach(a => followingIds.value.add(a.id))
  } catch (e) {
    console.warn('Could not fetch following list:', e)
  }
})

async function handleFollow(artistId) {
  try {
    if (followingIds.value.has(artistId)) {
      await unfollowArtist(artistId)
      followingIds.value.delete(artistId)
    } else {
      await followArtist(artistId)
      followingIds.value.add(artistId)
    }
    // Force reactivity update for the Set by creating a new reference
    followingIds.value = new Set(followingIds.value)
  } catch (e) {
    alert('Action failed: ' + e.message)
  }
}

const filteredCatalogues = computed(() => {
  if (searchType.value === 'artist') return []
  if (!searchQuery.value) return catalogues.value
  const query = searchQuery.value.toLowerCase()
  return (catalogues.value || []).filter(c => 
    (c.title || '').toLowerCase().includes(query) || 
    (c.artist || '').toLowerCase().includes(query)
  )
})

const filteredArtists = computed(() => {
  if (searchType.value === 'catalogue') return []
  if (!searchQuery.value) return artists.value
  const query = searchQuery.value.toLowerCase()
  return (artists.value || []).filter(a => 
    (a.name || '').toLowerCase().includes(query) || 
    (a.category || '').toLowerCase().includes(query)
  )
})

const displayedCatalogues = computed(() => {
  if (showAllCatalogues.value || searchQuery.value) return filteredCatalogues.value
  return filteredCatalogues.value.slice(0, 3)
})

const displayedArtists = computed(() => {
  if (showAllArtists.value || searchQuery.value) return filteredArtists.value
  return filteredArtists.value.slice(0, 4)
})
</script>

<style scoped>
.page-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 40px 40px;
  font-family: 'DM Sans', sans-serif;
}

.header-section {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 50px;
}

.page-title {
  font-family: 'Playfair Display', serif;
  font-size: 32px;
  font-weight: 700;
  margin: 0;
}

.search-container {
  width: 500px;
}

.search-flex-input {
  display: flex;
  background: #fdfaf8;
  border: 1px solid #e8e0d8;
  border-radius: 30px;
  overflow: hidden;
  transition: all 0.3s ease;
}

.search-flex-input:focus-within {
  border-color: #C4622D;
  box-shadow: 0 0 0 4px rgba(196, 98, 45, 0.05);
  background: #fff;
}

.search-type-select {
  background: #f7ede4;
  border: none;
  border-right: 1px solid #e8e0d8;
  padding: 0 15px 0 20px;
  font-family: 'DM Sans', sans-serif;
  font-size: 13px;
  font-weight: 600;
  color: #C4622D;
  outline: none;
  cursor: pointer;
}

.input-wrapper {
  position: relative;
  flex: 1;
}

.search-input {
  width: 100%;
  padding: 12px 20px 12px 40px;
  border: none;
  background: transparent;
  font-size: 14px;
  outline: none;
}

.search-icon {
  position: absolute;
  left: 15px;
  top: 50%;
  transform: translateY(-50%);
  color: #888;
  font-size: 14px;
}

.section-container {
  margin-bottom: 60px;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
}

.section-title {
  font-family: 'Playfair Display', serif;
  font-size: 24px;
  font-weight: 600;
  color: #000;
  margin: 0;
}

.more-btn {
  background: transparent;
  border: none;
  color: #C4622D;
  font-weight: 600;
  font-size: 14px;
  cursor: pointer;
  padding: 8px 16px;
  border-radius: 4px;
  transition: background 0.2s;
}

.more-btn:hover {
  background: #fdf2ed;
}

/* Catalogues Grid */
.grid-container {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 24px;
}

.catalogue-card {
  border-radius: 12px;
  overflow: hidden;
  height: 320px;
  transition: transform 0.3s ease;
}

.catalogue-card:hover {
  transform: translateY(-5px);
}

.catalogue-image {
  width: 100%;
  height: 100%;
  background-size: cover;
  background-position: center;
  position: relative;
}

.catalogue-overlay {
  position: absolute;
  inset: 0;
  background: linear-gradient(to top, rgba(0,0,0,0.8) 0%, rgba(0,0,0,0.2) 60%, transparent 100%);
  padding: 24px;
  display: flex;
  flex-direction: column;
  justify-content: flex-end;
  color: white;
}

.catalogue-date {
  font-size: 11px;
  text-transform: uppercase;
  letter-spacing: 1px;
  margin-bottom: 8px;
  color: #e0e0e0;
}

.catalogue-title {
  font-family: 'Playfair Display', serif;
  font-size: 20px;
  font-weight: 600;
  margin: 0 0 4px 0;
}

.catalogue-artist {
  font-size: 13px;
  color: #ccc;
  margin-bottom: 20px;
}

.explore-btn {
  background: rgba(255, 255, 255, 0.2);
  backdrop-filter: blur(8px);
  border: 1px solid rgba(255, 255, 255, 0.4);
  color: white;
  padding: 8px 20px;
  border-radius: 6px;
  text-decoration: none;
  font-size: 13px;
  font-weight: 600;
  align-self: flex-start;
  transition: all 0.2s;
}

.explore-btn:hover {
  background: white;
  color: black;
}

/* Artists Grid */
.artists-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 20px;
}

.artist-card {
  background: #fff;
  border: 1px solid #f0f0f0;
  border-radius: 12px;
  padding: 24px;
  text-align: center;
  display: flex;
  flex-direction: column;
  align-items: center;
  transition: box-shadow 0.3s ease;
}

.artist-card:hover {
  box-shadow: 0 10px 20px rgba(0,0,0,0.05);
}

.artist-avatar {
  width: 80px;
  height: 80px;
  border-radius: 50%;
  background-size: cover;
  background-position: center;
  margin-bottom: 16px;
  border: 3px solid #fdf2ed;
}

.artist-info {
  margin-bottom: 20px;
}

.artist-name {
  font-family: 'Playfair Display', serif;
  font-size: 18px;
  font-weight: 600;
  color: #000;
  text-decoration: none;
  display: block;
  margin-bottom: 4px;
}

.artist-meta {
  font-size: 12px;
  color: #888;
}

.follow-btn {
  width: 100%;
  padding: 10px;
  border-radius: 20px;
  border: none;
  background: #fdf2ed;
  color: #C4622D;
  font-weight: 600;
  font-size: 13px;
  cursor: pointer;
  transition: all 0.2s;
}

.follow-btn:hover {
  background: #C4622D;
  color: #fff;
}

.follow-btn.is-following {
  background: #2D2A26;
  color: #fff;
}

.follow-btn.is-following:hover {
  background: #d94242; /* Red for unfollow hint */
}

.no-results {
  text-align: center;
  padding: 40px;
  color: #888;
  font-style: italic;
}
</style>
