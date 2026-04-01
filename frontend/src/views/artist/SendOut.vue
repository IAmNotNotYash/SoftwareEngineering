<template>
  <div class="subscribers-page">
    <ArtistNavbar />

    <main class="page-container">
      <div class="page-header">
        <div>
          <h1 class="page-title">Subscribers & Broadcasts</h1>
          <p class="subtitle">Manage your audience and send out multi-platform campaigns.</p>
        </div>
      </div>

      <!-- Subscribers Overview CRM -->
      <section class="audience-overview">
        <div class="audience-card">
          <div class="audience-icon follower-icon">👥</div>
          <div class="audience-info">
            <span class="audience-label">Followers</span>
            <span class="audience-value">18,402</span>
            <span class="audience-trend positive">+124 this week</span>
          </div>
        </div>
        <div class="audience-card">
          <div class="audience-icon fan-icon">⭐</div>
          <div class="audience-info">
            <span class="audience-label">Fans</span>
            <span class="audience-value">4,193</span>
            <span class="audience-trend positive">+45 this week</span>
          </div>
        </div>
        <div class="audience-card">
          <div class="audience-icon patron-icon">💎</div>
          <div class="audience-info">
            <span class="audience-label">Patrons</span>
            <span class="audience-value">842</span>
            <span class="audience-trend positive">+12 this week</span>
          </div>
        </div>
      </section>

      <!-- Broadcast Composer Layout -->
      <div class="composer-layout">
        <div class="composer-form panel card">
          <h2>New Broadcast</h2>
          <p class="field-hint">Send a direct message or campaign update to your subscribers.</p>

          <div class="form-group">
            <label>Select Campaign / Catalogue</label>
            <div class="catalog-select">
              <div 
                v-for="c in catalogues" 
                :key="c.name" 
                class="catalog-option"
                :class="{ selected: selectedCatalogue === c.name }"
                @click="selectedCatalogue = c.name"
              >
                <div class="catalog-dot" :style="{ background: c.color }"></div>
                <span>{{ c.name }}</span>
              </div>
            </div>
          </div>

          <div class="form-group" style="margin-top: 24px;">
            <label>Broadcast Message</label>
            <textarea 
              v-model="message" 
              class="input-field" 
              rows="5" 
              placeholder="Write your exciting news here..."
            ></textarea>
          </div>

          <div class="form-group" style="margin-top: 24px;">
            <label>Intent / Call to Action</label>
            <div class="intent-options">
              <button 
                v-for="intent in intents" 
                :key="intent.value"
                class="intent-btn"
                :class="{ selected: selectedIntent === intent.value }"
                @click="selectedIntent = intent.value"
              >
                {{ intent.emoji }} {{ intent.label }}
              </button>
            </div>
          </div>

          <div class="form-group" style="margin-top: 24px;">
            <label>Cross-Platform Sync</label>
            <p class="field-hint" style="margin-bottom: 12px; font-size: 13px;">Automatically post this update to your connected socials.</p>
            <div class="platform-options">
              <button 
                v-for="p in platforms" 
                :key="p.id"
                class="platform-toggle"
                :class="{ active: p.active }"
                @click="p.active = !p.active"
              >
                {{ p.icon }} {{ p.label }}
              </button>
            </div>
          </div>

          <div class="panel-actions" style="margin-top: 40px;">
            <button class="btn secondary-btn" @click="resetForm">Clear Form</button>
            <button class="btn primary-btn" @click="sendBroadcast">Send Broadcast 🚀</button>
          </div>
        </div>

        <div class="composer-preview">
          <div class="preview-device">
            <div class="preview-header">
              <div class="preview-avatar"></div>
              <div class="preview-sender">
                <strong>Your Studio</strong>
                <span>Just now • {{ intents.find(i => i.value === selectedIntent)?.label }}</span>
              </div>
            </div>
            <div class="preview-content">
              <p>{{ message || 'Your message preview will appear here...' }}</p>
            </div>
            <div class="preview-attachment" v-if="selectedCatalogue">
              <div class="attachment-img" :style="{ background: catalogues.find(c => c.name === selectedCatalogue)?.color }">
                 <span>{{ selectedCatalogue }}</span>
              </div>
              <div class="attachment-btn">View Catalogue</div>
            </div>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import ArtistNavbar from '../../components/ArtistNavbar.vue'

const message = ref("🎨 Exciting news! Check out my latest collection — crafted with love and available now at special prices. Don't miss out!")
const selectedIntent = ref('launch')
const selectedCatalogue = ref('Summer Art Collection')

const catalogues = [
  { name: 'None (Just Message)', color: '#e8e0d8' },
  { name: 'Summer Art Collection', color: '#C4622D' },
  { name: 'Earth Tone Ceramics', color: '#6A7E6A' },
  { name: 'Digital Workshop Series', color: '#2D3748' },
]

const intents = [
  { emoji: '🚀', label: 'New Launch', value: 'launch' },
  { emoji: '📦', label: 'Pre-Orders Open', value: 'preorder' },
  { emoji: '⚡', label: 'Flash Sale', value: 'flash' },
  { emoji: '🎫', label: 'Exclusive Reveal', value: 'exclusive' },
]

const platforms = ref([
  { id: 'email', icon: '✉️', label: 'Email List', active: true },
  { id: 'ig', icon: '📸', label: 'Instagram', active: false },
  { id: 'fb', icon: '📘', label: 'Facebook', active: false },
  { id: 'tg', icon: '✈️', label: 'Telegram', active: true },
])

