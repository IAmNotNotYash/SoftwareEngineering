const API_URL = 'http://127.0.0.1:5000/api/auth'

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
    return new Promise(() => { })
  }
  const data = await res.json()
  if (!res.ok) throw new Error(data.error || 'Request failed')
  return data
}

export async function loginAPI(email, password) {
  const response = await fetch(`${API_URL}/login`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ email, password })
  })
  return handleResponse(response)
}

export async function registerAPI(payload) {
  const response = await fetch(`${API_URL}/register`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload)
  })
  return handleResponse(response)
}

export async function getProfile() {
  const response = await fetch(`${API_URL}/profile`, {
    headers: authHeaders()
  })
  return handleResponse(response)
}

export async function updateProfile(payload) {
  const response = await fetch(`${API_URL}/profile`, {
    method: 'PATCH',
    headers: authHeaders(),
    body: JSON.stringify(payload)
  })
  return handleResponse(response)
}

export async function uploadProfileImage(file, type = 'profile') {
  const formData = new FormData()
  formData.append('file', file)
  
  const token = sessionStorage.getItem('token')
  const response = await fetch(`${API_URL}/profile/upload-image?type=${type}`, {
    method: 'POST',
    headers: {
      ...(token ? { Authorization: `Bearer ${token}` } : {}),
    },
    body: formData
  })
  return handleResponse(response)
}
