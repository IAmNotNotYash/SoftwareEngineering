// API functions for Buyer frontend (Dummy endpoints)

export const getDashboardStats = async () => {
  // Simulating network delay
  await new Promise((resolve) => setTimeout(resolve, 500))
  return {
    followedArtists: 12,
    favoriteProducts: 34,
    recentOrders: 5,
    upcomingDeliveries: 2,
  }
}

export const getRecentStories = async () => {
  await new Promise((resolve) => setTimeout(resolve, 400))
  return [
    { id: 1, title: "The Earth Tones Collection", artist: "Luna Ceramics", date: "2 days ago", cover: "https://images.unsplash.com/photo-1610701596007-11502861dcfa?auto=format&fit=crop&q=80&w=800" },
    { id: 2, title: "Weaving Shadows", artist: "Mihir Desai", date: "4 days ago", cover: "https://images.unsplash.com/photo-1541961017774-22349e4a1262?auto=format&fit=crop&q=80&w=800" },
    { id: 3, title: "Roots of Bamboo", artist: "Earth Tones", date: "1 week ago", cover: "https://images.unsplash.com/photo-1620189507195-68309c04c4d0?auto=format&fit=crop&q=80&w=800" },
  ]
}

export const getCatalogue = async (id) => {
  await new Promise((resolve) => setTimeout(resolve, 400))
  // Mock data for a specific catalogue
  return {
    id: id,
    title: "The Earth Tones Collection",
    date: "2 days ago",
    cover: "https://images.unsplash.com/photo-1610701596007-11502861dcfa?auto=format&fit=crop&q=80&w=1200",
    artist: {
      name: "Luna Ceramics",
      avatar: "https://images.unsplash.com/photo-1494790108377-be9c29b29330?auto=format&fit=crop&q=80&w=200",
      followers: "4.1k"
    },
    philosophy: "This collection explores the raw textures of unfired clay, celebrating the imperfections and natural hues found deep within the earth. We focus on bridging the gap between natural landscapes and indoor sanctuaries.",
    artistNote: "Every piece in this catalogue was wheel-thrown in my home studio during the monsoon. I let the humidity dictate the drying process, leaving unpredictable and organic warping on the rims. I hope these pieces bring a grounded serenity to your space.",
    products: [
      { id: 101, title: "Handcrafted Ceramic Vase", artist: "Luna Ceramics", price: 4500, image: "https://images.unsplash.com/photo-1610701596007-11502861dcfa?auto=format&fit=crop&q=80&w=800" },
      { id: 108, title: "Raw Clay Pitcher", artist: "Luna Ceramics", price: 3200, image: "https://images.unsplash.com/photo-1603006905003-be475563bc59?auto=format&fit=crop&q=80&w=800" },
      { id: 109, title: "Earthy Serving Bowl", artist: "Luna Ceramics", price: 2100, image: "https://images.unsplash.com/photo-1620189507195-68309c04c4d0?auto=format&fit=crop&q=80&w=800" }
    ]
  }
}

export const getProductDetails = async (id) => {
  await new Promise((resolve) => setTimeout(resolve, 300))
  return {
    id: id,
    title: "Handcrafted Ceramic Vase",
    artist: {
      name: "Luna Ceramics",
      avatar: "https://images.unsplash.com/photo-1494790108377-be9c29b29330?auto=format&fit=crop&q=80&w=200"
    },
    price: 4500,
    image: "https://images.unsplash.com/photo-1610701596007-11502861dcfa?auto=format&fit=crop&q=80&w=800",
    gallery: [
      "https://images.unsplash.com/photo-1610701596007-11502861dcfa?auto=format&fit=crop&q=80&w=800",
      "https://images.unsplash.com/photo-1599839619722-39751411ea63?auto=format&fit=crop&q=80&w=800",
      "https://images.unsplash.com/photo-1613843553250-9fbb34f664db?auto=format&fit=crop&q=80&w=800"
    ],
    description: "A beautifully hand-thrown ceramic vase with subtle, organic textures. The unglazed exterior highlights the earth tones of the raw clay, while the interior is fully sealed to hold water for fresh or dried florals.",
    materials: "Stoneware clay, speckled matte glaze interior",
    dimensions: "12in Height x 6in Diameter (approximate)",
    inStock: true
  }
}

