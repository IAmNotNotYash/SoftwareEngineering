<template>
  <div>
    <AdminNavbar />
    <div class="page-container">
      <div class="header-flex">
        <h1 class="page-title">Platform Overview</h1>
        <div class="date-badge">{{ currentDate }}</div>
      </div>

      <div class="alert-banner" v-if="stats.pendingVerifications > 0">
        <div class="alert-content">
          <span class="icon">⚠️</span>
          <span><strong>Action Required:</strong> {{ stats.pendingVerifications }} artist(s) awaiting verification.</span>
        </div>
        <RouterLink to="/admin/verification" class="alert-link">Review Now</RouterLink>
      </div>

      <div class="kpi-grid">
        <div class="kpi-card">
          <div class="card-icon revenue">₹</div>
          <div class="kpi-info">
            <div class="kpi-label">Total Revenue</div>
            <div class="kpi-value">₹{{ stats.totalRevenue?.toLocaleString('en-IN') || 0 }}</div>
            <div class="kpi-trend positive">↑ 12.5% vs last month</div>
          </div>
        </div>
        <div class="kpi-card">
          <div class="card-icon orders">📦</div>
          <div class="kpi-info">
            <div class="kpi-label">Total Orders</div>
            <div class="kpi-value">{{ stats.totalOrders || 0 }}</div>
            <div class="kpi-trend positive">↑ 8% vs last month</div>
          </div>
        </div>
        <div class="kpi-card">
          <div class="card-icon artists">🎨</div>
          <div class="kpi-info">
            <div class="kpi-label">Registered Artists</div>
            <div class="kpi-value">{{ stats.registeredArtists || 0 }}</div>
            <div class="kpi-trend neutral">Steady growth</div>
          </div>
        </div>
        <div class="kpi-card">
          <div class="card-icon buyers">👥</div>
          <div class="kpi-info">
            <div class="kpi-label">Registered Buyers</div>
            <div class="kpi-value">{{ stats.registeredBuyers || 0 }}</div>
            <div class="kpi-trend positive">↑ 15% new users</div>
          </div>
        </div>
      </div>

      <div class="dashboard-body">
        <div class="chart-container card">
          <div class="card-header">
            <h3>Revenue Trend</h3>
          </div>
          <div class="chart-wrapper">
            <canvas ref="revenueChartCanvas"></canvas>
          </div>
        </div>
        
        <div class="recent-orders card">
          <div class="card-header">
            <h3>Recent Orders</h3>
            <RouterLink to="/admin/orders" class="view-all">View All</RouterLink>
          </div>
          <div class="order-list">
            <div class="order-item" v-for="order in recentOrders" :key="order.id">
              <div class="order-avatar">{{ order.buyer ? order.buyer.charAt(0).toUpperCase() : '?' }}</div>
              <div class="order-details">
                <strong>{{ order.buyer }}</strong>
                <span>purchased from {{ order.artist }}</span>
              </div>
              <div class="order-price">₹{{ order.total?.toLocaleString('en-IN') || 0 }}</div>
            </div>
            <div v-if="!recentOrders.length" class="empty-state">No recent orders yet.</div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, nextTick } from 'vue'
import AdminNavbar from '../../components/AdminNavbar.vue'
import { getDashboardStats, getPlatformAnalytics, getOrders } from '../../api/admin.js'
import Chart from 'chart.js/auto'

const stats = ref({})
const analytics = ref({})
const recentOrders = ref([])
const revenueChartCanvas = ref(null)

const currentDate = new Date().toLocaleDateString('en-US', { weekday: 'short', year: 'numeric', month: 'short', day: 'numeric' })

onMounted(async () => {
  stats.value = await getDashboardStats()
  
  try {
    const data = await getPlatformAnalytics()
    analytics.value = data
    
    const orders = await getOrders()
    recentOrders.value = orders.slice(0, 5)

    await nextTick()

    if (revenueChartCanvas.value && data.revenueOverTime) {
      new Chart(revenueChartCanvas.value, {
        type: 'line',
        data: {
          labels: data.revenueOverTime.map(d => d.month),
          datasets: [{
            label: 'Revenue',
            data: data.revenueOverTime.map(d => d.revenue),
            borderColor: '#C4622D',
            backgroundColor: 'rgba(196, 98, 45, 0.08)',
            borderWidth: 2.5,
            tension: 0.4,
            fill: true,
            pointBackgroundColor: '#C4622D',
            pointBorderColor: '#fff',
            pointBorderWidth: 2,
            pointRadius: 4,
            pointHoverRadius: 6
          }]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: { legend: { display: false }, tooltip: { padding: 10, cornerRadius: 8, titleFont: { family: 'DM Sans' }, bodyFont: { family: 'DM Sans', size: 14 } } },
          scales: {
            x: { grid: { display: false }, ticks: { font: { family: 'DM Sans', size: 12 }, color: '#888' } },
            y: { grid: { color: '#f0f0f0', borderDash: [4, 4] }, border: { display: false }, ticks: { font: { family: 'DM Sans', size: 12 }, color: '#888', callback: (value) => '₹' + (value/1000) + 'k', maxTicksLimit: 6 } }
          },
          interaction: { intersect: false, mode: 'index' }
        }
      })
    }
  } catch(e) {
    console.error("Dashboard failed to load analytics/orders", e)
  }
})
</script>

