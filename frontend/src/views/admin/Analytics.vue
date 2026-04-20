<template>
  <div class="analytics-page">
    <AdminNavbar />

    <div class="page-container">
      <h1 class="page-title">Analytics</h1>

      <!-- Tabs -->
      <div class="tabs">
        <button :class="{ active: activeTab === 'overview' }" @click="activeTab = 'overview'">Overview</button>
        <button :class="{ active: activeTab === 'artists' }" @click="activeTab = 'artists'">By Artist</button>
        <button :class="{ active: activeTab === 'geo' }" @click="activeTab = 'geo'">Geographic</button>
      </div>

      <!-- Overview Tab -->
      <div v-if="activeTab === 'overview'">
        <div v-if="errorMessage" class="error-banner">{{ errorMessage }}</div>

        <!-- KPI Cards -->
        <div class="kpi-grid">
          <div class="kpi-card" v-for="kpi in kpis" :key="kpi.label">
            <p class="kpi-label">{{ kpi.label }}</p>
            <h2 class="kpi-value">{{ kpi.value }}</h2>
          </div>
        </div>

        <!-- Charts -->
        <div class="charts">
          <div class="chart-card">
            <h3 class="chart-title">Revenue Trend</h3>
            <canvas ref="revenueCanvas"></canvas>
          </div>
          <div class="chart-card">
            <h3 class="chart-title">Orders Trend</h3>
            <canvas ref="ordersCanvas"></canvas>
          </div>
        </div>

        <!-- AI Summary -->
        <div class="ai-summary" v-if="aiSummary">
          <div class="ai-top">
            <span class="ai-pill">AI INSIGHTS</span>
            <h3>Platform Pulse</h3>
            <p class="ai-subtitle">A quick narrative snapshot of marketplace momentum.</p>
          </div>
          <div class="ai-chips">
            <span class="ai-chip" v-for="chip in insightChips" :key="chip">{{ chip }}</span>
          </div>
          <p class="ai-body">{{ aiSummary.ai_summary }}</p>
        </div>
      </div>

      <!-- By Artist Tab -->
      <div v-if="activeTab === 'artists'" class="table-card">
        <table>
          <thead>
            <tr>
              <th>Artist</th>
              <th>Revenue</th>
              <th>Orders</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="artist in artistStats" :key="artist.name">
              <td>{{ artist.name }}</td>
              <td>₹{{ artist.revenue }}</td>
              <td>{{ artist.orders }}</td>
            </tr>
          </tbody>
        </table>
      </div>

      <!-- Geographic Tab -->
      <div v-if="activeTab === 'geo'">
        <div class="map-placeholder">
          Map visualization will be added here.
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed, ref, watch, onMounted, onBeforeUnmount, nextTick } from 'vue'
import AdminNavbar from '../../components/AdminNavbar.vue'
import { getAnalytics } from '../../api/admin.js'
import Chart from 'chart.js/auto'

const activeTab = ref('overview')
const kpis = ref([])
const artistStats = ref([])
const aiSummary = ref(null)
const errorMessage = ref('')
const analyticsData = ref(null)

const revenueCanvas = ref(null)
const ordersCanvas = ref(null)

let revenueChart = null
let ordersChart = null

const insightChips = computed(() => {
  const byLabel = Object.fromEntries((kpis.value || []).map(k => [k.label, k.value]))
  return [
    `Revenue ${byLabel['Total Revenue'] || '₹0'}`,
    `Orders ${byLabel['Total Orders'] || '0'}`,
    `Artists ${byLabel['Registered Artists'] || '0'}`,
  ]
})

function destroyCharts() {
  if (revenueChart) {
    revenueChart.destroy()
    revenueChart = null
  }
  if (ordersChart) {
    ordersChart.destroy()
    ordersChart = null
  }
}

function renderCharts(data) {
  if (!revenueCanvas.value || !ordersCanvas.value) return
  destroyCharts()

  const revenueData = Array.isArray(data?.revenueTrend?.data) ? data.revenueTrend.data : []
  const ordersData = Array.isArray(data?.ordersTrend?.data) ? data.ordersTrend.data : []
  const labels = Array.isArray(data?.revenueTrend?.labels) ? data.revenueTrend.labels : []

  // Revenue Chart
  revenueChart = new Chart(revenueCanvas.value, {
    type: 'line',
    data: {
      labels: data.revenueTrend.labels,
      datasets: [{
        label: 'Revenue',
        data: revenueData,
        borderWidth: 2,
        tension: 0.3
      }]
    },
    options: {
      responsive: true,
      plugins: { legend: { display: false } }
    }
  })

  // Orders Chart
  ordersChart = new Chart(ordersCanvas.value, {
    type: 'bar',
    data: {
      labels: labels,
      datasets: [{
        label: 'Orders',
        data: ordersData,
        borderWidth: 1
      }]
    },
    options: {
      responsive: true,
      plugins: { legend: { display: false } }
    }
  })
}

