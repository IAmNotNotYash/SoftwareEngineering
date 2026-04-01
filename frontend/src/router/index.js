import { createRouter, createWebHistory } from 'vue-router'

// Public views
import HomePage from '../views/homepage/Home.vue'
import LoginPage from '../views/auth/Login.vue'
import RegisterPage from '../views/auth/Register.vue'

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
import BuyerFollowing from '../views/buyer/Following.vue'
import BuyerProfile from '../views/buyer/Profile.vue'

//Artist views
import ArtistDashboard from '../views/artist/Dashboards.vue'
import ArtistCampaign from '../views/artist/Catalogues.vue'
import ArtistNewCampaign from '../views/artist/NewCatalogue.vue'
import ArtistProducts from '../views/artist/Products.vue'
import ArtistSendOuts from '../views/artist/SendOut.vue'
import ArtistOrders from '../views/artist/Orders.vue'
import ArtistStory from '../views/artist/NewStory.vue'

const routes = [
  // Public routes
  { path: '/',                   component: HomePage },
  { path: '/auth/login',         component: LoginPage },
  { path: '/auth/register',      component: RegisterPage },

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
  { path: '/buyer/following',    component: BuyerFollowing },
  { path: '/buyer/profile',      component: BuyerProfile },
  
  // Artist routes
  { path: '/artist/dashboard',    component: ArtistDashboard },
  { path: '/artist/catalogues',     component: ArtistCampaign  },
  { path: '/artist/newcatalogue',     component: ArtistNewCampaign  },
  { path: '/artist/products',     component: ArtistProducts  },
  { path: '/artist/sendouts',     component: ArtistSendOuts  },
  { path: '/artist/orders',     component: ArtistOrders  },
  { path: '/artist/story',     component: ArtistStory  },

  // Default redirect
  { path: '/:pathMatch(.*)*', redirect: '/' },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

export default router
