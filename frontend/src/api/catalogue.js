const API_URL = 'http://127.0.0.1:5000/api/catalogues'

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
  // so we must remove Content-Type if we're sending a FormData object
  if (options.body instanceof FormData) {
    delete headers['Content-Type']
  }

  const res = await fetch(`${API_URL}${path}`, {
    ...options,
    headers
  })
  return handleResponse(res)
}

// ── Browse ────────────────────────────────────────────────────────────────────
export function getCatalogues({ status = 'live', artist_id = '', user_id = '', search = '' } = {}) {
  const params = new URLSearchParams()
  if (status) params.set('status', status)
  if (artist_id) params.set('artist_id', artist_id)
  if (user_id) params.set('user_id', user_id)
  if (search) params.set('search', search)
  const qs = params.toString()
  return request(`${qs ? '?' + qs : ''}`)
}

export function getCatalogueCategories() {
  return request('/categories')
}

// ── Detail (also records a view) ──────────────────────────────────────────────
export function getCatalogue(id) {
  return request(`/${id}`)
}

export function getCatalogueFeed() {
  return request('/feed')
}

// ── Artist CRUD ───────────────────────────────────────────────────────────────
export function createCatalogue(payload) {
  return request('', { method: 'POST', body: JSON.stringify(payload) })
}

export function updateCatalogue(id, payload) {
  return request(`/${id}`, { method: 'PATCH', body: JSON.stringify(payload) })
}

export function deleteCatalogue(id) {
  return request(`/${id}`, { method: 'DELETE' })
}

// ── Like / Unlike ─────────────────────────────────────────────────────────────
export function likeCatalogue(id) {
  return request(`/${id}/like`, { method: 'POST' })
}

export function unlikeCatalogue(id) {
  return request(`/${id}/like`, { method: 'DELETE' })
}

export function checkLike(id) {
  return request(`/${id}/like`, { method: 'GET' })
}

// ── Visuals Upload ────────────────────────────────────────────────────────────
export function uploadCatalogueCover(id, file) {
  const fd = new FormData()
  fd.append('file', file)
  return request(`/${id}/upload-cover`, {
    method: 'POST',
    body: fd
  })
}

export function uploadStoryFrame(id, file) {
  const fd = new FormData()
  fd.append('file', file)
  return request(`/${id}/upload-story`, {
    method: 'POST',
    body: fd
  })
}
