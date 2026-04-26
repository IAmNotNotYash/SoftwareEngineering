<template>
  <div class="auth-page">
    <div class="auth-shell">
      <section class="auth-showcase">
        <RouterLink to="/" class="brand-mark">Kala</RouterLink>
        <p class="eyebrow">Collector Access</p>
        <h1 class="showcase-title">Continue your journey with independent craft.</h1>
        <p class="showcase-copy">
          Sign in to browse curated catalogues, track your orders, and keep your favorite
          artists close.
        </p>
      </section>

      <section class="auth-panel">
        <div class="panel-card">
          <p class="panel-kicker">Welcome Back</p>
          <h2 class="panel-title">Login to Kala</h2>
          <p class="panel-copy">
            Use your registered email and password. Social login and password reset can be
            connected later.
          </p>

          <form class="auth-form" @submit.prevent="handleLogin">
            <label class="field">
              <span>Email Address</span>
              <input
                v-model="form.email"
                type="email"
                placeholder="Enter your email"
                autocomplete="email"
              />
            </label>

            <label class="field">
              <span>Password</span>
              <input
                v-model="form.password"
                type="password"
                placeholder="Enter your password"
                autocomplete="current-password"
              />
            </label>

            <div class="form-meta">
              <label class="remember-me">
                <input v-model="rememberMe" type="checkbox" />
                <span>Keep me signed in</span>
              </label>
              <a href="#" @click.prevent>Forgot password?</a>
            </div>

            <p v-if="statusMessage" class="status-message">{{ statusMessage }}</p>

            <button type="submit" class="primary-btn">Sign In</button>
          </form>

          <p class="switch-copy">
            New to Kala?
            <RouterLink to="/auth/register">Create an account</RouterLink>
          </p>
        </div>
      </section>
    </div>
  </div>
</template>

<script setup>
import { reactive, ref, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useAuthStore } from '../../stores/auth'
import { loginAPI } from '../../api/auth'

const router = useRouter()
const route = useRoute()
const authStore = useAuthStore()

const form = reactive({
  email: '',
  password: '',
})

const rememberMe = ref(true)
const statusMessage = ref('')

onMounted(() => {
  if (route.query.msg === 'blocked') {
    statusMessage.value = 'Your session has ended or your account has been blocked.'
  }
})

async function handleLogin() {
  statusMessage.value = 'Logging in...'
  try {
    const data = await loginAPI(form.email, form.password)
    authStore.setAuth(data)
    
    if (data.user.role === 'admin') {
      router.push('/admin/artists')
    } else if (data.user.role === 'artist') {
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
  grid-template-columns: 1.05fr 0.95fr;
  border: 1px solid var(--color-border);
  border-radius: 18px;
  overflow: hidden;
  background: #ffffff;
  box-shadow: var(--shadow-md);
}

.auth-showcase {
  padding: 56px;
  background: linear-gradient(180deg, #f8f3ec 0%, #f1e7dc 100%);
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  gap: 32px;
}

.brand-mark {
  font-family: var(--font-heading);
  font-size: 32px;
  font-weight: 600;
  color: var(--color-primary);
  width: fit-content;
  font-style: italic;
}

.eyebrow,
.panel-kicker,
.showcase-label {
  font-size: 12px;
  font-weight: 600;
  letter-spacing: 0.14em;
  text-transform: uppercase;
  color: var(--color-primary);
}

.showcase-title,
.panel-title {
  font-size: 46px;
  line-height: 1.1;
  margin-bottom: 16px;
}

.showcase-copy,
.panel-copy,
.switch-copy {
  font-size: 16px;
  line-height: 1.7;
  color: #5b5752;
}

.showcase-card {
  max-width: 420px;
  background: rgba(255, 255, 255, 0.82);
  border: 1px solid rgba(196, 98, 45, 0.14);
  border-radius: 14px;
  padding: 24px;
  box-shadow: var(--shadow-sm);
}

.credential-row {
  display: flex;
  justify-content: space-between;
  gap: 20px;
  padding-top: 16px;
  margin-top: 16px;
  border-top: 1px solid var(--color-border);
  font-size: 15px;
  color: var(--color-text-body);
}

.credential-row strong {
  color: var(--color-text-dark);
}

.auth-panel {
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 48px;
}

.panel-card {
  width: 100%;
  max-width: 460px;
}

.auth-form {
  margin-top: 32px;
}

.field {
  display: block;
  margin-bottom: 20px;
}

.field span {
  display: block;
  margin-bottom: 8px;
  font-size: 14px;
  font-weight: 500;
  color: var(--color-text-dark);
}

.field input {
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

.field input:focus {
  border-color: var(--color-primary);
  box-shadow: 0 0 0 3px rgba(196, 98, 45, 0.1);
}

.form-meta {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 16px;
  margin: 4px 0 20px;
  font-size: 14px;
}

.remember-me {
  display: flex;
  align-items: center;
  gap: 8px;
  color: #5b5752;
}

.remember-me input {
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

@media (max-width: 960px) {
  .auth-page {
    padding: 20px;
  }

  .auth-shell {
    grid-template-columns: 1fr;
  }

  .auth-showcase,
  .auth-panel {
    padding: 32px 24px;
  }

  .showcase-title,
  .panel-title {
    font-size: 36px;
  }
}
</style>
