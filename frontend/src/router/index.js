import { createRouter, createWebHistory } from 'vue-router'

// Admin views
import AdminDashboard from '../views/admin/Dashboard.vue'
import AdminVerification from '../views/admin/Verification.vue'
import AdminArtists from '../views/admin/Artists.vue'
import AdminBuyers from '../views/admin/Buyers.vue'
import AdminOrders from '../views/admin/Orders.vue'
import AdminAnalytics from '../views/admin/Analytics.vue'

const routes = [
  { path: '/admin/dashboard',    component: AdminDashboard },
  { path: '/admin/verification', component: AdminVerification },
  { path: '/admin/artists',      component: AdminArtists },
  { path: '/admin/buyers',       component: AdminBuyers },
  { path: '/admin/orders',       component: AdminOrders },
  { path: '/admin/analytics',    component: AdminAnalytics },
  // Default redirect
  { path: '/:pathMatch(.*)*', redirect: '/admin/dashboard' },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

export default router