// In dev, Vite proxies /api to the backend on port 8000.
// In production the backend serves the built app from the same origin.
const API_BASE = import.meta.env.PROD ? '' : '/api'

export function getToken() {
  return localStorage.getItem('token')
}

export function setToken(token) {
  if (token) localStorage.setItem('token', token)
  else localStorage.removeItem('token')
}

async function request(path, { method = 'GET', body, headers = {}, auth = true } = {}) {
  const finalHeaders = { ...headers }
  const token = getToken()
  if (auth && token) finalHeaders.Authorization = `Bearer ${token}`

  let payload = body
  if (body !== undefined && !(body instanceof URLSearchParams)) {
    finalHeaders['Content-Type'] = 'application/json'
    payload = JSON.stringify(body)
  }

  const res = await fetch(API_BASE + path, { method, headers: finalHeaders, body: payload })

  if (res.status === 401 && auth) setToken(null)

  const text = await res.text()
  let data = null
  try {
    data = text ? JSON.parse(text) : null
  } catch {
    data = text
  }

  if (!res.ok) {
    const detail = (data && (data.detail || data.message || data.error)) || res.statusText
    throw new Error(typeof detail === 'string' ? detail : JSON.stringify(detail))
  }
  return data
}

export const api = {
  // auth
  login: (username, password) =>
    request('/auth/token', {
      method: 'POST',
      body: new URLSearchParams({ username, password }),
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
      auth: false,
    }),
  register: (payload) => request('/auth/creat_user', { method: 'POST', body: payload, auth: false }),

  // profile
  getProfile: () => request('/user/profile'),
  saveProfile: (payload) => request('/user/edit_profile', { method: 'PUT', body: payload }),

  // pet
  getPets: () => request('/pet/read_pet_info'),
  createPet: (payload) => request('/pet/creat_pet', { method: 'POST', body: payload }),

  // points
  getDaily: () => request('/points/daily'),
  getTotal: () => request('/points/total'),

  // targets
  getRecommended: () => request('/targets/recommended'),
  getTargets: () => request('/targets/read_targets'),
  saveTargets: (payload) => request('/targets/add_targets', { method: 'POST', body: payload }),

  // meals
  logMeal: (payload) => request('/meals/log_meals', { method: 'POST', body: payload }),
  getMealTotals: () => request('/meals/today_total_macros'),
  getTodayMeals: () => request('/meals/read_today_meals'),
  deleteMeal: (id) => request(`/meals/delete_meal/${id}`, { method: 'DELETE' }),

  // water
  logWater: (payload) => request('/water/log_water', { method: 'POST', body: payload }),
  getWaterTotals: () => request('/water/today_totals_liters'),
  getTodayWater: () => request('/water/read_today_water'),
  deleteWater: (id) => request(`/water/delete_water/${id}`, { method: 'DELETE' }),

  // sleep
  logSleep: (payload) => request('/sleep/log_sleep', { method: 'POST', body: payload }),
  getSleepTotals: () => request('/sleep/today_totals'),
  getTodaySleep: () => request('/sleep/read_today_sleep'),
  deleteSleep: (id) => request(`/sleep/delete_sleep/${id}`, { method: 'DELETE' }),

  // steps
  logSteps: (payload) => request('/steps/log_steps', { method: 'POST', body: payload }),
  getStepTotals: () => request('/steps/today_totals'),
  getTodaySteps: () => request('/steps/read_today_steps'),
  deleteSteps: (id) => request(`/steps/delete_steps/${id}`, { method: 'DELETE' }),
}

export const LEVELS = [500, 1000, 2000, 3000, 5000, 7500, 10000, 12500, 15000]

export function levelInfo(total) {
  let level = 1
  for (let i = 0; i < LEVELS.length; i++) {
    if (total <= LEVELS[i]) break
    level = i + 2
  }
  if (level > 10) level = 10
  const next = level < 10 ? LEVELS[level - 1] : null
  const prev = level === 1 ? 0 : level === 10 ? LEVELS[8] : LEVELS[level - 2]
  const pct = next ? Math.min(100, Math.round(((total - prev) / (next - prev)) * 100)) : 100
  return { level, next, pct }
}
