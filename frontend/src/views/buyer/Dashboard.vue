<template>
  <div>
    <BuyerNavbar />
    <div class="page-container">
      <h1 class="page-title">Welcome back, Buyer!</h1>

      <!-- 1. Summary Statistics -->
      <div class="kpi-grid">
        <div class="kpi-card">
          <div class="kpi-label">FOLLOWED ARTISTS</div>
          <div class="kpi-value">{{ stats.followedArtists || 0 }}</div>
        </div>
        <div class="kpi-card">
          <div class="kpi-label">FAVORITE PRODUCTS</div>
          <div class="kpi-value">{{ stats.favoriteProducts || 0 }}</div>
        </div>
        <div class="kpi-card">
          <div class="kpi-label">RECENT ORDERS</div>
          <div class="kpi-value">{{ stats.recentOrders || 0 }}</div>
        </div>
        <div class="kpi-card">
          <div class="kpi-label">UPCOMING DELIVERIES</div>
          <div class="kpi-value text-highlight">{{ stats.upcomingDeliveries || 0 }}</div>
        </div>
      </div>

      <!-- 2. Recent Stories (Catalogues) -->
      <div class="section-container">
        <h2 class="section-title">New Catalogue from Your Creators</h2>
        <div class="stories-grid">
          <div v-for="story in recentStories" :key="story.id" class="story-card" :style="{ backgroundImage: `url(${story.cover})` }">
            <div class="story-overlay">
              <div class="story-date">{{ story.date }}</div>
              <div class="story-title">{{ story.title }}</div>
              <div class="story-artist">by <span>{{ story.artist }}</span></div>
              <RouterLink :to="`/buyer/catalogue/${story.id}`" class="view-story-btn">View Catalogue</RouterLink>
            </div>
          </div>
        </div>
      </div>

      <!-- 3. Artists to Follow -->
      <div class="section-container">
        <h2 class="section-title">Discover Creators</h2>
        <div class="artists-grid">
          <div v-for="artist in artistsToFollow" :key="artist.id" class="artist-card">
            <RouterLink :to="`/buyer/artist/${artist.id}`" class="artist-avatar" :style="{ backgroundImage: `url(${artist.avatar})` }"></RouterLink>
            <div class="artist-info">
              <RouterLink :to="`/buyer/artist/${artist.id}`" style="text-decoration:none; color:inherit;">
                <div class="artist-name" style="color:#000;">{{ artist.name }}</div>
              </RouterLink>
              <div class="artist-category">{{ artist.category }} • {{ artist.followers }} Followers</div>
            </div>
            <button class="follow-btn">Follow</button>
          </div>
        </div>
      </div>

      <!-- 4. Art & Culture Insights -->
      <div class="section-container">
        <h2 class="section-title">Behind the Art: History & Culture</h2>
        <div class="insights-grid">
          <div v-for="insight in insights" :key="insight.id" class="insight-card">
            <div class="insight-image" :style="{ backgroundImage: `url(${insight.image})` }"></div>
            <div class="insight-content">
              <div class="insight-artist">Insight by {{ insight.artist }}</div>
              <h3 class="insight-title">{{ insight.title }}</h3>
              <p class="insight-excerpt">{{ insight.excerpt }}</p>
              <RouterLink :to="`/buyer/insight/${insight.id}`" class="read-more-btn" style="display:inline-block; text-decoration:none;">Read Story</RouterLink>
            </div>
          </div>
        </div>
      </div>

      <!-- 5. Featured Products -->
      <div class="section-container" style="margin-bottom: 60px;">
        <h2 class="section-title">Trending Handcrafts</h2>
        <div class="products-grid">
          <div v-for="product in featuredProducts" :key="product.id" class="product-card">
            <RouterLink :to="`/buyer/product/${product.id}`" style="display: block;">
              <div class="product-image" :style="{ backgroundImage: `url(${product.image})` }"></div>
            </RouterLink>
            <div class="product-info">
              <div class="product-artist">{{ product.artist }}</div>
              <RouterLink :to="`/buyer/product/${product.id}`" style="text-decoration:none; color:inherit;">
                <div class="product-title" style="transition: color 0.2s;" onmouseover="this.style.color='#C4622D'" onmouseout="this.style.color='#000'">{{ product.title }}</div>
              </RouterLink>
              <div class="product-footer">
                <span class="product-price">₹{{ product.price.toLocaleString('en-IN') }}</span>
                <button class="add-cart-btn" @click="cartState.addItem(product)">Add to Cart</button>
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
import BuyerNavbar from '../../components/BuyerNavbar.vue'
import { getDashboardStats, getFeaturedProducts, getRecentStories, getArtistsToFollow, getArtInsights } from '../../api/buyer.js'
import { cartState } from '../../store/cart.js'