export const getArtistsToFollow = async () => {
  await new Promise((resolve) => setTimeout(resolve, 300))
  return [
    { id: 1, name: "Aurum Studio", category: "Jewelry", followers: "2.4k", avatar: "https://images.unsplash.com/photo-1534528741775-53994a69daeb?auto=format&fit=crop&q=80&w=200" },
    { id: 2, name: "Scribe Co.", category: "Stationery", followers: "840", avatar: "https://images.unsplash.com/photo-1506794778202-cad84cf45f1d?auto=format&fit=crop&q=80&w=200" },
    { id: 3, name: "Lumina", category: "Home Decor", followers: "4.1k", avatar: "https://images.unsplash.com/photo-1494790108377-be9c29b29330?auto=format&fit=crop&q=80&w=200" },
    { id: 4, name: "Canvas & Clay", category: "Mixed Media", followers: "1.1k", avatar: "https://images.unsplash.com/photo-1517841905240-472988babdf9?auto=format&fit=crop&q=80&w=200" },
  ]
}

export const getArtInsights = async () => {
  await new Promise((resolve) => setTimeout(resolve, 300))
  return [
    { id: 1, title: "The Deep Roots of Terracotta", artist: "Luna Ceramics", excerpt: "Terracotta has been a vital part of human history since 24,000 BC. In this post, I explore how I source local regional clays to honor that tradition...", image: "https://images.unsplash.com/photo-1610701596007-11502861dcfa?auto=format&fit=crop&q=80&w=800" },
    { id: 2, title: "Pigments of the Past", artist: "Mihir Desai", excerpt: "Understanding how ancient painters sourced their vibrant ochres and lapis lazuli directly influences how I mix my paints today...", image: "https://images.unsplash.com/photo-1541961017774-22349e4a1262?auto=format&fit=crop&q=80&w=800" },
  ]
}

export const getCartItems = async () => {
  await new Promise((resolve) => setTimeout(resolve, 300))
  return [
    { id: 101, title: "Handcrafted Ceramic Vase", artist: "Luna Ceramics", price: 4500, quantity: 1, image: "https://images.unsplash.com/photo-1610701596007-11502861dcfa?auto=format&fit=crop&q=80&w=800" },
    { id: 102, title: "Abstract Canvas Art", artist: "Mihir Desai", price: 12000, quantity: 2, image: "https://images.unsplash.com/photo-1541961017774-22349e4a1262?auto=format&fit=crop&q=80&w=800" }
  ]
}

export const getFeaturedProducts = async () => {
  await new Promise((resolve) => setTimeout(resolve, 600))
  return [
    { id: 101, title: "Handcrafted Ceramic Vase", artist: "Luna Ceramics", price: 4500, image: "https://images.unsplash.com/photo-1610701596007-11502861dcfa?auto=format&fit=crop&q=80&w=800" },
    { id: 102, title: "Abstract Canvas Art", artist: "Mihir Desai", price: 12000, image: "https://images.unsplash.com/photo-1541961017774-22349e4a1262?auto=format&fit=crop&q=80&w=800" },
    { id: 103, title: "Woven Bamboo Basket", artist: "Earth Tones", price: 2100, image: "https://images.unsplash.com/photo-1620189507195-68309c04c4d0?auto=format&fit=crop&q=80&w=800" },
  ]
}

export const getProducts = async () => {
  await new Promise((resolve) => setTimeout(resolve, 800))
  return [
    { id: 101, title: "Handcrafted Ceramic Vase", artist: "Luna Ceramics", price: 4500, category: "Home Decor", image: "https://images.unsplash.com/photo-1610701596007-11502861dcfa?auto=format&fit=crop&q=80&w=800" },
    { id: 102, title: "Abstract Canvas Art", artist: "Mihir Desai", price: 12000, category: "Fine Art", image: "https://images.unsplash.com/photo-1541961017774-22349e4a1262?auto=format&fit=crop&q=80&w=800" },
    { id: 103, title: "Woven Bamboo Basket", artist: "Earth Tones", price: 2100, category: "Home Decor", image: "https://images.unsplash.com/photo-1620189507195-68309c04c4d0?auto=format&fit=crop&q=80&w=800" },
    { id: 104, title: "Silver Minimalist Necklace", artist: "Aurum Studio", price: 8500, category: "Jewelry", image: "https://images.unsplash.com/photo-1599643478524-fb524458f407?auto=format&fit=crop&q=80&w=800" },
    { id: 105, title: "Leather Bound Journal", artist: "Scribe Co.", price: 1500, category: "Stationery", image: "https://images.unsplash.com/photo-1544816155-12df9643f363?auto=format&fit=crop&q=80&w=800" },
    { id: 106, title: "Hand-poured Soy Candle", artist: "Lumina", price: 900, category: "Home Decor", image: "https://images.unsplash.com/photo-1603006905003-be475563bc59?auto=format&fit=crop&q=80&w=800" },
  ]
}

