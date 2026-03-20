<template>
  <div class="new-campaign">
    <div class="page-back">
      <router-link to="/campaigns" class="back-btn">← Back</router-link>
      <div>
        <h1>Launch New Campaign</h1>
        <p>Create something amazing for your audience.</p>
      </div>
    </div>

    <!-- Step tabs -->
    <div class="steps">
      <div
        v-for="(step, i) in steps"
        :key="step"
        class="step-tab"
        :class="{ active: currentStep === i, done: currentStep > i }"
        @click="currentStep > i && (currentStep = i)"
      >
        {{ step }}
      </div>
    </div>

    <!-- Step 0: Details -->
    <div v-if="currentStep === 0" class="card step-card">
      <div class="form-group">
        <label>Campaign Name</label>
        <input v-model="form.name" class="input-field" placeholder="e.g., Summer Art Collection 2024" />
      </div>
      <div class="form-group">
        <label>Summary (5 lines max)</label>
        <textarea v-model="form.summary" class="input-field" rows="4" placeholder="Describe what this campaign is about..."></textarea>
      </div>
      <div class="form-group">
        <label>Cover Image</label>
        <div class="upload-zone">
          <span class="upload-icon">🖼</span>
          <span>Drop an image or click to upload</span>
        </div>
      </div>
    </div>

    <!-- Step 1: Content -->
    <div v-if="currentStep === 1" class="card step-card">
      <div class="form-group">
        <label>Post Caption / Write-up</label>
        <textarea v-model="form.caption" class="input-field" rows="5" placeholder="Write your post caption..."></textarea>
      </div>
      <div class="form-group">
        <label>Campaign Intent</label>
        <div class="intent-options">
          <button
            v-for="intent in intents"
            :key="intent.value"
            class="intent-btn"
            :class="{ selected: form.intent === intent.value }"
            @click="form.intent = intent.value"
          >
            {{ intent.emoji }} {{ intent.label }}
          </button>
        </div>
      </div>
    </div>

    <!-- Step 2: Products -->
    <div v-if="currentStep === 2" class="card step-card">
      <div class="form-group">
        <label>Select Products for this Campaign</label>
        <div class="product-selects">
          <div
            v-for="p in availableProducts"
            :key="p.name"
            class="product-select-card"
            :class="{ selected: form.products.includes(p.name) }"
            @click="toggleProduct(p.name)"
          >
            <div class="product-thumb" :style="{ background: p.color }"></div>
            <div class="product-select-info">
              <strong>{{ p.name }}</strong>
              <span>₹{{ p.price }} · Follower</span>
            </div>
            <div class="product-check">{{ form.products.includes(p.name) ? '✓' : '' }}</div>
          </div>
        </div>
      </div>
    </div>

    <!-- Step 3: Send-Out -->
    <div v-if="currentStep === 3" class="step-card-wide">
      <div class="card" style="padding:20px; margin-bottom:16px">
        <div class="preview-banner">
          <span>🖼</span>
          <p>Auto-generated preview</p>
        </div>
        <div class="form-group" style="margin-top:16px">
          <label>Caption / Write-up</label>
          <textarea v-model="form.caption" class="input-field" rows="4" :placeholder="defaultCaption"></textarea>
        </div>
      </div>

      <div class="card" style="padding:20px; margin-bottom:16px">
        <label>Campaign Intent</label>
        <div class="intent-options">
          <button
            v-for="intent in intents"
            :key="intent.value"
            class="intent-btn"
            :class="{ selected: form.intent === intent.value }"
            @click="form.intent = intent.value"
          >
            {{ intent.emoji }} {{ intent.label }}
          </button>
        </div>
      </div>

      <div class="card" style="padding:20px; margin-bottom:16px">
        <label>Share To</label>
        <div class="share-platforms">
          <button v-for="p in platforms" :key="p.label" class="platform-btn">
            {{ p.icon }} {{ p.label }}
          </button>
        </div>
      </div>

      <!-- Focus Survey -->
      <div v-if="form.intent === 'focus'" class="card focus-survey">
        <div class="focus-header">
          <span>📋</span>
          <div>
            <strong>Focus Survey</strong>
            <p>Collect feedback from your followers via email</p>
          </div>
        </div>

        <div class="survey-section">
          <label>📊 How likely are you to buy this product?</label>
          <div class="likelihood-options">
            <button
              v-for="opt in likelihoodOpts"
              :key="opt"
              class="pill-btn"
              :class="{ selected: survey.likelihood === opt }"
              @click="survey.likelihood = opt"
            >{{ opt }}</button>
          </div>
        </div>

        <div class="survey-section">
          <label>🔥 What price are you ready to pay?</label>
          <input type="range" v-model="survey.price" min="50" max="5000" step="50" class="price-slider" />
          <div class="price-labels">
            <span>₹50</span>
            <span class="price-current">₹{{ survey.price }}</span>
            <span>₹5,000</span>
          </div>
        </div>

        <div class="survey-section">
          <label>🎯 Which option works best for you?</label>
          <div class="option-radios">
            <label v-for="opt in packageOpts" :key="opt.value" class="radio-card" :class="{ selected: survey.package === opt.value }" @click="survey.package = opt.value">
              <input type="radio" :value="opt.value" v-model="survey.package" />
              <div>
                <strong>{{ opt.label }}</strong>
                <span>{{ opt.desc }}</span>
              </div>
            </label>
          </div>
        </div>

        <div class="survey-section">
          <label>✉️ Send survey to followers via email</label>
          <input v-model="survey.emailList" class="input-field" placeholder="Enter follower email list or segment name..." />
          <p class="hint">Survey will be sent to your selected follower segment's email addresses.</p>
        </div>

        <div class="survey-section">
          <label>⭐ Points & Tier Thresholds</label>
          <p style="font-size:12px; color:var(--text-2); margin-bottom:12px">Set points earned per survey response and thresholds to level up tiers.</p>
          <div class="tier-thresholds">
            <div class="threshold-card">
              <span class="threshold-label">🎁 POINTS PER RESPONSE</span>
              <input v-model.number="survey.pointsPerResponse" class="input-field threshold-input" type="number" />
            </div>
            <div class="threshold-card fan">
              <span class="threshold-label">❤️ BECOME A FAN</span>
              <input v-model.number="survey.fanThreshold" class="input-field threshold-input" type="number" />
            </div>
            <div class="threshold-card patron">
              <span class="threshold-label">👑 BECOME A PATRON</span>
              <input v-model.number="survey.patronThreshold" class="input-field threshold-input" type="number" />
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Navigation -->
    <div class="step-nav">
      <button class="btn-secondary" @click="prevStep" :disabled="currentStep === 0">Previous</button>
      <button class="btn-primary" @click="nextStep">
        {{ currentStep === steps.length - 1 ? '🚀 Launch Campaign' : 'Next Step' }}
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const currentStep = ref(0)
const steps = ['Details', 'Content', 'Products', 'Send-Out']

