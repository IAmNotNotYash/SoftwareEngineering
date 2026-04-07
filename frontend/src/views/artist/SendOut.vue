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
            <span class="audience-label">Total Followers</span>
            <span class="audience-value">{{ audienceSize.toLocaleString() }}</span>
            <span class="audience-trend positive">Active Audience</span>
          </div>
        </div>
      </section>

      <!-- CRM Navigation Tabs -->
      <div class="crm-tabs">
        <button 
          v-for="tab in ['composer', 'history', 'audience']" 
          :key="tab"
          class="tab-btn" 
          :class="{ active: activeTab === tab }"
          @click="activeTab = tab"
        >
          {{ tab.charAt(0).toUpperCase() + tab.slice(1) }}
        </button>
      </div>

      <!-- Tab Content: Composer -->
      <div v-if="activeTab === 'composer'" class="composer-layout slide-in">
        <div class="composer-form panel card">
          <h2>New Broadcast</h2>
          <p class="field-hint">Send a direct message or campaign update to your subscribers.</p>

          <div class="form-group">
            <label>Select Campaign / Catalogue</label>
            <div class="catalog-select">
              <div 
                v-for="c in catalogues" 
                :key="c.id" 
                class="catalog-option"
                :class="{ selected: selectedCatalogueId === c.id }"
                @click="selectedCatalogueId = c.id"
              >
                <div class="catalog-dot" :style="{ background: c.theme === 'earth' ? '#C4622D' : '#6A7E6A' }"></div>
                <span>{{ c.title }}</span>
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
            <div class="preview-attachment" v-if="selectedCatalogueId">
              <div class="attachment-img" :style="{ background: '#C4622D' }">
                 <span>{{ catalogues.find(c => c.id === selectedCatalogueId)?.title }}</span>
              </div>
              <div class="attachment-btn">View Catalogue</div>
            </div>
              </div>
              <div class="attachment-btn">View Catalogue</div>
            </div>
          </div>
        </div>
      </div>

      <!-- Tab Content: History -->
      <div v-if="activeTab === 'history'" class="history-section panel card slide-in">
        <h2>Broadcast History</h2>
        <p class="field-hint">View the performance of your past campaigns.</p>
        
        <table class="premium-table">
          <thead>
            <tr>
              <th>Date</th>
              <th>Campaign</th>
              <th>Platforms</th>
              <th>Status</th>
              <th>Reach</th>
              <th>Engagement</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="h in broadcastHistory" :key="h.id">
              <td>{{ h.date }}</td>
              <td><strong>{{ h.title }}</strong></td>
              <td>
                <span v-for="icon in h.platforms" :key="icon" class="platform-icon-small">{{ icon }}</span>
              </td>
              <td><span class="status-badge sent">{{ h.status }}</span></td>
              <td>{{ h.reach.toLocaleString() }}</td>
              <td class="engagement-value">{{ h.engagement }}</td>
            </tr>
          </tbody>
        </table>
      </div>

      <!-- Tab Content: Audience -->
      <div v-if="activeTab === 'audience'" class="audience-section panel card slide-in">
        <div class="section-header-row">
          <div>
            <h2>Audience Management</h2>
            <p class="field-hint">Your loyal community members and their engagement.</p>
          </div>
          <div class="search-box">
            <input v-model="searchQuery" class="input-field small-input" placeholder="Search subscribers..." />
          </div>
        </div>

        <table class="premium-table">
          <thead>
            <tr>
              <th>Subscribers</th>
              <th>Tier</th>
              <th>Joined Date</th>
              <th>Total Orders</th>
              <th>Lifetime Value</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="s in filteredSubscribers" :key="s.id">
              <td class="user-cell">
                <div class="user-avatar" :style="{background: getRandomColor()}">{{ s.name.charAt(0) }}</div>
                <span>{{ s.name }}</span>
              </td>
              <td><span class="tier-badge" :class="s.type.toLowerCase()">{{ s.type }}</span></td>
              <td>{{ s.joined }}</td>
              <td>{{ s.orders }}</td>
              <td class="value-cell">{{ s.value }}</td>
              <td><button class="btn secondary-btn small-btn">Profile</button></td>
            </tr>
          </tbody>
        </table>
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import ArtistNavbar from '../../components/ArtistNavbar.vue'
import { getCatalogues } from '../../api/catalogue.js'
import { getAudienceSize, sendBroadcast as apiSendBroadcast } from '../../api/communication.js'

const activeTab = ref('composer')
const message = ref("🎨 Exciting news! Check out my latest collection — crafted with love and available now at special prices. Don't miss out!")
const selectedIntent = ref('launch')
const selectedCatalogueId = ref(null)
const audienceSize = ref(0)
const loading = ref(true)
const searchQuery = ref('')

const catalogues = ref([])

const intents = [
  { emoji: '🚀', label: 'New Launch', value: 'launch' },
  { emoji: '📦', label: 'Pre-Orders Open', value: 'preorder' },
  { emoji: '⚡', label: 'Flash Sale', value: 'flash' },
  { emoji: '🎫', label: 'Exclusive Reveal', value: 'exclusive' },
]

const platforms = ref([
  { id: 'email', icon: '✉️', label: 'Email List', active: true },
  { id: 'tg', icon: '✈️', label: 'Telegram', active: true },
])

