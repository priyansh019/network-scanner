import axios from 'axios'

const BASE_URL = 'https://network-scanner-1-p3wn.onrender.com/api/v1'

const api = axios.create({ baseURL: BASE_URL })

api.interceptors.request.use(config => {
  const token = localStorage.getItem('token')
  if (token) config.headers.Authorization = `Bearer ${token}`
  return config
})

api.interceptors.response.use(
  res => res,
  err => {
    if (err.response?.status === 401) {
      localStorage.removeItem('token')
      window.location.href = '/login'
    }
    return Promise.reject(err)
  }
)

export const auth = {
  register: (email, password) =>
    api.post('/auth/register', { email, password }),
  login: (email, password) =>
    api.post('/auth/login', { email, password }),
}

export const scans = {
  start: (target, ports) =>
    api.post('/scan/start', { target, ports }),
  history: (params) =>
    api.get('/scan/history', { params }),
  getById: (id) =>
    api.get(`/scan/${id}`),
  updateStatus: (id, status) =>
    api.patch(`/scan/${id}/status`, { status }),
}

export default api
