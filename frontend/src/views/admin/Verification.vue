<template>
  <div>
    <AdminNavbar />
    <div class="page-container">
      <h1 class="page-title">Artist Verification Queue</h1>

      <!-- Filter Tabs -->
      <div class="tabs">
        <button
          v-for="tab in tabs"
          :key="tab"
          class="tab"
          :class="{ active: activeTab === tab }"
          @click="activeTab = tab"
        >
          {{ tab }}
        </button>
      </div>

      <!-- Table -->
      <div class="table-wrapper">
        <table>
          <thead>
            <tr>
              <th>Artist</th>
              <th>Email</th>
              <th>Joined</th>
              <th>Status</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="artist in filteredArtists" :key="artist.id">
              <td class="name">{{ artist.name }}</td>
              <td class="muted">{{ artist.email }}</td>
              <td class="muted">{{ artist.joined }}</td>
              <td>
                <span class="badge" :class="artist.status">
                  {{ capitalise(artist.status) }}
                </span>
              </td>
              <td>
                <div class="actions" v-if="artist.status === 'pending'">
                  <button class="btn-approve" @click="handleApprove(artist)">Approve</button>
                  <button class="btn-reject" @click="openRejectModal(artist)">Reject</button>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>

      <!-- Reject Modal -->
      <div class="modal-overlay" v-if="showModal" @click.self="showModal = false">
        <div class="modal">
          <h2>Reject Artist</h2>
          <p>Rejecting <strong>{{ selectedArtist?.name }}</strong>. Provide an optional reason:</p>
          <textarea
            v-model="rejectReason"
            placeholder="Reason for rejection (optional)"
            rows="3"
          ></textarea>
          <div class="modal-actions">
            <button class="btn-cancel" @click="showModal = false">Cancel</button>
            <button class="btn-confirm-reject" @click="handleReject">Confirm Reject</button>
          </div>
        </div>
      </div>

    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import AdminNavbar from '../../components/AdminNavbar.vue'
import { getVerificationQueue, approveArtist, rejectArtist } from '../../api/admin.js'

const tabs = ['All', 'Pending', 'Approved', 'Rejected']
const activeTab = ref('All')

const artists = ref([])

onMounted(async () => {
  artists.value = await getVerificationQueue()
})

const filteredArtists = computed(() => {
  if (activeTab.value === 'All') return artists.value
  return artists.value.filter(a => a.status === activeTab.value.toLowerCase())
})

// Approve
async function handleApprove(artist) {
  await approveArtist(artist.id)
  artist.status = 'approved'
}

// Reject modal
const showModal = ref(false)
const selectedArtist = ref(null)
const rejectReason = ref('')

function openRejectModal(artist) {
  selectedArtist.value = artist
  rejectReason.value = ''
  showModal.value = true
}

async function handleReject() {
  await rejectArtist(selectedArtist.value.id, rejectReason.value)
  selectedArtist.value.status = 'rejected'
  showModal.value = false
}

function capitalise(str) {
  return str.charAt(0).toUpperCase() + str.slice(1)
}
</script>

<style scoped>
.tabs {
  display: flex;
  gap: 8px;
  margin-bottom: 24px;
}

.tab {
  padding: 7px 18px;
  border-radius: 20px;
  border: 1px solid #ddd;
  background: #fff;
  font-size: 13px;
  cursor: pointer;
  font-family: 'DM Sans', sans-serif;
  color: #555;
  transition: all 0.15s;
}

.tab:hover {
  border-color: #C4622D;
  color: #C4622D;
}

.tab.active {
  background: #C4622D;
  border-color: #C4622D;
  color: #fff;
  font-weight: 600;
}

.table-wrapper {
  background: #fff;
  border-radius: 10px;
  box-shadow: 0 1px 4px rgba(0,0,0,0.07);
  overflow: hidden;
}

table {
  width: 100%;
  border-collapse: collapse;
}

thead tr {
  border-bottom: 1px solid #eee;
}

th {
  text-align: left;
  padding: 12px 20px;
  font-size: 11px;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  color: #888;
  font-weight: 600;
}

td {
  padding: 14px 20px;
  font-size: 14px;
  border-bottom: 1px solid #f5f5f5;
}

tbody tr:last-child td {
  border-bottom: none;
}

tbody tr:hover {
  background: #fafafa;
}

td.name {
  font-weight: 500;
  color: #1A1A1A;
}

td.muted {
  color: #888;
}

.badge {
  display: inline-block;
  padding: 4px 10px;
  border-radius: 20px;
  font-size: 12px;
  font-weight: 500;
}

.badge.pending  { background: #fef3cd; color: #7a5c00; }
.badge.approved { background: #d1fae5; color: #065f46; }
.badge.rejected { background: #fee2e2; color: #991b1b; }

.actions {
  display: flex;
  gap: 8px;
}

.btn-approve {
  padding: 6px 14px;
  background: #22c55e;
  color: #fff;
  border: none;
  border-radius: 6px;
  font-size: 13px;
  cursor: pointer;
  font-family: 'DM Sans', sans-serif;
  transition: background 0.15s;
}

.btn-approve:hover { background: #16a34a; }

.btn-reject {
  padding: 6px 14px;
  background: transparent;
  color: #C4622D;
  border: 1px solid #C4622D;
  border-radius: 6px;
  font-size: 13px;
  cursor: pointer;
  font-family: 'DM Sans', sans-serif;
  transition: all 0.15s;
}

.btn-reject:hover {
  background: #C4622D;
  color: #fff;
}

/* Modal */
.modal-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0,0,0,0.35);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 200;
}

.modal {
  background: #fff;
  border-radius: 12px;
  padding: 32px;
  width: 440px;
  box-shadow: 0 8px 32px rgba(0,0,0,0.12);
}

.modal h2 {
  font-family: 'Playfair Display', serif;
  font-size: 20px;
  margin-bottom: 10px;
  color: #1A1A1A;
}

.modal p {
  font-size: 14px;
  color: #555;
  margin-bottom: 16px;
}

.modal textarea {
  width: 100%;
  padding: 10px 14px;
  border: 1px solid #ddd;
  border-radius: 8px;
  font-family: 'DM Sans', sans-serif;
  font-size: 14px;
  resize: none;
  outline: none;
  color: #1A1A1A;
}

.modal textarea:focus {
  border-color: #C4622D;
}

.modal-actions {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
  margin-top: 20px;
}

.btn-cancel {
  padding: 8px 18px;
  background: transparent;
  border: 1px solid #ddd;
  border-radius: 6px;
  font-size: 13px;
  cursor: pointer;
  font-family: 'DM Sans', sans-serif;
  color: #555;
}

.btn-cancel:hover { background: #f5f5f5; }

.btn-confirm-reject {
  padding: 8px 18px;
  background: #ef4444;
  color: #fff;
  border: none;
  border-radius: 6px;
  font-size: 13px;
  cursor: pointer;
  font-family: 'DM Sans', sans-serif;
  transition: background 0.15s;
}

.btn-confirm-reject:hover { background: #dc2626; }
</style>