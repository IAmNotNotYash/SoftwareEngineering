<template>
  <div class="home-page">
    <nav class="topbar">
      <RouterLink to="/" class="brand-mark">Kala</RouterLink>
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

    <main>
      <section id="artists" class="content-section">
        <div class="section-heading">
          <h2>Featured Artists</h2>
          <p>Makers who pour their soul into every creation.</p>
        </div>

        <div class="artist-grid">
          <article v-for="artist in artists" :key="artist.name" class="artist-card">
            <div class="artist-top">
              <div class="artist-avatar"></div>
              <div>
                <h3>{{ artist.name }}</h3>
                <p class="artist-tagline">{{ artist.tagline }}</p>
              </div>
            </div>
            <p class="artist-copy">{{ artist.copy }}</p>
            <span class="artist-followers">{{ artist.followers }}</span>
          </article>
        </div>
      </section>

      <section id="stories" class="content-section stories-section">
        <div class="section-heading">
          <h2>Trending Stories</h2>
          <p>Discover the craft behind the product.</p>
        </div>

        <div class="story-grid">
          <article v-for="story in stories" :key="story.title" class="story-card">
            <div class="story-cover">Story Cover</div>
            <div class="story-body">
              <h3>{{ story.title }}</h3>
              <p>{{ story.meta }}</p>
            </div>
          </article>
        </div>
      </section>

      <footer class="page-footer">
        <span class="footer-brand">Kala</span>
        <span class="footer-copy">© 2025 Kala. Crafted with intention.</span>
      </footer>
    </main>
  </div>
</template>

<script setup>
const artists = [
  {
    name: 'Nila Handlooms',
    tagline: 'Weaving stories into every thread',
    copy: 'Nila Handlooms is a third-generation textile studio based in Jaipur,...',
    followers: '1,240 followers',
  },
  {
    name: 'Clay & Co.',
    tagline: 'Earth, water, fire — shaped by hand',
    copy: 'Clay & Co. is a ceramics studio in Pondicherry creating functional pottery...',
    followers: '890 followers',
  },
  {
    name: 'The Ink Press',
    tagline: 'Block-printed with intention',
    copy: 'The Ink Press revives the ancient art of block printing from our workshop in...',
    followers: '2,100 followers',
  },
]

const stories = [
  {
    title: 'The Art of Jamdani Weaving',
    meta: 'by Nila Handlooms · 5 slides',
  },
  {
    title: 'Indigo: From Plant to Fabric',
    meta: 'by Nila Handlooms · 5 slides',
  },
  {
    title: 'From Earth to Table',
    meta: 'by Clay & Co. · 6 slides',
  },
]
</script>

<style scoped>
.home-page {
  min-height: 100vh;
  background: #f8f6f2;
}

.topbar {
  position: sticky;
  top: 0;
  z-index: 10;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 14px 24px;
  background: rgba(255, 255, 255, 0.95);
  border-bottom: 1px solid #ddd6cd;
}

.brand-mark {
  font-family: var(--font-heading);
  font-size: 30px;
  font-weight: 600;
  color: var(--color-primary);
  font-style: italic;
}

.signin-btn,
.primary-btn,
.secondary-btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  min-width: 116px;
  height: 46px;
  padding: 0 22px;
  border-radius: 10px;
  font-size: 15px;
  font-weight: 600;
  transition: all 0.2s ease;
}

.signin-btn,
.primary-btn {
  background: var(--color-primary);
  color: var(--color-text-light);
  border: 1px solid var(--color-primary);
}

.signin-btn:hover,
.primary-btn:hover {
  background: var(--color-primary-hover);
  color: var(--color-text-light);
}

.secondary-btn {
  background: #ffffff;
  color: var(--color-text-dark);
  border: 1px solid #ddd6cd;
}

.secondary-btn:hover {
  color: var(--color-primary);
  border-color: var(--color-primary);
}

.hero-section {
  min-height: 76vh;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 52px 24px 124px;
}

.hero-inner {
  max-width: 980px;
  text-align: center;
}

.hero-title {
  margin: 0 0 28px;
  font-size: clamp(72px, 9vw, 96px);
  line-height: 0.96;
  letter-spacing: -0.04em;
  color: #151515;
}

.hero-text {
  margin: 0 auto;
  max-width: 980px;
  font-size: 25px;
  line-height: 1.45;
  color: #5f6673;
}

.hero-actions {
  display: flex;
  justify-content: center;
  gap: 18px;
  flex-wrap: wrap;
  margin-top: 36px;
}

.content-section {
  padding: 34px 20px 120px;
  border-top: 1px solid #ddd6cd;
}

.stories-section {
  padding-bottom: 88px;
}

.section-heading {
  margin-bottom: 48px;
}

.section-heading h2 {
  margin: 0 0 12px;
  font-size: clamp(44px, 5vw, 64px);
  line-height: 1;
  color: #111111;
}

.section-heading p {
  margin: 0;
  font-size: 22px;
  line-height: 1.5;
  color: #5f6673;
}

.artist-grid,
.story-grid {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 26px;
}

.artist-card,
.story-card {
  background: #ffffff;
  border: 1px solid #ddd6cd;
  border-radius: 18px;
  box-shadow: 0 1px 4px rgba(0, 0, 0, 0.04);
}

.artist-card {
  padding: 36px 30px 28px;
}

.artist-top {
  display: flex;
  align-items: flex-start;
  gap: 18px;
  margin-bottom: 22px;
}

.artist-avatar {
  width: 72px;
  height: 72px;
  flex-shrink: 0;
  border-radius: 50%;
  border: 1px solid #efcc83;
  background: linear-gradient(135deg, #ffe7ae 0%, #ffd899 100%);
}

.artist-card h3,
.story-body h3 {
  margin: 0 0 6px;
  font-size: 28px;
  line-height: 1.15;
  color: #222222;
}

.artist-tagline,
.artist-copy,
.artist-followers,
.story-body p {
  font-family: var(--font-body);
  color: #6a6a6a;
}

.artist-tagline {
  margin: 0;
  font-size: 18px;
  line-height: 1.35;
}

.artist-copy {
  margin: 0 0 18px;
  font-size: 17px;
  line-height: 1.5;
}

.artist-followers {
  font-size: 16px;
}

.story-cover {
  height: 220px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-bottom: 1px solid #ddd6cd;
  border-radius: 18px 18px 0 0;
  background: linear-gradient(135deg, #fff0bc 0%, #ffd69b 100%);
  color: #b9a174;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  font-size: 15px;
}

.story-body {
  padding: 24px 26px 22px;
}

.story-body p {
  margin: 0;
  font-size: 17px;
  line-height: 1.45;
}

.page-footer {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 16px;
  padding: 28px 24px 20px;
  border-top: 1px solid #ddd6cd;
  background: #ffffff;
}

.footer-brand {
  font-family: var(--font-heading);
  font-size: 24px;
  color: var(--color-primary);
  font-style: italic;
}

.footer-copy {
  font-size: 18px;
  color: #5f6673;
}

@media (max-width: 960px) {
  .hero-title {
    font-size: 56px;
  }

  .hero-text {
    font-size: 20px;
  }

  .artist-grid,
  .story-grid {
    grid-template-columns: 1fr;
  }

  .section-heading p,
  .footer-copy {
    font-size: 17px;
  }

  .page-footer {
    flex-direction: column;
    align-items: flex-start;
  }
}
</style>
