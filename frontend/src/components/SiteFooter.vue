<template>
  <footer class="site-footer">
    <span class="footer-brand">Kala</span>
    <span class="footer-copy">© 2026 Kala. Crafted with intention.</span>
  </footer>
</template>

<style scoped>
.site-footer {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 60px;
  height: 80px;
  border-top: 1px solid rgba(232, 224, 216, 0.6);
  background: var(--color-footer-bg);
  width: 100%;
  box-sizing: border-box;
}

.footer-brand {
  font-family: 'Playfair Display', serif;
  font-size: 24px;
  font-weight: 700;
  color: #1a1a1a;
  display: flex;
  align-items: center;
  gap: 12px;
  letter-spacing: 0.5px;
}

.footer-copy {
  font-size: 14px;
  color: #888;
  font-family: 'DM Sans', sans-serif;
  letter-spacing: 0.5px;
}
</style>
