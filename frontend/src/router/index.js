import { createRouter, createWebHashHistory } from 'vue-router'
import Dashboard from '../pages/Dashboard.vue'
import Campaigns from '../pages/Campaigns.vue'
import NewCampaign from '../pages/NewCampaign.vue'
import Products from '../pages/Products.vue'
import SendOut from '../pages/SendOut.vue'
 
const routes = [
  { path: '/', redirect: '/dashboard' },
  { path: '/dashboard', component: Dashboard },
  { path: '/campaigns', component: Campaigns },
  { path: '/campaigns/new', component: NewCampaign },
  { path: '/products', component: Products },
  { path: '/sendout', component: SendOut },
]
 
export default createRouter({ history: createWebHashHistory(), routes })