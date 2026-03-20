import { createRouter, createWebHistory } from 'vue-router'

// Admin views
import AdminDashboard from '../views/admin/Dashboard.vue'
import AdminVerification from '../views/admin/Verification.vue'
import AdminArtists from '../views/admin/Artists.vue'
import AdminBuyers from '../views/admin/Buyers.vue'
import AdminOrders from '../views/admin/Orders.vue'
import AdminAnalytics from '../views/admin/Analytics.vue'

// Buyer views
import BuyerDashboard from '../views/buyer/Dashboard.vue'
import BuyerProducts from '../views/buyer/Products.vue'
import BuyerOrders from '../views/buyer/Orders.vue'
import BuyerCart from '../views/buyer/Cart.vue'
import BuyerCatalogue from '../views/buyer/Catalogue.vue'
import BuyerProductDetails from '../views/buyer/ProductDetails.vue'
import BuyerInsight from '../views/buyer/Insight.vue'
import BuyerCheckout from '../views/buyer/Checkout.vue'
import BuyerArtist from '../views/buyer/Artist.vue'

const routes = [
  // Admin routes
  { path: '/admin/dashboard',    component: AdminDashboard },
  { path: '/admin/verification', component: AdminVerification },
  { path: '/admin/artists',      component: AdminArtists },
  { path: '/admin/buyers',       component: AdminBuyers },
  { path: '/admin/orders',       component: AdminOrders },
  { path: '/admin/analytics',    component: AdminAnalytics },
  
  // Buyer routes
  { path: '/buyer/dashboard',    component: BuyerDashboard },
  { path: '/buyer/products',     component: BuyerProducts },
  { path: '/buyer/orders',       component: BuyerOrders },
  { path: '/buyer/cart',         component: BuyerCart },
  { path: '/buyer/catalogue/:id',component: BuyerCatalogue },
  { path: '/buyer/product/:id',  component: BuyerProductDetails },
  { path: '/buyer/insight/:id',  component: BuyerInsight },
  { path: '/buyer/artist/:id',   component: BuyerArtist },
  { path: '/buyer/checkout',     component: BuyerCheckout },
  
  // Default redirect
  { path: '/:pathMatch(.*)*', redirect: '/buyer/dashboard' },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

export default router