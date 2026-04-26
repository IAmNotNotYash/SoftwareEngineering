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

        <div v-if="post.cover_image_url" class="hero-image" :style="{ backgroundImage: `url(${post.cover_image_url})` }">
          <button class="article-like-btn" @click="toggleLike" :class="{ liked: post.has_liked }">
            {{ post.has_liked ? '❤' : '♡' }}
          </button>
        </div>

        <div class="article-body">
          <div class="body-text" v-html="formattedBody"></div>
          <div class="article-footer-stats">
            {{ post.likes_count }} people loved this story
          </div>
        </div>
      </article>

      <div class="divider"></div>

      <!-- Comments Section -->
      <div class="comments-section">
        <h2 class="section-title">Community Thoughts</h2>
        
        <div v-if="authStore.user?.role === 'buyer'" class="comment-form card">
          <h4>Leave a Thought</h4>
          <textarea v-model="newCommentBody" placeholder="What do you think of this story?" rows="3"></textarea>
          <div class="form-actions">
            <button class="btn-primary" @click="submitComment" :disabled="submittingComment">Post Comment</button>
          </div>
        </div>

        <div class="comments-list">
          <div v-for="rev in reviews" :key="rev.id" class="comment-item">
            <div class="comment-avatar" :style="rev.buyer_avatar ? { backgroundImage: `url(${resolveURL(rev.buyer_avatar)})` } : { background: '#fdf2ed' }">
              <span v-if="!rev.buyer_avatar">{{ rev.buyer_name?.charAt(0) }}</span>
            </div>
            <div class="comment-content-wrap">
              <div class="comment-header">
                <strong>{{ rev.buyer_name }}</strong>
                <span>{{ new Date(rev.created_at).toLocaleDateString() }}</span>
              </div>
              <p>{{ rev.body }}</p>
            </div>
          </div>
          <div v-if="!reviews.length" class="no-comments">
            No thoughts shared yet. Be the first!
          </div>
        </div>
      </div>
    </div>
    
    <div class="page-container loading-container" v-else-if="loading">
      <p>Loading the artisan's journey...</p>
    </div>
    
    <div class="page-container error-container" v-else>
      <div v-if="!loading">
        <p>Could not find story ID: <code style="background: #eee; padding: 2px 4px; border-radius: 4px;">{{ route.params.id }}</code></p>
        <p>It might have been moved or archived.</p>
        <RouterLink to="/" class="back-link">Back to Discovery</RouterLink>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRoute } from 'vue-router'
import BuyerNavbar from '../../components/BuyerNavbar.vue'
import { getPost, likePost, unlikePost, getReviews, createReview } from '../../api/social.js'
import { useAuthStore } from '../../stores/auth'

const route = useRoute()
const authStore = useAuthStore()
const post = ref(null)
const loading = ref(true)

const reviews = ref([])
const newCommentBody = ref('')
const submittingComment = ref(false)

onMounted(async () => {
  const id = route.params.id
  if (!id) return
  
  loading.value = true
  try {
    console.log("Kala Insight: Fetching story ID", id)
    // 1. Try to get the post. If it fails due to auth, try as guest.
    try {
      post.value = await getPost(id)
    } catch (err) {
      if (err.message?.includes('401') || err.message?.includes('token')) {
        console.warn("Kala: Token expired, trying as guest...")
        sessionStorage.removeItem('token')
        post.value = await getPost(id)
      } else { throw err }
    }

    // 2. Load comments (Don't crash if they fail)
    try {
      reviews.value = await getReviews('post', id)
    } catch (err) {
      console.warn("Kala: Comments unavailable for guest", err)
      reviews.value = []
    }
  } catch (err) {
    console.error("Kala Critical: Story could not be fetched", err)
  } finally {
    loading.value = false
  }
})

async function toggleLike() {
  if (!authStore.user) return alert('Please log in to like stories.')
  try {
    if (post.value.has_liked) {
      await unlikePost(post.value.id)
      post.value.has_liked = false
      post.value.likes_count--
    } else {
      await likePost(post.value.id)
      post.value.has_liked = true
      post.value.likes_count++
    }
  } catch (e) { alert(e.message) }
}

async function submitComment() {
  if (!newCommentBody.value.trim()) return
  submittingComment.value = true
  try {
    const rev = await createReview({
      target_type: 'post',
      target_id: post.value.id,
      body: newCommentBody.value,
      rating: 5
    })
    reviews.value.unshift(rev)
    newCommentBody.value = ''
  } catch (e) {
    alert(e.message)
  } finally {
    submittingComment.value = false
  }
}

