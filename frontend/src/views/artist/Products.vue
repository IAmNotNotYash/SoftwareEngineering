<template>
  <div class="products-page">
    <ArtistNavbar />

    <main class="page-container">
      <div class="page-header">
        <div>
          <h1 class="page-title">Products</h1>
          <p class="subtitle">Manage your product catalog and tier-based pricing rings.</p>
        </div>
        <button class="btn primary-btn" @click="showAddProduct = true">+ Add Product</button>
      </div>

      <div class="products-grid">
        <div class="product-card" v-for="p in products" :key="p.name">
          <div class="product-gallery" :style="p.images.length ? `background-image: url(${p.images[0]})` : `background: ${p.gradient}`">
            <span class="photo-count">🖼 {{ p.photos || p.images.length }} photos</span>
          </div>
          <div class="product-body">
            <h3>{{ p.name }}</h3>
            <div class="tier-prices">
              <div class="tier-row">
                <span class="tier-badge"><span class="tier-dot follower-dot"></span> Follower</span>
                <span>₹{{ p.follower.toLocaleString() }}</span>
              </div>
              <div class="tier-row">
                <span class="tier-badge"><span class="tier-dot fan-dot"></span> Fan</span>
                <span>₹{{ p.fan.toLocaleString() }}</span>
              </div>
              <div class="tier-row">
                <span class="tier-badge"><span class="tier-dot patron-dot"></span> Patron</span>
                <span>₹{{ p.patron.toLocaleString() }}</span>
              </div>
            </div>
            <button class="btn secondary-btn edit-btn">Edit Product</button>
          </div>
        </div>
      </div>

      <!-- Add Product Modal -->
      <div v-if="showAddProduct" class="modal-overlay" @click.self="showAddProduct = false">
        <div class="modal">
          <div class="modal-header">
            <div>
              <h2 class="modal-title">Add New Product</h2>
              <p class="modal-subtitle">Upload product images and set pricing tiers.</p>
            </div>
            <button class="close-btn" @click="showAddProduct = false">×</button>
          </div>

          <div class="modal-body">
            <div class="form-section">
              <label class="form-label">Basic Information</label>
              <div class="form-group">
                <input v-model="newProduct.name" class="input-field" placeholder="Product Name (e.g. Handmade Ceramic Vase)" />
              </div>
              <div class="form-group">
                <textarea v-model="newProduct.description" class="input-field" rows="3" placeholder="Describe the crafting process and materials..."></textarea>
              </div>
            </div>

            <div class="form-section">
              <label class="form-label">Product Imagery</label>
              <div class="upload-zone" @click="triggerUpload">
                <input type="file" ref="fileInput" hidden multiple accept="image/*" @change="handleImageUpload" />
                <div class="upload-content" v-if="!newProduct.images.length">
                  <span class="upload-icon">📸</span>
                  <p>Click or drag images to upload</p>
                  <small>JPG, PNG up to 10MB</small>
                </div>
                <div class="image-previews" v-else>
                  <div class="preview-box" v-for="(img, idx) in newProduct.images" :key="idx" :style="{ backgroundImage: `url(${img})` }">
                    <button class="remove-img" @click.stop="removeImage(idx)">×</button>
                  </div>
                  <div class="preview-box add-more" @click.stop="triggerUpload">
                    <span>+</span>
                  </div>
                </div>
              </div>
            </div>

            <div class="form-section">
              <label class="form-label">Tiered Pricing</label>
              <div class="tier-inputs">
                <div class="tier-input-card">
                  <span class="tier-badge"><span class="tier-dot follower-dot"></span> Follower</span>
                  <div class="currency-input">
                    <span>₹</span>
                    <input v-model.number="newProduct.follower" type="number" placeholder="0" />
                  </div>
                </div>
                <div class="tier-input-card">
                  <span class="tier-badge"><span class="tier-dot fan-dot"></span> Fan</span>
                  <div class="currency-input">
                    <span>₹</span>
                    <input v-model.number="newProduct.fan" type="number" placeholder="0" />
                  </div>
                </div>
                <div class="tier-input-card">
                  <span class="tier-badge"><span class="tier-dot patron-dot"></span> Patron</span>
                  <div class="currency-input">
                    <span>₹</span>
                    <input v-model.number="newProduct.patron" type="number" placeholder="0" />
                  </div>
                </div>
              </div>
            </div>
          </div>

          <div class="modal-footer">
            <button class="btn secondary-btn" @click="showAddProduct = false">Cancel</button>
            <button class="btn primary-btn" @click="createProduct">Publish Product</button>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import ArtistNavbar from '../../components/ArtistNavbar.vue'

const showAddProduct = ref(false)
const fileInput = ref(null)

const products = ref([
  { name: 'Abstract Canvas Print', photos: 4, gradient: 'linear-gradient(135deg,#e8e0d8,#faf8f5)', images: ['https://images.unsplash.com/photo-1544816155-12df9643f363?w=600'], follower: 1200, fan: 999, patron: 799 },
  { name: 'Digital Art Bundle', photos: 6, gradient: 'linear-gradient(135deg,#e8e0d8,#faf8f5)', images: ['https://images.unsplash.com/photo-1534528741775-53994a69daeb?w=600'], follower: 500, fan: 399, patron: 299 },
  { name: 'Earth Tone Teapot', photos: 3, gradient: 'linear-gradient(135deg,#e8e0d8,#faf8f5)', images: ['https://images.unsplash.com/photo-1610701596007-11502861dcfa?w=600'], follower: 3500, fan: 2999, patron: 2499 },
])

const newProduct = reactive({ name: '', description: '', images: [], follower: 0, fan: 0, patron: 0 })

const triggerUpload = () => {
  fileInput.value.click()
}

const handleImageUpload = (e) => {
  const files = e.target.files
  if (!files) return
  
  for(let i=0; i < files.length; i++) {
    const url = URL.createObjectURL(files[i])
    newProduct.images.push(url)
  }
}

const removeImage = (idx) => {
  newProduct.images.splice(idx, 1)
}

const createProduct = () => {
  if (!newProduct.name) return
  
  products.value.unshift({
    name: newProduct.name,
    photos: newProduct.images.length,
    gradient: 'linear-gradient(135deg,#f0f0f0,#e0e0e0)',
    images: [...newProduct.images],
    follower: newProduct.follower,
    fan: newProduct.fan,
    patron: newProduct.patron,
  })
  
  Object.assign(newProduct, { name: '', description: '', images: [], follower: 0, fan: 0, patron: 0 })
  showAddProduct.value = false
}
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
  padding: 16px;
  display: flex;
  align-items: flex-end;
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