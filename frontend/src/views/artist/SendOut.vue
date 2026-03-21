<template>
  <div class="sendout">
        <ArtistNavbar />

    <div class="page-header">
      <div>
        <h1>Send-Out</h1>
        <p>Generate and share your campaign across platforms.</p>
      </div>
    </div>

    <div class="sendout-layout">
      <div class="left-col">
        <div class="card" style="padding:20px; margin-bottom:16px">
          <div class="preview-banner">
            <span>🖼</span>
            <p>Auto-generated preview</p>
          </div>
          <div class="form-group" style="margin-top:16px">
            <label>Caption / Write-up</label>
            <textarea v-model="caption" class="input-field" rows="4"></textarea>
          </div>
        </div>

        <div class="card" style="padding:20px; margin-bottom:16px">
          <label>Campaign Intent</label>
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

        <div class="card" style="padding:20px">
          <label>Share To</label>
          <div class="share-platforms">
            <button v-for="p in platforms" :key="p.label" class="platform-btn">
              {{ p.icon }} {{ p.label }}
            </button>
          </div>
        </div>
      </div>

      <div class="right-col">
        <div class="card campaign-pick">
          <h4>Select Campaign</h4>
          <div
            v-for="c in campaigns"
            :key="c.name"
            class="campaign-option"
            :class="{ selected: selectedCampaign === c.name }"
            @click="selectedCampaign = c.name"
          >
            <div class="campaign-dot" :style="{ background: c.color }"></div>
            <div>
              <strong>{{ c.name }}</strong>
              <span>{{ c.status }}</span>
            </div>
          </div>
        </div>

        <div class="card" style="padding:20px; margin-top:16px">
          <h4>Quick Stats</h4>
          <div class="quick-stat" v-for="s in quickStats" :key="s.label">
            <span>{{ s.icon }}</span>
            <div>
              <strong>{{ s.value }}</strong>
              <small>{{ s.label }}</small>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import ArtistNavbar from '../../components/ArtistNavbar.vue'

import { ref } from 'vue'

const caption = ref('🎨 Exciting news! Check out my latest collection — crafted with love and available now at special prices for my fans & patrons. Don\'t miss out!')
const selectedIntent = ref('ready')
const selectedCampaign = ref('Summer Art Collection')

const intents = [
  { emoji: '🛍', label: 'Ready to Sale', value: 'ready' },
  { emoji: '🚀', label: 'Preorder / Crowdsource', value: 'preorder' },
  { emoji: '⚡', label: 'Flash Sale', value: 'flash' },
  { emoji: '🔨', label: 'Bidding Notice', value: 'bidding' },
  { emoji: '📊', label: 'Focus Survey', value: 'focus' },
]

const platforms = [
  { icon: '▶️', label: 'YouTube' },
  { icon: '📘', label: 'Facebook' },
  { icon: '📌', label: 'Pinterest' },
  { icon: '📸', label: 'Instagram' },
  { icon: '✈️', label: 'Telegram' },
]

const campaigns = [
  { name: 'Summer Art Collection', status: 'Live', color: '#F97316' },
  { name: 'Limited Edition Prints', status: 'Live', color: '#FB923C' },
  { name: 'Digital Workshop Series', status: 'Draft', color: '#D1D5DB' },
]

const quickStats = [
  { icon: '👁', value: '24,500', label: 'Total Reach' },
  { icon: '❤️', value: '3,200', label: 'Total Likes' },
  { icon: '🛒', value: '128', label: 'Orders' },
  { icon: '₹', value: '₹45,200', label: 'Revenue' },
]
</script>

<style scoped>
.sendout { display: flex; flex-direction: column; gap: 24px; }
.page-header{margin:20px;}
.page-header h1 { font-size: 26px; margin-bottom: 4px; }
.page-header p { color: var(--text-2); }

.sendout-layout { 
    display: grid; 
    grid-template-columns: 60% 40%; 
    gap: 20px;
margin:20px }

.preview-banner {
  height: 160px;
  background: linear-gradient(135deg, #F97316, #FBBF24);
  border-radius: 10px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  color: white;
  gap: 8px;
}
.preview-banner span { font-size: 32px; }
.preview-banner p { font-size: 14px; opacity: 0.9; }

.form-group { margin-bottom: 0; }
textarea.input-field { resize: vertical; }

.intent-options { display: flex; flex-wrap: wrap; gap: 8px; margin-top: 8px; }
.intent-btn {
  padding: 8px 14px;
  border-radius: 20px;
  border: 1.5px solid var(--border);
  background: white;
  font-size: 13px;
  font-weight: 500;
  color: var(--text-2);
  transition: all 0.12s;
  cursor: pointer;
}
.intent-btn:hover { border-color: var(--orange); color: var(--orange); }
.intent-btn.selected { background: var(--orange); color: white; border-color: var(--orange); }

.share-platforms { display: flex; flex-wrap: wrap; gap: 10px; margin-top: 8px; }
.platform-btn {
  padding: 9px 16px;
  border: 1.5px solid var(--border);
  border-radius: 10px;
  background: white;
  font-size: 13px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.12s;
  display: flex;
  align-items: center;
  gap: 7px;
}
.platform-btn:hover { border-color: var(--orange); color: var(--orange); background: var(--orange-pale); }

.campaign-pick { padding: 20px; }
.campaign-pick h4 { font-size: 14px; font-weight: 600; margin-bottom: 12px; }

.campaign-option {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 10px;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.12s;
  margin-bottom: 4px;
}
.campaign-option:hover { background: var(--bg); }
.campaign-option.selected { background: var(--orange-pale); }
.campaign-dot { width: 12px; height: 12px; border-radius: 50%; flex-shrink: 0; }
.campaign-option strong { display: block; font-size: 13px; }
.campaign-option span { font-size: 12px; color: var(--text-2); }

.quick-stat {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 10px 0;
  border-bottom: 1px solid var(--border);
  font-size: 18px;
}
.quick-stat:last-child { border-bottom: none; }
.quick-stat strong { display: block; font-size: 15px; font-family: 'Fraunces', serif; }
.quick-stat small { font-size: 12px; color: var(--text-2); }
</style>