const form = reactive({
  name: '',
  summary: '',
  caption: '🎨 Exciting news! Check out my latest collection — crafted with love and available now at special prices for my fans & patrons. Don\'t miss out!',
  intent: 'ready',
  products: [],
})

const survey = reactive({
  likelihood: '',
  price: 500,
  package: '',
  emailList: '',
  pointsPerResponse: 10,
  fanThreshold: 100,
  patronThreshold: 500,
})

const defaultCaption = '🎨 Exciting news! Check out my latest collection...'

const intents = [
  { emoji: '🛍', label: 'Ready to Sale', value: 'ready' },
  { emoji: '🚀', label: 'Preorder / Crowdsource', value: 'preorder' },
  { emoji: '⚡', label: 'Flash Sale', value: 'flash' },
  { emoji: '🔨', label: 'Bidding Notice', value: 'bidding' },
  { emoji: '📊', label: 'Focus Survey', value: 'focus' },
]

const availableProducts = [
  { name: 'Abstract Canvas Print', price: '1,200', color: 'linear-gradient(135deg,#F97316,#FBBF24)' },
  { name: 'Digital Art Bundle', price: '500', color: 'linear-gradient(135deg,#8B5CF6,#EC4899)' },
  { name: 'Custom Portrait', price: '3,500', color: 'linear-gradient(135deg,#3B82F6,#06B6D4)' },
]

