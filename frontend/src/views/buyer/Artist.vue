<template>
  <div>
    <BuyerNavbar />
    <div v-if="!artist" class="loading-state">
      Loading artist profile...
    </div>
    <div v-else class="artist-profile-layout">
      
      <!-- Artist Cover & Info -->
      <div class="cover-photo" :style="{ backgroundImage: `url(${artist.coverImage})` }">
        <div class="cover-overlay"></div>
      </div>

      <div class="page-container">
        <div class="profile-header">
          <div 
            class="profile-avatar" 
            :style="artist.profileImage ? { backgroundImage: `url(${artist.profileImage})` } : { background: '#fdf2ed' }"
          >
            <span v-if="!artist.profileImage" class="avatar-placeholder">{{ artist.name.charAt(0) }}</span>
          </div>
          <div class="profile-info">
            <h1 class="artist-name">{{ artist.name }}</h1>
            <div class="artist-meta">
              <span>📍 {{ artist.location }}</span>
              <span>👥 {{ artist.followers.toLocaleString() }} Followers</span>
            </div>
          </div>
          <div class="profile-actions">
            <button class="follow-btn" @click="toggleFollow">
              {{ isFollowing ? 'Following' : 'Follow Artist' }}
            </button>
          </div>
        </div>

        <!-- Artist Bio -->
        <div class="bio-section" v-if="artist.bio || !isFollowing">
          <h2>About the Artist</h2>
          <p v-if="artist.bio" class="bio-text">{{ artist.bio }}</p>
          <p v-else class="bio-placeholder">This artist is currently curating their artisan journey and history. Follow them to stay updated on their latest stories.</p>
        </div>

        <div class="divider"></div>

        <!-- Artist's Catalogues -->
        <div class="catalogues-section" v-if="artist.catalogues && artist.catalogues.length > 0">
          <h2>Latest Catalogues</h2>
          <div class="catalogues-grid">
            <div v-for="catalogue in artist.catalogues" :key="catalogue.id" class="catalogue-card">
              <div class="catalogue-image" :style="{ backgroundImage: `url(${catalogue.cover})` }"></div>
              <div class="catalogue-info">
                <div class="catalogue-date">{{ catalogue.date }}</div>
                <h3 class="catalogue-title">{{ catalogue.title }}</h3>
                <RouterLink :to="`/buyer/catalogue/${catalogue.id}`" class="view-catalogue-link">View Catalogue</RouterLink>
              </div>
            </div>
          </div>
        </div>

        <div class="divider"></div>

        <!-- Artist's Library/Products -->
        <div class="portfolio-section">
          <h2>Artworks by {{ artist.name }}</h2>
          <div class="products-grid">
            <div v-for="product in artist.products" :key="product.id" class="product-card">
              <RouterLink :to="`/buyer/product/${product.id}`" style="display: block; text-decoration: none; color: inherit;">
                <div class="product-image" :style="{ backgroundImage: `url(${product.image})` }">
                  <div class="category-badge">{{ product.category }}</div>
                </div>
              </RouterLink>
              <div class="product-info">
                <div class="product-artist">{{ product.artist }}</div>
                <RouterLink :to="`/buyer/product/${product.id}`" class="product-title-link">
                  <div class="product-title">{{ product.title }}</div>
                </RouterLink>
                <div class="product-footer">
                  <span class="product-price">₹{{ product.price.toLocaleString('en-IN') }}</span>
                  <button class="add-cart-btn" @click="handleAddToCart(product.id)">Add to Cart</button>
                </div>
              </div>
            </div>
          </div>
        </div>

        <div class="divider" v-if="stories.length > 0"></div>

        <!-- Artist's Stories/Insights -->
        <div class="stories-feed-section" v-if="stories.length > 0">
          <h2>Stories & Insights</h2>
          <div class="stories-feed-grid">
            <div v-for="story in stories" :key="story.id" class="story-feed-card">
              <div class="story-feed-image" v-if="story.image" :style="{ backgroundImage: `url(${story.image})` }"></div>
              <div class="story-feed-content">
                <div class="story-feed-type">{{ story.type === 'insight' ? 'Insight' : 'Story' }}</div>
                <h3>{{ story.title }}</h3>
                <p>{{ story.excerpt }}</p>
                <RouterLink :to="`/buyer/insight/${story.id}`" class="read-story-link">Read More</RouterLink>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import BuyerNavbar from '../../components/BuyerNavbar.vue'
import { getArtistDetails } from '../../api/buyer.js'
import { followArtist, unfollowArtist, checkFollowStatus, getPosts } from '../../api/social.js'
import { useCartStore } from '../../stores/cart.js'

const cartStore = useCartStore()

