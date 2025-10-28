// API service для взаимодействия с backend
import type { User, TestResult, TestResultCreate, LeaderboardEntry, TokenResponse } from '@/shared/types/api'

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8001'

class ApiService {
  private token: string | null

  constructor() {
    this.token = localStorage.getItem('token')
  }

  setToken(token: string) {
    this.token = token
    localStorage.setItem('token', token)
  }

  clearToken() {
    this.token = null
    localStorage.removeItem('token')
    localStorage.removeItem('username')
  }

  private getHeaders(): Record<string, string> {
    const headers: Record<string, string> = {
      'Content-Type': 'application/json',
    }
    if (this.token) {
      headers['Authorization'] = `Bearer ${this.token}`
    }
    return headers
  }

  private async request<T>(endpoint: string, options: RequestInit = {}): Promise<T> {
    const response = await fetch(`${API_URL}${endpoint}`, {
      ...options,
      headers: {
        ...this.getHeaders(),
        ...options.headers,
      },
    })

    if (!response.ok) {
      const error = await response.json().catch(() => ({ detail: 'Unknown error' }))
      throw new Error(error.detail || `HTTP error! status: ${response.status}`)
    }

    return response.json()
  }

  // Auth
  async register(username: string, password: string): Promise<TokenResponse> {
    const data = await this.request<TokenResponse>('/api/auth/register', {
      method: 'POST',
      body: JSON.stringify({ username, password }),
    })
    this.setToken(data.access_token)
    localStorage.setItem('username', data.username)
    return data
  }

  async login(username: string, password: string): Promise<TokenResponse> {
    const formData = new URLSearchParams()
    formData.append('username', username)
    formData.append('password', password)

    const response = await fetch(`${API_URL}/api/auth/login`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
      },
      body: formData,
    })

    if (!response.ok) {
      const error = await response.json().catch(() => ({ detail: 'Unknown error' }))
      throw new Error(error.detail || 'Login failed')
    }

    const data = await response.json()
    this.setToken(data.access_token)
    localStorage.setItem('username', data.username)
    return data
  }

  async getCurrentUser(): Promise<User> {
    return this.request<User>('/api/users/me')
  }

  // Words
  async getWords(limit: number = 100): Promise<string[]> {
    return this.request<string[]>(`/api/words?limit=${limit}`)
  }

  // Test Results
  async saveTestResult(result: TestResultCreate): Promise<TestResult> {
    return this.request<TestResult>('/api/results', {
      method: 'POST',
      body: JSON.stringify(result),
    })
  }

  async getUserResults(username: string, limit: number = 50): Promise<TestResult[]> {
    return this.request<TestResult[]>(`/api/results/user/${username}?limit=${limit}`)
  }

  async getUserProfile(username: string): Promise<User> {
    return this.request<User>(`/api/profile/${username}`)
  }

  // Leaderboard
  async getLeaderboardWpm(limit: number = 100): Promise<LeaderboardEntry[]> {
    return this.request<LeaderboardEntry[]>(`/api/leaderboard/wpm?limit=${limit}`)
  }

  async getLeaderboardAccuracy(limit: number = 100): Promise<LeaderboardEntry[]> {
    return this.request<LeaderboardEntry[]>(`/api/leaderboard/accuracy?limit=${limit}`)
  }
}

export const apiService = new ApiService()
