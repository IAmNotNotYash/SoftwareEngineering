import { getPlatformTrend, getAnalyticsSnapshot } from './analytics.js'

const BASE_URL = 'http://127.0.0.1:5000/api/admin'

function getAuthHeaders() {
  const token = sessionStorage.getItem('token')
  console.log("DEBUG: Sending token:", token ? token.substring(0, 10) + '...' : 'NONE')
  if (!token || token === 'undefined' || token === 'null') {
    console.warn("No valid JWT token found in sessionStorage")
    return { 'Content-Type': 'application/json' }
  }
  return {
    'Content-Type': 'application/json',
    'Authorization': `Bearer ${token}`
  }
}

async function handleResponse(res) {
  if (res.status === 401) {
    sessionStorage.clear()
    // Optional: add a query param to show a message on login page
    window.location.href = '/auth/login?msg=blocked'
    return new Promise(() => { }) // halt further execution
  }
  let data = {}
  try {
    data = await res.json()
  } catch (e) {
    throw new Error(`Server returned status ${res.status} (invalid JSON)`)
  }

  if (!res.ok) {
    if (res.status === 422) {
      console.error("Authentication error: Please log out and back in.")
    }
    throw new Error(data.error || data.msg || `Request failed with status ${res.status}`)
  }
  return data
}

export async function getDashboardStats() {
  const res = await fetch(`${BASE_URL}/stats`, { headers: getAuthHeaders() })
  return handleResponse(res)
}

export async function getVerificationQueue() {
  const res = await fetch(`${BASE_URL}/verification/queue`, { headers: getAuthHeaders() })
  return handleResponse(res)
}

export async function approveArtist(artistId) {
  const res = await fetch(`${BASE_URL}/verification/${artistId}/status`, {
    method: 'PATCH',
    headers: getAuthHeaders(),
    body: JSON.stringify({ status: 'approved' })
  })
  return handleResponse(res)
}

export async function rejectArtist(artistId, reason) {
  const res = await fetch(`${BASE_URL}/verification/${artistId}/status`, {
    method: 'PATCH',
    headers: getAuthHeaders(),
    body: JSON.stringify({ status: 'rejected', rejection_reason: reason })
  })
  return handleResponse(res)
}

export async function getArtists(limit = 10, offset = 0) {
  const res = await fetch(`${BASE_URL}/artists?limit=${limit}&offset=${offset}`, { headers: getAuthHeaders() })
  return handleResponse(res)
}

export async function suspendArtist(artistId) {
  const res = await fetch(`${BASE_URL}/artists?limit=100`, { headers: getAuthHeaders() })
  const artistsData = await handleResponse(res)
  const artist = artistsData.artists.find(a => a.id === artistId)
  if (!artist) throw new Error('Artist not found')
  return toggleUserSuspension(artist.user_id)
}

export async function getBuyers(limit = 10, offset = 0) {
  const res = await fetch(`${BASE_URL}/buyers?limit=${limit}&offset=${offset}`, { headers: getAuthHeaders() })
  return handleResponse(res)
}

export async function suspendBuyer(buyerId) {
  const res = await fetch(`${BASE_URL}/buyers`, { headers: getAuthHeaders() })
  const buyersData = await handleResponse(res)
  const buyer = buyersData.buyers.find(b => b.id === buyerId)
  if (!buyer) throw new Error('Buyer not found')
  return toggleUserSuspension(buyer.user_id)
}

export async function toggleUserSuspension(userId) {
  const res = await fetch(`${BASE_URL}/users/${userId}/toggle-suspend`, {
    method: 'POST',
    headers: getAuthHeaders()
  })
  return handleResponse(res)
}

export async function getOrders() {
  const token = sessionStorage.getItem('token')
  const res = await fetch('http://127.0.0.1:5000/api/commerce/orders', {
    headers: { 'Authorization': `Bearer ${token}` }
  })
  const data = await handleResponse(res)
  // Mapping display format
  return data.map(o => ({
    id: o.display_id,
    buyer: o.buyer_name,
    artist: o.artist_name,
    total: o.total,
    date: o.created_at.split('T')[0],
    status: o.status
  }))
}

// Added this back for Dashboard.vue
export async function getPlatformAnalytics() {
  return {
    revenueThisMonth: 57600,
    newSignups: 13,
    totalOrders: 17,
    avgOrderValue: 3388,
    revenueOverTime: [
      { month: 'Oct', revenue: 58000 },
      { month: 'Nov', revenue: 62000 },
      { month: 'Dec', revenue: 61000 },
      { month: 'Jan', revenue: 67000 },
      { month: 'Feb', revenue: 75000 },
      { month: 'Mar', revenue: 97000 },
    ],
    ordersByStatus: [
      { status: 'Delivered', count: 6 },
      { status: 'Incomplete', count: 8 },
      { status: 'Cancelled', count: 3 },
    ],
  }
}

export async function getArtistPerformance() {
  const res = await fetch(`${BASE_URL}/analytics/artists`, { headers: getAuthHeaders() })
  return handleResponse(res)
}

export const getAnalytics = async () => {
  try {
    const [stats, trendData, aiSnapshot, performance] = await Promise.all([
      getDashboardStats(),
      getPlatformTrend(),
      getAnalyticsSnapshot('platform'),
      getArtistPerformance()
    ])

    // Map backend trend to frontend chart format
    const labels = trendData.map(t => t.month)
    const revenueData = trendData.map(t => t.total_revenue || t.revenue || 0)
    const ordersData = trendData.map(t => t.total_orders || t.orders || 0)

    const totalRev = stats.totalRevenue || 0
    const totalOrders = stats.totalOrders || 0

    return {
      kpis: [
        { label: 'Total Revenue', value: `₹${totalRev.toLocaleString('en-IN')}` },
        { label: 'Total Orders', value: totalOrders.toString() },
        { label: 'Avg Order Value', value: `₹${totalOrders ? Math.round(totalRev / totalOrders) : 0}` },
        { label: 'Registered Artists', value: (stats.registeredArtists || 0).toString() },
        { label: 'Registered Buyers', value: (stats.registeredBuyers || 0).toString() }
      ],
      artistStats: performance.map(p => ({
        name: `${p.name} (${p.brand})`,
        revenue: p.revenue,
        orders: p.orders
      })),
      revenueTrend: {
        labels: labels,
        data: revenueData
      },
      ordersTrend: {
        labels: labels,
        data: ordersData
      },
      aiSummary: aiSnapshot
    }
  } catch (e) {
    console.error("Failed to fetch real analytics", e)
    return null
  }
}