const formattedBody = computed(() => {
  if (!post.value?.body) return ''
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

function resolveURL(url) {
  if (!url) return ''
  if (url.startsWith('http')) return url
  return `http://127.0.0.1:5000${url.startsWith('/') ? '' : '/'}${url}`
}
</script>

<style scoped>
.page-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 60px 40px;
  font-family: 'DM Sans', sans-serif;
}

.article-container {
  max-width: 800px;
}

.breadcrumb {
  font-size: 13px;
  color: #888;
  margin-bottom: 40px;
}

.breadcrumb a {
  color: #888;
  text-decoration: none;
}

.breadcrumb a:hover {
  color: #C4622D;
}

.separator {
  margin: 0 8px;
  color: #e8e0d8;
}

.current {
  color: #000;
  font-weight: 500;
}

.article-header {
  margin-bottom: 40px;
  text-align: center;
}

.artist-meta {
  font-size: 14px;
  color: #C4622D;
  text-transform: uppercase;
  letter-spacing: 1px;
  margin-bottom: 16px;
}

.article-title {
  font-family: 'Playfair Display', serif;
  font-size: 48px;
  line-height: 1.1;
  margin-bottom: 24px;
  color: #000;
}

.article-date {
  font-size: 14px;
  color: #888;
}

.hero-image {
  width: 100%;
  height: 480px;
  background-size: cover;
  background-position: center;
  border-radius: 12px;
  margin-bottom: 60px;
  position: relative;
}

.article-like-btn {
  position: absolute;
  bottom: 24px;
  right: 24px;
  background: rgba(255, 255, 255, 0.2);
  backdrop-filter: blur(12px);
  border: 1px solid rgba(255, 255, 255, 0.4);
  width: 56px;
  height: 56px;
  border-radius: 50%;
  font-size: 24px;
  color: white;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s;
}

.article-like-btn.liked {
  background: white;
  color: #ff4d4d;
  border-color: white;
}

.article-body {
  font-size: 18px;
  line-height: 1.8;
  color: #333;
}

.article-body :deep(p) {
  margin-bottom: 30px;
}

.article-footer-stats {
  margin-top: 40px;
  padding-top: 20px;
  border-top: 1px solid #f5f0eb;
  font-size: 14px;
  color: #888;
  font-weight: 600;
}

.divider {
  height: 1px;
  background: #e8e0d8;
  margin: 60px 0;
}

.section-title {
  font-family: 'Playfair Display', serif;
  font-size: 28px;
  font-weight: 600;
  color: #000;
  margin-bottom: 32px;
}

/* Comments Section Styles */
.comment-form {
  background: #fdfaf8;
  padding: 24px;
  border: 1px solid #e8e0d8;
  border-radius: 8px;
  margin-bottom: 40px;
}

.comment-form h4 {
  margin: 0 0 16px 0;
  font-family: 'Playfair Display', serif;
}

.comment-form textarea {
  width: 100%;
  padding: 12px;
  border: 1px solid #e8e0d8;
  border-radius: 4px;
  font-family: 'DM Sans', sans-serif;
  margin-bottom: 16px;
  resize: vertical;
}

.form-actions {
  display: flex;
  justify-content: flex-end;
}

.btn-primary {
  background: #C4622D;
  color: white;
  border: none;
  padding: 12px 24px;
  border-radius: 4px;
  font-weight: 600;
  cursor: pointer;
  transition: background 0.2s;
}

.btn-primary:hover {
  background: #a95224;
}

.comments-list {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.comment-item {
  padding-bottom: 24px;
  border-bottom: 1px solid #f5f0eb;
  display: flex;
  gap: 16px;
}

.comment-avatar {
  width: 44px;
  height: 44px;
  border-radius: 50%;
  background-size: cover;
  background-position: center;
  flex-shrink: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  font-family: 'Playfair Display', serif;
  font-weight: 700;
  color: #C4622D;
  border: 1px solid #f5f0eb;
}

.comment-content-wrap {
  flex: 1;
}

.comment-header {
  display: flex;
  justify-content: space-between;
  margin-bottom: 8px;
}

.comment-header strong {
  font-size: 15px;
  color: #000;
}

.comment-header span {
  font-size: 12px;
  color: #888;
}

.comment-item p {
  font-size: 15px;
  line-height: 1.6;
  color: #444;
  margin: 0;
}

.no-comments {
  text-align: center;
  padding: 60px;
  color: #888;
  font-style: italic;
  border: 1px dashed #e8e0d8;
  border-radius: 12px;
}

.loading-container, .error-container {
  text-align: center;
  padding: 100px 0;
  color: #888;
}

.back-link {
  display: inline-block;
  margin-top: 20px;
  color: #C4622D;
  text-decoration: none;
  font-weight: 600;
}
</style>
