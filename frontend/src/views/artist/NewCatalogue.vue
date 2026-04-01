<template>
  <div class="builder-page">
    <ArtistNavbar />
    
    <main class="page-container">
      <div class="page-header">
        <div>
          <router-link to="/artist/catalogues" class="back-link">← Back to Catalogues</router-link>
          <h1 class="page-title">Catalogue Builder</h1>
          <p class="subtitle">Design and launch a highly aesthetic product catalogue.</p>
        </div>
      </div>

      <div class="builder-layout">
        <!-- Sidebar Navigation -->
        <aside class="sidebar-steps">
          <div 
            v-for="(step, idx) in steps" 
            :key="idx" 
            class="step-item"
            :class="{ active: currentStep === idx, completed: currentStep > idx }"
            @click="currentStep > idx ? currentStep = idx : null"
          >
            <div class="step-indicator">
              <span v-if="currentStep > idx">✓</span>
              <span v-else>{{ idx + 1 }}</span>
            </div>
            <span class="step-label">{{ step }}</span>
          </div>
        </aside>

        <!-- Builder Content Panels -->
        <section class="builder-content">
          
          <!-- Step 1: Details -->
          <div class="panel card" v-if="currentStep === 0">
            <h2>Catalogue Details</h2>
            <div class="form-group">
              <label>Catalogue Title</label>
              <input v-model="form.title" class="input-field" placeholder="e.g. Earth Tone Spring Collection" />
            </div>
            <div class="form-group">
              <label>Brand Narrative / Tagline</label>
              <textarea v-model="form.narrative" class="input-field" rows="3" placeholder="Set the mood for this catalogue..."></textarea>
            </div>
          </div>

          <!-- Step 2: Visuals -->
          <div class="panel card" v-if="currentStep === 1">
            <h2>Cover Visuals</h2>
            <p class="field-hint">Upload a stunning full-bleed cover photo for your catalogue landing page.</p>
            
            <div 
              class="cover-upload-zone" 
              :class="{ 'has-image': form.coverPhoto }"
              :style="form.coverPhoto ? { backgroundImage: `url(${form.coverPhoto})` } : {}"
              @click="!form.coverPhoto ? $refs.fileInput.click() : null"
            >
              <input type="file" ref="fileInput" hidden accept="image/*" @change="handleCoverUpload" />
              
              <div class="upload-prompt" v-if="!form.coverPhoto">
                <span class="upload-icon">📸</span>
                <p>Upload High-Res Cover Image</p>
                <small>Recommended: 1920x1080</small>
              </div>
              
              <button class="remove-btn btn secondary-btn small-btn" v-if="form.coverPhoto" @click.stop="form.coverPhoto = null">
                Change Cover
              </button>
            </div>
            
            <div class="form-group" style="margin-top:24px">
              <label>Theme Palette</label>
              <div class="palette-options">
                <div class="palette-pip" style="background:#fdf2ed" :class="{active: form.theme === 'warm'}" @click="form.theme = 'warm'">Warm</div>
                <div class="palette-pip" style="background:#f4f0ea" :class="{active: form.theme === 'earth'}" @click="form.theme = 'earth'">Earth</div>
                <div class="palette-pip" style="background:#eaf2f8" :class="{active: form.theme === 'cool'}" @click="form.theme = 'cool'">Cool</div>
                <div class="palette-pip" style="background:#1a1a1a; color:#fff" :class="{active: form.theme === 'dark'}" @click="form.theme = 'dark'">Dark</div>
              </div>
            </div>
          </div>

          <!-- Step 3: Products -->
          <div class="panel card" v-if="currentStep === 2">
            <h2>Link Products</h2>
            <p class="field-hint">Select the products you want to feature in this catalogue.</p>
            
            <div class="product-grid">
              <div 
                v-for="p in availableProducts" 
                :key="p.id"
                class="product-cube"
                :class="{ selected: form.selectedProducts.includes(p.id) }"
                :style="{ backgroundImage: `url(${p.img})` }"
                @click="toggleProduct(p.id)"
              >
                <div class="cube-overlay">
                  <span class="product-name">{{ p.name }}</span>
                  <div class="check-circle">✓</div>
                </div>
              </div>
            </div>
          </div>

          <!-- Step 4: Launch -->
          <div class="panel card" v-if="currentStep === 3">
            <h2>Ready for Launch</h2>
            <p class="field-hint">Your catalogue is ready to be published to your subscribers.</p>
            
            <div class="publish-summary">
              <ul>
                <li><strong>Title:</strong> {{ form.title || 'Untitled' }}</li>
                <li><strong>Products:</strong> {{ form.selectedProducts.length }} linked</li>
                <li><strong>Theme:</strong> {{ form.theme }}</li>
              </ul>
            </div>
            
            <div class="form-group" style="margin-top:24px">
              <label>Launch Intent</label>
              <div class="intent-options">
                <button class="intent-btn" :class="{selected: form.intent==='live'}" @click="form.intent='live'">🚀 Live Sale</button>
                <button class="intent-btn" :class="{selected: form.intent==='preview'}" @click="form.intent='preview'">👀 Exclusive Preview</button>
                <button class="intent-btn" :class="{selected: form.intent==='preorder'}" @click="form.intent='preorder'">📦 Pre-Order</button>
              </div>
            </div>
          </div>

          <div class="panel-actions">
            <button class="btn secondary-btn" @click="prevStep" :disabled="currentStep === 0">Previous Step</button>
            <button class="btn primary-btn" @click="nextStep">
              {{ currentStep === steps.length - 1 ? 'Publish Catalogue' : 'Continue' }}
            </button>
          </div>
        </section>
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import ArtistNavbar from '../../components/ArtistNavbar.vue'

