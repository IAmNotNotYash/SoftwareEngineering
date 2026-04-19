<template>
  <div class="orders-page">
    <ArtistNavbar />
    
    <main class="page-container">
      <div class="page-header">
        <div>
          <h1 class="page-title">Orders Management</h1>
          <p class="subtitle">Track and fulfill purchases from your audience using the kanban board.</p>
        </div>
      </div>
      
      <div class="orders-board">
        <div class="status-column" v-for="status in columns" :key="status.id">
          <div class="column-header">
            <h3>{{ status.title }}</h3>
            <span class="count">{{ getOrdersInStatus(status.id).length }}</span>
          </div>
          
          <div class="order-list">
            <div 
              class="order-card" 
              v-for="order in getOrdersInStatus(status.id)" 
              :key="order.id"
            >
              <div class="order-id">#{{ order.id }}</div>
              <div class="order-buyer">{{ order.buyerName }}</div>
              <div class="order-items">
                <div v-for="item in order.items" :key="item.name" class="item">
                  <span>{{ item.qty }}x {{ item.name }}</span>
                  <span>₹{{ item.price.toLocaleString() }}</span>
                </div>
              </div>
              <div class="order-footer">
                <span class="order-total">Total: ₹{{ order.total.toLocaleString() }}</span>
                <button 
                  class="btn secondary-btn small-btn" 
                  v-if="status.nextAction"
                  @click="advanceOrder(order, status.nextId)"
                >
                  {{ status.nextAction }} →
                </button>
              </div>
            </div>
            <div class="empty-state" v-if="getOrdersInStatus(status.id).length === 0">
              No orders here.
            </div>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import ArtistNavbar from '../../components/ArtistNavbar.vue'
import { getOrders, updateOrderStatus } from '../../api/commerce.js'

const columns = [
  { id: 'pending', title: 'New Orders', nextAction: 'Mark Processing', nextId: 'processing' },
  { id: 'processing', title: 'Processing', nextAction: 'Mark Shipped', nextId: 'shipped' },
  { id: 'shipped', title: 'Shipped', nextAction: 'Mark Delivered', nextId: 'delivered' },
  { id: 'delivered', title: 'Delivered', nextAction: null, nextId: null }
]

const orders = ref([])
const loading = ref(true)

const fetchOrders = async () => {
  try {
    const data = await getOrders()
    orders.value = data.map(o => ({
      ...o,
      buyerName: o.buyer_name || 'Guest Buyer',
      // items are already in o.items from the backend to_dict
    }))
  } catch (err) {
    console.error("Failed to fetch orders:", err)
  } finally {
    loading.value = false
  }
}

onMounted(fetchOrders)

const getOrdersInStatus = (statusId) => {
  return orders.value.filter(o => o.status === statusId)
}

const advanceOrder = async (order, nextId) => {
  try {
    // API uses real UUIDs, but display_id is ORD-xxxx
    await updateOrderStatus(order.id, nextId)
    order.status = nextId
  } catch (err) {
    alert("Failed to update order: " + err.message)
  }
}
</script>

<style scoped>
.orders-page {
  min-height: 100vh;
  background: var(--color-bg-page);
  font-family: var(--font-body);
}

.page-container {
  max-width: 1400px;
  margin: 0 auto;
  padding: 60px 40px;
}

.page-header {
  margin-bottom: 48px;
}

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

.orders-board {
  display: flex;
  gap: 24px;
  overflow-x: auto;
  padding-bottom: 20px;
}

.status-column {
  flex: 1;
  min-width: 300px;
  background: #fdfaf8;
  border-radius: 12px;
  border: 1px solid #e8e0d8;
  display: flex;
  flex-direction: column;
  height: 65vh;
}

.column-header {
  padding: 20px;
  border-bottom: 1px solid #e8e0d8;
  display: flex;
  justify-content: space-between;
  align-items: center;
  background: #ffffff;
  border-top-left-radius: 12px;
  border-top-right-radius: 12px;
}

.column-header h3 {
  margin: 0;
  font-size: 16px;
  font-weight: 600;
  color: #1a1a1a;
}

.count {
  background: #e8e0d8;
  color: #555;
  font-size: 12px;
  font-weight: 600;
  padding: 4px 10px;
  border-radius: 20px;
}

.order-list {
  padding: 20px;
  overflow-y: auto;
  display: flex;
  flex-direction: column;
  gap: 16px;
  flex: 1;
}

.empty-state {
  text-align: center;
  color: #aaa;
  font-size: 14px;
  margin-top: 20px;
  font-style: italic;
}

.order-card {
  background: #ffffff;
  border: 1px solid #e8e0d8;
  border-radius: 8px;
  padding: 16px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.02);
  transition: transform 0.2s;
}

.order-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 16px rgba(0,0,0,0.04);
}

.order-id {
  font-size: 11px;
  color: #C4622D;
  font-weight: 600;
  letter-spacing: 0.5px;
  margin-bottom: 8px;
}

.order-buyer {
  font-family: var(--font-heading);
  font-size: 18px;
  font-weight: 600;
  color: #1a1a1a;
  margin-bottom: 12px;
}

.order-items {
  display: flex;
  flex-direction: column;
  gap: 6px;
  margin-bottom: 16px;
  border-top: 1px dashed #e8e0d8;
  padding-top: 12px;
}

.item {
  display: flex;
  justify-content: space-between;
  font-size: 13px;
  color: #555;
}

.order-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  border-top: 1px solid #f0f0f0;
  padding-top: 12px;
}

.order-total {
  font-weight: 600;
  color: #1a1a1a;
  font-size: 15px;
}

.btn {
  padding: 8px 16px;
  border-radius: 6px;
  font-size: 13px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
}

.secondary-btn {
  background: #fff;
  border: 1px solid #e8e0d8;
  color: #1a1a1a;
}
.secondary-btn:hover { border-color: #C4622D; color: #C4622D; }

.small-btn {
  padding: 6px 12px;
  font-size: 11px;
}
</style>
