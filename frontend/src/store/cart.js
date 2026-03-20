import { reactive, computed } from 'vue'

export const cartState = reactive({
  items: [
    { 
      id: 101, 
      title: "Handcrafted Ceramic Vase", 
      artist: "Luna Ceramics", 
      price: 4500, 
      quantity: 1, 
      image: "https://images.unsplash.com/photo-1610701596007-11502861dcfa?auto=format&fit=crop&q=80&w=800" 
    },
    { 
      id: 102, 
      title: "Abstract Canvas Art", 
      artist: "Mihir Desai", 
      price: 12000, 
      quantity: 2, 
      image: "https://images.unsplash.com/photo-1541961017774-22349e4a1262?auto=format&fit=crop&q=80&w=800" 
    }
  ],
  shipping: 500,

  addItem(product) {
    const existing = this.items.find(i => i.id === product.id)
    if (existing) {
      existing.quantity += 1
    } else {
      this.items.push({
        id: product.id,
        title: product.title,
        artist: typeof product.artist === 'string' ? product.artist : (product.artist?.name || 'Unknown Artist'),
        price: product.price,
        quantity: 1,
        image: product.image
      })
    }
  },
  
  removeItem(id) {
    const index = this.items.findIndex(i => i.id === id)
    if (index !== -1) {
      this.items.splice(index, 1)
    }
  },
  
  updateQuantity(id, delta) {
    const item = this.items.find(i => i.id === id)
    if (item) {
      item.quantity += delta
      if (item.quantity < 1) item.quantity = 1
    }
  },
  
  clearCart() {
    this.items = []
  }
})

export const cartSubtotal = computed(() => {
  return cartState.items.reduce((total, item) => total + (item.price * item.quantity), 0)
})

export const cartTotal = computed(() => {
  return cartSubtotal.value > 0 ? cartSubtotal.value + cartState.shipping : 0
})