const platforms = [
  { icon: '▶️', label: 'YouTube' },
  { icon: '📘', label: 'Facebook' },
  { icon: '📌', label: 'Pinterest' },
  { icon: '📸', label: 'Instagram' },
  { icon: '✈️', label: 'Telegram' },
]

const likelihoodOpts = ['Definitely', 'Very Likely', 'Maybe', 'Unlikely', 'Not Interested']

const packageOpts = [
  { value: 'premium', label: 'Option A — Premium Bundle', desc: 'Full collection + extras' },
  { value: 'standard', label: 'Option B — Standard Pack', desc: 'Core items only' },
  { value: 'lite', label: 'Option C — Lite / Sample', desc: 'Try before you commit' },
]

function toggleProduct(name) {
  const idx = form.products.indexOf(name)
  if (idx >= 0) form.products.splice(idx, 1)
  else form.products.push(name)
}

function nextStep() {
  if (currentStep.value < steps.length - 1) currentStep.value++
  else router.push('/campaigns')
}

function prevStep() {
  if (currentStep.value > 0) currentStep.value--
}
</script>

<style scoped>
.new-campaign { display: flex; flex-direction: column; gap: 24px; }

.page-back {
  display: flex;
  align-items: flex-start;
  gap: 16px;
}

.back-btn {
  color: var(--text-2);
  font-size: 13px;
  font-weight: 500;
  margin-top: 4px;
  transition: color 0.12s;
}
.back-btn:hover { color: var(--orange); }

.page-back h1 { font-size: 24px; margin-bottom: 4px; }
.page-back p { color: var(--text-2); }

.steps {
  display: flex;
  gap: 0;
  background: white;
  border: 1px solid var(--border);
  border-radius: 10px;
  overflow: hidden;
  width: fit-content;
}

.step-tab {
  padding: 10px 24px;
  font-size: 14px;
  font-weight: 500;
  color: var(--text-2);
  background: white;
  cursor: default;
  border-right: 1px solid var(--border);
  transition: all 0.15s;
}

.step-tab:last-child { border-right: none; }

.step-tab.active {
  background: var(--orange);
  color: white;
  font-weight: 600;
}

.step-tab.done {
  color: var(--orange);
  cursor: pointer;
}

.step-card { padding: 24px; max-width: 700px; }
.step-card-wide { max-width: 700px; }

.form-group { margin-bottom: 20px; }
.form-group:last-child { margin-bottom: 0; }

textarea.input-field { resize: vertical; }

.upload-zone {
  border: 2px dashed var(--border);
  border-radius: 10px;
  padding: 40px;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 10px;
  color: var(--text-3);
  cursor: pointer;
  transition: all 0.15s;
}
.upload-zone:hover { border-color: var(--orange); color: var(--orange); background: var(--orange-pale); }
.upload-icon { font-size: 28px; }

.intent-options { display: flex; flex-wrap: wrap; gap: 8px; margin-top: 4px; }

.intent-btn {
  padding: 8px 16px;
  border-radius: 20px;
  border: 1.5px solid var(--border);
  background: white;
  font-size: 13px;
  font-weight: 500;
  color: var(--text-2);
  transition: all 0.12s;
}
.intent-btn:hover { border-color: var(--orange); color: var(--orange); }
.intent-btn.selected { background: var(--orange); color: white; border-color: var(--orange); }

