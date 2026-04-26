<template>
  <div>
    <BuyerNavbar />
    
    <div v-if="catalogue" class="catalogue-wrapper">
      <!-- Hero Header -->
      <div class="hero-section" :style="{ backgroundImage: `url(${resolveURL(catalogue.cover_photo_url)})` }">
        <div class="hero-overlay">
          <div class="hero-content">
            <div class="meta-date">{{ catalogue.published_at ? new Date(catalogue.published_at).toLocaleDateString('en-IN', { year:'numeric', month:'long', day:'numeric' }) : '' }}</div>
            <h1 class="hero-title">{{ catalogue.title }}</h1>
            <div class="catalogue-categories" v-if="catalogue.category">
              <span v-for="cat in catalogue.category.split(',').filter(c => c.trim())" :key="cat" class="cat-pill">
                {{ cat.trim() }}
              </span>
            </div>
            <div class="artist-badge">
              <div class="artist-avatar" :style="{ backgroundImage: `url(${resolveURL(catalogue.artist_profile_image)})` }"></div>
              <span>By <strong>{{ catalogue.artist_name }}</strong></span>
            </div>
          </div>
        </div>
      </div>

      <!-- Main Content Container -->
      <div class="page-container">
        
        <!-- 1. Artist Note & Stories Top Section -->
        <div class="story-details" style="margin-bottom: 40px;">
          <div class="artist-note-section" v-if="catalogue.artist_note">
            <div class="note-box">
              <h3 class="note-title">Artist's Note</h3>
              <p class="note-text">"{{ catalogue.artist_note }}"</p>
            </div>
          </div>
        </div>

        <!-- Stories List -->
        <div v-if="catalogue.stories?.length" class="catalogue-stories-top">
          <div class="stories-container">
            <div v-for="story in catalogue.stories" :key="story.id" class="story-item card" style="margin-bottom: 40px;">
              <div class="story-header" style="padding: 20px 30px; border-bottom: 1px solid #f5f0eb;">
                <h3 class="story-title-display" style="margin:0; font-family: 'Playfair Display', serif; font-size: 24px;">{{ story.title }}</h3>
              </div>
              <div v-if="story.cover_image_url" class="story-media" :style="{ backgroundImage: `url(${resolveURL(story.cover_image_url)})` }">
                <button class="story-like-btn" @click="toggleStoryLike(story)" :class="{ liked: story.has_liked }">
                  {{ story.has_liked ? '❤' : '♡' }}
                </button>
              </div>
              <div class="story-content" style="padding: 32px;">
                <div class="story-body html-content" v-html="truncateHTML(story.body, 180)"></div>
                <div style="margin-top: 16px; display: flex; justify-content: space-between; align-items: center;">
                  <RouterLink :to="`/buyer/insight/${story.id}`" class="read-full-link">Read Full Story →</RouterLink>
                  <div class="story-footer" style="font-size: 13px; color: #888; font-weight: 600;">{{ story.likes_count }} people loved this</div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <div style="margin-bottom: 32px; display:flex; gap:12px; align-items:center;">
          <button class="like-btn" @click="toggleLike" :class="{ liked: isLiked }">
            {{ isLiked ? '❤ Liked' : '♡ Like this Catalogue' }}
          </button>
          <span style="font-size:13px; color:#888;">{{ catalogue.stats?.total_views || 0 }} views · {{ catalogue.stats?.total_likes || 0 }} likes</span>
        </div>

        <div class="divider"></div>

        <!-- 2. Products Next -->
        <div class="catalogue-products" style="margin-bottom: 80px;">
          <div class="products-header">
            <h2 class="section-title">Pieces in this Catalogue</h2>
            <div class="catalogue-search">
              <input 
                type="text" 
                v-model="productSearch" 
                placeholder="Search products in this catalogue..." 
                class="inner-search-input"
              />
            </div>
          </div>
          
          <div class="products-grid" v-if="filteredProducts.length > 0">
            <div v-for="product in filteredProducts" :key="product.id" class="product-card">
              <RouterLink :to="`/buyer/product/${product.id}`" style="display: block;">
                <div class="product-image" :style="{ backgroundImage: `url(${resolveURL(product.image)})` }"></div>
              </RouterLink>
              <div class="product-info">
                <div class="product-artist">{{ product.artist_name }}</div>
                <RouterLink :to="`/buyer/product/${product.id}`" style="text-decoration:none; color:inherit;">
                  <div class="product-title">{{ product.title }}</div>
                </RouterLink>
                <div class="product-footer">
                  <span class="product-price">₹{{ product.price.toLocaleString('en-IN') }}</span>
                  <button class="add-cart-btn" @click="handleAddToCart(product)" :disabled="addingId === product.id || !product.in_stock">
                    {{ addingId === product.id ? '...' : (product.in_stock ? 'Add to Cart' : 'Sold Out') }}
                  </button>
                </div>
              </div>
            </div>
          </div>
          <div v-else class="no-products-found">
            No products match your search within this catalogue.
          </div>
        </div>

        <div class="divider"></div>

        <!-- 3. Community Thoughts Last -->
        <div class="reviews-section">
          <h2 class="section-title">Community Thoughts</h2>
          
          <div v-if="authStore.user?.role === 'buyer'" class="review-form card">
            <h4>Leave a Thought</h4>
            <textarea v-model="newReviewBody" placeholder="What do you think of this collection?" rows="3"></textarea>
            <div class="form-actions">
              <button class="btn-primary" @click="submitReview" :disabled="submittingReview">Post Comment</button>
            </div>
          </div>

          <div class="reviews-list">
            <div v-for="rev in reviews" :key="rev.id" class="review-item">
              <div class="comment-avatar" :style="rev.buyer_avatar ? { backgroundImage: `url(${resolveURL(rev.buyer_avatar)})` } : { background: '#fdf2ed' }">
                <span v-if="!rev.buyer_avatar">{{ rev.buyer_name?.charAt(0) }}</span>
              </div>
              <div class="comment-content-wrap">
                <div class="review-header">
                  <strong>{{ rev.buyer_name }}</strong>
                  <span>{{ new Date(rev.created_at).toLocaleDateString() }}</span>
                </div>
                <p>{{ rev.body }}</p>
              </div>
            </div>
            <div v-if="!reviews.length" class="no-reviews">
              No thoughts shared yet. Be the first!
            </div>
          </div>
        </div>
      </div>
    </div>
    
    <div v-else class="loading-state">
      Loading catalogue...
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import BuyerNavbar from '../../components/BuyerNavbar.vue'
import { getCatalogue, likeCatalogue, unlikeCatalogue, checkLike } from '../../api/catalogue.js'
import { getReviews, createReview, likePost, unlikePost } from '../../api/social.js'
import { useCartStore } from '../../stores/cart.js'
import { useAuthStore } from '../../stores/auth.js'

