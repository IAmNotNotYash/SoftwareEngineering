<template>
  <div class="home-page">
    <nav class="topbar">
      <RouterLink to="/" class="brand-mark">
        <img src="../../assets/logo1.png" alt="Kala" class="nav-logo" />
        Kala
      </RouterLink>
      <RouterLink to="/auth/login" class="signin-btn">Sign In</RouterLink>
    </nav>

    <header class="hero-section">
      <div class="hero-inner">
        <h1 class="hero-title">Discover the story behind every piece.</h1>
        <p class="hero-text">
          A marketplace where independent artisans share the craft, passion, and heritage behind
          their handmade creations.
        </p>
        <div class="hero-actions">
          <a href="#artists" class="primary-btn">Explore Artists</a>
          <RouterLink to="/auth/register" class="secondary-btn">Start Selling</RouterLink>
        </div>
      </div>
    </header>

    <main class="page-container">
      <section id="artists" class="content-section">
        <div class="section-heading">
          <h2>Featured Artists</h2>
          <p>Makers who pour their soul into every creation.</p>
        </div>

        <div class="artists-grid">
          <div v-for="artist in artists" :key="artist.name" class="artist-card">
            <div class="artist-avatar" :style="{ backgroundImage: `url(${artist.avatar})` }"></div>
            <div class="artist-info">
              <div class="artist-name">{{ artist.name }}</div>
              <div class="artist-category">{{ artist.category }} • {{ artist.followers }} Followers</div>
              <p class="artist-tagline-text">{{ artist.tagline }}</p>
            </div>
            <RouterLink to="/auth/register" class="follow-btn">Discover More</RouterLink>
          </div>
        </div>
      </section>

      <section id="stories" class="content-section stories-section">
        <div class="section-heading">
          <h2>Trending Stories</h2>
          <p>Discover the craft behind the product.</p>
        </div>

        <div class="stories-grid">
          <div v-for="story in stories" :key="story.title" class="story-card" :style="{ backgroundImage: `url(${story.cover})` }">
            <div class="story-overlay">
              <div class="story-date">{{ story.date }}</div>
              <div class="story-title">{{ story.title }}</div>
              <div class="story-artist">by <span>{{ story.artist }}</span></div>
              <RouterLink to="/auth/register" class="view-story-btn">Read Story</RouterLink>
            </div>
          </div>
        </div>
      </section>
    </main>
  </div>
</template>

<script setup>
const artists = [
  {
    name: 'Nila Handlooms',
    category: 'Textiles',
    tagline: 'Weaving stories into every thread',
    followers: '1,240',
    avatar: 'https://images.unsplash.com/photo-1544005313-94ddf0286df2?auto=format&fit=crop&q=80&w=400'
  },
  {
    name: 'Clay & Co.',
    category: 'Ceramics',
    tagline: 'Earth, water, fire — shaped by hand',
    followers: '890',
    avatar: 'https://images.unsplash.com/photo-1573496359142-b8d87734a5a2?auto=format&fit=crop&q=80&w=400'
  },
  {
    name: 'The Ink Press',
    category: 'Printmaking',
    tagline: 'Block-printed with intention',
    followers: '2,100',
    avatar: 'https://images.unsplash.com/photo-1534528741775-53994a69daeb?auto=format&fit=crop&q=80&w=400'
  },
]

const stories = [
  {
    title: 'The Art of Jamdani Weaving',
    artist: 'Nila Handlooms',
    date: '2 Days Ago',
    cover: 'https://images.unsplash.com/photo-1610701596007-11502861dcfa?auto=format&fit=crop&q=80&w=800'
  },
  {
    title: 'Indigo: From Plant to Fabric',
    artist: 'Nila Handlooms',
    date: '1 Week Ago',
    cover: 'https://images.unsplash.com/photo-1541961017774-22349e4a1262?auto=format&fit=crop&q=80&w=800'
  },
  {
    title: 'From Earth to Table',
    artist: 'Clay & Co.',
    date: '2 Weeks Ago',
    cover: 'https://images.unsplash.com/photo-1620189507195-68309c04c4d0?auto=format&fit=crop&q=80&w=800'
  },
]
</script>

<style scoped>
.home-page {
  min-height: 100vh;
  font-family: 'DM Sans', sans-serif;
}

.topbar {
  position: sticky;
  top: 0;
  z-index: 10;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 60px;
  height: 72px;
  background: var(--color-nav-bg);
  backdrop-filter: blur(16px);
  -webkit-backdrop-filter: blur(16px);
  border-bottom: 1px solid rgba(232, 224, 216, 0.4);
  box-shadow: 0 4px 30px rgba(0, 0, 0, 0.03);
  transition: all 0.3s ease;
}

.brand-mark {
  font-family: 'Playfair Display', serif;
  font-size: 22px;
  font-weight: 700;
  color: #C4622D;
  text-decoration: none;
  display: flex;
  align-items: center;
  gap: 8px;
}

.nav-logo {
  height: 28px;
  width: auto;
  object-fit: contain;
}

.signin-btn,
.primary-btn,
.secondary-btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  padding: 10px 24px;
  border-radius: 8px;
  font-size: 15px;
  font-weight: 600;
  transition: all 0.2s ease;
  text-decoration: none;
}

