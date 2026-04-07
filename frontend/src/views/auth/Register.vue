<template>
  <div class="auth-page">
    <div class="auth-shell">
      <section class="auth-panel">
        <div class="panel-card">
          <RouterLink to="/" class="brand-mark">Kala</RouterLink>
          <p class="panel-kicker">Join The Platform</p>
          <h1 class="panel-title">Create your account</h1>
          <p class="panel-copy">
            Set up a buyer profile to discover craft-led collections and shop directly from
            artists. Additional profile verification can be added later.
          </p>

          <form class="auth-form" @submit.prevent="handleRegister">
            <div class="grid-two">
              <label class="field">
                <span>First Name</span>
                <input v-model="form.firstName" type="text" placeholder="Aarav" />
              </label>

              <label class="field">
                <span>Last Name</span>
                <input v-model="form.lastName" type="text" placeholder="Sharma" />
              </label>
            </div>

            <label class="field">
              <span>Email Address</span>
              <input v-model="form.email" type="email" placeholder="name@example.com" />
            </label>

            <div class="grid-two">
              <label class="field">
                <span>Password</span>
                <input v-model="form.password" type="password" placeholder="Create a password" />
              </label>

              <label class="field">
                <span>Confirm Password</span>
                <input v-model="form.confirmPassword" type="password" placeholder="Re-enter password" />
              </label>
            </div>

            <label class="field">
              <span>Account Type</span>
              <select v-model="form.accountType">
                <option value="buyer">Buyer</option>
                <option value="artist">Artist</option>
              </select>
            </label>

            <label class="field" v-if="form.accountType === 'artist'">
              <span>Brand Name</span>
              <input v-model="form.brandName" type="text" placeholder="e.g. Luna Ceramics" />
            </label>

            <label class="consent">
              <input v-model="acceptTerms" type="checkbox" />
              <span>I agree to the placeholder terms, privacy policy, and marketplace guidelines.</span>
            </label>

            <p v-if="statusMessage" class="status-message">{{ statusMessage }}</p>

            <button type="submit" class="primary-btn">Create Account</button>
          </form>

          <p class="switch-copy">
            Already have an account?
            <RouterLink to="/auth/login">Login here</RouterLink>
          </p>
        </div>
      </section>

      <section class="auth-showcase">
        <div>
          <p class="eyebrow">Why Kala</p>
          <h2 class="showcase-title">A marketplace shaped by stories, culture, and craft.</h2>
          <p class="showcase-copy">
            Registration is currently a frontend placeholder flow. You can later connect this
            page to backend validation, OTP, or role-based onboarding.
          </p>
        </div>

        <div class="feature-stack">
          <article class="feature-card">
            <h3>Curated Discoverability</h3>
            <p>Browse artist catalogues, product stories, and editorial insight in one place.</p>
          </article>
          <article class="feature-card">
            <h3>Trust Signals</h3>
            <p>Profiles, verification tags, and order history can be connected as backend data arrives.</p>
          </article>
          <article class="feature-card">
            <h3>Flexible Onboarding</h3>
            <p>Use this layout for both buyer and artist registration with placeholder role selection.</p>
          </article>
        </div>
      </section>
    </div>
  </div>
</template>