const route = useRoute()
const cartStore = useCartStore()
const authStore = useAuthStore()

const catalogue = ref(null)
const isLiked = ref(false)
const addingId = ref(null)
const productSearch = ref('')

const reviews = ref([])
const newReviewBody = ref('')
const submittingReview = ref(false)

const filteredProducts = computed(() => {
  if (!catalogue.value) return []
  if (!productSearch.value) return catalogue.value.products
  const query = productSearch.value.toLowerCase()
  return catalogue.value.products.filter(p => 
    p.title.toLowerCase().includes(query)
  )
})

onMounted(async () => {
  const id = route.params.id
  catalogue.value = await getCatalogue(id)
  
  // Load reviews
  try {
    reviews.value = await getReviews('catalogue', id)
  } catch (e) { console.error(e) }

  // Only check like status if logged in as buyer
  if (authStore.user?.role === 'buyer') {
    try {
      const res = await checkLike(id)
      isLiked.value = res.liked
    } catch { /* not logged in */ }
  }
})

async function toggleLike() {
  if (!authStore.user) return alert('Please log in to like catalogues.')
  try {
    if (isLiked.value) {
      await unlikeCatalogue(catalogue.value.id)
      isLiked.value = false
      if (catalogue.value.stats) catalogue.value.stats.total_likes--
    } else {
      await likeCatalogue(catalogue.value.id)
      isLiked.value = true
      if (catalogue.value.stats) catalogue.value.stats.total_likes++
    }
  } catch (e) { alert(e.message) }
}

async function handleAddToCart(product) {
  if (!authStore.user || authStore.user.role !== 'buyer') {
    alert(authStore.user?.role === 'artist' 
      ? 'Artists cannot purchase items. Please log in with a Buyer account.' 
      : 'Please log in to add this piece to your cart.')
    return
  }
  addingId.value = product.id
  try { await cartStore.addItem(product.id) }
  catch (e) { alert(e.message) }
  finally { addingId.value = null }
}

async function toggleStoryLike(story) {
  if (!authStore.user) return alert('Please log in to like stories.')
  try {
    if (story.has_liked) {
      await unlikePost(story.id)
      story.has_liked = false
      story.likes_count--
    } else {
      await likePost(story.id)
      story.has_liked = true
      story.likes_count++
    }
  } catch (e) { alert(e.message) }
}

