<template>
  <div class="app-layout">
    <aside class="sidebar">
      <div class="sidebar-logo">
        <div class="logo-icon">A</div>
        <span class="logo-text">Artistly</span>
      </div>

      <nav class="sidebar-nav">
        <p class="nav-label">Menu</p>
        <router-link to="/dashboard" class="nav-item">
          <span class="nav-icon">⊞</span> Dashboard
        </router-link>
        <router-link to="/campaigns" class="nav-item">
          <span class="nav-icon">🚀</span> Campaigns
        </router-link>
        <router-link to="/products" class="nav-item">
          <span class="nav-icon">🛍</span> Products
        </router-link>
        <router-link to="/sendout" class="nav-item">
          <span class="nav-icon">📤</span> Send-Out
        </router-link>

        <p class="nav-label" style="margin-top:24px">Actions</p>
        <router-link to="/campaigns/new" class="nav-item nav-action">
          <span>＋</span> New Campaign
        </router-link>
      </nav>

      <router-link to="/dashboard" class="sidebar-settings">
        <span>⚙</span> Settings
      </router-link>
    </aside>

    <main class="main-content">
      <header class="top-bar">
        <span class="page-title">Artistly</span>
      </header>
      <div class="page-body">
        <router-view />
      </div>
    </main>
  </div>
</template>

<style scoped>
.app-layout {
  display: flex;
  height: 100vh;
  overflow: hidden;
}

.sidebar {
  width: 220px;
  min-width: 220px;
  background: white;
  border-right: 1px solid var(--border);
  display: flex;
  flex-direction: column;
  padding: 20px 12px;
}

.sidebar-logo {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 4px 8px 20px;
}

.logo-icon {
  width: 34px;
  height: 34px;
  border-radius: 9px;
  background: var(--orange);
  color: white;
  font-weight: 700;
  font-size: 16px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-family: 'Fraunces', serif;
}

.logo-text {
  font-size: 17px;
  font-weight: 600;
  font-family: 'Fraunces', serif;
  color: var(--text);
}

.nav-label {
  font-size: 11px;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  color: var(--text-3);
  padding: 0 8px;
  margin-bottom: 4px;
}

.nav-item {
  display: flex;
  align-items: center;
  gap: 9px;
  padding: 8px 10px;
  border-radius: 8px;
  font-weight: 500;
  font-size: 14px;
  color: var(--text-2);
  transition: all 0.12s;
  margin-bottom: 1px;
}

.nav-item:hover {
  background: var(--orange-pale);
  color: var(--orange);
}

.nav-item.router-link-active {
  background: var(--orange-pale);
  color: var(--orange);
  font-weight: 600;
}

.nav-icon { font-size: 16px; }

.nav-action {
  color: var(--text);
  font-size: 13px;
}

.sidebar-settings {
  margin-top: auto;
  display: flex;
  align-items: center;
  gap: 9px;
  padding: 8px 10px;
  border-radius: 8px;
  font-size: 14px;
  font-weight: 500;
  color: var(--text-2);
  transition: all 0.12s;
}
.sidebar-settings:hover { color: var(--orange); background: var(--orange-pale); }

.main-content {
  flex: 1;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.top-bar {
  padding: 14px 28px;
  border-bottom: 1px solid var(--border);
  background: white;
  display: flex;
  align-items: center;
  gap: 10px;
}

.page-title {
  font-family: 'Fraunces', serif;
  font-size: 15px;
  font-weight: 600;
}

.page-body {
  flex: 1;
  overflow-y: auto;
  padding: 28px;
}
</style>