const router = useRouter()
const currentStep = ref(0)
const steps = ['Overview', 'Visuals', 'Products', 'Launch']

const form = reactive({
  title: '',
  narrative: '',
  coverPhoto: null,
  theme: 'earth',
  selectedProducts: [],
  intent: 'live'
})

const availableProducts = [
  { id: 1, name: 'Abstract Canvas Print', img: 'https://images.unsplash.com/photo-1544816155-12df9643f363?w=300' },
  { id: 2, name: 'Digital Art Bundle', img: 'https://images.unsplash.com/photo-1534528741775-53994a69daeb?w=300' },
  { id: 3, name: 'Earth Tone Teapot', img: 'https://images.unsplash.com/photo-1610701596007-11502861dcfa?w=300' },
  { id: 4, name: 'Custom Portrait', img: 'https://images.unsplash.com/photo-1513364776144-60967b0f800f?w=300' },
]

const handleCoverUpload = (e) => {
  const file = e.target.files[0]
  if (file) {
    form.coverPhoto = URL.createObjectURL(file)
  }
}

const toggleProduct = (id) => {
  const idx = form.selectedProducts.indexOf(id)
  if (idx > -1) form.selectedProducts.splice(idx, 1)
  else form.selectedProducts.push(id)
}

const nextStep = () => {
  if (currentStep.value < steps.length - 1) currentStep.value++
  else {
    alert("Catalogue launched successfully!")
    router.push('/artist/catalogues')
  }
}

const prevStep = () => {
  if (currentStep.value > 0) currentStep.value--
}
</script>

<style scoped>
.builder-page {
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
  margin-bottom: 40px;
}

