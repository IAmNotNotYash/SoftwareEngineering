<template>
  <div class="campaigns">
    <div class="page-header">
      <div>
        <h1>Campaigns</h1>
        <p>Manage and track all your campaigns.</p>
      </div>
      <router-link to="/campaigns/new" class="btn-primary">＋ New Campaign</router-link>
    </div>

    <div class="campaigns-grid">
      <div class="campaign-card card" v-for="c in campaigns" :key="c.name">
        <div class="campaign-cover" :style="{ background: c.gradient }">
          <div class="campaign-overlay"></div>
        </div>
        <div class="campaign-body">
          <div class="campaign-title-row">
            <h3>{{ c.name }}</h3>
            <button class="more-btn">···</button>
          </div>
          <div class="badge" :class="c.status.toLowerCase()">{{ c.status }}</div>
          <div class="campaign-stats">
            <div class="cstat"><span>₹</span> {{ c.revenue }}</div>
            <div class="cstat"><span>🛒</span> {{ c.orders }} orders</div>
            <div class="cstat"><span>👁</span> {{ c.reach }} reach</div>
            <div class="cstat"><span>❤️</span> {{ c.likes }} likes</div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
const campaigns = [
  { name: 'Summer Art Collection', status: 'Live', revenue: '₹45,200', orders: 128, reach: '24,500', likes: '3,200', gradient: 'linear-gradient(135deg,#F97316,#FBBF24)' },
  { name: 'Limited Edition Prints', status: 'Live', revenue: '₹32,800', orders: 95, reach: '18,200', likes: '2,800', gradient: 'linear-gradient(135deg,#FB923C,#F59E0B)' },
  { name: 'Digital Workshop Series', status: 'Draft', revenue: '₹0', orders: 0, reach: '0', likes: '0', gradient: 'linear-gradient(135deg,#FDBA74,#FCD34D)' },
  { name: 'Portrait Commission Sale', status: 'Ended', revenue: '₹68,400', orders: 42, reach: '31,000', likes: '5,100', gradient: 'linear-gradient(135deg,#EA580C,#F97316)' },
  { name: 'Holiday Gift Bundles', status: 'Ended', revenue: '₹52,100', orders: 186, reach: '28,400', likes: '4,200', gradient: 'linear-gradient(135deg,#F97316,#FB923C)' },
  { name: 'Watercolor Basics Course', status: 'Draft', revenue: '₹0', orders: 0, reach: '0', likes: '0', gradient: 'linear-gradient(135deg,#FED7AA,#FDE68A)' },
]
</script>

<style scoped>
.campaigns { display: flex; flex-direction: column; gap: 24px; }

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
}

.page-header h1 { font-size: 26px; margin-bottom: 4px; }
.page-header p { color: var(--text-2); }

.campaigns-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 20px;
}

.campaign-card { overflow: hidden; transition: transform 0.15s, box-shadow 0.15s; }
.campaign-card:hover { transform: translateY(-2px); box-shadow: var(--shadow-md); }

.campaign-cover {
  height: 140px;
  position: relative;
}

.campaign-body { padding: 16px; }

.campaign-title-row {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 8px;
}

.campaign-title-row h3 { font-size: 15px; font-family: 'DM Sans', sans-serif; font-weight: 600; }

.more-btn {
  background: none;
  color: var(--text-3);
  font-size: 18px;
  padding: 0 4px;
  letter-spacing: 1px;
}

.badge {
  display: inline-block;
  font-size: 11px;
  font-weight: 600;
  padding: 3px 10px;
  border-radius: 20px;
  margin-bottom: 14px;
}
.badge.live { background: #DCFCE7; color: #16A34A; }
.badge.draft { background: #F3F4F6; color: #6B7280; }
.badge.ended { background: #FEE2E2; color: #DC2626; }

.campaign-stats {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 6px;
}

.cstat {
  font-size: 13px;
  color: var(--text-2);
  display: flex;
  align-items: center;
  gap: 6px;
}
</style>