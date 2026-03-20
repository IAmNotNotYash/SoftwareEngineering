<template>
  <div>
    <BuyerNavbar />
    
    <div v-if="catalogue" class="catalogue-wrapper">
      <!-- Hero Header -->
      <div class="hero-section" :style="{ backgroundImage: `url(${catalogue.cover})` }">
        <div class="hero-overlay">
          <div class="hero-content">
            <div class="meta-date">{{ catalogue.date }}</div>
            <h1 class="hero-title">{{ catalogue.title }}</h1>
            <div class="artist-badge">
              <div class="artist-avatar" :style="{ backgroundImage: `url(${catalogue.artist.avatar})` }"></div>
              <span>By <strong>{{ catalogue.artist.name }}</strong></span>
            </div>
          </div>
        </div>
      </div>

      <!-- Main Content Container -->
      <div class="page-container">
        
        <!-- Philosophy and Artist Note -->
        <div class="story-details">
          <div class="philosophy-section">
            <h2 class="section-title">Philosophy</h2>
            <p class="body-text">{{ catalogue.philosophy }}</p>
          </div>
          
          <div class="artist-note-section">
            <div class="note-box">
              <h3 class="note-title">Artist's Note</h3>
              <p class="note-text">"{{ catalogue.artistNote }}"</p>
            </div>
          </div>
        </div>

        <div class="divider"></div>

        <!-- Products in Catalogue -->
        <div class="catalogue-products">
          <h2 class="section-title">Pieces in this Catalogue</h2>
          <div class="products-grid">
            <div v-for="product in catalogue.products" :key="product.id" class="product-card">
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
    
    <div v-else class="loading-state">
      Loading catalogue...
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import BuyerNavbar from '../../components/BuyerNavbar.vue'
import { getCatalogue } from '../../api/buyer.js'
import { cartState } from '../../store/cart.js'

const route = useRoute()
const catalogue = ref(null)

onMounted(async () => {
  const id = route.params.id
  catalogue.value = await getCatalogue(id)
})
</script>

<style scoped>
.catalogue-wrapper {
  font-family: 'DM Sans', sans-serif;
}

.hero-section {
  width: 100%;
  height: 480px;
  background-size: cover;
  background-position: center;
  position: relative;
}

.hero-overlay {
  position: absolute;
  inset: 0;
  background: linear-gradient(to top, rgba(0,0,0,0.85) 0%, rgba(0,0,0,0.3) 50%, rgba(0,0,0,0.1) 100%);
  display: flex;
  align-items: flex-end;
  padding: 60px 80px;
}

.hero-content {
  color: white;
  max-width: 800px;
}

.meta-date {
  font-size: 13px;
  text-transform: uppercase;
  letter-spacing: 1px;
  color: #e0e0e0;
  margin-bottom: 12px;
}

.hero-title {
  font-family: 'Playfair Display', serif;
  font-size: 48px;
  font-weight: 600;
  line-height: 1.2;
  margin-bottom: 24px;
}

.artist-badge {
  display: flex;
  align-items: center;
  gap: 12px;
}

.artist-avatar {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background-size: cover;
  background-position: center;
  border: 2px solid rgba(255,255,255,0.2);
}

.artist-badge span {
  font-size: 15px;
  color: #eeeeee;
}

.artist-badge strong {
  color: white;
  font-weight: 600;
}

.page-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 60px 40px;
}

/* Story Details Layout */
.story-details {
  display: flex;
  gap: 60px;
  margin-bottom: 60px;
}

.philosophy-section {
  flex: 1.5;
}

.artist-note-section {
  flex: 1;
}

.section-title {
  font-family: 'Playfair Display', serif;
  font-size: 28px;
  font-weight: 600;
  color: #000;
  margin-bottom: 24px;
}

.body-text {
  font-size: 16px;
  line-height: 1.8;
  color: #444;
}

.note-box {
  background: #fdfaf8;
  border-left: 4px solid #C4622D;
  padding: 32px;
  border-radius: 0 8px 8px 0;
}

.note-title {
  font-family: 'Playfair Display', serif;
  font-size: 18px;
  color: #C4622D;
  margin-bottom: 16px;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.note-text {
  font-family: 'Playfair Display', serif;
  font-size: 18px;
  line-height: 1.7;
  color: #333;
  font-style: italic;
}

.divider {
  height: 1px;
  background: #e8e0d8;
  margin: 0 0 60px 0;
}

/* Products Layout */
.products-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 32px;
}

.product-card {
  background: #ffffff;
  border-radius: 8px;
  overflow: hidden;
  border: 1px solid #e8e0d8;
  transition: box-shadow 0.2s;
  display: flex;
  flex-direction: column;
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
  flex: 1;
  display: flex;
  flex-direction: column;
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
  flex: 1;
}

.product-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: auto;
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
  padding: 8px 16px;
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

.loading-state {
  text-align: center;
  padding: 100px 0;
  font-family: 'DM Sans', sans-serif;
  font-size: 18px;
  color: #888;
}
</style>
