const API_URL = 'http://127.0.0.1:5000/api/social'

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

export function followArtist(artist_id) {
  return request('/follows', {
    method: 'POST',
    body: JSON.stringify({ artist_id })
  })
}

export function unfollowArtist(artist_id) {
  return request(`/follows/${artist_id}`, { method: 'DELETE' })
}

export function checkFollowStatus(artist_id) {
  return request(`/follows/check/${artist_id}`)
}

export function getFollowing() {
  return request('/following')
}

export function getFollowers() {
  return request('/followers')
}

export async function getPosts({ type = '', artist_id = '' } = {}) {
  const params = new URLSearchParams()
  if (type) params.set('type', type)
  if (artist_id) params.set('artist_id', artist_id)
  const data = await request(`/posts?${params.toString()}`)
  return data.map(p => ({
    ...p,
    cover_image_url: p.cover_image_url ? (p.cover_image_url.startsWith('http') ? p.cover_image_url : `http://localhost:5000${p.cover_image_url}`) : ''
  }))
}

export async function getPost(post_id) {
  const p = await request(`/posts/${post_id}`)
  return {
    ...p,
    cover_image_url: p.cover_image_url ? (p.cover_image_url.startsWith('http') ? p.cover_image_url : `http://localhost:5000${p.cover_image_url}`) : ''
  }
}

export function createPost(payload) {
  return request('/posts', {
    method: 'POST',
    body: JSON.stringify(payload)
  })
}

export function updatePost(post_id, payload) {
  return request(`/posts/${post_id}`, {
    method: 'PATCH',
    body: JSON.stringify(payload)
  })
}

export function deletePost(post_id) {
  return request(`/posts/${post_id}`, { method: 'DELETE' })
}

export function likePost(post_id) {
  return request(`/posts/${post_id}/like`, { method: 'POST' })
}

export function unlikePost(post_id) {
  return request(`/posts/${post_id}/like`, { method: 'DELETE' })
}

export function createReview(payload) {
  return request('/reviews', {
    method: 'POST',
    body: JSON.stringify(payload)
  })
}

export function getReviews(target_type, target_id) {
  return request(`/reviews/${target_type}/${target_id}`)
}