async function submitReview() {
  if (!newReviewBody.value.trim()) return
  submittingReview.value = true
  try {
    const rev = await createReview({
      target_type: 'catalogue',
      target_id: catalogue.value.id,
      body: newReviewBody.value,
      rating: 5 // Default for comments
    })
    reviews.value.unshift(rev)
    newReviewBody.value = ''
  } catch (e) {
    alert(e.message)
  } finally {
    submittingReview.value = false
  }
}

function resolveURL(url) {
  if (!url) return ''
  if (url.startsWith('http')) return url
  return `http://127.0.0.1:5000${url.startsWith('/') ? '' : '/'}${url}`
}

function truncateHTML(html, limit) {
  if (!html) return ''
  const doc = new DOMParser().parseFromString(html, 'text/html')
  const text = doc.body.textContent || ""
  if (text.length <= limit) return text
  return text.substring(0, limit) + '...'
}
</script>

<style scoped>
.catalogue-wrapper {
  font-family: 'DM Sans', sans-serif;
}

.hero-section {
  width: 100%;
  height: 480px;
  background-size: cover;
  background-position: center;
  position: relative;
}

.hero-overlay {
  position: absolute;
  inset: 0;
  background: linear-gradient(to top, rgba(0,0,0,0.85) 0%, rgba(0,0,0,0.3) 50%, rgba(0,0,0,0.1) 100%);
  display: flex;
  align-items: flex-end;
  padding: 60px 80px;
}

.hero-content {
  color: white;
  max-width: 800px;
}

.meta-date {
  font-size: 13px;
  text-transform: uppercase;
  letter-spacing: 1px;
  color: #e0e0e0;
  margin-bottom: 12px;
}

.hero-title {
  font-family: 'Playfair Display', serif;
  font-size: 48px;
  font-weight: 600;
  line-height: 1.2;
  margin-bottom: 12px;
}

.catalogue-categories {
  display: flex;
  gap: 8px;
  margin-bottom: 24px;
}

.cat-pill {
  background: rgba(255,255,255,0.15);
  backdrop-filter: blur(8px);
  padding: 4px 12px;
  border-radius: 20px;
  font-size: 13px;
  font-weight: 600;
  color: #fff;
  border: 1px solid rgba(255,255,255,0.2);
  text-transform: capitalize;
}

.artist-badge {
  display: flex;
  align-items: center;
  gap: 12px;
}

.artist-avatar {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background-size: cover;
  background-position: center;
  border: 2px solid rgba(255,255,255,0.2);
}

.artist-badge span {
  font-size: 15px;
  color: #eeeeee;
}

.artist-badge strong {
  color: white;
  font-weight: 600;
}

.page-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 60px 40px;
}

/* Story Details Layout */
.story-details {
  display: flex;
  margin-bottom: 60px;
}

/* Stories Vertical Scroll Styles */
.catalogue-chronicles {
  margin-bottom: 60px;
}

.stories-container {
  display: flex;
  flex-direction: column;
  gap: 40px;
  max-width: 800px; /* Increased for better reading */
}

.story-item {
  background: white;
  border-radius: 12px;
  overflow: hidden;
  border: 1px solid #e8e0d8;
  box-shadow: 0 4px 20px rgba(0,0,0,0.03);
}

.story-media {
  aspect-ratio: 16 / 9; /* Landscape aspect ratio */
  background-size: cover;
  background-position: center;
  position: relative;
  max-height: 400px;
}

.story-like-btn {
  position: absolute;
  bottom: 20px;
  right: 20px;
  background: rgba(255,255,255,0.2);
  backdrop-filter: blur(8px);
  border: 1px solid rgba(255,255,255,0.4);
  width: 44px;
  height: 44px;
  border-radius: 50%;
  font-size: 20px;
  color: white;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s;
}

.story-like-btn.liked {
  background: white;
  color: #ff4d4d;
  border-color: white;
}

.html-content :deep(p) {
  margin-bottom: 1rem;
}

.html-content :deep(ol), .html-content :deep(ul) {
  margin-left: 20px;
  margin-bottom: 1rem;
}

.html-content :deep(blockquote) {
  border-left: 3px solid #C4622D;
  padding-left: 16px;
  font-style: italic;
  color: #666;
  margin: 1.5rem 0;
}

.philosophy-section {
  flex: 1.5;
}

.artist-note-section {
  flex: 1;
}

.empty-story-space {
  flex: 1.5;
}

.story-placeholder {
  background: #fdfaf8;
  border: 1px dashed #e8e0d8;
  border-radius: 12px;
  padding: 40px;
  text-align: center;
  color: #888;
  font-style: italic;
  display: flex;
  align-items: center;
  justify-content: center;
}

.section-title {
  font-family: 'Playfair Display', serif;
  font-size: 28px;
  font-weight: 600;
  color: #000;
  margin-bottom: 24px;
}

.body-text {
  font-size: 16px;
  line-height: 1.8;
  color: #444;
}

