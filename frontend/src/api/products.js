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
  const headers = { ...authHeaders(), ...(options.headers || {}) }
  
  // Browsers automatically set the correct boundary for FormData
  if (options.body instanceof FormData) {
    delete headers['Content-Type']
  }

  const res = await fetch(`${API_URL}${path}`, {
    ...options,
    headers
  })
  return handleResponse(res)
}

/**
 * Fetch all products
 * @param {Object} params - { category, search, artist_id }
 */
export function getProducts(params = {}) {
  const qs = new URLSearchParams(params).toString()
  return request(`/products${qs ? '?' + qs : ''}`)
}

export function getProduct(id) {
  return request(`/products/${id}`)
}

export function createProduct(payload) {
  return request('/products', {
    method: 'POST',
    body: JSON.stringify(payload)
  })
}

export function updateProduct(id, payload) {
  return request(`/products/${id}`, {
    method: 'PATCH',
    body: JSON.stringify(payload)
  })
}

export function deleteProduct(id) {
  return request(`/products/${id}`, {
    method: 'DELETE'
  })
}

/**
 * Add an image to a product
 * @param {string} productId
 * @param {Object} imageData - { image_url, is_primary, sort_order }
 */
export function addProductImage(productId, imageData) {
  return request(`/products/${productId}/images`, {
    method: 'POST',
    body: JSON.stringify(imageData)
  })
}

export function deleteProductImage(productId, imageId) {
  return request(`/products/${productId}/images/${imageId}`, {
    method: 'DELETE'
  })
}

export function uploadProductImageFile(id, file) {
  const fd = new FormData()
  fd.append('file', file)
  return request(`/products/${id}/upload-image`, {
    method: 'POST',
    body: fd
  })
}
