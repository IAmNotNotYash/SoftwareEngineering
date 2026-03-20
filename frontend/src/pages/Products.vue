<template>
  <div class="products">
    <div class="page-header">
      <div>
        <h1>Products</h1>
        <p>Manage your product catalog with tiered pricing.</p>
      </div>
      <button class="btn-primary" @click="showAddProduct = true">＋ Add Product</button>
    </div>

    <div class="products-grid">
      <div class="product-card card" v-for="p in products" :key="p.name">
        <div class="product-gallery" :style="{ background: p.gradient }">
          <span class="photo-count">🖼 {{ p.photos }} photos</span>
        </div>
        <div class="product-body">
          <h3>{{ p.name }}</h3>
          <div class="tier-prices">
            <div class="tier-row follower">
              <span class="tier-badge"><span class="tier-dot follower-dot"></span> Follower</span>
              <span>₹{{ p.follower.toLocaleString() }}</span>
            </div>
            <div class="tier-row fan">
              <span class="tier-badge"><span class="tier-dot fan-dot"></span> Fan</span>
              <span>₹{{ p.fan.toLocaleString() }}</span>
            </div>
            <div class="tier-row patron">
              <span class="tier-badge"><span class="tier-dot patron-dot"></span> Patron</span>
              <span>₹{{ p.patron.toLocaleString() }}</span>
            </div>
          </div>
          <button class="btn-secondary edit-btn">Edit Product</button>
        </div>
      </div>
    </div>

    <!-- Add Product Modal -->
    <div v-if="showAddProduct" class="modal-overlay" @click.self="showAddProduct = false">
      <div class="modal card">
        <div class="modal-header">
          <div class="modal-back" @click="showAddProduct = false">← Back</div>
          <div>
            <h2>Add Product</h2>
            <p>Create a new product with tiered pricing for your audience.</p>
          </div>
        </div>

        <div class="modal-body">
          <div class="card section-card">
            <h4>Basic Info</h4>
            <div class="form-group">
              <label>Product Name</label>
              <input v-model="newProduct.name" class="input-field" placeholder="e.g. Abstract Canvas Print" />
            </div>
            <div class="form-group">
              <label>Description</label>
              <textarea v-model="newProduct.description" class="input-field" rows="3" placeholder="Describe your product..."></textarea>
            </div>
          </div>

          <div class="card section-card">
            <h4>Image Gallery</h4>
            <div class="gallery-grid">
              <div class="add-image-box">
                <span>＋</span>
                <small>Add Image</small>
              </div>
            </div>
          </div>

          <div class="card section-card">
            <h4>Tiered Pricing</h4>
            <p style="font-size:12px; color:var(--text-2); margin-bottom:14px">Set different prices for each audience tier.</p>
            <div class="tier-inputs">
              <div class="tier-input-card">
                <span class="tier-label"><span class="tier-dot follower-dot"></span> Follower</span>
                <div class="rupee-input">
                  <span>₹</span>
                  <input v-model.number="newProduct.follower" class="input-field" type="number" placeholder="0" />
                </div>
              </div>
              <div class="tier-input-card fan-card">
                <span class="tier-label"><span class="tier-dot fan-dot"></span> Fan</span>
                <div class="rupee-input">
                  <span>₹</span>
                  <input v-model.number="newProduct.fan" class="input-field" type="number" placeholder="0" />
                </div>
              </div>
              <div class="tier-input-card patron-card">
                <span class="tier-label"><span class="tier-dot patron-dot"></span> Patron</span>
                <div class="rupee-input">
                  <span>₹</span>
                  <input v-model.number="newProduct.patron" class="input-field" type="number" placeholder="0" />
                </div>
              </div>
            </div>
          </div>
        </div>

        <div class="modal-footer">
          <button class="btn-secondary" @click="showAddProduct = false">Cancel</button>
          <button class="btn-primary" @click="createProduct">💾 Create Product</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'

const showAddProduct = ref(false)

const products = ref([
  { name: 'Abstract Canvas Print', photos: 4, gradient: 'linear-gradient(135deg,#F9A8D4,#FDE68A)', follower: 1200, fan: 999, patron: 799 },
  { name: 'Digital Art Bundle', photos: 6, gradient: 'linear-gradient(135deg,#A5B4FC,#DDD6FE)', follower: 500, fan: 399, patron: 299 },
  { name: 'Custom Portrait', photos: 3, gradient: 'linear-gradient(135deg,#6EE7B7,#BAE6FD)', follower: 3500, fan: 2999, patron: 2499 },
])

