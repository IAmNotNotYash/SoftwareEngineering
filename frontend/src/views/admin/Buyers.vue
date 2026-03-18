<template>
  <div class="buyers-page">
    <AdminNavbar />

    <div class="container">
      <h1 class="title">Buyers</h1>

      <!-- Search Bar -->
      <div class="search-bar">
        <input
          v-model="searchQuery"
          type="text"
          placeholder="Search buyers..."
        />
      </div>

      <!-- Table -->
      <div class="table-card">
        <table>
          <thead>
            <tr>
              <th>Name</th>
              <th>Email</th>
              <th>Orders</th>
              <th>Status</th>
              <th>Joined</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="buyer in filteredBuyers" :key="buyer.id">
              <td>{{ buyer.name }}</td>
              <td>{{ buyer.email }}</td>
              <td>{{ buyer.orderCount }}</td>
              <td>
                <span
                  class="badge"
                  :class="buyer.suspended ? 'suspended' : 'active'"
                >
                  {{ buyer.suspended ? 'Suspended' : 'Active' }}
                </span>
              </td>
              <td>{{ buyer.joined }}</td>
              <td>
                <button
                  class="suspend-btn"
                  :disabled="buyer.suspended"
                  @click="openModal(buyer)"
                >
                  {{ buyer.suspended ? 'Suspended' : 'Suspend' }}
                </button>
              </td>
            </tr>
          </tbody>
        </table>

        <p v-if="filteredBuyers.length === 0" class="empty">
          No buyers found.
        </p>
      </div>
    </div>

    <!-- Confirmation Modal -->
    <div v-if="showModal" class="modal-overlay">
      <div class="modal">
        <h3>Confirm Suspension</h3>
        <p>Are you sure you want to suspend {{ selectedBuyer?.name }}?</p>

        <div class="modal-actions">
          <button class="cancel" @click="closeModal">Cancel</button>
          <button class="confirm" @click="confirmSuspend">Suspend</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import AdminNavbar from '../../components/AdminNavbar.vue'
import { getBuyers, suspendBuyer } from '../../api/admin.js'

const buyers = ref([])
const searchQuery = ref('')
const debouncedQuery = ref('')

const showModal = ref(false)
const selectedBuyer = ref(null)

onMounted(async () => {
  buyers.value = await getBuyers()
})

// Debounce search
let timeout = null
watch(searchQuery, (val) => {
  clearTimeout(timeout)
  timeout = setTimeout(() => {
    debouncedQuery.value = val
  }, 300)
})

const filteredBuyers = computed(() => {
  if (!debouncedQuery.value) return buyers.value

  const query = debouncedQuery.value.toLowerCase()

  return buyers.value.filter(b =>
    b.name.toLowerCase().includes(query) ||
    b.email.toLowerCase().includes(query)
  )
})

const openModal = (buyer) => {
  selectedBuyer.value = buyer
  showModal.value = true
}

const closeModal = () => {
  showModal.value = false
  selectedBuyer.value = null
}

const confirmSuspend = async () => {
  if (!selectedBuyer.value) return

  await suspendBuyer(selectedBuyer.value.id)

  // optimistic update
  buyers.value = buyers.value.map(b =>
    b.id === selectedBuyer.value.id ? { ...b, suspended: true } : b
  )

  closeModal()
}
</script>

<style scoped>
.buyers-page {
  background: #faf8f5;
  min-height: 100vh;
}

.container {
  padding: 24px 40px;
}

.title {
  font-family: 'Playfair Display', serif;
  font-size: 32px;
  margin-bottom: 20px;
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
</style>