const stats = ref({})
const featuredProducts = ref([])
const recentStories = ref([])
const artistsToFollow = ref([])
const insights = ref([])

onMounted(async () => {
  stats.value = await getDashboardStats()
  recentStories.value = await getRecentStories()
  artistsToFollow.value = await getArtistsToFollow()
  featuredProducts.value = await getFeaturedProducts()
  insights.value = await getArtInsights()
})
</script>

<style scoped>
.page-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 40px 40px;
}

.page-title {
  font-family: 'Playfair Display', serif;
  font-size: 28px;
  font-weight: 600;
  color: #000;
  margin-bottom: 32px;
}

.kpi-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 20px;
  margin-bottom: 56px;
}

.kpi-card {
  background: #ffffff;
  border-radius: 8px;
  padding: 24px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
  border: 1px solid #f0f0f0;
}

.kpi-label {
  font-family: 'DM Sans', sans-serif;
  font-size: 11px;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  color: #888;
  margin-bottom: 12px;
}

.kpi-value {
  font-family: 'Playfair Display', serif;
  font-size: 32px;
  color: #000;
  font-weight: 500;
}

.text-highlight {
  color: #C4622D;
}

.section-container {
  margin-bottom: 56px;
}

.section-title {
  font-family: 'Playfair Display', serif;
  font-size: 24px;
  font-weight: 600;
  color: #000;
  margin-bottom: 24px;
}

/* Stories Styles */
.stories-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 24px;
}

.story-card {
  background-size: cover;
  background-position: center;
  border-radius: 8px;
  height: 300px;
  position: relative;
  overflow: hidden;
  transition: transform 0.2s;
}

.story-card:hover {
  transform: translateY(-4px);
}

.story-overlay {
  position: absolute;
  inset: 0;
  background: linear-gradient(to top, rgba(0,0,0,0.8) 0%, rgba(0,0,0,0.2) 60%, transparent 100%);
  padding: 24px;
  display: flex;
  flex-direction: column;
  justify-content: flex-end;
  color: white;
}

.story-date {
  font-family: 'DM Sans', sans-serif;
  font-size: 11px;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  color: #e0e0e0;
  margin-bottom: 6px;
}

.story-title {
  font-family: 'Playfair Display', serif;
  font-size: 20px;
  font-weight: 600;
  margin-bottom: 6px;
  line-height: 1.3;
}

.story-artist {
  font-family: 'DM Sans', sans-serif;
  font-size: 13px;
  color: #ccc;
  margin-bottom: 20px;
}

.story-artist span {
  color: #ffffff;
  font-weight: 600;
}

.view-story-btn {
  font-family: 'DM Sans', sans-serif;
  background: rgba(255, 255, 255, 0.15);
  backdrop-filter: blur(4px);
  color: white;
  border: 1px solid rgba(255, 255, 255, 0.4);
  padding: 8px 16px;
  border-radius: 4px;
  font-size: 13px;
  font-weight: 600;
  cursor: pointer;
  align-self: flex-start;
  transition: background 0.2s;
  text-decoration: none;
}

.view-story-btn:hover {
  background: white;
  color: #000;
}

/* Artists Styles */
.artists-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 20px;
}