const broadcastHistory = ref([
  { id: 1, date: '2026-03-28', title: 'Summer Art Collection', status: 'Delivered', reach: 18402, engagement: '12.4%', platforms: ['✉️', '✈️'] },
  { id: 2, date: '2026-03-15', title: 'Flash Sale: Ceramics', status: 'Delivered', reach: 17950, engagement: '8.1%', platforms: ['✉️', '📸', '📘'] },
  { id: 3, date: '2026-02-28', title: 'Exclusive Reveal', status: 'Delivered', reach: 16200, engagement: '15.2%', platforms: ['✉️', '✈️'] },
])

const subscribers = ref([
  { id: 1, name: 'Aarav Sharma', type: 'Patron', joined: '2025-11-20', orders: 12, value: '₹42,500' },
  { id: 2, name: 'Mira Desai', type: 'Fan', joined: '2026-01-05', orders: 4, value: '₹8,200' },
  { id: 3, name: 'Rohan Gupta', type: 'Follower', joined: '2026-02-14', orders: 1, value: '₹1,200' },
  { id: 4, name: 'Kavya Singh', type: 'Patron', joined: '2025-09-12', orders: 28, value: '₹89,400' },
  { id: 5, name: 'Aditya Patel', type: 'Follower', joined: '2026-03-01', orders: 0, value: '₹0' },
  { id: 6, name: 'Sana Khan', type: 'Fan', joined: '2026-03-10', orders: 2, value: '₹3,500' },
])

const filteredSubscribers = computed(() => {
  if (!searchQuery.value) return subscribers.value
  return subscribers.value.filter(s => s.name.toLowerCase().includes(searchQuery.value.toLowerCase()))
})

const getRandomColor = () => {
  const colors = ['#C4622D', '#6A7E6A', '#2D3748', '#8B4513', '#556B2F']
  return colors[Math.floor(Math.random() * colors.length)]
}

onMounted(async () => {
  try {
    const [audienceData, catalogueData] = await Promise.all([
      getAudienceSize(),
      getCatalogues()
    ])
    audienceSize.value = audienceData.count
    catalogues.value = catalogueData.catalogues || []
    if (catalogues.value.length) {
      selectedCatalogueId.value = catalogues.value[0].id
    }
  } catch (err) {
    console.error("Failed to load broadcast data", err)
  } finally {
    loading.value = false
  }
})
const resetForm = () => {
  message.value = ''
  selectedIntent.value = 'launch'
  selectedCatalogueId.value = null
}

const sendBroadcast = async () => {
  try {
    const payload = {
      message: message.value,
      intent: selectedIntent.value,
      catalogue_id: selectedCatalogueId.value,
      platforms: platforms.value.filter(p => p.active).map(p => p.id)
    }
    await apiSendBroadcast(payload)
    alert(`Broadcast successfully sent to ${audienceSize.value} followers!`)
    resetForm()
  } catch (err) {
    alert("Error sending broadcast: " + err.message)
  }
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

/* Tabs */
.crm-tabs {
  display: flex;
  gap: 8px;
  margin-bottom: 32px;
  background: #f4f0ea;
  padding: 6px;
  border-radius: 10px;
  width: max-content;
}

.tab-btn {
  padding: 10px 24px;
  border-radius: 8px;
  border: none;
  background: transparent;
  color: #888;
  font-weight: 600;
  font-size: 14px;
  cursor: pointer;
  transition: all 0.2s ease;
}

.tab-btn.active {
  background: #ffffff;
  color: #C4622D;
  box-shadow: 0 2px 8px rgba(0,0,0,0.05);
}

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

.small-input {
  padding: 10px 16px;
  font-size: 14px;
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

/* Tables */
.premium-table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 10px;
}

.premium-table th {
  text-align: left;
  padding: 16px;
  font-size: 12px;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  color: #888;
  border-bottom: 2px solid #f4f0ea;
}

.premium-table td {
  padding: 20px 16px;
  border-bottom: 1px solid #f4f0ea;
  font-size: 14px;
  color: #333;
}

.premium-table tr:hover {
  background: #fdfaf8;
}

.status-badge {
  padding: 4px 10px;
  border-radius: 20px;
  font-size: 11px;
  font-weight: 700;
  text-transform: uppercase;
}

.status-badge.sent { background: #DCFCE7; color: #15803D; }

.engagement-value {
  font-weight: 700;
  color: #C4622D;
}

.platform-icon-small {
  margin-right: 4px;
  font-size: 16px;
}

.section-header-row {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 24px;
}

.user-cell {
  display: flex;
  align-items: center;
  gap: 12px;
  font-weight: 600;
}

.user-avatar {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  color: #fff;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 12px;
  font-weight: 700;
}

.tier-badge {
  padding: 4px 10px;
  border-radius: 20px;
  font-size: 11px;
  font-weight: 600;
}

.tier-badge.patron { background: #F3E8FF; color: #9333EA; }
.tier-badge.fan { background: #FEF3C7; color: #D97706; }
.tier-badge.follower { background: #E0E7FF; color: #4F46E5; }

.value-cell {
  font-family: var(--font-heading);
  font-weight: 600;
}

/* Animations */
.slide-in {
  animation: slideUp 0.4s ease-out;
}

@keyframes slideUp {
  from { opacity: 0; transform: translateY(20px); }
  to { opacity: 1; transform: translateY(0); }
}

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

.small-btn {
  padding: 6px 12px;
  font-size: 11px;
}
</style>