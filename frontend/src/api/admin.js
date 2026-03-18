// src/api/admin.js
// -------------------------------------------------------------
// All admin-related API calls live here.
// Currently returning mock data.
// When the backend is ready, replace the return statements
// with fetch() calls to the Flask API — component code stays
// the same.
// -------------------------------------------------------------

export async function getDashboardStats() {
  return {
    totalRevenue: 57600,
    totalOrders: 17,
    registeredArtists: 3,
    registeredBuyers: 10,
    pendingVerifications: 1,
    activeStories: 7,
  }
}

export async function getVerificationQueue() {
  return [
    { id: 1, name: 'Priya Sharma',   email: 'priya@nilahandlooms.com',  joined: '2024-03-15', status: 'approved' },
    { id: 2, name: 'Arjun Mehta',    email: 'arjun@clayandco.in',       joined: '2024-05-20', status: 'approved' },
    { id: 3, name: 'Meera Krishnan', email: 'meera@theinkpress.co',     joined: '2024-01-10', status: 'pending'  },
  ]
}

export async function approveArtist(artistId) {
  console.log(`[MOCK] Approving artist ${artistId}`)
  return { success: true }
}

export async function rejectArtist(artistId, reason) {
  console.log(`[MOCK] Rejecting artist ${artistId} — reason: ${reason}`)
  return { success: true }
}

export async function getArtists() {
  return [
    { id: 1, name: 'Priya Sharma',   brand: 'Nila Handlooms', email: 'priya@nilahandlooms.com', verified: true,  joined: '2024-03-15' },
    { id: 2, name: 'Arjun Mehta',    brand: 'Clay & Co.',     email: 'arjun@clayandco.in',      verified: true,  joined: '2024-05-20' },
    { id: 3, name: 'Meera Krishnan', brand: 'The Ink Press',  email: 'meera@theinkpress.co',    verified: false, joined: '2024-01-10' },
  ]
}

export async function suspendArtist(artistId) {
  console.log(`[MOCK] Suspending artist ${artistId}`)
  return { success: true }
}

export async function getBuyers() {
  return [
    { id: 1,  name: 'Ananya Gupta',  email: 'ananya@email.com', orders: 2, joined: '2024-06-15' },
    { id: 2,  name: 'Rohan Patel',   email: 'rohan@email.com',  orders: 2, joined: '2024-07-20' },
    { id: 3,  name: 'Sneha Iyer',    email: 'sneha@email.com',  orders: 2, joined: '2024-08-10' },
    { id: 4,  name: 'Kabir Singh',   email: 'kabir@email.com',  orders: 2, joined: '2024-09-05' },
    { id: 5,  name: 'Lakshmi Nair',  email: 'lakshmi@email.com',orders: 2, joined: '2024-10-01' },
    { id: 6,  name: 'Vikram Joshi',  email: 'vikram@email.com', orders: 2, joined: '2024-11-15' },
    { id: 7,  name: 'Divya Menon',   email: 'divya@email.com',  orders: 1, joined: '2024-12-20' },
    { id: 8,  name: 'Aditya Rao',    email: 'aditya@email.com', orders: 2, joined: '2025-01-10' },
    { id: 9,  name: 'Ishita Sharma', email: 'ishita@email.com', orders: 1, joined: '2025-02-01' },
    { id: 10, name: 'Nikhil Das',    email: 'nikhil@email.com', orders: 1, joined: '2025-02-15' },
  ]
}

export async function suspendBuyer(buyerId) {
  console.log(`[MOCK] Suspending buyer ${buyerId}`)
  return { success: true }
}

export async function getOrders() {
  return [
    { id: 'ORD-001', buyer: 'Ananya Gupta', artist: 'Nila Handlooms', total: 4500, date: '2025-02-15', status: 'delivered'  },
    { id: 'ORD-002', buyer: 'Rohan Patel',  artist: 'Clay & Co.',     total: 4700, date: '2025-02-18', status: 'delivered'  },
    { id: 'ORD-003', buyer: 'Sneha Iyer',   artist: 'The Ink Press',  total: 1900, date: '2025-02-20', status: 'incomplete' },
    { id: 'ORD-004', buyer: 'Kabir Singh',  artist: 'The Ink Press',  total: 3600, date: '2025-02-22', status: 'incomplete' },
    { id: 'ORD-005', buyer: 'Lakshmi Nair', artist: 'Nila Handlooms', total: 3450, date: '2025-02-25', status: 'delivered'  },
    { id: 'ORD-006', buyer: 'Vikram Joshi', artist: 'Clay & Co.',     total: 3600, date: '2025-02-28', status: 'incomplete' },
    { id: 'ORD-007', buyer: 'Ananya Gupta', artist: 'The Ink Press',  total: 2250, date: '2025-03-01', status: 'delivered'  },
    { id: 'ORD-008', buyer: 'Aditya Rao',   artist: 'Nila Handlooms', total: 3200, date: '2025-03-02', status: 'incomplete' },
    { id: 'ORD-009', buyer: 'Sneha Iyer',   artist: 'Clay & Co.',     total: 4100, date: '2025-03-03', status: 'delivered'  },
    { id: 'ORD-010', buyer: 'Ishita Sharma',artist: 'The Ink Press',  total: 2750, date: '2025-03-04', status: 'incomplete' },
    { id: 'ORD-011', buyer: 'Divya Menon',  artist: 'Nila Handlooms', total: 1600, date: '2025-03-05', status: 'cancelled'  },
    { id: 'ORD-012', buyer: 'Nikhil Das',   artist: 'Nila Handlooms', total: 4700, date: '2025-03-06', status: 'incomplete' },
    { id: 'ORD-013', buyer: 'Kabir Singh',  artist: 'Clay & Co.',     total: 6000, date: '2025-03-07', status: 'delivered'  },
    { id: 'ORD-014', buyer: 'Vikram Joshi', artist: 'The Ink Press',  total: 1800, date: '2025-03-08', status: 'incomplete' },
    { id: 'ORD-015', buyer: 'Rohan Patel',  artist: 'Clay & Co.',     total: 4200, date: '2025-03-09', status: 'cancelled'  },
  ]
}

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
      { status: 'Delivered',  count: 6 },
      { status: 'Incomplete', count: 8 },
      { status: 'Cancelled',  count: 3 },
    ],
  }
}

export const getAnalytics = async () => {
  await new Promise(resolve => setTimeout(resolve, 300))

  return {
    kpis: [
      { label: 'Total Revenue', value: '₹1,25,000' },
      { label: 'Total Orders', value: '150' },
      { label: 'Active Artists', value: '3' },
      { label: 'Active Buyers', value: '10' },
      { label: 'Avg Order Value', value: '₹833' },
      { label: 'Conversion Rate', value: '4.2%' }
    ],

    artistStats: [
      { name: 'Priya Sharma (Nila Handlooms)', revenue: 45000, orders: 50 },
      { name: 'Arjun Mehta (Clay & Co.)', revenue: 35000, orders: 40 },
      { name: 'Meera Krishnan (The Ink Press)', revenue: 45000, orders: 60 }
    ],

    revenueTrend: {
      labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
      data: [15000, 18000, 22000, 20000, 25000, 30000]
    },

    ordersTrend: {
      labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
      data: [20, 25, 30, 28, 35, 40]
    }
  }
}