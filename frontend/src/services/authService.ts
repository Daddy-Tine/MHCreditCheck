import api from './api'

export const authService = {
  async login(email: string, password: string) {
    const formData = new FormData()
    formData.append('username', email)
    formData.append('password', password)

    // Use axios directly for form data (api client might not handle FormData well)
    const response = await axios.post(`${API_URL}/api/v1/auth/login`, formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    })

    const { access_token, refresh_token } = response.data.data
    localStorage.setItem('access_token', access_token)
    localStorage.setItem('refresh_token', refresh_token)

    // Get user info using the api client
    const userResponse = await api.get('/api/v1/auth/me')
    const user = userResponse.data.data

    return { access_token, refresh_token, user }
  },

  async getCurrentUser() {
    const response = await api.get('/api/v1/auth/me')
    return response.data.data
  },

  async register(userData: {
    email: string
    password: string
    full_name: string
    role: string
    bank_id?: number
  }) {
    const response = await api.post('/api/v1/auth/register', userData)
    return response.data.data
  },
}

