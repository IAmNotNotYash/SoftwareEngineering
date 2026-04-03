<template>
  <div class="artists-page">
    <AdminNavbar />

    <div class="page-container">
      <h1 class="page-title">Artists</h1>

      <!-- Search Bar -->
      <div class="search-bar">
        <input
          v-model="searchQuery"
          type="text"
          placeholder="Search artists..."
        />
      </div>

      <!-- Table -->
      <div class="table-card">
        <table>
          <thead>
            <tr>
              <th>Name</th>
              <th>Brand</th>
              <th>Email</th>
              <th>Verified</th>
              <th>Status</th>
              <th>Joined</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="artist in filteredArtists" :key="artist.id">
              <td>{{ artist.name }}</td>
              <td>{{ artist.brand }}</td>
              <td>{{ artist.email }}</td>
              <td>
                <span
                  class="badge"
                  :class="artist.verified ? 'verified' : 'unverified'"
                >
                  {{ artist.verified ? 'Verified' : 'Unverified' }}
                </span>
              </td>
              <td>
                <span
                  class="badge"
                  :class="artist.is_suspended ? 'suspended' : 'active'"
                >
                  {{ artist.is_suspended ? 'Suspended' : 'Active' }}
                </span>
              </td>
              <td>{{ artist.joined }}</td>
              <td>
                <button
                  class="suspend-btn"
                  @click="openModal(artist)"
                >
                  {{ artist.is_suspended ? 'Unsuspend' : 'Suspend' }}
                </button>
              </td>
            </tr>
          </tbody>
        </table>

        <p v-if="filteredArtists.length === 0" class="empty">
          No artists found.
        </p>

        <div v-if="hasMore" class="pagination-footer">
          <button class="load-more-btn" @click="loadMore" :disabled="loadingMore">
            {{ loadingMore ? 'Loading...' : 'Load More' }}
          </button>
        </div>
      </div>
    </div>

    <!-- Confirmation Modal -->
    <div v-if="showModal" class="modal-overlay">
      <div class="modal">
        <h3>{{ selectedArtist?.is_suspended ? 'Confirm Unsuspension' : 'Confirm Suspension' }}</h3>
        <p>Are you sure you want to {{ selectedArtist?.is_suspended ? 'unsuspend' : 'suspend' }} {{ selectedArtist?.name }}?</p>

        <div class="modal-actions">
          <button class="cancel" @click="closeModal">Cancel</button>
          <button class="confirm" @click="confirmSuspend">{{ selectedArtist?.is_suspended ? 'Unsuspend' : 'Suspend' }}</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import AdminNavbar from '../../components/AdminNavbar.vue'
import { getArtists, suspendArtist } from '../../api/admin.js'

const artists = ref([])
const totalArtists = ref(0)
const limit = 10
const offset = ref(0)
const loadingMore = ref(false)

const searchQuery = ref('')
const debouncedQuery = ref('')

const showModal = ref(false)
const selectedArtist = ref(null)

onMounted(async () => {
  const data = await getArtists(limit, offset.value)
  artists.value = data.artists
  totalArtists.value = data.total
})

const hasMore = computed(() => artists.value.length < totalArtists.value)

async function loadMore() {
  loadingMore.value = true
  try {
    offset.value += limit
    const data = await getArtists(limit, offset.value)
    artists.value = [...artists.value, ...data.artists]
    totalArtists.value = data.total
  } finally {
    loadingMore.value = false
  }
}

// Debounce logic
let timeout = null
watch(searchQuery, (val) => {
  clearTimeout(timeout)
  timeout = setTimeout(() => {
    debouncedQuery.value = val
  }, 300)
})

const filteredArtists = computed(() => {
  if (!debouncedQuery.value) return artists.value

  const query = debouncedQuery.value.toLowerCase()

  return artists.value.filter(a =>
    a.name.toLowerCase().includes(query) ||
    a.brand.toLowerCase().includes(query) ||
    a.email.toLowerCase().includes(query)
  )
})

const openModal = (artist) => {
  selectedArtist.value = artist
  showModal.value = true
}

const closeModal = () => {
  showModal.value = false
  selectedArtist.value = null
}

const confirmSuspend = async () => {
  if (!selectedArtist.value) return

  const res = await suspendArtist(selectedArtist.value.id)

  // optimistic update
  artists.value = artists.value.map(a =>
    a.id === selectedArtist.value.id ? { ...a, is_suspended: res.is_suspended } : a
  )

  closeModal()
}
</script>

<style scoped>
.artists-page {
  background: #faf8f5;
  min-height: 100vh;
}

.page-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 60px 40px;
  font-family: 'DM Sans', sans-serif;
}

.page-title {
  font-family: 'Playfair Display', serif;
  font-size: 32px;
  margin-bottom: 24px;
  color: #1A1A1A;
}

.search-bar {
  margin-bottom: 20px;
}

.search-bar input {
  width: 100%;
  max-width: 300px;
  padding: 10px 12px;
  border-radius: 8px;
  border: none;
  box-shadow: 0 2px 6px rgba(0,0,0,0.05);
  font-family: 'DM Sans', sans-serif;
}

.table-card {
  background: white;
  border-radius: 12px;
  padding: 20px;
  box-shadow: 0 4px 12px rgba(0,0,0,0.05);
}

table {
  width: 100%;
  border-collapse: collapse;
  font-family: 'DM Sans', sans-serif;
}

th {
  text-align: left;
  font-size: 14px;
  color: #666;
  padding-bottom: 12px;
}

td {
  padding: 12px 0;
}

.badge {
  padding: 4px 10px;
  border-radius: 999px;
  font-size: 12px;
}

.verified {
  background: #e6f4ea;
  color: #2e7d32;
}

.unverified {
  background: #fbe9e7;
  color: #c4622d;
}

.active {
  background: #e8f5e9;
  color: #2e7d32;
}

.suspended {
  background: #fbe9e7;
  color: #c4622d;
}

.suspend-btn {
  background: transparent;
  border: none;
  color: #c4622d;
  cursor: pointer;
  font-weight: 500;
}

.suspend-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0,0,0,0.4);
  display: flex;
  align-items: center;
  justify-content: center;
}

.modal {
  background: white;
  padding: 24px;
  border-radius: 12px;
  width: 300px;
  box-shadow: 0 4px 12px rgba(0,0,0,0.1);
  font-family: 'DM Sans', sans-serif;
}

.modal h3 {
  margin-bottom: 10px;
}

.modal-actions {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
  margin-top: 20px;
}

.cancel {
  background: none;
  border: none;
  cursor: pointer;
}

.confirm {
  background: #c4622d;
  color: white;
  border: none;
  padding: 6px 12px;
  border-radius: 6px;
  cursor: pointer;
}

.empty {
  text-align: center;
  margin-top: 20px;
  color: #999;
}

.pagination-footer {
  display: flex;
  justify-content: center;
  padding: 20px 0 10px;
}

.load-more-btn {
  background: white;
  border: 1px solid #C4622D;
  color: #C4622D;
  padding: 8px 24px;
  border-radius: 20px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
}

.load-more-btn:hover:not(:disabled) {
  background: #C4622D;
  color: white;
}

.load-more-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}
</style>
