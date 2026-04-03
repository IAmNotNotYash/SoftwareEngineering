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
  const res = await fetch(`${API_URL}${path}`, {
    ...options,
    headers: { ...authHeaders(), ...(options.headers || {}) },
  })
  return handleResponse(res)
}

// ── Browse ────────────────────────────────────────────────────────────────────
export function getCatalogues({ status = 'live', artist_id = '', search = '' } = {}) {
  const params = new URLSearchParams()
  if (status) params.set('status', status)
  if (artist_id) params.set('artist_id', artist_id)
  if (search) params.set('search', search)
  const qs = params.toString()
  return request(`${qs ? '?' + qs : ''}`)
}

// ── Detail (also records a view) ──────────────────────────────────────────────
export function getCatalogue(id) {
  return request(`/${id}`)
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
