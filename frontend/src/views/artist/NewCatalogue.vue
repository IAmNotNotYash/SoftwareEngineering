<template>
  <div class="builder-page">
    <ArtistNavbar />
    
    <div v-if="notification" class="notification-banner">
      {{ notification }}
      <button @click="notification = null" class="close-notify">×</button>
    </div>

    <main class="page-container">
      <div class="page-header">
        <div>
          <router-link to="/artist/catalogues" class="back-link">← Back to Catalogues</router-link>
          <h1 class="page-title">Catalogue Builder</h1>
          <p class="subtitle">Design and launch a highly aesthetic product catalogue.</p>
        </div>
      </div>

      <div class="builder-layout">
        <!-- Sidebar Navigation -->
        <aside class="sidebar-steps">
          <div 
            v-for="(step, idx) in steps" 
            :key="idx" 
            class="step-item"
            :class="{ 
              active: currentStep === idx, 
              completed: catalogueId && isStepComplete(idx),
              unlocked: catalogueId || currentStep >= idx
            }"
            @click="gotoStep(idx)"
          >
            <div class="step-indicator">
              <span v-if="isStepComplete(idx)">✓</span>
              <span v-else>-</span>
            </div>
            <span class="step-label">{{ step }}</span>
          </div>
        </aside>

        <!-- Builder Content Panels -->
        <section class="builder-content">
          
          <!-- Step 1: Details -->
          <div class="panel card" v-if="currentStep === 0">
            <h2>Catalogue Details</h2>
            <div class="form-group">
              <label>Catalogue Title</label>
              <input v-model="form.title" class="input-field" placeholder="e.g. Earth Tone Spring Collection" />
            </div>
            <div class="form-group">
              <label>Brand Narrative / Tagline</label>
              <textarea v-model="form.narrative" class="input-field" rows="3" placeholder="Set the mood for this catalogue..."></textarea>
            </div>
          </div>

          <!-- Step 2: Visuals -->
          <div class="panel card" v-if="currentStep === 1">
            <h2>Cover Visuals</h2>
            <p class="field-hint">Upload a stunning full-bleed cover photo for your catalogue landing page.</p>
            
            <div 
              class="cover-upload-zone" 
              :class="{ 'has-image': form.coverPhoto }"
              :style="form.coverPhoto ? { backgroundImage: `url(${form.coverPhoto})` } : {}"
              @click="!form.coverPhoto ? $refs.fileInput.click() : null"
            >
              <input type="file" ref="fileInput" hidden accept="image/*" @change="handleCoverUpload" />
              
              <div class="upload-prompt" v-if="!form.coverPhoto">
                <span class="upload-icon">📸</span>
                <p>Upload High-Res Cover Image</p>
                <small>Recommended: 1920x1080</small>
              </div>
              
              <button class="remove-btn btn secondary-btn small-btn" v-if="form.coverPhoto" @click.stop="form.coverPhoto = null">
                Change Cover
              </button>
            </div>
            
            <div class="form-group" style="margin-top:24px">
              <label>Theme Palette</label>
              <div class="palette-options">
                <div class="palette-pip" style="background:#fdf2ed" :class="{active: form.theme === 'warm'}" @click="form.theme = 'warm'">Warm</div>
                <div class="palette-pip" style="background:#f4f0ea" :class="{active: form.theme === 'earth'}" @click="form.theme = 'earth'">Earth</div>
                <div class="palette-pip" style="background:#eaf2f8" :class="{active: form.theme === 'cool'}" @click="form.theme = 'cool'">Cool</div>
                <div class="palette-pip" style="background:#1a1a1a; color:#fff" :class="{active: form.theme === 'dark'}" @click="form.theme = 'dark'">Dark</div>
              </div>
            </div>
          </div>

          <!-- Step 3: Stories (Blog Style) -->
          <div class="panel card" v-if="currentStep === 2">
            <div class="panel-header-inline">
              <div>
                <h2>Catalogue Blog</h2>
                <p class="field-hint">Create multiple blog entries to tell the story of this collection. Each entry can have its own title, cover, and rich text content.</p>
              </div>
              <button class="btn primary-btn small-btn" @click="addNewBlogEntry">+ Add New Entry</button>
            </div>
            
            <div class="blog-entries-list" v-if="form.stories.length > 0">
              <div 
                v-for="(entry, eidx) in form.stories" 
                :key="entry.localId" 
                class="blog-entry-card"
              >
                <!-- Card View (Comic Style) -->
                <div v-if="!entry.isEditing" class="entry-display comic-panel">
                  <div class="entry-cover-huge" :style="{ backgroundImage: `url(${entry.preview || '/placeholder-img.jpg'})` }">
                    <!-- Top Narrative Box -->
                    <div class="narrative-box top">
                      <h3 class="comic-title">{{ entry.title || 'Untitled Entry' }}</h3>
                      
                      <!-- Quick Edit Burst -->
                      <button class="mini-zap-btn edit" @click="editEntry(eidx)" title="Edit Entry">✎</button>
                    </div>
                    
                    <!-- Status bubble -->
                    <div class="zap-badge" :class="{ live: entry.is_published }">
                      {{ entry.is_published ? 'LIVE!' : 'DRAFT' }}
                    </div>

                    <!-- Bottom Overlay (Excerpt) -->
                    <div class="narrative-box bottom" v-if="entry.body">
                       <p class="comic-text" v-html="stripHtml(entry.body)"></p>
                       <button class="mini-zap-btn delete" @click="removeEntry(eidx)" title="Delete Entry">×</button>
                    </div>

                  </div>
                </div>

                <!-- Edit View -->
                <div v-else class="entry-editor">
                  <div class="editor-row">
                    <div class="editor-main">
                      <div class="form-group">
                        <label>Entry Title</label>
                        <input v-model="entry.title" class="input-field" placeholder="Entry Title..." />
                      </div>
                      <div class="form-group quill-wrap">
                        <label>Content</label>
                        <QuillEditor 
                          v-model:content="entry.body" 
                          contentType="html" 
                          theme="snow" 
                          toolbar="essential"
                          placeholder="Tell your story..."
                        />
                      </div>
                    </div>
                    <div class="editor-side">
                      <div class="form-group">
                        <label>Cover Image</label>
                        <div class="mini-upload" :style="{ backgroundImage: `url(${entry.preview})` }" @click="triggerEntryImageUpload(eidx)">
                           <input type="file" :ref="el => entryImageRefs[eidx] = el" hidden accept="image/*" @change="e => handleEntryImageUpload(e, eidx)" />
                           <span v-if="!entry.preview">Add Image</span>
                        </div>
                      </div>
                      <div class="form-group">
                        <label class="toggle-label">
                          <input type="checkbox" v-model="entry.is_published" />
                          <span>Go Live</span>
                        </label>
                      </div>
                    </div>
                  </div>
                  <div class="editor-footer">
                    <button class="btn secondary-btn small-btn" @click="entry.isEditing = false">Cancel</button>
                    <button class="btn primary-btn small-btn" @click="saveEntry(eidx)">{{ entry.id ? 'Update Entry' : 'Save Entry' }}</button>
                  </div>
                </div>
              </div>
            </div>

            <div v-else class="empty-blog-state">
              <div class="empty-icon">📝</div>
              <p>No blog entries yet. Start narrating your collection's soul.</p>
              <button class="btn secondary-btn small-btn" @click="addNewBlogEntry">Create First Entry</button>
            </div>
          </div>

          <!-- Step 4: Products -->
          <div class="panel card" v-if="currentStep === 3">
            <h2>Catalogue Products</h2>
            <p class="field-hint">Create and manage products exclusively for this catalogue.</p>
            
            <div class="product-grid">
              <!-- Add New Product Card -->
              <div class="product-cube add-new" @click="openProductModal()">
                <div class="cube-content">
                  <span class="plus">+</span>
                  <span class="label">ADD NEW</span>
                </div>
              </div>

              <!-- Product list -->
              <div 
                v-for="p in availableProducts" 
                :key="p.id"
                class="product-card-wrap"
              >
                <div class="product-top-bar">
                  <span class="product-name-new">{{ p.name }}</span>
                </div>
                
                <div 
                  class="product-cube"
                  :style="{ backgroundImage: `url(${p.img})` }"
                >
                  <div class="cube-overlay">
                    <div class="cube-actions">
                      <button class="mini-icon-btn" @click="openProductModal(p)" title="Edit Product">✎</button>
                      <button class="mini-icon-btn del" @click="handleProductDelete(p.id, $event)" title="Delete Product">×</button>
                    </div>
                  </div>
                </div>
                
                <div class="product-bottom-bar">
                  <span class="product-price" title="Price">₹{{ formatPrice(p.price) }}</span>
                  <span class="product-orders" title="Number of orders">📦 {{ p.orders || 0 }}</span>
                </div>
              </div>
            </div>
          </div>

          <!-- Step 5: Launch -->
          <div class="panel card" v-if="currentStep === 4">
            <h2>Ready for Launch</h2>
            <p class="field-hint">Your catalogue is ready to be published to your subscribers.</p>
            
            <div class="publish-summary">
              <ul>
                <li><strong>Title:</strong> {{ form.title || 'Untitled' }}</li>
                <li><strong>Products:</strong> {{ availableProducts.length }} linked</li>
                <li><strong>Theme:</strong> {{ form.theme }}</li>
              </ul>
            </div>
            
            <div class="form-group" style="margin-top:24px">
              <label>Launch Intent</label>
              <div class="intent-options">
                <button class="intent-btn" :class="{selected: form.intent==='live'}" @click="form.intent='live'">🚀 Live Sale</button>
                <button class="intent-btn" :class="{selected: form.intent==='preview'}" @click="form.intent='preview'">👀 Exclusive Preview</button>
                <button class="intent-btn" :class="{selected: form.intent==='preorder'}" @click="form.intent='preorder'">📦 Pre-Order</button>
              </div>
            </div>
          </div>

          <div class="panel-actions">
            <button class="btn secondary-btn" @click="prevStep" :disabled="currentStep === 0">Previous Step</button>
            <button class="btn primary-btn" @click="nextStep">
              {{ currentStep === steps.length - 1 ? 'Publish Catalogue' : 'Continue' }}
            </button>
          </div>
        </section>
      </div>
    </main>

    <!-- Product Modal -->
    <div class="modal-overlay" v-if="productModal.isOpen" @click.self="productModal.isOpen = false">
      <div class="modal-content product-modal comic-border">
        <h2 class="comic-title">{{ productModal.isEditing ? 'EDIT PRODUCT' : 'NEW PRODUCT' }}</h2>
        
        <div class="modal-body">
          <div class="form-group">
            <label>Title</label>
            <input v-model="productModal.form.title" class="input-field" placeholder="Product name..." />
          </div>
          <div class="editor-row">
            <div class="form-group" style="flex:1">
              <label>Price (₹)</label>
              <input v-model="productModal.form.price" type="number" class="input-field" placeholder="0" />
            </div>
            <div class="form-group" style="flex:1">
              <label>Category</label>
              <select v-model="productModal.form.category" class="input-field">
                <option value="Art">Original Art</option>
                <option value="Print">Fine Art Print</option>
                <option value="Merch">Merchandise</option>
                <option value="Digital">Digital Asset</option>
              </select>
            </div>
          </div>
          <div class="form-group">
            <label>Description</label>
            <textarea v-model="productModal.form.description" class="textarea-field" rows="3" placeholder="Describe your masterpiece..."></textarea>
          </div>
          <div class="form-group">
            <label>Product Image</label>
            <div class="mini-upload" style="height: 150px; width: 100%; border-radius: 8px;" :style="{ backgroundImage: `url(${productModal.form.image_url})` }" @click="triggerProductImageUpload">
               <input type="file" ref="productImageInput" hidden accept="image/*" @change="handleProductImageUpload" />
               <span v-if="!productModal.form.image_url">Click to Upload Image</span>
            </div>
          </div>
        </div>

        <div class="modal-footer">
          <button class="btn secondary-btn" @click="productModal.isOpen = false">Cancel</button>
          <button class="btn primary-btn" @click="saveProduct">
            {{ productModal.isEditing ? 'Save Changes' : 'Add to Inventory' }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import ArtistNavbar from '../../components/ArtistNavbar.vue'
import { useAuthStore } from '../../stores/auth'
import { createCatalogue, updateCatalogue, uploadCatalogueCover, uploadStoryFrame, getCatalogue } from '../../api/catalogue'
import { getProducts, createProduct, updateProduct, deleteProduct as apiDeleteProduct, uploadProductImageFile } from '../../api/products'
import { createPost, updatePost, deletePost } from '../../api/social'
import { QuillEditor } from '@vueup/vue-quill'
import '@vueup/vue-quill/dist/vue-quill.snow.css'
import { v4 as uuidv4 } from 'uuid'

// Load Comic Fonts
const link = document.createElement('link')
link.rel = 'stylesheet'
link.href = 'https://fonts.googleapis.com/css2?family=Bangers&family=Permanent+Marker&display=swap'
document.head.appendChild(link)

const router = useRouter()
const route = useRoute()
const authStore = useAuthStore()
const currentStep = ref(0)
const steps = ['Overview', 'Visuals', 'Stories', 'Products', 'Launch']
const notification = ref(null)
const catalogueId = ref(null)
const isLoading = ref(false)

const showNotification = (msg, type = 'success') => {
  // If you have a types array, you can use it, but for now we'll just set it.
  notification.value = msg
  setTimeout(() => {
    if(notification.value === msg) notification.value = null
  }, 4000)
}

onMounted(async () => {
  const editId = route.params.id
  if (editId) {
    isLoading.value = true
    try {
      const cat = await getCatalogue(editId)
      catalogueId.value = cat.id
      
      // Map data to form
      form.title = cat.title || ''
      form.narrative = cat.narrative || ''
      form.theme = cat.theme || 'earth'
      
      // If your backend stores launch_intent or similar:
      if (cat.launch_intent) form.intent = cat.launch_intent

      // Visuals
      if (cat.cover_photo_url) {
        form.coverPhoto = getFullImageUrl(cat.cover_photo_url)
      }

      // Products
      if (cat.products) {
        form.selectedProducts = cat.products.map(p => p.id)
      }

      // Stories
      if (cat.stories) {
        form.stories = cat.stories.map(s => ({
          localId: s.id,
          id: s.id,
          title: s.title || '',
          body: s.body || '',
          preview: getFullImageUrl(s.cover_image_url),
          is_published: s.is_published,
          isEditing: false
        }))
      }
      if (cat.status) {
        catalogueStatus.value = cat.status
      }

      // Jump to the requested section if specified in the query param
      // e.g. ?section=products → step index 3
      const sectionMap = { overview: 0, visuals: 1, stories: 2, products: 3, launch: 4 }
      const requestedSection = route.query.section
      if (requestedSection && sectionMap[requestedSection] !== undefined) {
        currentStep.value = sectionMap[requestedSection]
      }
    } catch (err) {
      console.error("Failed to load catalogue:", err)
    } finally {
      isLoading.value = false
    }
  }

  // Load available products from inventory
  await loadProducts()
})

const catalogueStatus = ref('draft')

const isStepComplete = (idx) => {
  if (idx === 0) return form.title.trim().length > 0 && form.narrative.trim().length > 0;
  if (idx === 1) return !!form.coverPhoto;
  if (idx === 2) return form.stories && form.stories.length > 0;
  if (idx === 3) return availableProducts.value.length > 0;
  if (idx === 4) return catalogueStatus.value === 'live';
  return false;
}

const getFullImageUrl = (url) => {
  if (!url) return null
  if (url.startsWith('http')) return url
  return `http://localhost:5000${url}`
}

const form = reactive({
  title: '',
  narrative: '',
  coverPhoto: null,
  theme: 'earth',
  stories: [],
  intent: 'live'
})

const availableProducts = ref([])

// Product Modal State
const productImageInput = ref(null)
const productImageFile = ref(null)

const productModal = reactive({
  isOpen: false,
  isEditing: false,
  productId: null,
  form: {
    title: '',
    price: '',
    description: '',
    category: '',
    image_url: '' // Preview URL
  }
})

const loadProducts = async () => {
  if (!catalogueId.value) {
    availableProducts.value = []
    return
  }
  try {
    const res = await getProducts({ catalogue_id: catalogueId.value })
    // Map backend fields to the template's expected structure
    availableProducts.value = res.map(p => ({
      id: p.id,
      name: p.title,
      img: getFullImageUrl(p.image) || 'https://images.unsplash.com/photo-1544816155-12df9643f363?w=300',
      price: p.price,
      orders: p.order_count || 0,
      description: p.description
    }))
  } catch (err) {
    console.error("Failed to load products:", err)
  }
}

const openProductModal = (product = null) => {
  productImageFile.value = null
  if (product) {
    productModal.isEditing = true
    productModal.productId = product.id
    productModal.form = {
      title: product.name,
      price: product.price,
      description: product.description,
      category: 'Art',
      image_url: product.img
    }
  } else {
    productModal.isEditing = false
    productModal.productId = null
    productModal.form = { title: '', price: '', description: '', category: 'Art', image_url: '' }
  }
  productModal.isOpen = true
}

const triggerProductImageUpload = () => {
  if (productImageInput.value) {
    productImageInput.value.click()
  }
}

const handleProductImageUpload = (e) => {
  const file = e.target.files[0]
  if (!file) return
  productImageFile.value = file
  productModal.form.image_url = URL.createObjectURL(file)
}

const saveProduct = async () => {
  try {
    isLoading.value = true
    const payload = { ...productModal.form }
    
    // We do not send image_url in payload if we are uploading a file later
    if (productImageFile.value) {
      delete payload.image_url
    } else if (!productModal.isEditing) {
      // If we don't have a file, try to use the image_url if present
      payload.images = [payload.image_url || '']
    }

    let savedProduct;
    if (productModal.isEditing) {
      savedProduct = await updateProduct(productModal.productId, payload)
    } else {
      payload.catalogue_id = catalogueId.value
      savedProduct = await createProduct(payload)
    }
    
    // Handle image upload if a file was selected
    if (productImageFile.value) {
      const targetId = savedProduct.id || productModal.productId;
      await uploadProductImageFile(targetId, productImageFile.value)
    }

    showNotification(productModal.isEditing ? "Product updated successfully!" : "Product added to your inventory!")
    
    await loadProducts()
    productModal.isOpen = false
  } catch (err) {
    console.error("Failed to save product:", err)
    showNotification("Error saving product: " + err.message, "error")
  } finally {
    isLoading.value = false
  }
}

const handleProductDelete = async (id, e) => {
  e.stopPropagation() // Don't toggle selection
  if (!confirm("Are you sure you want to delete this product from your inventory?")) return
  
  try {
    isLoading.value = true
    await apiDeleteProduct(id)
    await loadProducts()
    showNotification("Product deleted.")
  } catch (err) {
    console.error("Failed to delete product:", err)
    showNotification("Error deleting product", "error")
  } finally {
    isLoading.value = false
  }
}

const handleCoverUpload = async (e) => {
  const file = e.target.files[0]
  if (!file || !catalogueId.value) return

  // Show immediate feedback
  form.coverPhoto = URL.createObjectURL(file)
  
  try {
    const res = await uploadCatalogueCover(catalogueId.value, file)
    form.coverPhoto = res.url // Update with server URL
    notification.value = `Cover visual has been updated for catalogue named "${form.title}"`
    setTimeout(() => notification.value = null, 5000)
  } catch (err) {
    alert("Upload failed: " + err.message)
  }
}

const entryImageRefs = reactive({})

const addNewBlogEntry = () => {
  form.stories.unshift({
    localId: uuidv4(),
    id: null,
    title: '',
    body: '',
    preview: '',
    is_published: false,
    isEditing: true,
    isSaved: false
  })
}

const editEntry = (idx) => {
  form.stories[idx].isEditing = true
}

const triggerEntryImageUpload = (idx) => {
  if (entryImageRefs[idx]) entryImageRefs[idx].click()
}

const handleEntryImageUpload = async (e, idx) => {
  const file = e.target.files[0]
  if (!file || !catalogueId.value) return
  
  const entry = form.stories[idx]
  entry.preview = URL.createObjectURL(file)
  
  try {
    const res = await uploadStoryFrame(catalogueId.value, file)
    entry.preview = res.url
  } catch (err) {
    alert("Image upload failed")
  }
}

const saveEntry = async (idx) => {
  const entry = form.stories[idx]
  if (!entry.title || !entry.body) {
    alert("Please provide both a title and content.")
    return
  }

  try {
    const payload = {
      catalogue_id: catalogueId.value,
      type: 'story',
      title: entry.title,
      body: entry.body,
      cover_image_url: entry.preview,
      is_published: entry.is_published
    }

    if (!entry.id) {
      const res = await createPost(payload)
      entry.id = res.id
      notification.value = "New blog entry created!"
    } else {
      await updatePost(entry.id, payload)
      notification.value = "Blog entry updated!"
    }

    entry.isEditing = false
    entry.isSaved = true
    setTimeout(() => notification.value = null, 3000)
  } catch (err) {
    alert("Failed to save entry: " + err.message)
  }
}

const removeEntry = async (idx) => {
  const entry = form.stories[idx]
  if (entry.id) {
    if (!confirm("Are you sure you want to delete this entry?")) return
    try {
      await deletePost(entry.id)
    } catch (err) {
      alert("Delete failed")
      return
    }
  }
  form.stories.splice(idx, 1)
}

const stripHtml = (html) => {
  const doc = new DOMParser().parseFromString(html, 'text/html')
  const text = doc.body.textContent || ""
  return text.length > 120 ? text.substring(0, 120) + '...' : text
}

const formatPrice = (val) => {
  return new Intl.NumberFormat('en-IN', {
    maximumFractionDigits: 0
  }).format(val || 0)
}


const saveCatalogueDetails = async () => {
  // Validation
  const title = form.title.trim()
  const narrative = form.narrative.trim()
  const wordCount = narrative ? narrative.split(/\s+/).length : 0

  if (title.length < 3) {
    alert("Catalogue title must be at least 3 characters.")
    return false
  }
  if (wordCount < 3) {
    alert("Brand narrative must be at least 3 words.")
    return false
  }

  // API Call
  try {
    const payload = {
      title: title,
      narrative: narrative,
      theme: form.theme,
      launch_intent: form.intent,
      status: 'draft'
    }

    const artistName = authStore.user?.name || 'Artist'
    
    if (!catalogueId.value) {
      const response = await createCatalogue(payload)
      catalogueId.value = response.id
      notification.value = `New Catalogue "${title}" has been generated for Artist ${artistName}`
    } else {
      await updateCatalogue(catalogueId.value, payload)
    }
    
    setTimeout(() => {
      notification.value = null
    }, 5000)
    
    return true
  } catch (err) {
    alert("Failed to save catalogue draft: " + err.message)
    return false
  }
}

const gotoStep = async (idx) => {
  if (currentStep.value === idx) return
  
  if (currentStep.value === 0) {
    const success = await saveCatalogueDetails()
    if (!success) return
  }

  if (catalogueId.value) {
    currentStep.value = idx
  }
}

const nextStep = async () => {
  if (currentStep.value === 0) {
    const success = await saveCatalogueDetails()
    if (!success) return
  }

  // No need for separate save in nextStep as blog entries are saved immediately
  if (currentStep.value === 2) {
    // We already save entries individually
  }

  if (currentStep.value < steps.length - 1) {
    currentStep.value++
  } else {
    // Final publish logic (optional: update status to live)
    if (catalogueId.value) {
      await updateCatalogue(catalogueId.value, { 
        status: 'live',
      })
    }
    alert("Catalogue launched successfully!")
    router.push('/artist/catalogues')
  }
}

const prevStep = () => {
  if (currentStep.value > 0) currentStep.value--
}
</script>

<style scoped>
.builder-page {
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
  margin-bottom: 40px;
}

.back-link {
  color: #888;
  font-size: 14px;
  text-decoration: none;
  font-weight: 500;
  display: inline-block;
  margin-bottom: 12px;
}
.back-link:hover { color: #C4622D; }

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

.builder-layout {
  display: flex;
  gap: 40px;
}

.sidebar-steps {
  width: 240px;
  flex-shrink: 0;
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.step-item {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 16px 20px;
  border-radius: 8px;
  background: #ffffff;
  border: 1px solid #e8e0d8;
  color: #888;
  cursor: not-allowed;
  transition: all 0.2s;
}

.step-item.unlocked {
  cursor: pointer;
  color: #333;
}

.step-item.unlocked:hover {
  background: #fdfaf8;
  border-color: #C4622D;
}

.step-item.active {
  background: #fdf2ed;
  border-color: #C4622D;
  color: #C4622D;
  font-weight: 600;
}

.step-indicator {
  width: 24px;
  height: 24px;
  border-radius: 50%;
  border: 1px solid currentColor;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 12px;
  font-weight: 700;
}

.step-item.completed .step-indicator {
  background: #C4622D;
  color: #fff;
  border-color: #C4622D;
}

.builder-content {
  flex: 1;
}

.panel {
  background: #ffffff;
  border-radius: 12px;
  border: 1px solid #e8e0d8;
  padding: 40px;
  box-shadow: 0 4px 20px rgba(0,0,0,0.02);
}

.panel h2 {
  font-family: var(--font-heading);
  font-size: 24px;
  margin: 0 0 8px;
  color: #1a1a1a;
}

.field-hint {
  font-size: 14px;
  color: #666;
  margin: 0 0 32px 0;
}

.form-group {
  margin-bottom: 24px;
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.form-group label {
  font-size: 14px;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  color: #333;
}

.input-field {
  padding: 12px 16px;
  border: 1px solid #e8e0d8;
  border-radius: 8px;
  font-family: var(--font-body);
  font-size: 15px;
  width: 100%;
  box-sizing: border-box;
}

.input-field:focus {
  outline: none;
  border-color: #C4622D;
}

.cover-upload-zone {
  width: 100%;
  height: 300px;
  border: 2px dashed #e8e0d8;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  background-size: cover;
  background-position: center;
  transition: all 0.2s;
  background-color: #fdfaf8;
  position: relative;
}

.cover-upload-zone:hover:not(.has-image) {
  border-color: #C4622D;
  background-color: #fdf2ed;
}

.upload-prompt {
  text-align: center;
  color: #666;
}

.upload-prompt p {
  font-weight: 600;
  margin: 8px 0 4px;
  color: #333;
}

.upload-icon {
  font-size: 40px;
}

.remove-btn {
  position: absolute;
  top: 16px;
  right: 16px;
  background: rgba(255,255,255,0.9);
  backdrop-filter: blur(4px);
}

.palette-options {
  display: flex;
  gap: 16px;
}

.palette-pip {
  width: 80px;
  height: 80px;
  border-radius: 12px;
  border: 2px solid #e8e0d8;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
}

.palette-pip:hover { box-shadow: 0 4px 12px rgba(0,0,0,0.1); }
.palette-pip.active { border-color: #C4622D; outline: 2px solid #C4622D; outline-offset: 2px; }

.product-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 16px;
}

.product-card-wrap {
  display: flex;
  flex-direction: column;
  background: transparent;
}

.product-top-bar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 8px 4px;
}

.product-name-new {
  font-family: var(--font-heading);
  font-weight: 600;
  font-size: 15px;
  color: #333;
}

.product-bottom-bar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 8px 4px;
  font-size: 14px;
  color: #666;
}

.product-price {
  font-weight: 600;
  color: #C4622D;
}

.product-orders {
  font-weight: 500;
}

.product-cube {
  height: 180px;
  border-radius: 12px;
  background-size: cover;
  background-position: center;
  position: relative;
  cursor: pointer;
  overflow: hidden;
  border: 1px solid #e8e0d8;
  transition: all 0.2s;
}

.cube-overlay {
  position: absolute;
  inset: 0;
  background: rgba(0,0,0,0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  opacity: 0;
  transition: opacity 0.2s;
}

.product-cube:hover .cube-overlay {
  opacity: 1;
}

.cube-actions {
  display: flex;
  gap: 8px;
}

.mini-icon-btn {
  width: 32px;
  height: 32px;
  background: #fff;
  border: none;
  border-radius: 50%;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  color: #333;
  font-size: 16px;
  transition: all 0.2s;
}

.mini-icon-btn:hover {
  background: #fdfaf8;
  color: #C4622D;
  transform: translateY(-2px);
}

.mini-icon-btn.del:hover {
  color: #d9534f;
}

.intent-options {
  display: flex;
  gap: 16px;
}

.intent-btn {
  padding: 12px 24px;
  border-radius: 8px;
  border: 1px solid #e8e0d8;
  background: #fff;
  font-size: 14px;
  font-weight: 600;
  color: #555;
  cursor: pointer;
  transition: all 0.2s;
}

.intent-btn.selected {
  background: #fdf2ed;
  border-color: #C4622D;
  color: #C4622D;
}

.publish-summary {
  background: #fdfaf8;
  border: 1px solid #e8e0d8;
  border-radius: 8px;
  padding: 20px;
}

.publish-summary ul {
  list-style: none;
  padding: 0;
  margin: 0;
  display: flex;
  flex-direction: column;
  gap: 8px;
  font-size: 15px;
  color: #333;
}

/* Stories Builder Styles */
.stories-builder-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(180px, 1fr));
  gap: 20px;
}

.story-builder-card {
  background: #fff;
  border: 1px solid #e8e0d8;
  border-radius: 12px;
  overflow: hidden;
  display: flex;
  flex-direction: column;
}

.story-preview {
  aspect-ratio: 9/16;
  background-size: cover;
  background-position: center;
  position: relative;
}

.remove-story {
  position: absolute;
  top: 8px;
  right: 8px;
  width: 24px;
  height: 24px;
  border-radius: 50%;
  background: rgba(0,0,0,0.5);
  color: #fff;
  border: none;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 16px;
}

.story-inputs {
  padding: 12px;
}

.small-text {
  font-size: 13px !important;
  height: 60px;
  resize: none;
}

.add-story-card {
  aspect-ratio: 9/16;
  border: 2px dashed #e8e0d8;
  border-radius: 12px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  color: #888;
  transition: all 0.2s;
}

.add-story-card:hover { border-color: #C4622D; color: #C4622D; background: #fdfaf8; }
.plus-icon { font-size: 32px; font-weight: 300; margin-bottom: 4px; }

/* Blog Manager Styles */
.panel-header-inline {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 24px;
}

/* Comic Book Redesign */
.blog-entries-list {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
  gap: 40px;
  padding: 20px;
  background-image: radial-gradient(#d1d1d1 1px, transparent 1px);
  background-size: 20px 20px; /* Halftone effect */
}

.blog-entry-card {
  background: #000;
  border: 4px solid #000;
  box-shadow: 10px 10px 0px rgba(0,0,0,0.1);
  transform: rotate(-1deg);
  transition: transform 0.2s;
}

.blog-entry-card:nth-child(even) {
  transform: rotate(1deg);
}

.blog-entry-card:hover {
  transform: rotate(0deg) scale(1.02);
  z-index: 10;
}

.comic-panel {
  padding: 0 !important;
  position: relative;
}

.entry-cover-huge {
  width: 100%;
  aspect-ratio: 3/4;
  background-size: cover;
  background-position: center;
  position: relative;
  border: 2px solid #000;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
}

.narrative-box {
  background: #ffde00;
  border: 3px solid #000;
  margin: 15px;
  padding: 10px 15px;
  box-shadow: 4px 4px 0px #000;
  position: relative;
  z-index: 2;
}

.narrative-box.top {
  align-self: flex-start;
  max-width: 80%;
}

.narrative-box.bottom {
  align-self: flex-end;
  background: #fff;
  max-width: 70%;
  transform: rotate(1deg);
}

.comic-title {
  font-family: 'Bangers', cursive;
  font-size: 24px;
  margin: 0;
  color: #000;
  letter-spacing: 1px;
}

.comic-text {
  font-family: 'Permanent Marker', cursive;
  font-size: 14px;
  margin: 0;
  color: #000;
  line-height: 1.2;
}

.zap-badge {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%) rotate(-15deg);
  background: #ff3300;
  color: #fff;
  padding: 8px 15px;
  font-family: 'Bangers', cursive;
  font-size: 20px;
  border: 3px solid #000;
  clip-path: polygon(10% 0%, 90% 10%, 100% 50%, 90% 90%, 10% 100%, 0% 50%);
  box-shadow: 4px 4px 0px #000;
  z-index: 3;
}

.zap-badge.live { background: #00cc00; }

.panel-actions-overlay {
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  background: rgba(0,0,0,0.7);
  padding: 10px;
  display: flex;
  gap: 10px;
  justify-content: center;
  opacity: 0;
  transition: opacity 0.2s;
}

.blog-entry-card:hover .panel-actions-overlay {
  opacity: 1;
}

.comic-action-btn {
  background: #fff;
  border: 2px solid #000;
  font-family: 'Bangers', cursive;
  padding: 5px 15px;
  cursor: pointer;
  box-shadow: 3px 3px 0px #000;
}

.product-name {
  font-family: 'Bangers', cursive;
  font-size: 16px;
  color: #fff;
  text-align: center;
  text-shadow: 2px 2px 0px #000;
}

.cube-actions {
  position: absolute;
  top: 10px;
  right: 10px;
  display: flex;
  gap: 6px;
  opacity: 0;
  transform: translateY(-5px);
  transition: all 0.2s;
}

.product-cube:hover .cube-actions {
  opacity: 1;
  transform: translateY(0);
}

.mini-icon-btn {
  width: 28px;
  height: 28px;
  background: #fff;
  border: 2px solid #000;
  border-radius: 50%;
  box-shadow: 2px 2px 0px #000;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 14px;
}

.mini-icon-btn:hover { transform: scale(1.1); background: var(--color-acc-yellow); }
.mini-icon-btn.del:hover { background: #ff3300; color: #fff; }

.product-cube.add-new {
  background: var(--color-bg-page);
  border: 4px dashed #ccc;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  box-shadow: none;
  background-image: none !important;
}

.product-cube.add-new:hover { border-color: var(--color-acc-orange); background: #fffcf9; }

.product-cube.add-new .plus { font-size: 40px; color: #ccc; display: block; line-height: 1; }
.product-cube.add-new .label { font-size: 12px; font-weight: 800; color: #999; letter-spacing: 1px; }
.product-cube.add-new:hover .plus, .product-cube.add-new:hover .label { color: var(--color-acc-orange); }

.modal-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0,0,0,0.6);
  backdrop-filter: blur(4px);
  z-index: 1000;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 20px;
}

.modal-content.product-modal { max-width: 500px; width: 100%; border-radius: 12px; background: #fff; }

.comic-title {
  font-family: 'Bangers', cursive;
  font-size: 32px;
  letter-spacing: 2px;
  color: #1a1a1a;
  margin-bottom: 20px;
}

.modal-body { padding: 24px; }
.modal-footer { padding: 24px; display: flex; justify-content: flex-end; gap: 12px; border-top: 1px solid #eee; }

.cube-content { text-align: center; }

@keyframes notificationIn {
  0% { transform: translate(-50%, 100%); opacity: 0; }
  10% { transform: translate(-50%, -20px); opacity: 1; }
  90% { transform: translate(-50%, -20px); opacity: 1; }
  100% { transform: translate(-50%, 100%); opacity: 0; }
}

.comic-action-btn.edit { color: #C4622D; }
.comic-action-btn.delete { color: #cc3333; }
.comic-action-btn:active { transform: translate(2px, 2px); box-shadow: 1px 1px 0px #000; }

.mini-zap-btn {
  position: absolute;
  width: 30px;
  height: 30px;
  border: 2px solid #000;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: bold;
  cursor: pointer;
  background: #fff;
  box-shadow: 2px 2px 0px #000;
  transition: all 0.1s;
  z-index: 10;
}

.mini-zap-btn.edit {
  top: -10px;
  right: -10px;
  background: #ffde00;
}

.mini-zap-btn.delete {
  bottom: -10px;
  left: -10px;
  background: #ff3300;
  color: #fff;
}

.mini-zap-btn:hover {
  transform: scale(1.1);
  box-shadow: 3px 3px 0px #000;
}

.entry-editor { padding: 30px; background: #fff; }
.editor-row { display: flex; gap: 30px; }
.editor-main { flex: 1; }
.editor-side { width: 220px; }

.quill-wrap { height: 350px; margin-bottom: 60px; }
:deep(.ql-container) { font-family: var(--font-body); font-size: 15px; height: 280px; }
:deep(.ql-toolbar) { border-radius: 8px 8px 0 0; }
:deep(.ql-container) { border-radius: 0 0 8px 8px; }

.mini-upload {
  width: 100%;
  aspect-ratio: 1;
  border: 1px dashed #ccc;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  background-size: cover;
  background-position: center;
  font-size: 13px;
  color: #888;
}

.toggle-label {
  display: flex;
  align-items: center;
  gap: 10px;
  cursor: pointer;
  font-weight: 600;
  font-size: 14px;
}

.editor-footer {
  margin-top: 24px;
  display: flex;
  justify-content: flex-end;
  gap: 12px;
  border-top: 1px solid #eee;
  padding-top: 20px;
}

.empty-blog-state {
  padding: 60px;
  text-align: center;
  border: 2px dashed #e8e0d8;
  border-radius: 12px;
  color: #888;
}

.empty-icon { font-size: 48px; margin-bottom: 16px; }

.panel-actions {
  display: flex;
  justify-content: space-between;
  margin-top: 24px;
}

.btn {
  padding: 12px 24px;
  border-radius: 8px;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
  border: none;
}

.primary-btn { background: #C4622D; color: #fff; }
.primary-btn:hover { background: #a85427; }

.secondary-btn { background: #fff; border: 1px solid #e8e0d8; color: #1a1a1a; }
.secondary-btn:hover:not(:disabled) { border-color: #C4622D; color: #C4622D; }
.secondary-btn:disabled { color: #ccc; cursor: not-allowed; }

.small-btn { padding: 6px 12px; font-size: 13px; }
.notification-banner {
  position: fixed;
  top: 80px;
  left: 50%;
  transform: translateX(-50%);
  background: #1a1a1a;
  color: #fff;
  padding: 12px 24px;
  border-radius: 40px;
  font-size: 14px;
  font-weight: 500;
  display: flex;
  align-items: center;
  gap: 16px;
  box-shadow: 0 8px 30px rgba(0,0,0,0.2);
  z-index: 1000;
  animation: slideDown 0.4s cubic-bezier(0.16, 1, 0.3, 1);
}

.close-notify {
  background: none;
  border: none;
  color: rgba(255,255,255,0.5);
  font-size: 20px;
  cursor: pointer;
  padding: 0;
  line-height: 1;
}

.close-notify:hover {
  color: #fff;
}

@keyframes slideDown {
  from { opacity: 0; transform: translate(-50%, -20px); }
  to { opacity: 1; transform: translate(-50%, 0); }
}
</style>