export const getOrders = async () => {
  await new Promise((resolve) => setTimeout(resolve, 700))
  return [
    { id: "ORD-99382", date: "2026-03-15", total: 6000, status: "Shipped", items: 2 },
    { id: "ORD-99341", date: "2026-03-01", total: 12000, status: "Delivered", items: 1 },
    { id: "ORD-99120", date: "2026-02-18", total: 4500, status: "Delivered", items: 1 },
  ]
}

export const getArtistDetails = async (id) => {
  return new Promise((resolve) => {
    setTimeout(() => {
      resolve({
        id: id,
        name: id === '2' ? 'Tara Singh' : 'Luna Ceramics',
        location: 'Jaipur, Rajasthan',
        bio: 'Creating sustainable, earth-fired ceramics using ancient local techniques. By sourcing regional clays during the dry season, I embrace imperfect materials that create incredibly rugged and unique finished pieces that tie back to human history.',
        profileImage: id === '2' ? 'https://images.unsplash.com/photo-1573496359142-b8d87734a5a2?auto=format&fit=crop&q=80&w=400' : 'https://images.unsplash.com/photo-1544005313-94ddf0286df2?auto=format&fit=crop&q=80&w=400',
        coverImage: 'https://images.unsplash.com/photo-1610701596007-11502861dcfa?auto=format&fit=crop&q=80&w=1200',
        followers: 1240,
        products: [
          { 
            id: 101, 
            title: "Handcrafted Ceramic Vase", 
            artist: "Luna Ceramics", 
            price: 4500, 
            category: "Ceramics",
            inStock: true,
            image: "https://images.unsplash.com/photo-1610701596007-11502861dcfa?auto=format&fit=crop&q=80&w=800" 
          },
          { 
            id: 103, 
            title: "Terracotta Planter", 
            artist: "Luna Ceramics", 
            price: 2800, 
            category: "Ceramics",
            inStock: true,
            image: "https://images.unsplash.com/photo-1620189507195-68309c04c4d0?auto=format&fit=crop&q=80&w=800" 
          }
        ]
      })
    }, 400)
  })
}

export const getFollowedArtists = async () => {
  await new Promise((resolve) => setTimeout(resolve, 300))
  // Mock data representing artists the buyer is currently following
  return [
    { id: 1, name: "Luna Ceramics", category: "Ceramics", followers: "4.1k", avatar: "https://images.unsplash.com/photo-1494790108377-be9c29b29330?auto=format&fit=crop&q=80&w=200" },
    { id: 2, name: "Mihir Desai", category: "Abstract Art", followers: "12k", avatar: "https://images.unsplash.com/photo-1573496359142-b8d87734a5a2?auto=format&fit=crop&q=80&w=200" },
    { id: 3, name: "Earth Tones", category: "Home Goods", followers: "3.2k", avatar: "https://images.unsplash.com/photo-1544005313-94ddf0286df2?auto=format&fit=crop&q=80&w=200" }
  ]
}

export const getBuyerProfile = async () => {
  await new Promise((resolve) => setTimeout(resolve, 300))
  return {
    id: "USR-089",
    name: "Alex Reed",
    email: "alex.reed@example.com",
    phone: "+91 98765 43210",
    joinDate: "January 14, 2026",
    shipping: {
      address: "42 Banyan Tree Avenue, Sector 5",
      city: "Bengaluru",
      state: "Karnataka",
      zip: "560001",
      country: "India"
    },
    payment: {
      cardType: "Visa",
      last4: "4242",
      expiry: "12/28"
    }
  }
}