onMounted(async () => {
  try {
    errorMessage.value = ''
    const data = await getAnalytics()
    if (!data) {
      errorMessage.value = 'Unable to load analytics right now. Please refresh.'
      return
    }
    analyticsData.value = data

    kpis.value = data.kpis || []
    artistStats.value = data.artistStats || []
    aiSummary.value = data.aiSummary || null

    await nextTick()
    renderCharts(data)
  } catch (e) {
    console.error('Analytics page failed to render', e)
    errorMessage.value = 'Unable to load analytics right now. Please refresh.'
  }
})

watch(activeTab, async (tab) => {
  if (tab === 'overview' && analyticsData.value) {
    await nextTick()
    renderCharts(analyticsData.value)
  } else {
    destroyCharts()
  }
})

onBeforeUnmount(() => {
  destroyCharts()
})
</script>

<style scoped>
.analytics-page {
  background: #faf8f5;
  min-height: 100vh;
}

.page-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 60px 40px;
  font-family: 'DM Sans', sans-serif;
}

.page-title {
  font-family: 'Playfair Display', serif;
  font-size: 32px;
  margin-bottom: 24px;
  color: #1A1A1A;
}

.tabs {
  display: flex;
  gap: 10px;
  margin-bottom: 20px;
}

.tabs button {
  padding: 8px 16px;
  border-radius: 20px;
  border: none;
  background: #eee;
  cursor: pointer;
  font-family: 'DM Sans', sans-serif;
}

.tabs button.active {
  background: #c4622d;
  color: white;
}

.kpi-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 16px;
  margin-bottom: 20px;
}

.kpi-card {
  background: white;
  padding: 16px;
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(0,0,0,0.05);
}

.kpi-label {
  font-size: 14px;
  color: #666;
}

.kpi-value {
  font-size: 24px;
}

.charts {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 16px;
  margin-bottom: 20px;
}

.chart-card {
  background: white;
  padding: 16px;
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(0,0,0,0.05);
}

.chart-title {
  margin: 0 0 10px 0;
  font-family: 'DM Sans', sans-serif;
  font-size: 15px;
  color: #555;
  font-weight: 600;
}

.ai-summary {
  background: linear-gradient(145deg, #fff9f4 0%, #ffffff 70%);
  border: 1px solid #f0dcca;
  padding: 18px;
  border-radius: 12px;
  box-shadow: 0 6px 16px rgba(196, 98, 45, 0.08);
}

.ai-top h3 {
  margin: 8px 0 4px;
  font-family: 'Playfair Display', serif;
  font-size: 28px;
  color: #1f1a15;
}

.ai-pill {
  display: inline-block;
  background: #c4622d;
  color: #fff;
  font-size: 11px;
  letter-spacing: 0.6px;
  font-weight: 700;
  border-radius: 999px;
  padding: 5px 10px;
}

.ai-subtitle {
  margin: 0;
  color: #6e6258;
  font-size: 13px;
}

.ai-chips {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  margin: 12px 0 14px;
}

.ai-chip {
  background: #fff;
  border: 1px solid #ead6c4;
  color: #7a5c44;
  border-radius: 999px;
  padding: 5px 10px;
  font-size: 12px;
  font-weight: 600;
}

.ai-body {
  margin: 0;
  font-size: 15px;
  line-height: 1.7;
  color: #2d2a26;
}

.placeholder {
  color: #999;
}

.table-card {
  background: white;
  border-radius: 12px;
  padding: 20px;
  box-shadow: 0 4px 12px rgba(0,0,0,0.05);
}

table {
  width: 100%;
  border-collapse: collapse;
  font-family: 'DM Sans', sans-serif;
}

th {
  text-align: left;
  font-size: 14px;
  color: #666;
  padding-bottom: 12px;
}

td {
  padding: 12px 0;
}

.map-placeholder {
  height: 300px;
  background: white;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #999;
  box-shadow: 0 4px 12px rgba(0,0,0,0.05);
}

.error-banner {
  margin-bottom: 16px;
  background: #fff4f4;
  color: #9b2c2c;
  border: 1px solid #f3c7c7;
  border-radius: 10px;
  padding: 10px 12px;
  font-size: 14px;
}
</style>
