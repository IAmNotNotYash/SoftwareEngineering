<template>
  <div class="story-page">
    <ArtistNavbar />
    
    <main class="page-container">
      <div class="composer-card">
        <header class="composer-header">
          <RouterLink to="/artist/dashboard" class="back-link">← Back to Dashboard</RouterLink>
          <button 
            class="btn primary-btn" 
            @click="publishStory" 
            :disabled="!title || !content || isPublishing"
          >
            {{ isPublishing ? 'Publishing...' : 'Publish Story' }}
          </button>
        </header>

        <div class="composer-body">
          <div 
            class="cover-upload-zone" 
            :class="{ 'has-image': coverImage }"
            :style="coverImage ? { backgroundImage: `linear-gradient(rgba(0,0,0,0.1), rgba(0,0,0,0.5)), url(${coverImage})` } : {}"
            @click="!coverImage ? triggerUpload() : null"
          >
            <input type="file" ref="fileInput" hidden accept="image/*" @change="handleImageUpload" />
            
            <div class="upload-prompt" v-if="!coverImage">
              <span class="upload-icon">📸</span>
              <p>Add a beautiful cover image</p>
            </div>
            
            <button class="remove-btn btn secondary-btn small-btn" v-if="coverImage" @click.stop="coverImage = null">
              Change Cover
            </button>
          </div>

          <input 
            v-model="title" 
            class="story-title-input" 
            placeholder="Give your story a title..." 
          />
          
          <textarea 
            v-model="content" 
            class="story-content-input" 
            placeholder="Tell your audience about your crafting process, inspirations, or updates..."
            rows="10"
          ></textarea>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import ArtistNavbar from '../../components/ArtistNavbar.vue'
import { createPost } from '../../api/social.js'

const router = useRouter()
const title = ref('')
const content = ref('')
const coverImage = ref(null) // Public URL
const coverFile = ref(null) // Real File object
const fileInput = ref(null)
const isPublishing = ref(false)

const triggerUpload = () => {
  fileInput.value.click()
}

const handleImageUpload = (e) => {
  const file = e.target.files[0]
  if (!file) return
  coverFile.value = file
  coverImage.value = URL.createObjectURL(file)
}

const publishStory = async () => {
  if (!title.value || !content.value) return
  
  isPublishing.value = true
  try {
    let finalCoverUrl = null
    
    // 1. Upload cover image if exists
    if (coverFile.value) {
      const formData = new FormData()
      formData.append('file', coverFile.value)
      
      const uploadRes = await fetch('http://localhost:5000/api/social/upload-image', {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${sessionStorage.getItem('token')}`
        },
        body: formData
      })
      
      if (uploadRes.ok) {
        const { url } = await uploadRes.json()
        finalCoverUrl = url
      }
    }
    
    // 2. Create the post
    await createPost({
      title: title.value,
      body: content.value,
      cover_image_url: finalCoverUrl,
      type: 'story',
      is_published: true
    })
    
    alert("Story successfully published!")
    router.push('/artist/dashboard')
  } catch (err) {
    alert("Failed to publish: " + err.message)
  } finally {
    isPublishing.value = false
  }
}
</script>

<style scoped>
.story-page {
  min-height: 100vh;
  background: var(--color-bg-page);
  font-family: var(--font-body);
}

.page-container {
  max-width: 800px; /* Narrower container for writing */
  margin: 0 auto;
  padding: 60px 40px;
}

.composer-card {
  background: #ffffff;
  border-radius: 16px;
  border: 1px solid #e8e0d8;
  box-shadow: 0 8px 32px rgba(0,0,0,0.03);
  overflow: hidden;
}

.composer-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px 32px;
  border-bottom: 1px solid #f0f0f0;
}

.back-link {
  color: #888;
  text-decoration: none;
  font-size: 14px;
  font-weight: 500;
  transition: color 0.2s;
}

.back-link:hover {
  color: #C4622D;
}

.composer-body {
  padding: 40px 48px;
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.cover-upload-zone {
  width: 100%;
  height: 280px;
  background-color: #fdfaf8;
  border: 2px dashed #e8e0d8;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.2s;
  background-size: cover;
  background-position: center;
  position: relative;
}

.cover-upload-zone:hover:not(.has-image) {
  border-color: #C4622D;
  background-color: #fdf2ed;
}

.cover-upload-zone.has-image {
  border: none;
  cursor: default;
}

.upload-prompt {
  text-align: center;
  color: #666;
}

.upload-icon {
  font-size: 40px;
  margin-bottom: 12px;
  display: block;
}

.remove-btn {
  position: absolute;
  top: 16px;
  right: 16px;
  background: rgba(255,255,255,0.9);
  backdrop-filter: blur(4px);
}

.story-title-input {
  width: 100%;
  border: none;
  font-family: var(--font-heading);
  font-size: 42px;
  font-weight: 700;
  color: #1a1a1a;
  outline: none;
  padding: 0;
}

.story-title-input::placeholder {
  color: #ccc;
}

.story-content-input {
  width: 100%;
  border: none;
  font-family: var(--font-body);
  font-size: 18px;
  line-height: 1.7;
  color: #333;
  outline: none;
  padding: 0;
  resize: vertical;
  min-height: 300px;
}

.story-content-input::placeholder {
  color: #ccc;
}

.btn {
  padding: 10px 24px;
  border-radius: 8px;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
  border: none;
}

.primary-btn {
  background: #C4622D;
  color: #fff;
}

.primary-btn:hover:not(:disabled) {
  background: #a85427;
}

.primary-btn:disabled {
  background: #e8e0d8;
  cursor: not-allowed;
  color: #aaa;
}

.secondary-btn {
  border: 1px solid #e8e0d8;
  color: #1a1a1a;
}
.secondary-btn:hover { border-color: #C4622D; color: #C4622D; }

.small-btn {
  padding: 6px 12px;
  font-size: 13px;
}
</style>
