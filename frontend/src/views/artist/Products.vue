<template>
  <div class="products-page">
    <ArtistNavbar />

    <main class="page-container">
      <div class="page-header">
        <div>
          <h1 class="page-title">Products</h1>
          <p class="subtitle">All products across your catalogues.</p>
        </div>
      </div>

      <!-- Catalogue filter tabs -->
      <div class="catalogue-tabs" v-if="catalogues.length">
        <button
          class="tab-btn"
          :class="{ active: selectedCatalogueId === null }"
          @click="selectedCatalogueId = null"
        >All</button>
        <button
          v-for="cat in catalogues"
          :key="cat.id"
          class="tab-btn"
          :class="{ active: selectedCatalogueId === cat.id }"
          @click="selectedCatalogueId = cat.id"
        >{{ cat.title }}</button>
      </div>

      <!-- Loading state -->
      <div v-if="loading" class="state-box">
        <div class="spinner"></div>
        <p>Loading your products…</p>
      </div>

      <!-- Error state -->
      <div v-else-if="error" class="state-box error-state">
        <span>⚠️</span>
        <p>{{ error }}</p>
        <button class="btn primary-btn" @click="fetchProducts">Retry</button>
      </div>

      <!-- Empty state -->
      <div v-else-if="filteredProducts.length === 0" class="state-box">
        <span class="empty-icon">🎨</span>
        <p>No products found{{ selectedCatalogueId ? ' in this catalogue' : '' }}.</p>
      </div>

      <!-- Product grid -->
      <div class="products-grid" v-else>
        <div class="product-card" v-for="p in filteredProducts" :key="p.id">
          <div
            class="product-gallery"
            :style="imageUrl(p) ? `background-image: url(${imageUrl(p)})` : `background: linear-gradient(135deg,#e8e0d8,#faf8f5)`"
          >
            <div class="gallery-row">
              <span class="photo-count">🖼 {{ (p.gallery && p.gallery.length) || 0 }} photo{{ (!p.gallery || p.gallery.length !== 1) ? 's' : '' }}</span>
              <span v-if="!p.in_stock" class="out-of-stock-badge">Out of Stock</span>
            </div>
          </div>
          <div class="product-body">
            <h3>{{ p.title }}</h3>
            <p class="product-desc" v-if="p.description">{{ p.description }}</p>
            <div class="price-row">
              <span class="price-label">Price</span>
              <span class="price-value">₹{{ Number(p.price).toLocaleString('en-IN') }}</span>
            </div>
            <div class="catalogue-tag" v-if="catalogueLabel(p.catalogue_id)">
              📁 {{ catalogueLabel(p.catalogue_id) }}
            </div>
            <div class="card-actions">
              <button class="btn primary-btn edit-btn" @click="openEdit(p)">Edit in Catalogue</button>
            </div>
          </div>
        </div>
      </div>


    </main>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import ArtistNavbar from '../../components/ArtistNavbar.vue'
import { getProducts } from '../../api/products.js'
import { getCatalogues } from '../../api/catalogue.js'

// ── State ────────────────────────────────────────────────────────────────────
const router = useRouter()
const products = ref([])
const catalogues = ref([])
const selectedCatalogueId = ref(null)
const loading = ref(true)
const error = ref(null)

// ── Computed ─────────────────────────────────────────────────────────────────
const filteredProducts = computed(() => {
  if (!selectedCatalogueId.value) return products.value
  return products.value.filter(p => p.catalogue_id === selectedCatalogueId.value)
})

// ── Helpers ───────────────────────────────────────────────────────────────────
// The API returns `p.image` (primary URL string) and `p.gallery` (array of URL strings)
function imageUrl(product) {
  const url = product.image || (product.gallery && product.gallery[0]) || null
  if (!url) return null
  // Prefix the Flask dev server base for local /static/ paths
  if (url.startsWith('/static/')) {
    return `http://localhost:5000${url}`
  }
  return url
}

function catalogueLabel(catalogueId) {
  if (!catalogueId) return null
  const cat = catalogues.value.find(c => c.id === catalogueId)
  return cat ? cat.title : null
}

