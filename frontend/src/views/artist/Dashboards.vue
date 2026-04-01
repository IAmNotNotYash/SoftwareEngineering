<template>
  <div class="artist-dashboard">
    <ArtistNavbar />
    
    <main class="page-container">
      <header class="dash-header">
        <div>
          <h1 class="page-title">Artist Dashboard</h1>
          <p class="subtitle">Here is how your brand and catalogues are performing.</p>
        </div>
        <div class="quick-actions">
          <RouterLink to="/artist/newcatalogue" class="btn primary-btn">+ New Catalogue</RouterLink>
          <RouterLink to="/artist/products" class="btn secondary-btn">+ Add Product</RouterLink>
          <RouterLink to="/artist/story" class="btn secondary-btn">+ Post Story</RouterLink>
        </div>
      </header>

      <section class="kpi-grid" v-if="!loading">
        <div class="kpi-card">
          <div class="kpi-label">TOTAL REVENUE (₹)</div>
          <div class="kpi-value highlight">{{ stats.totalRevenue }}</div>
        </div>
        <div class="kpi-card">
          <div class="kpi-label">TOTAL ORDERS</div>
          <div class="kpi-value">{{ stats.totalOrders }}</div>
        </div>
        <div class="kpi-card">
          <div class="kpi-label">CATALOGUE VIEWS</div>
          <div class="kpi-value">{{ stats.catalogueViews.toLocaleString() }}</div>
        </div>
        <div class="kpi-card">
          <div class="kpi-label">STORY ENGAGEMENT</div>
          <div class="kpi-value">{{ stats.storyEngagement }}</div>
        </div>
      </section>
      <div v-else class="loading-state">Loading actual performance metrics...</div>

      <section class="chart-section" v-if="!loading">
        <div class="chart-header">
          <h2>Performance Over Time</h2>
          <div class="legend">
            <span class="legend-item"><span class="dot rev-dot"></span> Revenue</span>
            <span class="legend-item"><span class="dot view-dot"></span> Catalogue Views</span>
          </div>
        </div>
        <div class="chart-container">
          <canvas ref="performanceChart"></canvas>
        </div>
      </section>
    </main>
  </div>
</template>

<script setup>
import { ref, onMounted, nextTick } from 'vue'
import { Chart, registerables } from 'chart.js'
import ArtistNavbar from '../../components/ArtistNavbar.vue'
import { getArtistStats } from '../../api/artist.js'

Chart.register(...registerables)

const stats = ref(null)
const loading = ref(true)
const performanceChart = ref(null)

onMounted(async () => {
  stats.value = await getArtistStats()
  loading.value = false
  
  await nextTick()
  initChart()
})

const initChart = () => {
  if (!performanceChart.value) return
  
  new Chart(performanceChart.value, {
    type: 'line',
    data: {
      labels: stats.value.months,
      datasets: [
        {
          label: 'Revenue',
          data: stats.value.revenueTrend,
          borderColor: '#C4622D',
          backgroundColor: 'rgba(196, 98, 45, 0.1)',
          fill: true,
          tension: 0.4,
          borderWidth: 3,
          yAxisID: 'y'
        },
        {
          label: 'Catalogue Views',
          data: stats.value.viewsTrend,
          borderColor: '#2D2A26',
          backgroundColor: 'rgba(45, 42, 38, 0.05)',
          fill: true,
          tension: 0.4,
          borderWidth: 2,
          yAxisID: 'y1'
        }
      ]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      interaction: {
        mode: 'index',
        intersect: false,
      },
      plugins: {
        legend: { display: false }
      },
      scales: {
        x: {
          grid: { display: false }
        },
        y: {
          type: 'linear',
          display: true,
          position: 'left',
          grid: { color: '#f0f0f0' }
        },
        y1: {
          type: 'linear',
          display: true,
          position: 'right',
          grid: { display: false }
        }
      }
    }
  })
}
</script>

<style scoped>
.artist-dashboard {
  min-height: 100vh;
  background: var(--color-bg-page);
  font-family: var(--font-body);
}

.page-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 60px 40px;
}

.dash-header {
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

.quick-actions {
  display: flex;
  gap: 16px;
}

.btn {
  padding: 10px 20px;
  border-radius: 6px;
  font-size: 14px;
  font-weight: 600;
  text-decoration: none;
  transition: all 0.2s ease;
  cursor: pointer;
}

.primary-btn {
  background: #C4622D;
  color: #fff;
  border: 1px solid #C4622D;
}

.primary-btn:hover {
  background: #a85427;
}

.secondary-btn {
  background: #fff;
  color: #1a1a1a;
  border: 1px solid #e8e0d8;
}

.secondary-btn:hover {
  border-color: #C4622D;
  color: #C4622D;
}

/* KPI Grid perfectly tracking dashboard style */
.kpi-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 24px;
  margin-bottom: 56px;
}

.kpi-card {
  background: #ffffff;
  border-radius: 12px;
  padding: 28px;
  border: 1px solid #e8e0d8;
  box-shadow: 0 4px 20px rgba(0,0,0,0.02);
}

.kpi-label {
  font-size: 11px;
  text-transform: uppercase;
  letter-spacing: 0.8px;
  color: #888;
  font-weight: 600;
  margin-bottom: 12px;
}

.kpi-value {
  font-family: var(--font-heading);
  font-size: 36px;
  font-weight: 600;
  color: #1a1a1a;
}

.kpi-value.highlight {
  color: #C4622D;
}

/* Chart Section */
.chart-section {
  background: #ffffff;
  border-radius: 12px;
  padding: 32px;
  border: 1px solid #e8e0d8;
  box-shadow: 0 4px 20px rgba(0,0,0,0.02);
}

.chart-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
}

.chart-header h2 {
  font-family: var(--font-heading);
  font-size: 22px;
  margin: 0;
  color: #1a1a1a;
}

.legend {
  display: flex;
  gap: 20px;
}

.legend-item {
  font-size: 13px;
  color: #555;
  display: flex;
  align-items: center;
  gap: 8px;
}

.dot {
  width: 10px;
  height: 10px;
  border-radius: 50%;
}

.rev-dot { background: #C4622D; }
.view-dot { background: #2D2A26; }

.chart-container {
  height: 380px;
  width: 100%;
}

.loading-state {
  text-align: center;
  padding: 80px 0;
  color: #888;
  font-size: 15px;
}
</style>