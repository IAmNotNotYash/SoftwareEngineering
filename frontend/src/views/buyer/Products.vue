<template>
  <div>
    <BuyerNavbar />
    <div class="page-container">
      <div class="header-section">
        <h1 class="page-title">Browse Catalogue</h1>
        <div class="filters">
          <input type="text" v-model="searchQuery" placeholder="Search pieces or artists..." class="search-input" />
          <select class="filter-select" v-model="selectedCategory">
            <option value="">All Categories</option>
            <option v-for="cat in categories" :key="cat" :value="cat">{{ cat }}</option>
          </select>
        </div>
      </div>

      <div class="products-grid">
          <div v-for="product in filteredProducts" :key="product.id" class="product-card">
            <RouterLink :to="`/buyer/product/${product.id}`" style="display: block; text-decoration: none; color: inherit;">
              <div class="product-image" :style="{ backgroundImage: `url(${product.image})` }">
                <div class="category-badge">{{ product.category }}</div>
              </div>
            </RouterLink>
            <div class="product-info">
              <div class="product-artist">{{ product.artist_name }}</div>
              <RouterLink :to="`/buyer/product/${product.id}`" class="product-title-link">
                <div class="product-title">{{ product.title }}</div>
              </RouterLink>
              <div class="product-footer">
                <span class="product-price">₹{{ product.price.toLocaleString('en-IN') }}</span>
                <button class="add-cart-btn" @click="handleAddToCart(product)" :disabled="addingId === product.id">
                  {{ addingId === product.id ? '...' : 'Add to Cart' }}
                </button>
              </div>
            </div>
          </div>
        <div v-if="filteredProducts.length === 0" class="no-results">
          No pieces match your search.
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import BuyerNavbar from '../../components/BuyerNavbar.vue'
import { getProducts } from '../../api/commerce.js'
import { useCartStore } from '../../stores/cart.js'

const cartStore = useCartStore()
const products = ref([])
const searchQuery = ref('')
const selectedCategory = ref('')
const addingId = ref(null)

onMounted(async () => {
  const data = await getProducts()
  // backend returns { products: [...] }
  products.value = Array.isArray(data) ? data : (data.products || [])
})

const filteredProducts = computed(() => {
  let list = products.value
  if (selectedCategory.value) list = list.filter(p => p.category === selectedCategory.value)
  if (searchQuery.value) {
    const q = searchQuery.value.toLowerCase()
    list = list.filter(p =>
      p.title.toLowerCase().includes(q) ||
      (p.artist_name || '').toLowerCase().includes(q) ||
      (p.category || '').toLowerCase().includes(q)
    )
  }
  return list
})

const categories = computed(() => [...new Set(products.value.map(p => p.category).filter(Boolean))])

async function handleAddToCart(product) {
  addingId.value = product.id
  try {
    await cartStore.addItem(product.id)
  } catch (e) {
    alert(e.message)
  } finally {
    addingId.value = null
  }
}
</script>

<style scoped>
.page-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 40px 40px;
}

.header-section {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 40px;
}

.page-title {
  font-family: 'Playfair Display', serif;
  font-size: 28px;
  font-weight: 600;
  color: #000;
  margin: 0;
}

.filters {
  display: flex;
  gap: 16px;
}

.search-input, .category-select {
  font-family: 'DM Sans', sans-serif;
  padding: 8px 16px;
  border: 1px solid #e8e0d8;
  border-radius: 4px;
  font-size: 14px;
  outline: none;
  transition: border-color 0.2s;
  color: #555;
}

.search-input:focus, .category-select:focus {
  border-color: #C4622D;
}

.products-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 24px;
}

.product-card {
  font-family: 'DM Sans', sans-serif;
  background: #ffffff;
  border-radius: 8px;
  overflow: hidden;
  border: 1px solid #f0f0f0;
  transition: box-shadow 0.2s;
  display: flex;
  flex-direction: column;
}

.product-card:hover {
  box-shadow: 0 6px 16px rgba(0, 0, 0, 0.06);
}

.product-image {
  height: 200px;
  background-size: cover;
  background-position: center;
  position: relative;
}

.category-badge {
  position: absolute;
  top: 12px;
  left: 12px;
  background: rgba(255, 255, 255, 0.95);
  color: #000;
  font-size: 10px;
  font-weight: 600;
  padding: 4px 10px;
  border-radius: 4px;
  text-transform: uppercase;
  letter-spacing: 0.5px;
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

.product-title-link {
  text-decoration: none;
  color: inherit;
  flex: 1;
}

.product-title-link:hover .product-title {
  color: #C4622D;
}

.product-title {
  font-family: 'Playfair Display', serif;
  font-size: 16px;
  font-weight: 600;
  color: #000;
  margin-bottom: 24px;
  line-height: 1.4;
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
  font-size: 16px;
  font-weight: 600;
  color: #000;
}

.add-cart-btn {
  font-family: 'DM Sans', sans-serif;
  background: transparent;
  color: #C4622D;
  border: 1px solid #C4622D;
  padding: 6px 12px;
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

.no-results {
  grid-column: 1 / -1;
  text-align: center;
  padding: 60px 0;
  color: #888;
  font-size: 16px;
  font-family: 'DM Sans', sans-serif;
}

.loading-state {
  text-align: center;
  padding: 60px 0;
  font-size: 16px;
  font-family: 'DM Sans', sans-serif;
  color: #888;
}
</style>
