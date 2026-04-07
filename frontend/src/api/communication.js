const API_URL = 'http://127.0.0.1:5000/api/communication'

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

export function sendBroadcast(payload) {
  return request('/broadcasts', {
    method: 'POST',
    body: JSON.stringify(payload)
  })
}

export function getBroadcasts() {
  return request('/broadcasts')
}

export function getAudienceSize() {
  return request('/audience-size')
}
