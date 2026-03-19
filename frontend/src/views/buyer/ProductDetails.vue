<template>
  <div>
    <BuyerNavbar />
    
    <div class="page-container" v-if="product">
      <!-- Breadcrumb -->
      <div class="breadcrumb">
        <RouterLink to="/buyer/products">Products</RouterLink>
        <span class="separator">/</span>
        <span class="current">{{ product.title }}</span>
      </div>

      <div class="product-layout">
        <!-- Image Gallery Left Side -->
        <div class="product-gallery">
          <div class="main-image" :style="{ backgroundImage: `url(${activeImage})` }"></div>
          <div class="thumbnails" v-if="product.gallery && product.gallery.length > 1">
            <div 
              v-for="(img, idx) in product.gallery" 
              :key="idx" 
              class="thumb" 
              :class="{ 'active-thumb': activeImage === img }"
              :style="{ backgroundImage: `url(${img})` }"
              @click="activeImage = img"
            ></div>
          </div>
        </div>

        <!-- Product Details Right Side -->
        <div class="product-details">
          <RouterLink to="/buyer/artist/1" style="text-decoration:none;">
            <div class="artist-badge">
              <div class="artist-avatar" :style="{ backgroundImage: `url(${product.artist.avatar})` }"></div>
              <span>{{ product.artist.name }}</span>
            </div>
          </RouterLink>

          <h1 class="product-title">{{ product.title }}</h1>
          <div class="product-price">₹{{ product.price.toLocaleString('en-IN') }}</div>

          <div class="stock-status">
            <span v-if="product.inStock" class="in-stock">● In Stock</span>
            <span v-else class="out-stock">● Sold Out</span>
          </div>

          <button class="add-cart-btn" @click="cartState.addItem(product)" :disabled="!product.inStock">Add to Cart</button>

          <div class="info-section">
            <h3>Description</h3>
            <p>{{ product.description }}</p>
          </div>

          <div class="info-section">
            <h3>Materials</h3>
            <p>{{ product.materials }}</p>
          </div>

          <div class="info-section">
            <h3>Dimensions</h3>
            <p>{{ product.dimensions }}</p>
          </div>
          
        </div>
      </div>
    </div>
    
    <div v-else class="loading-state">
      Loading product details...
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import BuyerNavbar from '../../components/BuyerNavbar.vue'
import { getProductDetails } from '../../api/buyer.js'
import { cartState } from '../../store/cart.js'

const route = useRoute()
const product = ref(null)
const activeImage = ref('')

onMounted(async () => {
  const id = route.params.id
  product.value = await getProductDetails(id)
  if (product.value) {
    activeImage.value = product.value.image
  }
})
</script>

<style scoped>
.page-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 40px;
  font-family: 'DM Sans', sans-serif;
}

.breadcrumb {
  font-size: 13px;
  color: #888;
  margin-bottom: 32px;
}

.breadcrumb a {
  color: #888;
  text-decoration: none;
}

.breadcrumb a:hover {
  color: #C4622D;
}

.separator {
  margin: 0 8px;
  color: #ccc;
}

.current {
  color: #000;
  font-weight: 500;
}

.product-layout {
  display: flex;
  gap: 60px;
}

/* Gallery */
.product-gallery {
  flex: 1.2;
}

.main-image {
  width: 100%;
  aspect-ratio: 4/5;
  background-size: cover;
  background-position: center;
  border-radius: 8px;
  border: 1px solid #f0f0f0;
  margin-bottom: 16px;
}

.thumbnails {
  display: flex;
  gap: 16px;
}

.thumb {
  width: 80px;
  height: 80px;
  background-size: cover;
  background-position: center;
  border-radius: 6px;
  cursor: pointer;
  border: 2px solid transparent;
  transition: border-color 0.2s;
  opacity: 0.7;
}

.thumb:hover {
  opacity: 1;
}

.active-thumb {
  border-color: #C4622D;
  opacity: 1;
}

/* Details */
.product-details {
  flex: 1;
  display: flex;
  flex-direction: column;
}

.artist-badge {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 24px;
}

.artist-avatar {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  background-size: cover;
  background-position: center;
  border: 1px solid #e8e0d8;
}

.artist-badge span {
  font-size: 14px;
  font-weight: 500;
  color: #555;
}

.product-title {
  font-family: 'Playfair Display', serif;
  font-size: 40px;
  font-weight: 600;
  color: #000;
  margin-bottom: 16px;
  line-height: 1.2;
}

.product-price {
  font-family: 'Playfair Display', serif;
  font-size: 28px;
  color: #000;
  margin-bottom: 24px;
}

.stock-status {
  margin-bottom: 32px;
  font-size: 13px;
  font-weight: 600;
  letter-spacing: 0.5px;
  text-transform: uppercase;
}

.in-stock {
  color: #10b981;
}

.out-stock {
  color: #d94242;
}

.add-cart-btn {
  background: #C4622D;
  color: white;
  border: none;
  padding: 16px;
  border-radius: 4px;
  font-family: 'DM Sans', sans-serif;
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
  transition: background 0.2s;
  margin-bottom: 48px;
}

.add-cart-btn:hover {
  background: #a95224;
}

.add-cart-btn:disabled {
  background: #ccc;
  cursor: not-allowed;
}

.info-section {
  margin-bottom: 32px;
}

.info-section h3 {
  font-family: 'Playfair Display', serif;
  font-size: 18px;
  font-weight: 600;
  color: #000;
  margin-bottom: 12px;
  border-bottom: 1px solid #e8e0d8;
  padding-bottom: 8px;
}

.info-section p {
  font-size: 15px;
  line-height: 1.6;
  color: #555;
}

.loading-state {
  text-align: center;
  padding: 100px 0;
  font-family: 'DM Sans', sans-serif;
  font-size: 18px;
  color: #888;
}
</style>