const route = useRoute()
const artist = ref(null)
const stories = ref([])
const isFollowing = ref(false)

onMounted(async () => {
  const id = route.params.id || '1'
  artist.value = await getArtistDetails(id)
  
  // Fetch artist's stories
  try {
    const posts = await getPosts({ artist_id: id })
    stories.value = posts.map(p => ({
      id: p.id,
      title: p.title,
      type: p.type,
      excerpt: stripTags(p.body).substring(0, 150) + '...',
      image: p.cover_image_url
    }))
  } catch (e) {
    console.error('Failed to fetch stories:', e)
  }
  
  // Check if current user is following this artist
  try {
    const res = await checkFollowStatus(id)
    isFollowing.value = res.is_following
  } catch (e) {
    console.error('Follow check failed:', e)
  }
})

const toggleFollow = async () => {
  if (!authStore.user) {
    alert('Please log in to follow artists.')
    return
  }
  const artistId = artist.value.id
  try {
    if (isFollowing.value) {
      await unfollowArtist(artistId)
      isFollowing.value = false
      artist.value.followers = Math.max(0, (artist.value.followers || 0) - 1)
    } else {
      await followArtist(artistId)
      isFollowing.value = true
      artist.value.followers = (artist.value.followers || 0) + 1
    }
  } catch (e) {
    alert('Action failed: ' + e.message)
  }
}

async function handleAddToCart(productId) {
  if (!authStore.user || authStore.user.role !== 'buyer') {
    alert(authStore.user?.role === 'artist' 
      ? 'Artists cannot purchase items. Please log in with a Buyer account.' 
      : 'Please log in to add items to your cart.')
    return
  }
  try {
    await cartStore.addItem(productId)
    alert('Added to cart!')
  } catch (e) {
    alert(e.message)
  }
}

function stripTags(html) {
  if (!html) return ''
  const doc = new DOMParser().parseFromString(html, 'text/html')
  return doc.body.textContent || ""
}
</script>

<style scoped>
.loading-state {
  text-align: center;
  padding: 100px;
  color: #888;
  font-family: 'DM Sans', sans-serif;
}

.cover-photo {
  width: 100%;
  height: 320px;
  background-size: cover;
  background-position: center;
  position: relative;
}

.cover-overlay {
  position: absolute;
  inset: 0;
  background: linear-gradient(to top, rgba(0,0,0,0.6), transparent);
}

.page-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 40px 80px 40px;
  font-family: 'DM Sans', sans-serif;
}

.profile-header {
  display: flex;
  align-items: flex-end;
  gap: 32px;
  margin-top: -80px;
  position: relative;
  z-index: 10;
  margin-bottom: 40px;
}

.profile-avatar {
  width: 160px;
  height: 160px;
  border-radius: 50%;
  border: 4px solid white;
  background-color: #fdfaf8;
  background-size: cover;
  background-position: center;
  box-shadow: 0 4px 12px rgba(0,0,0,0.1);
  flex-shrink: 0;
  display: flex;
  align-items: center;
  justify-content: center;
}

.avatar-placeholder {
  font-family: 'Playfair Display', serif;
  font-size: 64px;
  font-weight: 700;
  color: #C4622D;
}

.profile-info {
  flex: 1;
  padding-bottom: 16px;
}

.artist-name {
  font-family: 'Playfair Display', serif;
  font-size: 36px;
  font-weight: 600;
  color: #000;
  margin-top: 80px !important; /* Extremely high value to ensure it moves */
  margin-bottom: 8px;
}

.artist-meta {
  display: flex;
  gap: 24px;
  font-size: 14px;
  color: #555;
}

.profile-actions {
  padding-bottom: 24px;
}

.follow-btn {
  background: #C4622D;
  color: white;
  border: none;
  padding: 12px 32px;
  font-family: 'DM Sans', sans-serif;
  font-size: 15px;
  font-weight: 600;
  border-radius: 6px;
  cursor: pointer;
  transition: background 0.2s;
}

.follow-btn:hover {
  background: #a95224;
}

.bio-section {
  max-width: 800px;
  margin-bottom: 40px;
}

.bio-section h2 {
  font-family: 'Playfair Display', serif;
  font-size: 24px;
  margin-bottom: 16px;
  color: #000;
}

.bio-section p {
  font-size: 16px;
  line-height: 1.6;
  color: #444;
}

.bio-text {
  white-space: pre-line;
}

.bio-placeholder {
  font-style: italic;
  color: #888 !important;
}

.divider {
  height: 1px;
  background: #e8e0d8;
  margin: 40px 0;
}

/* Catalogues Section Styles */
.catalogues-section {
  margin-bottom: 60px;
}

