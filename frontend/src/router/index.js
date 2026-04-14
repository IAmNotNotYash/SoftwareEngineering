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
  { path: '/admin/dashboard',    component: AdminDashboard, meta: { requiresAuth: true, role: 'admin' } },
  { path: '/admin/verification', component: AdminVerification, meta: { requiresAuth: true, role: 'admin' } },
  { path: '/admin/artists',      component: AdminArtists, meta: { requiresAuth: true, role: 'admin' } },
  { path: '/admin/buyers',       component: AdminBuyers, meta: { requiresAuth: true, role: 'admin' } },
  { path: '/admin/orders',       component: AdminOrders, meta: { requiresAuth: true, role: 'admin' } },
  { path: '/admin/analytics',    component: AdminAnalytics, meta: { requiresAuth: true, role: 'admin' } },
  
  // Buyer routes
  { path: '/buyer/dashboard',    component: BuyerDashboard, meta: { requiresAuth: true, role: 'buyer' } },
  { path: '/buyer/products',     component: BuyerProducts, meta: { requiresAuth: true, role: 'buyer' } },
  { path: '/buyer/orders',       component: BuyerOrders, meta: { requiresAuth: true, role: 'buyer' } },
  { path: '/buyer/cart',         component: BuyerCart, meta: { requiresAuth: true, role: 'buyer' } },
  { path: '/buyer/catalogue/:id',component: BuyerCatalogue, meta: { requiresAuth: true, role: 'buyer' } },
  { path: '/buyer/product/:id',  component: BuyerProductDetails, meta: { requiresAuth: true, role: 'buyer' } },
  { path: '/buyer/insight/:id',  component: BuyerInsight, meta: { requiresAuth: true, role: 'buyer' } },
  { path: '/buyer/artist/:id',   component: BuyerArtist, meta: { requiresAuth: true, role: 'buyer' } },
  { path: '/buyer/checkout',     component: BuyerCheckout, meta: { requiresAuth: true, role: 'buyer' } },
  { path: '/buyer/following',    component: BuyerFollowing, meta: { requiresAuth: true, role: 'buyer' } },
  { path: '/buyer/profile',      component: BuyerProfile, meta: { requiresAuth: true, role: 'buyer' } },
  
  // Artist routes
  { path: '/artist/dashboard',    component: ArtistDashboard, meta: { requiresAuth: true, role: 'artist' } },
  { path: '/artist/catalogues',     component: ArtistCampaign, meta: { requiresAuth: true, role: 'artist' }  },
  { path: '/artist/newcatalogue',     component: ArtistNewCampaign, meta: { requiresAuth: true, role: 'artist' }  },
  { path: '/artist/edit-catalogue/:id', component: ArtistNewCampaign, meta: { requiresAuth: true, role: 'artist' }  },
  { path: '/artist/products',     component: ArtistProducts, meta: { requiresAuth: true, role: 'artist' }  },
  { path: '/artist/sendouts',     component: ArtistSendOuts, meta: { requiresAuth: true, role: 'artist' }  },
  { path: '/artist/orders',     component: ArtistOrders, meta: { requiresAuth: true, role: 'artist' }  },
  { path: '/artist/story',     component: ArtistStory, meta: { requiresAuth: true, role: 'artist' }  },
  { path: '/artist/profile',     component: () => import('../views/artist/Profile.vue'), meta: { requiresAuth: true, role: 'artist' } },

  // Default redirect
  { path: '/:pathMatch(.*)*', redirect: '/' },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

// Global Navigation Guard
router.beforeEach((to) => {
  // DEV PURPOSES: Automatically set artist session if no token is found
  if (!sessionStorage.getItem('token')) {
    sessionStorage.setItem('token', 'dev-artist-token');
    sessionStorage.setItem('user', JSON.stringify({ 
      id: 'dev-artist-id', 
      email: 'test@artist.com', 
      role: 'artist',
      full_name: 'Test Artist',
      brand_name: 'Test Brand'
    }));
  }

  // To avoid circular dependency during store init, we get sessionStorage directly
  const token = sessionStorage.getItem('token')
  const user = JSON.parse(sessionStorage.getItem('user') || 'null')

  if (to.meta.requiresAuth && !token) {
    return { path: '/auth/login' }
  }

  if (to.meta.role && user && user.role !== to.meta.role) {
    // Redirect to correct dashboard
    if (user.role === 'admin') return { path: '/admin/dashboard' }
    if (user.role === 'artist') return { path: '/artist/dashboard' }
    if (user.role === 'buyer') return { path: '/buyer/dashboard' }
    return { path: '/' }
  }
})

export default router