<style scoped>
.page-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 40px;
  font-family: 'DM Sans', sans-serif;
}

.header-flex {
  display: flex;
  justify-content: space-between;
  align-items: flex-end;
  margin-bottom: 24px;
}

.page-title {
  font-family: 'Playfair Display', serif;
  font-size: 32px;
  color: #1A1A1A;
  margin-bottom: 0;
}

.date-badge {
  background: white;
  padding: 6px 14px;
  border-radius: 20px;
  border: 1px solid #e8e0d8;
  font-size: 13px;
  font-weight: 500;
  color: #666;
}

.alert-banner {
  display: flex;
  align-items: center;
  justify-content: space-between;
  background: #fff8e1;
  border: 1px solid #ffeba0;
  border-left: 4px solid #f5b041;
  border-radius: 8px;
  padding: 14px 20px;
  margin-bottom: 28px;
  font-size: 14px;
  color: #7a5c00;
}

.alert-content {
  display: flex;
  align-items: center;
  gap: 10px;
}

.alert-link {
  text-decoration: none;
  background: #ffffff;
  color: #1A1A1A;
  border: 1px solid #e2d184;
  padding: 6px 14px;
  border-radius: 6px;
  font-size: 13px;
  font-weight: 600;
  transition: background 0.2s;
}

.alert-link:hover {
  background: #fdf7e3;
}

.kpi-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 20px;
  margin-bottom: 24px;
}

.kpi-card {
  background: #ffffff;
  border-radius: 12px;
  padding: 24px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.03);
  border: 1px solid #f0f0f0;
  display: flex;
  align-items: flex-start;
  gap: 16px;
  transition: transform 0.2s, box-shadow 0.2s;
}

.kpi-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 16px rgba(0, 0, 0, 0.06);
}

.card-icon {
  width: 48px;
  height: 48px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 20px;
  flex-shrink: 0;
}

.card-icon.revenue { background: #fdf2ed; color: #C4622D; }
.card-icon.orders { background: #f0f7ff; color: #3B82F6; }
.card-icon.artists { background: #f3e8ff; color: #8B5CF6; }
.card-icon.buyers { background: #ecfdf5; color: #10B981; }

.kpi-info {
  flex: 1;
}

.kpi-label {
  font-size: 12px;
  letter-spacing: 0.04em;
  text-transform: uppercase;
  font-weight: 600;
  color: #888;
  margin-bottom: 4px;
}

.kpi-value {
  font-family: 'Playfair Display', serif;
  font-size: 28px;
  font-weight: 700;
  color: #1A1A1A;
  line-height: 1.2;
  margin-bottom: 6px;
}

.kpi-trend {
  font-size: 12px;
  font-weight: 500;
}

.kpi-trend.positive { color: #10B981; }
.kpi-trend.neutral { color: #888; }
.kpi-trend.negative { color: #EF4444; }

.dashboard-body {
  display: grid;
  grid-template-columns: 2fr 1fr;
  gap: 20px;
}

.card {
  background: white;
  border-radius: 12px;
  border: 1px solid #f0f0f0;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.03);
  display: flex;
  flex-direction: column;
}

.card-header {
  padding: 20px 24px;
  border-bottom: 1px solid #f5f5f5;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.card-header h3 {
  font-family: 'Playfair Display', serif;
  font-size: 18px;
  margin: 0;
  color: #1A1A1A;
}

.view-all {
  font-size: 13px;
  color: #C4622D;
  text-decoration: none;
  font-weight: 600;
}

.view-all:hover {
  text-decoration: underline;
}

.chart-wrapper {
  padding: 20px;
  height: 320px;
  flex: 1;
  position: relative;
}

.order-list {
  padding: 10px 0;
  overflow-y: auto;
  max-height: 340px;
}

.order-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px 24px;
  border-bottom: 1px solid #f9f9f9;
  transition: background 0.15s;
}

.order-item:last-child {
  border-bottom: none;
}

.order-item:hover {
  background: #fafafa;
}

.order-avatar {
  width: 36px;
  height: 36px;
  background: #f0f0f0;
  color: #555;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 600;
  font-size: 14px;
}

.order-details {
  flex: 1;
  display: flex;
  flex-direction: column;
}

.order-details strong {
  font-size: 14px;
  color: #1A1A1A;
  margin-bottom: 2px;
}

.order-details span {
  font-size: 12px;
  color: #888;
}

.order-price {
  font-weight: 600;
  font-family: 'Playfair Display', serif;
  font-size: 15px;
  color: #1A1A1A;
}

.empty-state {
  padding: 40px 24px;
  text-align: center;
  color: #888;
  font-size: 14px;
}
</style>