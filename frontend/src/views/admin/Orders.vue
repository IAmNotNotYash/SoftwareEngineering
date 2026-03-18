<template>
  <div class="orders-page">
    <AdminNavbar />

    <div class="container">
      <h1 class="title">Orders</h1>

      <!-- Controls -->
      <div class="controls">
        <input
          v-model="searchQuery"
          type="text"
          placeholder="Search orders..."
        />

        <select v-model="statusFilter">
          <option value="all">All</option>
          <option value="delivered">Delivered</option>
          <option value="pending">Pending</option>
          <option value="cancelled">Cancelled</option>
        </select>
      </div>

      <!-- Table -->
      <div class="table-card">
        <table>
          <thead>
            <tr>
              <th>Order ID</th>
              <th>Buyer</th>
              <th>Artist</th>
              <th>Amount</th>
              <th>Status</th>
              <th>Date</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="order in filteredOrders" :key="order.id">
              <td>{{ order.id }}</td>
              <td>{{ order.buyer }}</td>
              <td>{{ order.artist }}</td>
              <td>₹{{ order.amount }}</td>
              <td>
                <span class="badge" :class="order.status">
                  {{ capitalize(order.status) }}
                </span>
              </td>
              <td>{{ order.date }}</td>
            </tr>
          </tbody>
        </table>

        <p v-if="filteredOrders.length === 0" class="empty">
          No orders found.
        </p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import AdminNavbar from '../../components/AdminNavbar.vue'
import { getOrders } from '../../api/admin.js'

const orders = ref([])
const searchQuery = ref('')
const debouncedQuery = ref('')
const statusFilter = ref('all')

onMounted(async () => {
  orders.value = await getOrders()
})

// debounce search
let timeout = null
watch(searchQuery, (val) => {
  clearTimeout(timeout)
  timeout = setTimeout(() => {
    debouncedQuery.value = val
  }, 300)
})

const filteredOrders = computed(() => {
  let result = orders.value

  // status filter
  if (statusFilter.value !== 'all') {
    result = result.filter(o => o.status === statusFilter.value)
  }

  // search filter
  if (debouncedQuery.value) {
    const q = debouncedQuery.value.toLowerCase()
    result = result.filter(o =>
      o.id.toLowerCase().includes(q) ||
      o.buyer.toLowerCase().includes(q) ||
      o.artist.toLowerCase().includes(q)
    )
  }

  return result
})

const capitalize = (str) => {
  return str.charAt(0).toUpperCase() + str.slice(1)
}
</script>

<style scoped>
.orders-page {
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

.controls {
  display: flex;
  gap: 12px;
  margin-bottom: 20px;
}

.controls input,
.controls select {
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

.delivered {
  background: #e6f4ea;
  color: #2e7d32;
}

.pending {
  background: #fff4e5;
  color: #b26a00;
}

.cancelled {
  background: #fbe9e7;
  color: #c4622d;
}

.empty {
  text-align: center;
  margin-top: 20px;
  color: #999;
}
</style>
