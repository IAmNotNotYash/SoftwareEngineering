<template>
  <div>
    <BuyerNavbar />
    
    <div class="page-container article-container" v-if="post">
      <!-- Breadcrumb -->
      <div class="breadcrumb">
        <RouterLink to="/buyer/dashboard">Dashboard</RouterLink>
        <span class="separator">/</span>
        <span class="current">{{ post.type === 'insight' ? 'Insight' : 'Story' }}</span>
      </div>

      <article class="insight-article">
        <div class="article-header">
          <div class="artist-meta">By <strong>{{ post.artist_name }}</strong></div>
          <h1 class="article-title">{{ post.title }}</h1>
          <div class="article-date">Published {{ formatDate(post.published_at || post.created_at) }}</div>
        </div>

        <div v-if="post.cover_image_url" class="hero-image" :style="{ backgroundImage: `url(${post.cover_image_url})` }"></div>

        <div class="article-body">
          <div class="body-text" v-html="formattedBody"></div>
        </div>
      </article>
    </div>
    
    <div class="page-container loading-container" v-else-if="loading">
      <p>Loading the artisan's journey...</p>
    </div>
    
    <div class="page-container error-container" v-else>
      <p>Could not find this story. It might have been moved or archived.</p>
      <RouterLink to="/buyer/dashboard" class="back-link">Back to Dashboard</RouterLink>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRoute } from 'vue-router'
import BuyerNavbar from '../../components/BuyerNavbar.vue'
import { getPost } from '../../api/social.js'

const route = useRoute()
const post = ref(null)
const loading = ref(true)

onMounted(async () => {
  try {
    const id = route.params.id
    post.value = await getPost(id)
  } catch (err) {
    console.error("Failed to load post:", err)
  } finally {
    loading.value = false
  }
})

const formattedBody = computed(() => {
  if (!post.value?.body) return ''
  // Convert newlines to paragraphs for basic formatting if it's plain text
  // If it's HTML (from a rich editor), it might already have tags
  if (post.value.body.includes('<p>')) return post.value.body
  return post.value.body.split('\n').map(p => p.trim() ? `<p>${p}</p>` : '').join('')
})

const formatDate = (dateStr) => {
  if (!dateStr) return 'Recently'
  return new Date(dateStr).toLocaleDateString('en-IN', {
    day: 'numeric',
    month: 'short',
    year: 'numeric'
  })
}
</script>

<style scoped>
.article-container {
  max-width: 800px;
}

.breadcrumb {
  font-size: 13px;
  color: var(--color-text-muted);
  margin-bottom: 40px;
}

.breadcrumb a {
  color: var(--color-text-muted);
  text-decoration: none;
}

.breadcrumb a:hover {
  color: var(--color-primary);
}

.separator {
  margin: 0 8px;
  color: var(--color-border);
}

.current {
  color: var(--color-text-dark);
  font-weight: 500;
}

.article-header {
  margin-bottom: 40px;
  text-align: center;
}

.artist-meta {
  font-size: 14px;
  color: var(--color-primary);
  text-transform: uppercase;
  letter-spacing: 1px;
  margin-bottom: 16px;
}

.article-title {
  font-size: 48px;
  line-height: 1.1;
  margin-bottom: 24px;
}

.article-date {
  font-size: 14px;
  color: var(--color-text-muted);
}

.hero-image {
  width: 100%;
  height: 400px;
  background-size: cover;
  background-position: center;
  border-radius: 12px;
  margin-bottom: 60px;
}

.article-body {
  font-size: 18px;
  line-height: 1.8;
  color: var(--color-text-body);
}

.lead-paragraph {
  font-size: 22px;
  line-height: 1.6;
  font-family: var(--font-heading);
  color: var(--color-text-dark);
  margin-bottom: 40px;
}

.article-body p {
  margin-bottom: 30px;
}

.article-body h2 {
  font-size: 28px;
  margin-top: 60px;
  margin-bottom: 24px;
}

.article-body blockquote {
  margin: 60px 0;
  padding: 0 40px;
  font-size: 24px;
  line-height: 1.5;
  font-family: var(--font-heading);
  font-style: italic;
  color: var(--color-primary);
  border-left: 4px solid var(--color-primary);
}

.inline-image {
  width: 100%;
  border-radius: 8px;
  margin: 40px 0;
}
</style>