const newProduct = reactive({ name: '', description: '', follower: 0, fan: 0, patron: 0 })

function createProduct() {
  if (!newProduct.name) return
  products.value.push({
    name: newProduct.name,
    photos: 0,
    gradient: 'linear-gradient(135deg,#FED7AA,#FDE68A)',
    follower: newProduct.follower,
    fan: newProduct.fan,
    patron: newProduct.patron,
  })
  Object.assign(newProduct, { name: '', description: '', follower: 0, fan: 0, patron: 0 })
  showAddProduct.value = false
}
</script>

<style scoped>
.products { display: flex; flex-direction: column; gap: 24px; }

.page-header { display: flex; justify-content: space-between; align-items: flex-start; }
.page-header h1 { font-size: 26px; margin-bottom: 4px; }
.page-header p { color: var(--text-2); }

.products-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 20px;
}

.product-card { overflow: hidden; transition: transform 0.15s, box-shadow 0.15s; }
.product-card:hover { transform: translateY(-2px); box-shadow: var(--shadow-md); }

.product-gallery {
  height: 180px;
  position: relative;
  display: flex;
  align-items: flex-end;
  padding: 10px;
}

.photo-count {
  background: rgba(0,0,0,0.3);
  color: white;
  font-size: 12px;
  padding: 3px 9px;
  border-radius: 20px;
  backdrop-filter: blur(4px);
}

.product-body { padding: 16px; }

.product-body h3 {
  font-size: 15px;
  font-family: 'DM Sans', sans-serif;
  font-weight: 600;
  margin-bottom: 12px;
}

.tier-prices { display: flex; flex-direction: column; gap: 6px; margin-bottom: 14px; }

.tier-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 13px;
}

.tier-badge {
  display: flex;
  align-items: center;
  gap: 7px;
  color: var(--text-2);
}

.tier-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  display: inline-block;
}
.follower-dot { background: var(--follower); }
.fan-dot { background: var(--fan); }
.patron-dot { background: var(--patron); }

.edit-btn { width: 100%; justify-content: center; }

/* Modal */
.modal-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0,0,0,0.3);
  backdrop-filter: blur(2px);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 100;
  padding: 20px;
}

.modal {
  width: 100%;
  max-width: 520px;
  max-height: 90vh;
  overflow-y: auto;
  padding: 24px;
}

.modal-header { margin-bottom: 20px; }
.modal-back {
  font-size: 13px;
  color: var(--text-2);
  cursor: pointer;
  margin-bottom: 8px;
  transition: color 0.12s;
}
.modal-back:hover { color: var(--orange); }
.modal-header h2 { font-size: 22px; margin-bottom: 4px; }
.modal-header p { font-size: 13px; color: var(--text-2); }

.modal-body { display: flex; flex-direction: column; gap: 16px; }

.section-card { padding: 16px; }
.section-card h4 { font-size: 14px; font-weight: 600; font-family: 'DM Sans', sans-serif; margin-bottom: 12px; }

.form-group { margin-bottom: 12px; }
.form-group:last-child { margin-bottom: 0; }
textarea.input-field { resize: vertical; }

.gallery-grid { display: flex; gap: 10px; }

.add-image-box {
  width: 80px;
  height: 80px;
  border: 2px dashed var(--border);
  border-radius: 10px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 4px;
  cursor: pointer;
  color: var(--text-3);
  font-size: 18px;
  transition: all 0.12s;
}
.add-image-box:hover { border-color: var(--orange); color: var(--orange); background: var(--orange-pale); }
.add-image-box small { font-size: 11px; }

.tier-inputs { display: grid; grid-template-columns: repeat(3, 1fr); gap: 10px; }

.tier-input-card {
  border: 1.5px solid var(--border);
  border-radius: 10px;
  padding: 12px;
}
.fan-card { border-color: #FED7AA; background: #FFF7ED; }
.patron-card { border-color: #DDD6FE; background: #F5F3FF; }

.tier-label {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 12px;
  font-weight: 600;
  color: var(--text-2);
  margin-bottom: 8px;
}

.rupee-input { display: flex; align-items: center; gap: 6px; }
.rupee-input span { color: var(--text-2); font-weight: 500; }
.rupee-input .input-field { padding: 8px 10px; }

.modal-footer {
  display: flex;
  justify-content: space-between;
  margin-top: 20px;
  padding-top: 16px;
  border-top: 1px solid var(--border);
}
</style>