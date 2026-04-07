const API_URL = 'http://127.0.0.1:5000/api/commerce'

function authHeaders() {
  const token = sessionStorage.getItem('token')
  return {
    'Content-Type': 'application/json',
    ...(token ? { Authorization: `Bearer ${token}` } : {}),
  }
}

async function handleResponse(res) {
  if (res.status === 401) {
    sessionStorage.clear()
    window.location.href = '/auth/login?msg=blocked'
    return new Promise(() => {})
  }
  const data = await res.json()
  if (!res.ok) throw new Error(data.error || 'Request failed')
  return data
}

async function request(path, options = {}) {
  const res = await fetch(`${API_URL}${path}`, {
    ...options,
    headers: { ...authHeaders(), ...(options.headers || {}) },
  })
  return handleResponse(res)
}

export async function getArtists() {
  return request('/artists')
}

// ── Products ──────────────────────────────────────────────────────────────────
export async function getProducts({ category = '', search = '', artist_id = '' } = {}) {
  const params = new URLSearchParams()
  if (category) params.set('category', category)
  if (search) params.set('search', search)
  if (artist_id) params.set('artist_id', artist_id)
  const qs = params.toString()
  return request(`/products${qs ? '?' + qs : ''}`)
}

export async function getProductDetails(id) {
  return request(`/products/${id}`)
}

// ── Cart ─────────────────────────────────────────────────────────────────────
export async function fetchCart() {
  return request('/cart')
}

export async function addToCart(product_id, quantity = 1) {
  return request('/cart', {
    method: 'POST',
    body: JSON.stringify({ product_id, quantity }),
  })
}

export async function updateCartItem(cartItemId, quantity) {
  return request(`/cart/${cartItemId}`, {
    method: 'PATCH',
    body: JSON.stringify({ quantity }),
  })
}

export async function removeFromCart(cartItemId) {
  return request(`/cart/${cartItemId}`, { method: 'DELETE' })
}

export async function clearCartAPI() {
  return request('/cart', { method: 'DELETE' })
}

// ── Orders ────────────────────────────────────────────────────────────────────
export async function placeOrder(payload) {
  return request('/orders', {
    method: 'POST',
    body: JSON.stringify(payload),
  })
}

export async function getOrders() {
  return request('/orders')
}

export async function getOrderDetails(orderId) {
  return request(`/orders/${orderId}`)
}

export async function getOrderTracking(orderId) {
  return request(`/orders/${orderId}/tracking`)
}
