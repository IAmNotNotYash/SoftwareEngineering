// API functions for Buyer frontend (Bridged to real backend)
import { getCatalogues, getCatalogue as getRealCatalogue } from './catalogue.js'
import { getProducts, getArtists, getProductDetails as getRealProductDetails } from './commerce.js'
import { getPosts } from './social.js'

export const getDashboardStats = async () => {
  // In a real app, this might be a specific endpoint. 
  // For now, we'll return empty/computed stats to avoid breaking the UI.
  return {
    followedArtists: 0,
    favoriteProducts: 0,
    recentOrders: 0,
    upcomingDeliveries: 0,
  }
}

export const getRecentStories = async () => {
  // Map real catalogues to "Stories" format if needed, or fetch stories/posts
  const catalogues = await getCatalogues({ status: 'live' })
  return catalogues.slice(0, 3).map(c => ({
    id: c.id,
    title: c.title,
    artist: c.artist_name,
    date: c.published_at ? new Date(c.published_at).toLocaleDateString() : 'Recently',
    cover: c.cover_photo_url ? `http://localhost:5000${c.cover_photo_url}` : null
  }))
}

export const getAllCatalogues = async () => {
  const catalogues = await getCatalogues({ status: 'live' })
  return catalogues.map(c => ({
    id: c.id,
    title: c.title,
    artist: c.artist_name,
    date: c.published_at ? new Date(c.published_at).toLocaleDateString() : 'Recently',
    cover: c.cover_photo_url ? `http://localhost:5000${c.cover_photo_url}` : null
  }))
}

export const getCatalogue = async (id) => {
  const c = await getRealCatalogue(id)
  return {
    id: c.id,
    title: c.title,
    date: c.published_at ? new Date(c.published_at).toLocaleDateString() : 'Recently',
    cover: c.cover_photo_url ? `http://localhost:5000${c.cover_photo_url}` : null,
    artist: {
      name: c.artist_name,
      avatar: c.artist_profile_image ? `http://localhost:5000${c.artist_profile_image}` : null,
      followers: c.stats?.total_likes || 0
    },
    philosophy: c.philosophy,
    artistNote: c.artist_note,
    stories: (c.stories || []).map(s => ({
      ...s,
      cover_image_url: s.cover_image_url ? (s.cover_image_url.startsWith('http') ? s.cover_image_url : `http://localhost:5000${s.cover_image_url}`) : null
    })),
    products: (c.products || []).map(p => ({
      id: p.id,
      title: p.title,
      artist_name: p.artist_name,
      price: p.price,
      image: p.image ? (p.image.startsWith('http') ? p.image : `http://localhost:5000${p.image}`) : null,
      in_stock: p.in_stock
    }))
  }
}

export const getProductDetails = async (id) => {
  const p = await getRealProductDetails(id)
  return {
    id: p.id,
    title: p.title,
    artist: {
      name: p.artist_name,
      avatar: p.artist_avatar ? (p.artist_avatar.startsWith('http') ? p.artist_avatar : `http://localhost:5000${p.artist_avatar}`) : null
    },
    price: p.price,
    image: p.image ? (p.image.startsWith('http') ? p.image : `http://localhost:5000${p.image}`) : null,
    gallery: (p.gallery || []).map(url => url.startsWith('http') ? url : `http://localhost:5000${url}`),
    description: p.description,
    materials: p.materials,
    dimensions: p.dimensions,
    in_stock: p.in_stock
  }
}

export const getArtistsToFollow = async () => {
  const artists = await getArtists()
  return artists.slice(0, 4).map(a => ({
    id: a.id,
    name: a.name,
    category: a.category || 'Artist',
    followers: a.followers || 0,
    avatar: a.avatar ? `http://localhost:5000${a.avatar}` : null
  }))
}

export const getAllArtists = async () => {
  const artists = await getArtists()
  return artists.map(a => ({
    id: a.id,
    name: a.name,
    category: a.category || 'Artist',
    followers: a.followers || 0,
    avatar: a.avatar ? `http://localhost:5000${a.avatar}` : null
  }))
}

export const getArtInsights = async () => {
  const posts = await getPosts({ type: 'insight' })
  return posts.map(p => ({
    id: p.id,
    title: p.title,
    artist: p.artist_name,
    excerpt: p.body.substring(0, 150) + '...',
    image: p.cover_image_url ? `http://localhost:5000${p.cover_image_url}` : null
  }))
}

export const getCartItems = async () => {
  // This is usually handled by the cart store via commerce.js
  return []
}

export const getFeaturedProducts = async () => {
  const products = await getProducts()
  return products.slice(0, 3).map(p => ({
    id: p.id,
    title: p.title,
    artist_name: p.artist_name,
    price: p.price,
    image: p.image ? (p.image.startsWith('http') ? p.image : `http://localhost:5000${p.image}`) : null,
    in_stock: p.in_stock
  }))
}

// Fixed getArtistDetails to call the real backend
import { getArtist as getRealArtist } from './commerce.js'
export const getArtistDetails = async (id) => {
  const a = await getRealArtist(id)
  return {
    id: a.id,
    name: a.name,
    location: a.location || 'Indian Artisan',
    bio: a.bio || '',
    profileImage: a.avatar ? `http://localhost:5000${a.avatar}` : null,
    coverImage: a.cover_image_url ? `http://localhost:5000${a.cover_image_url}` : null,
    followers: a.followers || 0,
    catalogues: (a.catalogues || []).map(c => ({
      ...c,
      cover: c.cover_photo_url ? `http://localhost:5000${c.cover_photo_url}` : null,
      date: c.published_at ? new Date(c.published_at).toLocaleDateString() : 'Active'
    })),
    products: (a.products || []).map(p => ({
      ...p,
      image: p.image ? (p.image.startsWith('http') ? p.image : `http://localhost:5000${p.image}`) : null
    }))
  }
}

export const getFollowedArtists = async () => {
  // This would need a "get following" endpoint
  return []
}

export const getBuyerProfile = async () => {
  // This would call /api/auth/profile or similar
  return null
}