.back-link {
  color: #888;
  font-size: 14px;
  text-decoration: none;
  font-weight: 500;
  display: inline-block;
  margin-bottom: 12px;
}
.back-link:hover { color: #C4622D; }

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

.builder-layout {
  display: flex;
  gap: 40px;
}

.sidebar-steps {
  width: 240px;
  flex-shrink: 0;
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.step-item {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 16px 20px;
  border-radius: 8px;
  background: #ffffff;
  border: 1px solid #e8e0d8;
  color: #888;
  cursor: not-allowed;
  transition: all 0.2s;
}

.step-item.completed {
  cursor: pointer;
  color: #333;
}

.step-item.completed:hover {
  background: #fdfaf8;
  border-color: #C4622D;
}

.step-item.active {
  background: #fdf2ed;
  border-color: #C4622D;
  color: #C4622D;
  font-weight: 600;
}

.step-indicator {
  width: 24px;
  height: 24px;
  border-radius: 50%;
  border: 1px solid currentColor;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 12px;
  font-weight: 700;
}

.step-item.completed .step-indicator {
  background: #C4622D;
  color: #fff;
  border-color: #C4622D;
}

.builder-content {
  flex: 1;
}

.panel {
  background: #ffffff;
  border-radius: 12px;
  border: 1px solid #e8e0d8;
  padding: 40px;
  box-shadow: 0 4px 20px rgba(0,0,0,0.02);
}

.panel h2 {
  font-family: var(--font-heading);
  font-size: 24px;
  margin: 0 0 8px;
  color: #1a1a1a;
}

.field-hint {
  font-size: 14px;
  color: #666;
  margin: 0 0 32px 0;
}

.form-group {
  margin-bottom: 24px;
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.form-group label {
  font-size: 14px;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  color: #333;
}

.input-field {
  padding: 12px 16px;
  border: 1px solid #e8e0d8;
  border-radius: 8px;
  font-family: var(--font-body);
  font-size: 15px;
  width: 100%;
  box-sizing: border-box;
}

.input-field:focus {
  outline: none;
  border-color: #C4622D;
}

.cover-upload-zone {
  width: 100%;
  height: 300px;
  border: 2px dashed #e8e0d8;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  background-size: cover;
  background-position: center;
  transition: all 0.2s;
  background-color: #fdfaf8;
  position: relative;
}

.cover-upload-zone:hover:not(.has-image) {
  border-color: #C4622D;
  background-color: #fdf2ed;
}

.upload-prompt {
  text-align: center;
  color: #666;
}

.upload-prompt p {
  font-weight: 600;
  margin: 8px 0 4px;
  color: #333;
}

.upload-icon {
  font-size: 40px;
}

.remove-btn {
  position: absolute;
  top: 16px;
  right: 16px;
  background: rgba(255,255,255,0.9);
  backdrop-filter: blur(4px);
}

.palette-options {
  display: flex;
  gap: 16px;
}

.palette-pip {
  width: 80px;
  height: 80px;
  border-radius: 12px;
  border: 2px solid #e8e0d8;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
}

.palette-pip:hover { box-shadow: 0 4px 12px rgba(0,0,0,0.1); }
.palette-pip.active { border-color: #C4622D; outline: 2px solid #C4622D; outline-offset: 2px; }

.product-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 16px;
}

.product-cube {
  height: 180px;
  border-radius: 12px;
  background-size: cover;
  background-position: center;
  position: relative;
  cursor: pointer;
  overflow: hidden;
  border: 2px solid transparent;
  transition: all 0.2s;
}

.product-cube.selected {
  border-color: #C4622D;
}

.cube-overlay {
  position: absolute;
  inset: 0;
  background: linear-gradient(0deg, rgba(0,0,0,0.8) 0%, rgba(0,0,0,0) 60%);
  display: flex;
  align-items: flex-end;
  padding: 16px;
}

.product-cube.selected .cube-overlay {
  background: linear-gradient(0deg, rgba(196,98,45,0.8) 0%, rgba(196,98,45,0.2) 100%);
}

.product-name {
  color: #fff;
  font-weight: 600;
  font-size: 14px;
}

.check-circle {
  position: absolute;
  top: 12px;
  right: 12px;
  width: 24px;
  height: 24px;
  border-radius: 50%;
  background: #fff;
  color: #C4622D;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 14px;
  font-weight: 700;
  opacity: 0;
  transition: opacity 0.2s;
}

.product-cube.selected .check-circle {
  opacity: 1;
}

.intent-options {
  display: flex;
  gap: 16px;
}

.intent-btn {
  padding: 12px 24px;
  border-radius: 8px;
  border: 1px solid #e8e0d8;
  background: #fff;
  font-size: 14px;
  font-weight: 600;
  color: #555;
  cursor: pointer;
  transition: all 0.2s;
}

.intent-btn.selected {
  background: #fdf2ed;
  border-color: #C4622D;
  color: #C4622D;
}

.publish-summary {
  background: #fdfaf8;
  border: 1px solid #e8e0d8;
  border-radius: 8px;
  padding: 20px;
}

.publish-summary ul {
  list-style: none;
  padding: 0;
  margin: 0;
  display: flex;
  flex-direction: column;
  gap: 8px;
  font-size: 15px;
  color: #333;
}

.panel-actions {
  display: flex;
  justify-content: space-between;
  margin-top: 24px;
}

.btn {
  padding: 12px 24px;
  border-radius: 8px;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
  border: none;
}

.primary-btn { background: #C4622D; color: #fff; }
.primary-btn:hover { background: #a85427; }

.secondary-btn { background: #fff; border: 1px solid #e8e0d8; color: #1a1a1a; }
.secondary-btn:hover:not(:disabled) { border-color: #C4622D; color: #C4622D; }
.secondary-btn:disabled { color: #ccc; cursor: not-allowed; }

.small-btn { padding: 6px 12px; font-size: 13px; }
</style>