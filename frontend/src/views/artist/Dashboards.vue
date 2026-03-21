<template>

  <div class="dashboard">
    <ArtistNavbar />

    <div class="page-header">
      <h1>Welcome back, Artist! 🎨</h1>
      <p>Here's how your creative business is doing.</p>
    </div>

    <div class="stats-grid">
      <div class="stat-card" v-for="stat in stats" :key="stat.label">
        <div class="stat-header">
          <span class="stat-label">{{ stat.label }}</span>
          <div class="stat-icon" :style="{ background: stat.iconBg }">
            <span>{{ stat.icon }}</span>
          </div>
        </div>
        <div class="stat-value">{{ stat.value }}</div>
        <div class="stat-change" :class="stat.changeType">{{ stat.change }}</div>
      </div>
    </div>

    <div class="bottom-row">
      <div class="card chart-card">
        <div class="chart-header">
          <h3>Growth Overview</h3>
          <div class="chart-legend">
            <span class="legend-dot" style="background:#22C55E"></span> Revenue
            <span class="legend-dot" style="background:#3B82F6"></span> Followers
          </div>
        </div>
        <!-- chart-wrap fills remaining space; canvas sizes to it -->
        <div class="chart-wrap">
          <canvas ref="chartCanvas"></canvas>
        </div>
      </div>

      <div class="card audience-card">
        <h3>Audience Segments</h3>
        <div class="segment" v-for="seg in segments" :key="seg.label">
          <div class="seg-header">
            <div class="seg-name">
              <span>{{ seg.icon }}</span>
              {{ seg.label }}
            </div>
            <strong>{{ seg.count.toLocaleString() }}</strong>
          </div>
          <div class="seg-bar-bg">
            <div class="seg-bar" :style="{ width: seg.pct + '%', background: seg.color }"></div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import ArtistNavbar from '../../components/ArtistNavbar.vue'
import { Chart, registerables } from 'chart.js'
Chart.register(...registerables)

const chartCanvas = ref(null)

const stats = [
  { label: 'Total Revenue', value: '₹1,85,400', icon: '₹', iconBg: '#DCFCE7', change: '↑ 12.5% this month', changeType: 'up' },
  { label: 'Total Followers', value: '16,575', icon: '👥', iconBg: '#DBEAFE', change: '↑ 8.3% this month', changeType: 'up' },
  { label: 'Total Orders', value: '842', icon: '🛒', iconBg: '#FED7AA', change: '↑ 5.1% this month', changeType: 'up' },
  { label: 'Pending Orders', value: '23', icon: '⏱', iconBg: '#FEF3C7', change: '↓ 3 new today', changeType: 'down' },
]

const segments = [
  { label: 'Followers', icon: '👥', count: 12840, pct: 78, color: '#3B82F6' },
  { label: 'Fans', icon: '❤️', count: 3250, pct: 45, color: '#F97316' },
  { label: 'Patrons', icon: '👑', count: 485, pct: 18, color: '#8B5CF6' },
]

const months = ['Jan','Feb','Mar','Apr','May','Jun','Jul']
const revenueData = [9000, 12000, 11000, 14000, 18000, 24000, 33000]
const followerData = [9000, 10000, 10500, 11200, 12000, 13000, 14200]

onMounted(() => {
  new Chart(chartCanvas.value, {
    type: 'line',
    data: {
      labels: months,
      datasets: [
        {
          label: 'Revenue',
          data: revenueData,
          borderColor: '#22C55E',
          backgroundColor: 'rgba(34,197,94,0.1)',
          fill: true,
          tension: 0.4,
          pointRadius: 0,
          borderWidth: 2.5,
        },
        {
          label: 'Followers',
          data: followerData,
          borderColor: '#3B82F6',
          backgroundColor: 'rgba(59,130,246,0.05)',
          fill: true,
          tension: 0.4,
          pointRadius: 0,
          borderWidth: 2,
        }
      ]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: { legend: { display: false } },
      scales: {
        x: { grid: { color: '#F0EDE8' }, ticks: { font: { family: 'DM Sans', size: 12 }, color: '#A09A94' } },
        y: { grid: { color: '#F0EDE8' }, ticks: { font: { family: 'DM Sans', size: 12 }, color: '#A09A94' } }
      }
    }
  })
})
</script>

<style scoped>
/*
  The dashboard must never grow taller than the viewport's available space.
  The trick: make .dashboard a flex column that fills its parent's height,
  then let .bottom-row absorb all leftover space (flex:1 + min-height:0).
  The chart-card is also a flex column so .chart-wrap can stretch inside it.
  Setting min-height:0 on every flex child prevents the default min-height:auto
  from allowing overflow.
*/

.dashboard {
  display: flex;
  flex-direction: column;
  gap: 24px;
  height: 100%;       /* fill parent — parent must also have a defined height */
  overflow: hidden;
}
.page-header{margin:20px;}
.page-header h1 { font-size: 26px; font-weight: 600; margin-bottom: 4px; }
.page-header p { color: var(--text-2); }

/* Fixed-height top section — stat cards never shrink */
.stats-grid {
  margin:20px;
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 16px;
  flex-shrink: 0;
}

.stat-card {
  background: white;
  border: 1px solid var(--border);
  border-radius: var(--radius);
  padding: 20px;
  box-shadow: var(--shadow);
}

.stat-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 12px;
}

.stat-label { font-size: 13px; color: var(--text-2); font-weight: 500; }

.stat-icon {
  width: 38px;
  height: 38px;
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 16px;
}

.stat-value {
  font-size: 28px;
  font-weight: 700;
  font-family: 'Fraunces', serif;
  margin-bottom: 8px;
}

.stat-change { font-size: 12px; font-weight: 500; }
.stat-change.up { color: var(--green); }
.stat-change.down { color: var(--red); }

/* Bottom row stretches to fill remaining vertical space */
.bottom-row {
      display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 20px;
    flex: 1;
    min-height: 0;
    margin: 20px; /* allow shrinking below content size — critical for flex children */
}

/* chart-card is a flex column so chart-wrap can grow inside it */
.chart-card {
  padding: 20px;
  display: flex;
  flex-direction: column;
  min-height: 0;
}

.chart-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
  flex-shrink: 0;   /* header never compresses */
}

.chart-header h3 { font-size: 16px; }
.chart-legend { display: flex; align-items: center; gap: 14px; font-size: 13px; color: var(--text-2); }
.legend-dot { width: 10px; height: 10px; border-radius: 50%; display: inline-block; margin-right: 4px; }

/*
  chart-wrap is the key: it fills all remaining height inside chart-card.
  position:relative + width/height 100% is the standard Chart.js responsive pattern.
*/
.chart-wrap {
  flex: 1;
  min-height: 0;
  position: relative;
}

.chart-wrap canvas {
  position: absolute;
  inset: 0;
}

.audience-card {
  padding: 20px;
  overflow-y: auto;  /* scroll if segments overflow */
}

.audience-card h3 { font-size: 16px; margin-bottom: 20px; }

.segment { margin-bottom: 18px; }
.seg-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px; font-size: 14px; }
.seg-name { display: flex; align-items: center; gap: 8px; color: var(--text-2); }
.seg-bar-bg { height: 6px; background: var(--bg); border-radius: 3px; overflow: hidden; }
.seg-bar { height: 100%; border-radius: 3px; transition: width 0.6s ease; }
</style>