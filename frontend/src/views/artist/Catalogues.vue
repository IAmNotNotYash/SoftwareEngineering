<template>
  <div class="catalogues-page">
    <ArtistNavbar />

    <main class="page-container">
      <div class="page-header">
        <div>
          <h1 class="page-title">Catalogues</h1>
          <p class="subtitle">Manage and track your active and past product catalogues.</p>
        </div>
        <router-link to="/artist/newcatalogue" class="btn primary-btn">+ New Catalogue</router-link>
      </div>

      <div class="catalogues-grid">
        <div class="catalogue-card" v-for="c in catalogues" :key="c.name">
          <div class="catalogue-bg" :style="{ backgroundImage: `url(${c.image})` }">
            <div class="catalogue-overlay">
              
              <!-- Top bar: Status & Actions -->
              <div class="card-top">
                <div class="status-badge" :class="c.status.toLowerCase()">{{ c.status }}</div>
                <div class="actions">
                  <button class="icon-btn edit-btn" title="Edit">✎</button>
                  <button class="icon-btn end-btn" title="End Catalogue">⏹</button>
                </div>
              </div>
              
              <!-- Bottom bar: Title & Stats -->
              <div class="card-bottom">
                <h3>{{ c.name }}</h3>
                <div class="catalogue-stats">
                  <div class="stat-item"><span class="stat-icon">₹</span> {{ c.revenue }}</div>
                  <div class="stat-item"><span class="stat-icon">📦</span> {{ c.orders }}</div>
                  <div class="stat-item"><span class="stat-icon">👁</span> {{ c.reach }}</div>
                  <div class="stat-item"><span class="stat-icon">❤</span> {{ c.likes }}</div>
                </div>
              </div>

            </div>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup>
import ArtistNavbar from '../../components/ArtistNavbar.vue'

const catalogues = [
  { name: 'Summer Art Collection', status: 'Live', revenue: '45,200', orders: 128, reach: '24.5K', likes: '3.2K', image: 'https://images.unsplash.com/photo-1544816155-12df9643f363?w=800' },
  { name: 'Earth Tone Ceramics', status: 'Live', revenue: '32,800', orders: 95, reach: '18.2K', likes: '2.8K', image: 'https://images.unsplash.com/photo-1610701596007-11502861dcfa?w=800' },
  { name: 'Digital Workshop Series', status: 'Draft', revenue: '0', orders: 0, reach: '0', likes: '0', image: 'https://images.unsplash.com/photo-1513364776144-60967b0f800f?w=800' },
  { name: 'Portrait Commission Sale', status: 'Ended', revenue: '68,400', orders: 42, reach: '31.0K', likes: '5.1K', image: 'https://images.unsplash.com/photo-1534528741775-53994a69daeb?w=800' },
]
</script>

<style scoped>
.catalogues-page {
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
  border: none;
}
.primary-btn:hover { background: #a85427; }

/* Grid matching Buyer aesthetic (large cards) */
.catalogues-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 32px;
}

.catalogue-card {
  position: relative;
  height: 320px;
  border-radius: 16px;
  overflow: hidden;
  box-shadow: 0 4px 24px rgba(0,0,0,0.06);
  transition: transform 0.3s ease, box-shadow 0.3s ease;
  cursor: pointer;
}

.catalogue-card:hover {
  transform: translateY(-6px);
  box-shadow: 0 12px 32px rgba(0,0,0,0.12);
}

.catalogue-bg {
  position: absolute;
  inset: 0;
  background-size: cover;
  background-position: center;
  transition: transform 0.4s ease;
}

.catalogue-card:hover .catalogue-bg {
  transform: scale(1.05);
}

.catalogue-overlay {
  position: absolute;
  inset: 0;
  background: linear-gradient(
    rgba(0,0,0,0.5) 0%, 
    rgba(0,0,0,0.1) 40%, 
    rgba(0,0,0,0.2) 60%, 
    rgba(0,0,0,0.85) 100%
  );
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  padding: 24px;
}

.card-top {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
}

.status-badge {
  font-size: 11px;
  font-weight: 700;
  padding: 6px 14px;
  border-radius: 20px;
  text-transform: uppercase;
  letter-spacing: 0.8px;
  backdrop-filter: blur(8px);
}
.status-badge.live { background: rgba(22, 163, 74, 0.85); color: #fff; }
.status-badge.draft { background: rgba(107, 114, 128, 0.85); color: #fff; }
.status-badge.ended { background: rgba(220, 38, 38, 0.85); color: #fff; }

.actions {
  display: flex;
  gap: 10px;
  opacity: 0;
  transform: translateY(-10px);
  transition: all 0.3s ease;
}

.catalogue-card:hover .actions {
  opacity: 1;
  transform: translateY(0);
}

.icon-btn {
  background: rgba(255,255,255,0.2);
  backdrop-filter: blur(8px);
  color: #fff;
  border: 1px solid rgba(255,255,255,0.4);
  width: 36px;
  height: 36px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  font-size: 16px;
  transition: all 0.2s;
}

.icon-btn:hover {
  background: #fff;
  color: #1a1a1a;
  border-color: #fff;
}
.end-btn { font-size: 14px; }
.end-btn:hover { color: #F59E0B; } /* Amber warn color for ending */

.card-bottom h3 {
  font-family: var(--font-heading);
  font-size: 26px;
  font-weight: 700;
  color: #ffffff;
  margin: 0 0 16px 0;
  text-shadow: 0 2px 8px rgba(0,0,0,0.5);
}

.catalogue-stats {
  display: flex;
  gap: 20px;
  background: rgba(0,0,0,0.4);
  backdrop-filter: blur(8px);
  padding: 12px 20px;
  border-radius: 8px;
  border: 1px solid rgba(255,255,255,0.15);
}

.stat-item {
  color: #fff;
  font-size: 14px;
  font-weight: 600;
  display: flex;
  align-items: center;
  gap: 8px;
  letter-spacing: 0.5px;
}

.stat-icon {
  font-size: 16px;
  opacity: 0.8;
}
</style>