.signin-btn {
  background: #ffffff;
  color: #1A1A1A;
  border: 1px solid #ddd;
}

.signin-btn:hover {
  border-color: #C4622D;
  color: #C4622D;
}

.secondary-btn {
  background: rgba(255, 255, 255, 0.15);
  backdrop-filter: blur(4px);
  color: #ffffff;
  border: 1px solid rgba(255, 255, 255, 0.5);
}

.secondary-btn:hover {
  background: #ffffff;
  color: #1A1A1A;
  border-color: #ffffff;
}

.primary-btn {
  background: #C4622D;
  color: white;
  border: 1px solid #C4622D;
}

.primary-btn:hover {
  background: #a85427;
}

.hero-section {
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 120px 24px 140px;
  background-image: linear-gradient(to right, rgba(20,20,20,0.7) 0%, rgba(20,20,20,0.4) 100%), url('https://images.unsplash.com/photo-1610701596007-11502861dcfa?auto=format&fit=crop&q=80&w=1920');
  background-size: cover;
  background-position: center;
  border-bottom: 1px solid #e8e0d8;
}

.hero-inner {
  max-width: 980px;
  text-align: center;
}

.hero-title {
  margin: 0 0 24px;
  font-family: 'Playfair Display', serif;
  font-size: 72px;
  line-height: 1.1;
  color: #ffffff;
}

.hero-text {
  margin: 0 auto;
  max-width: 800px;
  font-size: 20px;
  line-height: 1.6;
  color: #e0e0e0;
}

.hero-actions {
  display: flex;
  justify-content: center;
  gap: 16px;
  margin-top: 40px;
}

.page-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 60px 40px;
}

.content-section {
  margin-bottom: 80px;
}

.section-heading {
  margin-bottom: 40px;
  text-align: center;
}

.section-heading h2 {
  font-family: 'Playfair Display', serif;
  font-size: 40px;
  color: #000;
  margin-bottom: 12px;
}

.section-heading p {
  font-size: 18px;
  color: #666;
}

/* Artists Styles matching Buyer Dashboard */
.artists-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 30px;
}

.artist-card {
  background: #ffffff;
  border-radius: 8px;
  padding: 32px 24px;
  border: 1px solid #f0f0f0;
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  transition: transform 0.2s, box-shadow 0.2s;
}

.artist-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.06);
}

.artist-avatar {
  width: 96px;
  height: 96px;
  border-radius: 50%;
  background-size: cover;
  background-position: center;
  margin-bottom: 20px;
  border: 3px solid #fdf2ed;
}

.artist-name {
  font-family: 'Playfair Display', serif;
  font-size: 22px;
  font-weight: 600;
  color: #000;
  margin-bottom: 6px;
}

.artist-category {
  font-family: 'DM Sans', sans-serif;
  font-size: 13px;
  color: #C4622D;
  font-weight: 500;
  margin-bottom: 12px;
}

.artist-tagline-text {
  font-size: 14px;
  color: #666;
  margin-bottom: 24px;
  line-height: 1.5;
}

.follow-btn {
  font-family: 'DM Sans', sans-serif;
  background: #fdf2ed;
  color: #C4622D;
  border: none;
  padding: 10px 24px;
  border-radius: 24px;
  font-size: 14px;
  font-weight: 600;
  text-decoration: none;
  transition: all 0.2s;
  width: 80%;
  text-align: center;
}

.follow-btn:hover {
  background: #C4622D;
  color: white;
}

/* Stories Styles matching Buyer Dashboard */
.stories-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 30px;
}

.story-card {
  background-size: cover;
  background-position: center;
  border-radius: 12px;
  height: 380px;
  position: relative;
  overflow: hidden;
  transition: transform 0.2s, box-shadow 0.2s;
}

.story-card:hover {
  transform: translateY(-6px);
  box-shadow: 0 12px 30px rgba(0,0,0,0.15);
}

.story-overlay {
  position: absolute;
  inset: 0;
  background: linear-gradient(to top, rgba(0,0,0,0.85) 0%, rgba(0,0,0,0.3) 50%, transparent 100%);
  padding: 30px;
  display: flex;
  flex-direction: column;
  justify-content: flex-end;
  color: white;
}

.story-date {
  font-size: 12px;
  text-transform: uppercase;
  letter-spacing: 0.8px;
  color: #e8e0d8;
  margin-bottom: 8px;
  font-weight: 500;
}

.story-title {
  font-family: 'Playfair Display', serif;
  font-size: 26px;
  font-weight: 600;
  margin-bottom: 8px;
  line-height: 1.25;
}

.story-artist {
  font-size: 14px;
  color: #ddd;
  margin-bottom: 24px;
}

.story-artist span {
  color: #fff;
  font-weight: 600;
}

.view-story-btn {
  font-family: 'DM Sans', sans-serif;
  background: rgba(255, 255, 255, 0.15);
  backdrop-filter: blur(4px);
  color: white;
  border: 1px solid rgba(255, 255, 255, 0.4);
  padding: 10px 20px;
  border-radius: 6px;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  align-self: flex-start;
  transition: background 0.2s;
  text-decoration: none;
  text-align: center;
}

.view-story-btn:hover {
  background: white;
  color: #000;
}
</style>
