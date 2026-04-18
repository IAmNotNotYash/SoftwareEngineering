<template>
  <BuyerNavbar />
  <div class="following-page">
    <div class="header">
      <h1>Artists You Follow</h1>
      <p>Keep up with the latest creations from your favorite artists.</p>
    </div>

    <div v-if="loading" class="loading-state">
      <div class="spinner"></div>
      <p>Loading your artists...</p>
    </div>

    <div v-else class="artist-grid">
      <div v-for="artist in followedArtists" :key="artist.id" class="artist-card">
        <router-link :to="`/buyer/artist/${artist.id}`" class="card-link">
          <img :src="artist.profile_image_url || artist.avatar || 'https://via.placeholder.com/110'" :alt="artist.brand_name || artist.name" class="artist-avatar" />
          <div class="artist-info">
            <h3 class="artist-name">{{ artist.brand_name || artist.name || artist.full_name }}</h3>
            <p class="artist-category">{{ artist.location || 'Artisan' }}</p>
            <p class="artist-followers">{{ artist.follower_count || 0 }} followers</p>
          </div>
        </router-link>
        <button class="following-btn" @click="unfollow(artist.id)">
          <span class="btn-text">Following</span>
        </button>
      </div>
      
      <div v-if="followedArtists.length === 0" class="empty-state">
        <p>You aren't following any artists yet.</p>
        <router-link to="/buyer/products" class="explore-btn">Explore Art</router-link>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { getFollowing, unfollowArtist } from '../../api/social.js'
import BuyerNavbar from '../../components/BuyerNavbar.vue'

const followedArtists = ref([])
const loading = ref(true)

onMounted(async () => {
  try {
    const data = await getFollowing()
    followedArtists.value = Array.isArray(data) ? data : []
  } catch (e) {
    console.error('Failed to load following list:', e)
    followedArtists.value = []
  } finally {
    loading.value = false
  }
})

const unfollow = async (id) => {
  try {
    await unfollowArtist(id)
    followedArtists.value = followedArtists.value.filter(a => a.id !== id)
  } catch (e) {
    alert(e.message)
  }
}
</script>

<style scoped>
.following-page {
  padding: 40px;
  max-width: 1200px;
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

.loading-state, .empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 80px 0;
  color: #666;
  text-align: center;
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

.artist-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 30px;
}

.artist-card {
  background: white;
  border-radius: 12px;
  padding: 40px 20px 30px;
  text-align: center;
  border: 1px solid #eee;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.artist-card:hover {
  transform: translateY(-6px);
  box-shadow: 0 16px 32px rgba(0,0,0,0.06);
}

.card-link {
  text-decoration: none;
  color: inherit;
  width: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
  margin-bottom: 24px;
}

.artist-avatar {
  width: 110px;
  height: 110px;
  border-radius: 50%;
  object-fit: cover;
  margin-bottom: 20px;
  border: 3px solid #fdf2ed;
}

.artist-name {
  font-family: 'Playfair Display', serif;
  font-size: 20px;
  color: #2D2A26;
  margin-bottom: 6px;
}

.artist-category {
  font-size: 14px;
  color: #C4622D;
  font-weight: 500;
  margin-bottom: 8px;
}

.artist-followers {
  font-size: 13px;
  color: #888;
}

.following-btn {
  background: white;
  color: #2D2A26;
  border: 1px solid #ddd;
  padding: 10px 24px;
  border-radius: 24px;
  font-size: 14px;
  font-family: 'DM Sans', sans-serif;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
  width: 80%;
  position: relative;
  overflow: hidden;
}

.following-btn .btn-text {
  transition: opacity 0.2s;
}

.following-btn:hover {
  border-color: #ffcccc;
  background: #fff5f5;
  color: #d9534f;
}

.following-btn:hover .btn-text {
  display: none;
}

.following-btn:hover::after {
  content: "Unfollow";
  display: block;
}

.explore-btn {
  display: inline-block;
  margin-top: 20px;
  background: #C4622D;
  color: white;
  padding: 12px 32px;
  border-radius: 30px;
  text-decoration: none;
  font-weight: 600;
  transition: background 0.2s;
}

.explore-btn:hover {
  background: #a85427;
}
</style>
