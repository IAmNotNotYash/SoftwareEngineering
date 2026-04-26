import { defineStore } from 'pinia'
import { ref } from 'vue'

export const useAuthStore = defineStore('auth', () => {
  const token = ref(sessionStorage.getItem('token') || null)
  const user = ref(JSON.parse(sessionStorage.getItem('user')) || null)

  function setAuth(data) {
    if (data.token && data.user) {
      token.value = data.token
      user.value = data.user
      sessionStorage.setItem('token', data.token)
      sessionStorage.setItem('user', JSON.stringify(data.user))
    }
  }

  async function refreshUser() {
    if (!token.value) return
    try {
      const res = await fetch('http://127.0.0.1:5000/api/auth/profile', {
        headers: { 'Authorization': `Bearer ${token.value}` }
      })
      if (res.ok) {
        const profile = await res.json()
        // Update user object with the latest profile data
        const newUser = { 
          ...user.value, 
          name: profile.full_name || profile.name || user.value?.name,
          profile_image_url: profile.profile_image_url 
        }
        user.value = newUser
        sessionStorage.setItem('user', JSON.stringify(newUser))
      }
    } catch (e) {
      console.error("Failed to refresh user profile data", e)
    }
  }

  function logout() {
    token.value = null
    user.value = null
    sessionStorage.removeItem('token')
    sessionStorage.removeItem('user')
  }

  const isAuthenticated = () => !!token.value
  
  return { token, user, setAuth, logout, isAuthenticated, refreshUser }
})
