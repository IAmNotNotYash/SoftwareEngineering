<template>
  <nav class="navbar">
    <div class="navbar-logo"><i>Kala</i></div>
    <div class="navbar-links">
      <RouterLink to="/admin/dashboard">Dashboard</RouterLink>
      <RouterLink to="/admin/verification">Verification</RouterLink>
      <RouterLink to="/admin/artists">Artists</RouterLink>
      <RouterLink to="/admin/buyers">Buyers</RouterLink>
      <RouterLink to="/admin/orders">Orders</RouterLink>
      <RouterLink to="/admin/analytics">Analytics</RouterLink>
      <a href="#" class="logout">Logout</a>
    </div>
  </nav>
</template>

<style scoped>
.navbar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 40px;
  height: 56px;
  background: #ffffff;
  border-bottom: 1px solid #e8e0d8;
  position: sticky;
  top: 0;
  z-index: 100;
}

.navbar-logo {
  font-family: 'Playfair Display', serif;
  font-size: 22px;
  color: #C4622D;
  font-weight: 600;
  letter-spacing: 0.5px;
}

.navbar-links {
  display: flex;
  align-items: center;
  gap: 28px;
}

.navbar-links a {
  text-decoration: none;
  font-size: 14px;
  color: #555;
  font-family: 'DM Sans', sans-serif;
}

.navbar-links a:hover {
  color: #C4622D;
}

.navbar-links a.router-link-active {
  color: #C4622D;
  font-weight: 600;
}

.navbar-links .logout {
  color: #888;
}

.navbar-links .logout:hover {
  color: #C4622D;
}
</style>