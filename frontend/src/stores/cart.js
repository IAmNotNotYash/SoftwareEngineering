import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { fetchCart, addToCart, updateCartItem, removeFromCart, clearCartAPI } from '../api/commerce.js'

export const useCartStore = defineStore('cart', () => {
  const items = ref([])
  const shipping = 500

  async function loadCart() {
    try {
      const data = await fetchCart()
      items.value = data
    } catch (e) {
      // Not logged in or network error — keep cart empty
      items.value = []
    }
  }

  async function addItem(product_id) {
    await addToCart(product_id, 1)
    await loadCart()
  }

  async function updateItem(cartItemId, quantity) {
    await updateCartItem(cartItemId, quantity)
    await loadCart()
  }

  async function removeItem(cartItemId) {
    await removeFromCart(cartItemId)
    await loadCart()
  }

  async function clearCart() {
    await clearCartAPI()
    items.value = []
  }

  const subtotal = computed(() =>
    items.value.reduce((sum, i) => sum + i.price * i.quantity, 0)
  )

  const total = computed(() =>
    subtotal.value > 0 ? subtotal.value + shipping : 0
  )

  return { items, shipping, subtotal, total, loadCart, addItem, updateItem, removeItem, clearCart }
})
