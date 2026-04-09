const API_BASE_URL = 'http://127.0.0.1:5000/api'

const getHeaders = () => {
    const token = sessionStorage.getItem('token')
    return {
        'Content-Type': 'application/json',
        ...(token ? { 'Authorization': `Bearer ${token}` } : {})
    }
}

const request = async (endpoint, options = {}) => {
    const response = await fetch(`${API_BASE_URL}${endpoint}`, {
        ...options,
        headers: {
            ...getHeaders(),
            ...options.headers,
        },
    })
    
    if (!response.ok) {
        const error = await response.json()
        throw new Error(error.error || 'Network response was not ok')
    }
    
    return response.json()
}

export const getDashboardStats = async () => {
    try {
        const orders = await getOrders()
        return {
            followedArtists: 2,
            favoriteProducts: 0,
            recentOrders: orders.length,
            upcomingDeliveries: orders.filter(o => o.status === 'Processing' || o.status === 'Shipped').length,
        }
    } catch (e) {
        return { followedArtists: 0, favoriteProducts: 0, recentOrders: 0, upcomingDeliveries: 0 }
    }
}

export const getRecentStories = async () => {
    const posts = await request('/social/posts?type=story')
    return posts.map(p => ({
        ...p,
        artist: p.artist_name || 'Artisan',
        date: p.published_at ? new Date(p.published_at).toLocaleDateString() : 'Recently',
        cover: p.cover_image_url
    }))
}

export const getAllCatalogues = async () => {
    const catalogues = await request('/catalogues?status=live')
    return catalogues.map(c => ({
        ...c,
        artist: c.artist_name,
        cover: c.cover_photo_url,
        date: c.published_at ? new Date(c.published_at).toLocaleDateString() : 'Recently'
    }))
}

export const getCatalogue = async (id) => {
    const c = await request(`/catalogues/${id}`)
    return {
        ...c,
        cover: c.cover_photo_url, // For Explore/Dashboard
        artist: {
            name: c.artist_name,
            avatar: c.artist_profile_image,
            followers: "0" 
        }
    }
}

export const getProductDetails = async (id) => {
    const p = await request(`/commerce/products/${id}`)
    return p // Naturally matches ProductDetails.vue
}

export const getArtistsToFollow = async () => {
    const artists = await request('/commerce/artists')
    return artists.map(a => ({
        ...a,
        followers: "0"
    }))
}

export const getAllArtists = async () => {
    return request('/commerce/artists')
}

export const getArtInsights = async () => {
    const posts = await request('/social/posts?type=insight')
    return posts.map(p => ({
        ...p,
        artist: p.artist_name || 'Artisan',
        excerpt: p.body.substring(0, 150) + '...',
        image: p.cover_image_url
    }))
}

export const getCartItems = async () => {
    return request('/commerce/cart')
}

export const getFeaturedProducts = async () => {
    const products = await request('/commerce/products')
    return products.slice(0, 3).map(p => ({
        ...p,
        artist: p.artist_name,
        image: p.image_url || p.image // Backend returned 'image' in to_dict
    }))
}

export const getProducts = async () => {
    return request('/commerce/products')
}

export const getOrders = async () => {
    return request('/commerce/orders')
}

export const getArtistDetails = async (id) => {
    const a = await request(`/commerce/artists/${id}`)
    return {
        ...a,
        profileImage: a.avatar, // Frontend uses profileImage in Artist.vue
        coverImage: a.cover_image_url,
        catalogues: a.catalogues.map(c => ({
            ...c,
            cover: c.cover_photo_url,
            date: 'Recently'
        }))
    }
}

export const getFollowedArtists = async () => {
    // Placeholder - implement backend endpoint /api/social/follows/following
    return []
}

export const getBuyerProfile = async () => {
    const data = await request('/auth/profile')
    const p = data.profile
    const u = data.user
    
    return {
        ...p,
        name: p.full_name,
        email: u.email,
        phone: p.phone,
        joinDate: p.created_at ? new Date(p.created_at).toLocaleDateString('en-IN', { month: 'long', year: 'numeric' }) : "Recently",
        shipping: p.addresses && p.addresses.length > 0 ? {
            address: p.addresses[0].full_address,
            city: p.addresses[0].city,
            state: p.addresses[0].state,
            zip: p.addresses[0].pin_code,
            country: p.addresses[0].country
        } : null,
        payment: p.payment_methods && p.payment_methods.length > 0 ? {
            cardType: p.payment_methods[0].card_type,
            last4: p.payment_methods[0].last_4,
            expiry: `${p.payment_methods[0].expiry_month}/${p.payment_methods[0].expiry_year}`
        } : null
    }
}