.artist-card {
  background: #ffffff;
  border-radius: 8px;
  padding: 24px;
  border: 1px solid #f0f0f0;
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  transition: box-shadow 0.2s;
}

.artist-card:hover {
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
}

.artist-avatar {
  width: 80px;
  height: 80px;
  border-radius: 50%;
  background-size: cover;
  background-position: center;
  margin-bottom: 16px;
  border: 2px solid #fdf2ed;
}

.artist-name {
  font-family: 'Playfair Display', serif;
  font-size: 18px;
  font-weight: 600;
  color: #000;
  margin-bottom: 4px;
}

.artist-category {
  font-family: 'DM Sans', sans-serif;
  font-size: 12px;
  color: #888;
  margin-bottom: 20px;
}

.follow-btn {
  font-family: 'DM Sans', sans-serif;
  background: #fdf2ed;
  color: #C4622D;
  border: none;
  padding: 8px 24px;
  border-radius: 24px;
  font-size: 13px;
  font-weight: 600;
  cursor: pointer;
  transition: background 0.2s;
  width: 100%;
}

.follow-btn:hover {
  background: #C4622D;
  color: white;
}

/* Insights Styles */
.insights-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 32px;
}

.insight-card {
  background: #ffffff;
  border-radius: 8px;
  overflow: hidden;
  border: 1px solid #e8e0d8;
  display: flex;
  transition: box-shadow 0.2s;
}

.insight-card:hover {
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
}

.insight-image {
  width: 180px;
  background-size: cover;
  background-position: center;
  flex-shrink: 0;
}

.insight-content {
  padding: 24px;
  display: flex;
  flex-direction: column;
}

.insight-artist {
  font-family: 'DM Sans', sans-serif;
  font-size: 11px;
  color: #C4622D;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  margin-bottom: 8px;
  font-weight: 600;
}

.insight-title {
  font-family: 'Playfair Display', serif;
  font-size: 20px;
  font-weight: 600;
  color: #000;
  margin-bottom: 12px;
  margin-top: 0;
}

.insight-excerpt {
  font-family: 'DM Sans', sans-serif;
  font-size: 14px;
  color: #555;
  line-height: 1.5;
  margin-bottom: 20px;
  flex: 1;
}

.read-more-btn {
  font-family: 'DM Sans', sans-serif;
  background: transparent;
  color: #000;
  border: none;
  border-bottom: 1px solid #000;
  padding: 0 0 2px 0;
  font-size: 13px;
  font-weight: 600;
  cursor: pointer;
  align-self: flex-start;
  transition: color 0.2s, border-color 0.2s;
}

.read-more-btn:hover {
  color: #C4622D;
  border-color: #C4622D;
}

/* Products Styles (Reused) */
.products-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 32px;
}

.product-card {
  background: #ffffff;
  border-radius: 8px;
  overflow: hidden;
  border: 1px solid #f0f0f0;
  transition: box-shadow 0.2s;
  font-family: 'DM Sans', sans-serif;
}

.product-card:hover {
  box-shadow: 0 6px 16px rgba(0, 0, 0, 0.06);
}

.product-image {
  height: 240px;
  background-size: cover;
  background-position: center;
}

.product-info {
  padding: 20px;
}

.product-artist {
  font-size: 11px;
  color: #888;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  margin-bottom: 4px;
}

.product-title {
  font-family: 'Playfair Display', serif;
  font-size: 18px;
  font-weight: 600;
  color: #000;
  margin-bottom: 16px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.product-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.product-price {
  font-family: 'Playfair Display', serif;
  font-size: 18px;
  font-weight: 600;
  color: #000;
}

.add-cart-btn {
  font-family: 'DM Sans', sans-serif;
  background: transparent;
  color: #C4622D;
  border: 1px solid #C4622D;
  padding: 6px 16px;
  border-radius: 4px;
  font-size: 13px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
}

.add-cart-btn:hover {
  background: #C4622D;
  color: white;
}
</style>
