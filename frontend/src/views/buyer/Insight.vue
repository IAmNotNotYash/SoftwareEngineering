<template>
  <div>
    <BuyerNavbar />
    
    <div class="page-container article-container">
      <!-- Breadcrumb -->
      <div class="breadcrumb">
        <RouterLink to="/buyer/dashboard">Dashboard</RouterLink>
        <span class="separator">/</span>
        <span class="current">Art Insight</span>
      </div>

      <article class="insight-article">
        <div class="article-header">
          <div class="artist-meta">By <strong>Luna Ceramics</strong></div>
          <h1 class="article-title">The Deep Roots of Terracotta</h1>
          <div class="article-date">Published 3 days ago</div>
        </div>

        <div class="hero-image" style="background-image: url('https://images.unsplash.com/photo-1610701596007-11502861dcfa?auto=format&fit=crop&q=80&w=1200')"></div>

        <div class="article-body">
          <p class="lead-paragraph">Terracotta has been a vital part of human history since 24,000 BC. In this post, I explore how I source local regional clays to honor that tradition.</p>
          
          <p>Long before glazes and sophisticated kiln technologies existed, early human settlements relied on the natural earth baked in rudimentary fire pits. The porous nature of the fired earth was imperfect, yet perfectly suited for cooling water in hot climates. It's this raw, unfiltered connection to the planet's surface that continually draws me back to terracotta as my primary medium.</p>

          <blockquote>"There is an honesty in unglazed clay. It hides nothing. Every pinch, every coil, and every burn mark from the kiln remains as a permanent record of its creation."</blockquote>

          <h2>Sourcing the Clay</h2>
          <p>Instead of purchasing commercially mixed clays, I spend weeks during the dry season visiting local riverbanks and exposed hillsides. The regional clay here is rich in iron oxide, which gives it that signature rusty, sunset-orange hue when fired. Processing it takes time—slaking, sieving, and aging the clay for months—but the result is a material entirely unique to this geographical coordinate.</p>
          
          <img src="https://images.unsplash.com/photo-1620189507195-68309c04c4d0?auto=format&fit=crop&q=80&w=800" class="inline-image" />

          <h2>The Firing Process</h2>
          <p>We fire our pieces using a traditional wood-fired technique. The fluctuating temperatures and the ash that settles on the pieces during the firing create unpredictable flashes of color—blacks, grays, and deep reds—meaning no two vessels can ever be identical.</p>

          <p>When you hold one of these pieces, you are holding a fragment of the landscape, transformed by heat and human hands.</p>
        </div>
      </article>
    </div>
  </div>
</template>

<script setup>
import BuyerNavbar from '../../components/BuyerNavbar.vue'
// Note: In a real app, you would fetch the specific insight using route.params.id
// For this mock, we are displaying static beautiful article content.
</script>

<style scoped>
.article-container {
  max-width: 800px;
}

.breadcrumb {
  font-size: 13px;
  color: var(--color-text-muted);
  margin-bottom: 40px;
}

.breadcrumb a {
  color: var(--color-text-muted);
  text-decoration: none;
}

.breadcrumb a:hover {
  color: var(--color-primary);
}

.separator {
  margin: 0 8px;
  color: var(--color-border);
}

.current {
  color: var(--color-text-dark);
  font-weight: 500;
}

.article-header {
  margin-bottom: 40px;
  text-align: center;
}

.artist-meta {
  font-size: 14px;
  color: var(--color-primary);
  text-transform: uppercase;
  letter-spacing: 1px;
  margin-bottom: 16px;
}

.article-title {
  font-size: 48px;
  line-height: 1.1;
  margin-bottom: 24px;
}

.article-date {
  font-size: 14px;
  color: var(--color-text-muted);
}

.hero-image {
  width: 100%;
  height: 400px;
  background-size: cover;
  background-position: center;
  border-radius: 12px;
  margin-bottom: 60px;
}

.article-body {
  font-size: 18px;
  line-height: 1.8;
  color: var(--color-text-body);
}

.lead-paragraph {
  font-size: 22px;
  line-height: 1.6;
  font-family: var(--font-heading);
  color: var(--color-text-dark);
  margin-bottom: 40px;
}

.article-body p {
  margin-bottom: 30px;
}

.article-body h2 {
  font-size: 28px;
  margin-top: 60px;
  margin-bottom: 24px;
}

.article-body blockquote {
  margin: 60px 0;
  padding: 0 40px;
  font-size: 24px;
  line-height: 1.5;
  font-family: var(--font-heading);
  font-style: italic;
  color: var(--color-primary);
  border-left: 4px solid var(--color-primary);
}

.inline-image {
  width: 100%;
  border-radius: 8px;
  margin: 40px 0;
}
</style>
