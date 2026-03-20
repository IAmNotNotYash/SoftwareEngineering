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
          <div class="profile-avatar" :style="{ backgroundImage: `url(${artist.profileImage})` }"></div>
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
        <div class="bio-section">
          <h2>About the Artist</h2>
          <p>{{ artist.bio }}</p>
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
                  <button class="add-cart-btn" @click="cartState.addItem(product)">Add to Cart</button>
                </div>
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
import { cartState } from '../../store/cart.js'

const route = useRoute()
const artist = ref(null)
const isFollowing = ref(false)

onMounted(async () => {
  const id = route.params.id || '1'
  artist.value = await getArtistDetails(id)
})

const toggleFollow = () => {
  isFollowing.value = !isFollowing.value
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

.divider {
  height: 1px;
  background: #e8e0d8;
  margin: 40px 0;
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
</style>