// ── Fetch ─────────────────────────────────────────────────────────────────────
async function fetchProducts() {
  loading.value = true
  error.value = null
  try {
    const userJson = sessionStorage.getItem('user')
    const userId = userJson ? JSON.parse(userJson).id : null
    const [productsData, catalogueData] = await Promise.all([
      getProducts({ user_id: userId }),
      getCatalogues({ user_id: userId, status: '' })
    ])
    // API returns array directly for products
    products.value = Array.isArray(productsData) ? productsData : (productsData.products || [])
    catalogues.value = Array.isArray(catalogueData) ? catalogueData : (catalogueData.catalogues || [])
  } catch (err) {
    error.value = err.message || 'Failed to load products.'
  } finally {
    loading.value = false
  }
}

// ── Actions ───────────────────────────────────────────────────────────────────
function openEdit(product) {
  if (product.catalogue_id) {
    router.push({ path: `/artist/edit-catalogue/${product.catalogue_id}`, query: { section: 'products' } })
  } else {
    router.push('/artist/catalogues')
  }
}

onMounted(fetchProducts)
</script>


<style scoped>
.products-page {
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
  cursor: pointer;
  transition: all 0.2s ease;
  border: none;
}

.primary-btn {
  background: #C4622D;
  color: #fff;
}
.primary-btn:hover { background: #a85427; }

.secondary-btn {
  background: #fff;
  border: 1px solid #e8e0d8;
  color: #1a1a1a;
}

.danger-btn {
  background: #dc2626;
  color: #fff;
  border: none;
}
.danger-btn:hover:not(:disabled) { background: #b91c1c; }
.danger-btn:disabled { opacity: 0.6; cursor: not-allowed; }

/* Catalogue filter tabs */
.catalogue-tabs {
  display: flex;
  gap: 10px;
  flex-wrap: wrap;
  margin-bottom: 32px;
}

.tab-btn {
  padding: 8px 18px;
  border-radius: 20px;
  border: 1px solid #e8e0d8;
  background: #fff;
  font-size: 14px;
  font-weight: 500;
  color: #555;
  cursor: pointer;
  transition: all 0.2s ease;
}

.tab-btn:hover { border-color: #C4622D; color: #C4622D; }
.tab-btn.active { background: #C4622D; color: #fff; border-color: #C4622D; }

/* State boxes (loading / error / empty) */
.state-box {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 80px 20px;
  gap: 16px;
  color: #888;
  font-size: 16px;
}

.empty-icon { font-size: 48px; }

.error-state { color: #dc2626; }

/* Spinner */
.spinner {
  width: 40px;
  height: 40px;
  border: 3px solid #e8e0d8;
  border-top-color: #C4622D;
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}

@keyframes spin { to { transform: rotate(360deg); } }

/* Product card extras */
.product-desc {
  font-size: 13px;
  color: #888;
  margin: 0 0 12px 0;
  overflow: hidden;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
}

.price-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 10px;
}

.price-label {
  font-size: 13px;
  color: #888;
}

.price-value {
  font-size: 18px;
  font-weight: 700;
  color: #C4622D;
}

.catalogue-tag {
  font-size: 12px;
  color: #777;
  background: #faf8f5;
  border: 1px solid #e8e0d8;
  border-radius: 20px;
  padding: 4px 10px;
  display: inline-block;
  margin-bottom: 14px;
}

.card-actions {
  display: flex;
  gap: 8px;
}

.card-actions .btn {
  flex: 1;
  padding: 8px 12px;
  font-size: 13px;
}

.out-of-stock-badge {
  background: rgba(220,38,38,0.85);
  color: #fff;
  font-size: 11px;
  font-weight: 700;
  padding: 4px 10px;
  border-radius: 20px;
  backdrop-filter: blur(4px);
  margin-left: auto;
}

/* Confirm modal */
.confirm-modal {
  max-width: 420px;
}

.confirm-modal .modal-body p {
  font-size: 15px;
  color: #444;
  line-height: 1.6;
}
.secondary-btn:hover { border-color: #C4622D; color: #C4622D; }

/* Grid */
.products-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 24px;
}

.product-card {
  background: #ffffff;
  border-radius: 12px;
  border: 1px solid #e8e0d8;
  overflow: hidden;
  box-shadow: 0 4px 20px rgba(0,0,0,0.02);
  transition: transform 0.2s ease, box-shadow 0.2s;
}

.product-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 12px 30px rgba(0,0,0,0.06);
}

.product-gallery {
  height: 200px;
  background-size: cover;
  background-position: center;
  background-color: #f5f1ed;
  padding: 16px;
  display: flex;
  align-items: flex-end;
}

.gallery-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  width: 100%;
  gap: 8px;
}

.photo-count {
  background: rgba(0,0,0,0.5);
  color: white;
  font-size: 12px;
  font-weight: 600;
  padding: 4px 10px;
  border-radius: 20px;
  backdrop-filter: blur(4px);
}

.product-body {
  padding: 20px;
}

.product-body h3 {
  font-family: var(--font-heading);
  font-size: 20px;
  margin: 0 0 16px 0;
  color: #1a1a1a;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.tier-prices {
  display: flex;
  flex-direction: column;
  gap: 8px;
  margin-bottom: 24px;
}

.tier-row {
  display: flex;
  justify-content: space-between;
  font-size: 14px;
  color: #555;
}

.tier-badge {
  display: flex;
  align-items: center;
  gap: 8px;
}

.tier-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
}
.follower-dot { background: #3B82F6; }
.fan-dot { background: #F97316; }
.patron-dot { background: #8B5CF6; }

.edit-btn {
  width: 100%;
}

/* Modal */
.modal-overlay {
  position: fixed;
  inset: 0;
  background: rgba(20,20,20,0.6);
  backdrop-filter: blur(4px);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
  padding: 20px;
}

.modal {
  background: #ffffff;
  border-radius: 12px;
  width: 100%;
  max-width: 600px;
  max-height: 90vh;
  overflow-y: auto;
  box-shadow: 0 20px 40px rgba(0,0,0,0.2);
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 24px 32px;
  border-bottom: 1px solid #f0f0f0;
}

.modal-title {
  font-family: var(--font-heading);
  font-size: 24px;
  margin: 0 0 4px 0;
}

.modal-subtitle {
  font-size: 14px;
  color: #888;
  margin: 0;
}

.close-btn {
  background: none;
  border: none;
  font-size: 28px;
  color: #888;
  cursor: pointer;
}

.modal-body {
  padding: 32px;
  display: flex;
  flex-direction: column;
  gap: 32px;
}

.form-section {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.form-label {
  font-size: 14px;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  color: #C4622D;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.input-field {
  width: 100%;
  padding: 12px 16px;
  border: 1px solid #e8e0d8;
  border-radius: 6px;
  font-family: var(--font-body);
  font-size: 15px;
  box-sizing: border-box;
}

.input-field:focus {
  outline: none;
  border-color: #C4622D;
}

.upload-zone {
  border: 2px dashed #e8e0d8;
  border-radius: 8px;
  background: #faf8f5;
  padding: 32px;
  text-align: center;
  cursor: pointer;
  transition: all 0.2s;
}

.upload-zone:hover {
  border-color: #C4622D;
  background: #fdf2ed;
}

.upload-content p {
  margin: 8px 0 4px;
  font-weight: 600;
  color: #333;
}

.upload-content small {
  color: #888;
}

.upload-icon {
  font-size: 32px;
}

.image-previews {
  display: flex;
  gap: 12px;
  flex-wrap: wrap;
}

.preview-box {
  width: 80px;
  height: 80px;
  border-radius: 8px;
  background-size: cover;
  background-position: center;
  position: relative;
}

.remove-img {
  position: absolute;
  top: -6px;
  right: -6px;
  background: #1a1a1a;
  color: #fff;
  border: none;
  width: 20px;
  height: 20px;
  border-radius: 50%;
  font-size: 12px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
}

.add-more {
  border: 1px dashed #C4622D;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #C4622D;
  background: transparent;
  font-size: 24px;
}

.tier-inputs {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 16px;
}

.tier-input-card {
  padding: 16px;
  border: 1px solid #e8e0d8;
  border-radius: 8px;
  background: #faf8f5;
}

.currency-input {
  display: flex;
  align-items: center;
  gap: 8px;
  background: #fff;
  border: 1px solid #e8e0d8;
  border-radius: 6px;
  padding: 8px 12px;
  margin-top: 12px;
}

.currency-input input {
  border: none;
  outline: none;
  width: 100%;
  font-family: var(--font-body);
  font-size: 15px;
}

.modal-footer {
  padding: 24px 32px;
  border-top: 1px solid #f0f0f0;
  display: flex;
  justify-content: flex-end;
  gap: 16px;
  background: #faf8f5;
  border-bottom-left-radius: 12px;
  border-bottom-right-radius: 12px;
}
</style>