<template>
  <div class="analytics-page">
    <AdminNavbar />

    <div class="container">
      <h1 class="title">Analytics</h1>

      <!-- Tabs -->
      <div class="tabs">
        <button :class="{ active: activeTab === 'overview' }" @click="activeTab = 'overview'">Overview</button>
        <button :class="{ active: activeTab === 'artists' }" @click="activeTab = 'artists'">By Artist</button>
        <button :class="{ active: activeTab === 'geo' }" @click="activeTab = 'geo'">Geographic</button>
      </div>

      <!-- Overview Tab -->
      <div v-if="activeTab === 'overview'">
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
            <canvas ref="revenueCanvas"></canvas>
          </div>
          <div class="chart-card">
            <canvas ref="ordersCanvas"></canvas>
          </div>
        </div>

        <!-- AI Summary Placeholder -->
        <div class="ai-summary">
          <h3>AI Insights</h3>
          <p class="placeholder">
            AI-generated summary of platform performance will appear here.
          </p>
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
import { ref, onMounted, nextTick } from 'vue'
import AdminNavbar from '../../components/AdminNavbar.vue'
import { getAnalytics } from '../../api/admin.js'
import Chart from 'chart.js/auto'

const activeTab = ref('overview')
const kpis = ref([])
const artistStats = ref([])

const revenueCanvas = ref(null)
const ordersCanvas = ref(null)

let revenueChart = null
let ordersChart = null

onMounted(async () => {
  const data = await getAnalytics()
  kpis.value = data.kpis
  artistStats.value = data.artistStats

  await nextTick()

  // Revenue Chart
  revenueChart = new Chart(revenueCanvas.value, {
    type: 'line',
    data: {
      labels: data.revenueTrend.labels,
      datasets: [{
        label: 'Revenue',
        data: data.revenueTrend.data,
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
      labels: data.ordersTrend.labels,
      datasets: [{
        label: 'Orders',
        data: data.ordersTrend.data,
        borderWidth: 1
      }]
    },
    options: {
      responsive: true,
      plugins: { legend: { display: false } }
    }
  })
})
</script>

<style scoped>
.analytics-page {
  background: #faf8f5;
  min-height: 100vh;
}

.container {
  padding: 24px 40px;
}

.title {
  font-family: 'Playfair Display', serif;
  font-size: 32px;
  margin-bottom: 20px;
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

.ai-summary {
  background: white;
  padding: 16px;
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(0,0,0,0.05);
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
</style>
