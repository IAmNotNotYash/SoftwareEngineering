<template>
  <div>
    <BuyerNavbar />
    <div class="page-container">
      <h1 class="page-title">My Orders</h1>

      <div class="orders-list">
        <div v-for="order in orders" :key="order.id" class="order-card">
          <div class="order-header">
            <div class="header-info">
              <div class="order-id">{{ order.display_id || order.id }}</div>
              <div class="order-date">Placed on {{ new Date(order.created_at).toLocaleDateString('en-IN') }}</div>
            </div>
            <div class="order-status" :class="order.status">
              {{ order.status }}
            </div>
          </div>
          
          <div class="order-items">
            <div v-for="item in (order.items || [])" :key="item.id" class="order-item">
              <div class="item-img" :style="{ backgroundImage: `url(${item.image})` }"></div>
              <div class="item-details">
                <div class="item-title">{{ item.title }}</div>
                <div class="item-artist">{{ item.artist }}</div>
                <RouterLink 
                  v-if="order.status === 'delivered'"
                  :to="`/buyer/product/${item.product_id}#reviews`" 
                  class="review-link"
                >Write a Review</RouterLink>
              </div>
            </div>
          </div>
          
          <div class="order-footer">
            <div class="order-total">Total: ₹{{ order.total.toLocaleString('en-IN') }}</div>
            <div class="order-actions">
              <button class="btn-secondary" @click="toggleDetails(order.id)">View Details</button>
              <button class="btn-primary" @click="toggleTracking(order.id)">Track Order</button>
            </div>
          </div>

          <!-- Tracking Timeline (Conditional) -->
          <div class="tracking-container" v-if="trackingExpanded === order.id">
            <h4 class="tracking-title">Delivery Status</h4>
            <div class="timeline">
              <div
                v-for="event in (trackingEvents[order.id] || [])"
                :key="event.id"
                class="timeline-step completed"
              >
                <div class="step-indicator"></div>
                <div class="step-content">
                  <div class="step-label">{{ EVENT_LABEL[event.event] || event.event }}</div>
                  <div class="step-date">{{ new Date(event.created_at).toLocaleString('en-IN') }}</div>
                </div>
              </div>
              <div v-if="!(trackingEvents[order.id] || []).length" class="timeline-step">
                <div class="step-content"><div class="step-label" style="color:#888">No tracking events yet.</div></div>
              </div>
            </div>
          </div>

          <!-- Details (Conditional) -->
          <div class="tracking-container" v-if="detailsExpanded === order.id">
            <h4 class="tracking-title">Shipping Address</h4>
            <p style="color: #555; font-size: 14px; line-height: 1.6;" v-if="order.shipping_address_snapshot">
              {{ order.shipping_address_snapshot.full_address }}<br/>
              {{ order.shipping_address_snapshot.city }}, {{ order.shipping_address_snapshot.state }}<br/>
              {{ order.shipping_address_snapshot.country }} {{ order.shipping_address_snapshot.pin_code }}
            </p>
          </div>

        </div>
        
        <div v-if="orders.length === 0" class="loading-state">
          You have no orders yet.
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import BuyerNavbar from '../../components/BuyerNavbar.vue'
import { getOrders, getOrderTracking } from '../../api/commerce.js'

const orders = ref([])
const trackingExpanded = ref(null)
const detailsExpanded = ref(null)
const trackingEvents = ref({})

onMounted(async () => {
  const data = await getOrders()
  orders.value = Array.isArray(data) ? data : (data.orders || [])
})

async function toggleTracking(orderId) {
  detailsExpanded.value = null
  if (trackingExpanded.value === orderId) { trackingExpanded.value = null; return }
  trackingExpanded.value = orderId
  if (!trackingEvents.value[orderId]) {
    try {
      const data = await getOrderTracking(orderId)
      trackingEvents.value[orderId] = data.tracking_events || data
    } catch { trackingEvents.value[orderId] = [] }
  }
}

const toggleDetails = (id) => {
  trackingExpanded.value = null
  detailsExpanded.value = detailsExpanded.value === id ? null : id
}

const EVENT_LABEL = {
  confirmed: 'Order Confirmed', dispatched: 'Dispatched',
  out_for_delivery: 'Out for Delivery', delivered: 'Delivered', cancelled: 'Cancelled',
}
</script>

