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

  function logout() {
    token.value = null
    user.value = null
    sessionStorage.removeItem('token')
    sessionStorage.removeItem('user')
  }

  const isAuthenticated = () => !!token.value
  
  return { token, user, setAuth, logout, isAuthenticated }
})