.note-box {
  background: #fdfaf8;
  border-left: 4px solid #C4622D;
  padding: 32px;
  border-radius: 0 8px 8px 0;
}

.note-title {
  font-family: 'Playfair Display', serif;
  font-size: 18px;
  color: #C4622D;
  margin-bottom: 16px;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.note-text {
  font-family: 'Playfair Display', serif;
  font-size: 18px;
  line-height: 1.7;
  color: #333;
  font-style: italic;
}

.divider {
  height: 1px;
  background: #e8e0d8;
  margin: 0 0 60px 0;
}

.products-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 32px;
}

.products-header .section-title {
  margin-bottom: 0;
}

.inner-search-input {
  font-family: 'DM Sans', sans-serif;
  padding: 10px 20px;
  border: 1px solid #e8e0d8;
  border-radius: 8px;
  width: 300px;
  outline: none;
  transition: border-color 0.2s;
  background: #fdfaf8;
}

.inner-search-input:focus {
  border-color: #C4622D;
  background: #fff;
}

.no-products-found {
  text-align: center;
  padding: 60px;
  color: #888;
  font-style: italic;
  font-family: 'DM Sans', sans-serif;
  border: 1px dashed #e8e0d8;
  border-radius: 12px;
}

/* Products Layout */
.products-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 32px;
}

.product-card {
  background: #ffffff;
  border-radius: 8px;
  overflow: hidden;
  border: 1px solid #e8e0d8;
  transition: box-shadow 0.2s;
  display: flex;
  flex-direction: column;
}

.product-card:hover {
  box-shadow: 0 6px 16px rgba(0, 0, 0, 0.06);
}

.product-image {
  height: 240px;
  background-size: cover;
  background-position: center;
}

.product-info {
  padding: 20px;
  flex: 1;
  display: flex;
  flex-direction: column;
}

.product-artist {
  font-size: 11px;
  color: #888;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  margin-bottom: 4px;
}

.product-title {
  font-family: 'Playfair Display', serif;
  font-size: 18px;
  font-weight: 600;
  color: #000;
  margin-bottom: 16px;
  flex: 1;
}

.product-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: auto;
}

.product-price {
  font-family: 'Playfair Display', serif;
  font-size: 18px;
  font-weight: 600;
  color: #000;
}

.add-cart-btn {
  font-family: 'DM Sans', sans-serif;
  background: transparent;
  color: #C4622D;
  border: 1px solid #C4622D;
  padding: 8px 16px;
  border-radius: 4px;
  font-size: 13px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
}

.add-cart-btn:hover {
  background: #C4622D;
  color: white;
}

.like-btn {
  font-family: 'DM Sans', sans-serif;
  background: white;
  color: #888;
  border: 1px solid #e8e0d8;
  padding: 10px 20px;
  border-radius: 24px;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
}

.like-btn:hover {
  border-color: #C4622D;
  color: #C4622D;
}

.like-btn.liked {
  background: #fdf2ed;
  border-color: #C4622D;
  color: #C4622D;
}

.loading-state {
  text-align: center;
  padding: 100px 0;
  font-family: 'DM Sans', sans-serif;
  font-size: 18px;
  color: #888;
}

/* Reviews Styling */
.reviews-section {
  margin-bottom: 60px;
}

.review-form {
  background: white;
  padding: 24px;
  border: 1px solid #e8e0d8;
  border-radius: 8px;
  margin-bottom: 32px;
}

.review-form h4 {
  margin: 0 0 16px 0;
  font-family: 'Playfair Display', serif;
}

.review-form textarea {
  width: 100%;
  padding: 12px;
  border: 1px solid #e8e0d8;
  border-radius: 4px;
  font-family: 'DM Sans', sans-serif;
  margin-bottom: 12px;
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
  padding: 10px 20px;
  border-radius: 4px;
  font-weight: 600;
  cursor: pointer;
}

.reviews-list {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.review-item {
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

.review-header {
  display: flex;
  justify-content: space-between;
  margin-bottom: 8px;
}

.review-header strong {
  font-size: 14px;
  color: #333;
}

.review-header span {
  font-size: 12px;
  color: #888;
}

.review-item p {
  font-size: 14px;
  line-height: 1.5;
  color: #555;
  margin: 0;
}

.no-reviews {
  text-align: center;
  padding: 40px;
  color: #888;
  font-style: italic;
}

.read-full-link {
  color: #C4622D;
  text-decoration: none;
  font-weight: 700;
  font-size: 14px;
  transition: all 0.2s;
  border-bottom: 2px solid transparent;
}

.read-full-link:hover {
  border-bottom-color: #C4622D;
  padding-bottom: 2px;
}
</style>