.product-selects { display: flex; flex-direction: column; gap: 10px; }

.product-select-card {
  display: flex;
  align-items: center;
  gap: 14px;
  padding: 12px 16px;
  border: 2px solid var(--border);
  border-radius: 10px;
  cursor: pointer;
  transition: all 0.12s;
}
.product-select-card:hover { border-color: var(--orange); }
.product-select-card.selected { border-color: var(--orange); background: var(--orange-pale); }

.product-thumb { width: 40px; height: 40px; border-radius: 8px; flex-shrink: 0; }

.product-select-info { flex: 1; }
.product-select-info strong { display: block; font-size: 14px; margin-bottom: 2px; }
.product-select-info span { font-size: 12px; color: var(--text-2); }

.product-check { font-size: 18px; color: var(--orange); font-weight: 700; width: 20px; text-align: center; }

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

.share-platforms { display: flex; flex-wrap: wrap; gap: 10px; margin-top: 8px; }

.platform-btn {
  padding: 10px 18px;
  border: 1.5px solid var(--border);
  border-radius: 10px;
  background: white;
  font-size: 13px;
  font-weight: 500;
  color: var(--text);
  transition: all 0.12s;
  display: flex;
  align-items: center;
  gap: 7px;
}
.platform-btn:hover { border-color: var(--orange); color: var(--orange); background: var(--orange-pale); }

.focus-survey { padding: 20px; }

.focus-header {
  display: flex;
  align-items: flex-start;
  gap: 12px;
  margin-bottom: 24px;
  font-size: 22px;
}
.focus-header strong { display: block; font-size: 16px; }
.focus-header p { font-size: 13px; color: var(--text-2); }

.survey-section { margin-bottom: 24px; }
.survey-section label { font-size: 14px; color: var(--text); font-weight: 500; margin-bottom: 12px; }

.likelihood-options { display: flex; flex-wrap: wrap; gap: 8px; }

.pill-btn {
  padding: 8px 16px;
  border-radius: 20px;
  border: 1.5px solid var(--border);
  background: white;
  font-size: 13px;
  cursor: pointer;
  transition: all 0.12s;
}
.pill-btn.selected { background: var(--orange); color: white; border-color: var(--orange); }
.pill-btn:hover:not(.selected) { border-color: var(--orange); }

.price-slider {
  width: 100%;
  accent-color: var(--orange);
  margin-bottom: 8px;
}

.price-labels {
  display: flex;
  justify-content: space-between;
  font-size: 12px;
  color: var(--text-2);
}
.price-current { color: var(--orange); font-weight: 600; }

.option-radios { display: flex; flex-direction: column; gap: 10px; }

.radio-card {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 14px 16px;
  border: 1.5px solid var(--border);
  border-radius: 10px;
  cursor: pointer;
  transition: all 0.12s;
}
.radio-card.selected { border-color: var(--orange); background: var(--orange-pale); }
.radio-card input { accent-color: var(--orange); }
.radio-card strong { display: block; font-size: 14px; margin-bottom: 2px; }
.radio-card span { font-size: 12px; color: var(--text-2); }

.hint { font-size: 12px; color: var(--text-2); margin-top: 6px; }

.tier-thresholds { display: grid; grid-template-columns: repeat(3, 1fr); gap: 12px; }

.threshold-card {
  border: 1.5px solid var(--border);
  border-radius: 10px;
  padding: 14px;
  text-align: center;
}
.threshold-card.fan { border-color: #FED7AA; background: #FFF7ED; }
.threshold-card.patron { border-color: #DDD6FE; background: #F5F3FF; }

.threshold-label {
  display: block;
  font-size: 11px;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.06em;
  color: var(--text-2);
  margin-bottom: 10px;
}

.threshold-input { text-align: center; font-weight: 600; font-size: 18px; }

.step-nav {
  display: flex;
  justify-content: space-between;
  max-width: 700px;
}
</style>