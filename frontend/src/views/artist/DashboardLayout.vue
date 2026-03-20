<template>
  <div class="flex">
    <ArtistSidebar />
    <div class="flex-1">
      <router-view />
    </div>
  </div>
</template>

<script setup lang="ts">
import ArtistSidebar from "../../components/ArtistSidebar.vue"
</script>