<script setup>
import { reactive, ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../../stores/auth'
import { registerAPI } from '../../api/auth'

const router = useRouter()
const authStore = useAuthStore()

const form = reactive({
  firstName: '',
  lastName: '',
  email: '',
  password: '',
  confirmPassword: '',
  accountType: 'buyer',
  brandName: '',
})

const acceptTerms = ref(true)
const statusMessage = ref('')

async function handleRegister() {
  if (form.password !== form.confirmPassword) {
    statusMessage.value = "Passwords do not match."
    return
  }
  if (!acceptTerms.value) {
    statusMessage.value = "You must agree to the terms."
    return
  }

  const payload = {
    firstName: form.firstName,
    lastName: form.lastName,
    email: form.email,
    password: form.password,
    role: form.accountType,
  }
  
  if (form.accountType === 'artist') {
    if (!form.brandName) {
      statusMessage.value = "Brand Name is required for Artists."
      return
    }
    payload.brandName = form.brandName
  }

  statusMessage.value = "Creating account..."
  try {
    const data = await registerAPI(payload)
    authStore.setAuth(data)
    
    // Redirect based on role
    if (data.user.role === 'artist') {
      router.push('/artist/dashboard')
    } else {
      router.push('/buyer/dashboard')
    }
  } catch (err) {
    statusMessage.value = err.message
  }
}
</script>

<style scoped>
.auth-page {
  min-height: 100vh;
  background:
    linear-gradient(180deg, #faf7f3 0%, #f5f0e8 100%);
  padding: 40px;
}

.auth-shell {
  max-width: 1180px;
  min-height: calc(100vh - 80px);
  margin: 0 auto;
  display: grid;
  grid-template-columns: 1fr 0.9fr;
  border: 1px solid var(--color-border);
  border-radius: 18px;
  overflow: hidden;
  background: #ffffff;
  box-shadow: var(--shadow-md);
}

.auth-panel {
  padding: 48px 56px;
  display: flex;
  align-items: center;
}

.panel-card {
  width: 100%;
}

.brand-mark {
  display: inline-block;
  margin-bottom: 20px;
  font-family: var(--font-heading);
  font-size: 32px;
  font-weight: 600;
  color: var(--color-primary);
  font-style: italic;
}

.panel-kicker,
.eyebrow {
  font-size: 12px;
  font-weight: 600;
  letter-spacing: 0.14em;
  text-transform: uppercase;
  color: var(--color-primary);
}

.panel-title,
.showcase-title {
  font-size: 44px;
  line-height: 1.08;
  margin: 10px 0 16px;
}

.panel-copy,
.showcase-copy,
.switch-copy,
.feature-card p {
  font-size: 16px;
  line-height: 1.7;
  color: #5b5752;
}

.auth-form {
  margin-top: 28px;
}

.grid-two {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 16px;
}

.field {
  display: block;
  margin-bottom: 18px;
}

.field span {
  display: block;
  margin-bottom: 8px;
  font-size: 14px;
  font-weight: 500;
  color: var(--color-text-dark);
}

.field input,
.field select {
  width: 100%;
  height: 52px;
  padding: 0 16px;
  border: 1px solid var(--color-border);
  border-radius: 10px;
  background: #ffffff;
  color: var(--color-text-body);
  font-size: 15px;
  outline: none;
  transition: border-color 0.2s ease, box-shadow 0.2s ease;
}

.field input:focus,
.field select:focus {
  border-color: var(--color-primary);
  box-shadow: 0 0 0 3px rgba(196, 98, 45, 0.1);
}

.consent {
  display: flex;
  align-items: flex-start;
  gap: 10px;
  margin: 8px 0 20px;
  font-size: 14px;
  line-height: 1.6;
  color: #5b5752;
}

.consent input {
  margin-top: 3px;
  accent-color: var(--color-primary);
}

.status-message {
  margin: 0 0 16px;
  padding: 12px 14px;
  background: var(--color-primary-light);
  border: 1px solid rgba(196, 98, 45, 0.2);
  border-radius: 10px;
  font-size: 14px;
  color: #7a431f;
}

.primary-btn {
  width: 100%;
  height: 52px;
  border: none;
  border-radius: 12px;
  background: var(--color-primary);
  color: var(--color-text-light);
  font-size: 15px;
  font-weight: 600;
  cursor: pointer;
  transition: background 0.2s ease, transform 0.2s ease;
}

.primary-btn:hover {
  background: var(--color-primary-hover);
  transform: translateY(-1px);
}

.switch-copy {
  margin-top: 24px;
}

.auth-showcase {
  padding: 56px;
  background:
    radial-gradient(circle at top, rgba(196, 98, 45, 0.08), transparent 36%),
    linear-gradient(180deg, #f8f3ec 0%, #f1e7dc 100%);
  display: flex;
  flex-direction: column;
  justify-content: space-between;
}

.feature-stack {
  display: grid;
  gap: 16px;
}

.feature-card {
  background: rgba(255, 255, 255, 0.76);
  border: 1px solid rgba(196, 98, 45, 0.14);
  border-radius: 14px;
  padding: 22px;
}

.feature-card h3 {
  margin-bottom: 10px;
  font-size: 22px;
}

@media (max-width: 960px) {
  .auth-page {
    padding: 20px;
  }

  .auth-shell {
    grid-template-columns: 1fr;
  }

  .auth-panel,
  .auth-showcase {
    padding: 32px 24px;
  }

  .grid-two {
    grid-template-columns: 1fr;
    gap: 0;
  }

  .panel-title,
  .showcase-title {
    font-size: 36px;
  }
}
</style>