.catalogues-section h2 {
  font-family: 'Playfair Display', serif;
  font-size: 28px;
  color: #000;
  margin-bottom: 32px;
}

.catalogues-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
  gap: 32px;
}

.catalogue-card {
  background: white;
  border-radius: 12px;
  overflow: hidden;
  border: 1px solid #e8e0d8;
  display: flex;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.catalogue-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 10px 20px rgba(0,0,0,0.05);
}

.catalogue-image {
  width: 140px;
  height: 180px;
  background-size: cover;
  background-position: center;
  flex-shrink: 0;
}

.catalogue-info {
  padding: 24px;
  display: flex;
  flex-direction: column;
  justify-content: center;
}

.catalogue-date {
  font-size: 11px;
  text-transform: uppercase;
  letter-spacing: 1px;
  color: #C4622D;
  margin-bottom: 8px;
  font-weight: 600;
}

.catalogue-title {
  font-family: 'Playfair Display', serif;
  font-size: 20px;
  font-weight: 600;
  color: #000;
  margin-bottom: 20px;
  line-height: 1.3;
}

.view-catalogue-link {
  font-size: 13px;
  font-weight: 600;
  color: #000;
  text-decoration: none;
  border-bottom: 2px solid #C4622D;
  padding-bottom: 2px;
  align-self: flex-start;
  transition: color 0.2s;
}

.view-catalogue-link:hover {
  color: #C4622D;
}

.portfolio-section h2 {
  font-family: 'Playfair Display', serif;
  font-size: 28px;
  color: #000;
  margin-bottom: 32px;
}

/* Product Grid Shared Styles */
.products-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 32px;
}

.product-card {
  background: #ffffff;
  border: 1px solid var(--color-border);
  border-radius: 8px;
  overflow: hidden;
  transition: box-shadow 0.2s;
}

.product-card:hover {
  box-shadow: var(--shadow-hover);
}

.product-image {
  height: 280px;
  background-size: cover;
  background-position: center;
  position: relative;
}

.category-badge {
  position: absolute;
  top: 16px;
  left: 16px;
  background: rgba(255, 255, 255, 0.9);
  padding: 4px 12px;
  border-radius: 20px;
  font-size: 12px;
  font-weight: 600;
  color: var(--color-text-dark);
}

.product-info {
  padding: 24px;
}

.product-artist {
  font-size: 12px;
  color: var(--color-text-muted);
  text-transform: uppercase;
  letter-spacing: 0.5px;
  margin-bottom: 8px;
}

.product-title {
  font-family: var(--font-heading);
  font-size: 18px;
  font-weight: 600;
  color: var(--color-text-dark);
  margin-bottom: 16px;
}

.product-title-link {
  text-decoration: none;
}

.product-title-link:hover .product-title {
  color: var(--color-primary);
}

.product-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.product-price {
  font-weight: 600;
  font-size: 18px;
  color: var(--color-text-dark);
}

.add-cart-btn {
  background: transparent;
  color: var(--color-text-dark);
  border: 1px solid var(--color-border);
  padding: 8px 16px;
  border-radius: 4px;
  font-family: var(--font-body);
  font-size: 13px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
}

.add-cart-btn:hover {
  border-color: var(--color-primary);
  color: var(--color-primary);
}

/* Stories Feed Styles */
.stories-feed-section {
  margin-top: 60px;
}

.stories-feed-section h2 {
  font-family: 'Playfair Display', serif;
  font-size: 28px;
  color: #000;
  margin-bottom: 32px;
}

.stories-feed-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 32px;
}

.story-feed-card {
  background: white;
  border: 1px solid #e8e0d8;
  border-radius: 12px;
  overflow: hidden;
  transition: transform 0.3s ease;
}

.story-feed-card:hover {
  transform: translateY(-5px);
}

.story-feed-image {
  height: 200px;
  background-size: cover;
  background-position: center;
}

.story-feed-content {
  padding: 24px;
}

.story-feed-type {
  font-size: 11px;
  text-transform: uppercase;
  letter-spacing: 1px;
  color: #C4622D;
  margin-bottom: 8px;
  font-weight: 600;
}

.story-feed-content h3 {
  font-family: 'Playfair Display', serif;
  font-size: 20px;
  margin: 0 0 12px 0;
  color: #000;
}

.story-feed-content p {
  font-size: 14px;
  color: #666;
  line-height: 1.6;
  margin-bottom: 20px;
}

.read-story-link {
  font-size: 13px;
  font-weight: 600;
  color: #000;
  text-decoration: none;
  border-bottom: 2px solid #C4622D;
  padding-bottom: 2px;
  transition: color 0.2s;
}

.read-story-link:hover {
  color: #C4622D;
}
</style>
