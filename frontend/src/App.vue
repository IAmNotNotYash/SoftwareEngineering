<template>
  <div class="app-wrapper">
    <div class="main-content">
      <RouterView />
    </div>
    <SiteFooter />
  </div>
</template>

<script setup>
import SiteFooter from './components/SiteFooter.vue'
</script>

<style>
html, body {
  margin: 0;
  padding: 0;
  height: 100%;
}

#app {
  height: 100%;
}

.app-wrapper {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
}

.main-content {
  flex: 1;
}
</style>