const resetForm = () => {
  message.value = ''
  selectedIntent.value = 'launch'
  selectedCatalogue.value = 'None (Just Message)'
}

const sendBroadcast = () => {
  const activePlatforms = platforms.value.filter(p => p.active).map(p => p.label).join(', ')
  alert(`Broadcast successfully queued to be sent via: ${activePlatforms}`)
}
</script>

<style scoped>
.subscribers-page {
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

/* Audience Overview */
.audience-overview {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 24px;
  margin-bottom: 48px;
}

.audience-card {
  background: #ffffff;
  border: 1px solid #e8e0d8;
  border-radius: 12px;
  padding: 24px;
  display: flex;
  align-items: center;
  gap: 20px;
  box-shadow: 0 4px 20px rgba(0,0,0,0.02);
}

.audience-icon {
  width: 56px;
  height: 56px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 24px;
}

.follower-icon { background: #E0E7FF; color: #4F46E5; }
.fan-icon { background: #FEF3C7; color: #D97706; }
.patron-icon { background: #F3E8FF; color: #9333EA; }

.audience-info {
  display: flex;
  flex-direction: column;
}

.audience-label {
  font-size: 13px;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  color: #888;
  font-weight: 600;
  margin-bottom: 4px;
}

.audience-value {
  font-family: var(--font-heading);
  font-size: 28px;
  font-weight: 700;
  color: #1a1a1a;
  line-height: 1;
  margin-bottom: 6px;
}

.audience-trend {
  font-size: 12px;
  font-weight: 600;
}

.positive { color: #16A34A; }

/* Composer Layout */
.composer-layout {
  display: flex;
  gap: 40px;
}

.composer-form {
  flex: 3;
}

.composer-preview {
  flex: 2;
  display: flex;
  justify-content: center;
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
  padding: 16px;
  border: 1px solid #e8e0d8;
  border-radius: 8px;
  font-family: var(--font-body);
  font-size: 15px;
  width: 100%;
  box-sizing: border-box;
  resize: vertical;
}

.input-field:focus {
  outline: none;
  border-color: #C4622D;
}

.catalog-select {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 12px;
}

.catalog-option {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px 16px;
  border-radius: 8px;
  border: 1px solid #e8e0d8;
  cursor: pointer;
  background: #faf8f5;
  transition: all 0.2s;
}

.catalog-option:hover {
  border-color: #C4622D;
}

.catalog-option.selected {
  background: #fdf2ed;
  border-color: #C4622D;
  color: #C4622D;
  font-weight: 600;
}

.catalog-dot {
  width: 12px;
  height: 12px;
  border-radius: 50%;
}

.intent-options {
  display: flex;
  gap: 12px;
  flex-wrap: wrap;
}

.intent-btn {
  padding: 10px 20px;
  border-radius: 30px;
  border: 1px solid #e8e0d8;
  background: #fff;
  font-size: 14px;
  font-weight: 600;
  color: #555;
  cursor: pointer;
  transition: all 0.2s;
}

.intent-btn.selected {
  background: #1a1a1a;
  border-color: #1a1a1a;
  color: #fff;
}

.platform-options {
  display: flex;
  gap: 12px;
  flex-wrap: wrap;
}

.platform-toggle {
  padding: 10px 16px;
  border-radius: 8px;
  border: 1px solid #e8e0d8;
  background: #fff;
  font-size: 14px;
  font-weight: 600;
  color: #888;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 8px;
  transition: all 0.2s;
}

.platform-toggle.active {
  background: #eaf2f8;
  border-color: #3B82F6;
  color: #1d4ed8;
}

.panel-actions {
  display: flex;
  justify-content: flex-end;
  gap: 16px;
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
.secondary-btn:hover { border-color: #C4622D; color: #C4622D; }

/* Preview Device */
.preview-device {
  width: 340px;
  height: max-content;
  border: 8px solid #1a1a1a;
  border-radius: 36px;
  background: #fff;
  overflow: hidden;
  box-shadow: 0 20px 40px rgba(0,0,0,0.1);
  padding-bottom: 20px;
}

.preview-header {
  padding: 20px;
  display: flex;
  align-items: center;
  gap: 12px;
  border-bottom: 1px solid #f0f0f0;
}

.preview-avatar {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background: #C4622D;
}

.preview-sender {
  display: flex;
  flex-direction: column;
}

.preview-sender strong {
  font-size: 14px;
  color: #1a1a1a;
}

.preview-sender span {
  font-size: 11px;
  color: #888;
}

.preview-content {
  padding: 20px;
  font-size: 14px;
  line-height: 1.5;
  color: #333;
  white-space: pre-wrap;
}

.preview-attachment {
  margin: 0 20px;
  border-radius: 12px;
  border: 1px solid #e8e0d8;
  overflow: hidden;
}

.attachment-img {
  height: 140px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #fff;
  font-weight: 600;
  font-size: 16px;
  text-shadow: 0 2px 4px rgba(0,0,0,0.2);
  text-align: center;
  padding: 20px;
}

.attachment-btn {
  padding: 12px;
  background: #faf8f5;
  text-align: center;
  font-size: 13px;
  font-weight: 600;
  color: #C4622D;
  border-top: 1px solid #e8e0d8;
}
</style>