<style scoped>
.page-container {
  max-width: 1000px;
  margin: 0 auto;
  padding: 40px;
  font-family: 'DM Sans', sans-serif;
}

.page-title {
  font-family: 'Playfair Display', serif;
  font-size: 32px;
  font-weight: 600;
  color: #000;
  margin-bottom: 40px;
}

.orders-list {
  display: flex;
  flex-direction: column;
  gap: 32px;
}

.order-card {
  background: #ffffff;
  border-radius: 8px;
  border: 1px solid #e8e0d8;
  overflow: hidden;
  box-shadow: 0 2px 8px rgba(0,0,0,0.02);
}

.order-header {
  background: #fdfaf8;
  padding: 24px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  border-bottom: 1px solid #e8e0d8;
}

.order-id {
  font-family: 'Playfair Display', serif;
  font-size: 20px;
  font-weight: 600;
  color: #000;
  margin-bottom: 4px;
}

.order-date {
  font-size: 13px;
  color: #888;
}

.order-status {
  padding: 6px 16px;
  border-radius: 4px;
  font-size: 13px;
  font-weight: 600;
  background: #e8e0d8;
  color: #555;
  text-transform: capitalize;
}

.order-status.processing {
  background: #fff3cd;
  color: #856404;
}

.order-status.shipped {
  background: #d4edda;
  color: #155724;
}

.order-items {
  padding: 24px;
}

.order-item {
  display: flex;
  gap: 20px;
  margin-bottom: 24px;
}

.order-item:last-child {
  margin-bottom: 0;
}

.item-img {
  width: 80px;
  height: 80px;
  border-radius: 6px;
  background-size: cover;
  background-position: center;
  flex-shrink: 0;
}

.item-details {
  display: flex;
  flex-direction: column;
  justify-content: center;
}

.item-title {
  font-family: 'Playfair Display', serif;
  font-size: 16px;
  font-weight: 600;
  color: #000;
  margin-bottom: 4px;
}

.item-artist {
  font-size: 12px;
  color: #888;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  margin-bottom: 4px;
}

.review-link {
  font-size: 12px;
  color: #C4622D;
  text-decoration: none;
  font-weight: 600;
}

.review-link:hover {
  text-decoration: underline;
}

.order-footer {
  padding: 24px;
  border-top: 1px solid #e8e0d8;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.order-total {
  font-family: 'Playfair Display', serif;
  font-size: 22px;
  font-weight: 600;
  color: #000;
}

.order-actions {
  display: flex;
  gap: 16px;
}

.btn-secondary {
  background: white;
  color: #000;
  border: 1px solid #ccc;
  padding: 10px 20px;
  border-radius: 4px;
  font-family: 'DM Sans', sans-serif;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
}

.btn-secondary:hover {
  border-color: #000;
}

.btn-primary {
  background: #C4622D;
  color: white;
  border: none;
  padding: 10px 20px;
  border-radius: 4px;
  font-family: 'DM Sans', sans-serif;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  transition: background 0.2s;
}

.btn-primary:hover {
  background: #a95224;
}

/* Tracking Timeline CSS */
.tracking-container {
  background: #fdfaf8;
  border-top: 1px solid #e8e0d8;
  padding: 24px 32px;
}

.tracking-title {
  font-family: 'DM Sans', sans-serif;
  font-size: 15px;
  color: #000;
  margin-bottom: 24px;
}

.timeline {
  display: flex;
  flex-direction: column;
  gap: 20px;
  position: relative;
}

.timeline::before {
  content: '';
  position: absolute;
  left: 5px;
  top: 8px;
  bottom: 8px;
  width: 2px;
  background: #e8e0d8;
}

.timeline-step {
  display: flex;
  gap: 16px;
  position: relative;
  opacity: 0.5;
}

.timeline-step.completed {
  opacity: 1;
}

.step-indicator {
  width: 12px;
  height: 12px;
  border-radius: 50%;
  background: #e8e0d8;
  margin-top: 4px;
  z-index: 2;
}

.timeline-step.completed .step-indicator {
  background: #C4622D;
}

.step-label {
  font-size: 14px;
  font-weight: 600;
  color: #000;
}

.step-date {
  font-size: 12px;
  color: #888;
  margin-top: 2px;
}

.loading-state {
  text-align: center;
  padding: 60px 0;
  color: #888;
}
</style>
