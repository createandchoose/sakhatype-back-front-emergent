import { apiClient } from './client'
import type { UserResponse } from './auth'

export interface LeaderboardEntry {
  username: string
  wpm?: number
  accuracy?: number
  total_tests: number
  best_wpm: number
  best_accuracy: number
  level: number
}

export interface TimeModeLeaderboardEntry {
  username: string
  wpm: number
  accuracy: number
  raw: number
  consistency: number
  date: string
  level: number
}

export interface WeeklyXPLeaderboardEntry {
  username: string
  xp_gained: number
  time_typed: number
  last_activity: string
  level: number
}

export const userApi = {
  async getUserProfile(username: string): Promise<UserResponse> {
    return apiClient.request<UserResponse>(`/api/profile/${username}`)
  },
}

export const leaderboardApi = {
  async getLeaderboardWpm(limit: number = 100): Promise<LeaderboardEntry[]> {
    return apiClient.request<LeaderboardEntry[]>(`/api/leaderboard/wpm?limit=${limit}`)
  },

  async getLeaderboardAccuracy(limit: number = 100): Promise<LeaderboardEntry[]> {
    return apiClient.request<LeaderboardEntry[]>(`/api/leaderboard/accuracy?limit=${limit}`)
  },

  async getLeaderboardByTimeMode(timeMode: number, limit: number = 100): Promise<TimeModeLeaderboardEntry[]> {
    return apiClient.request<TimeModeLeaderboardEntry[]>(`/api/leaderboard/time-mode/${timeMode}?limit=${limit}`)
  },

  async getDailyLeaderboardByTimeMode(timeMode: number, limit: number = 100): Promise<TimeModeLeaderboardEntry[]> {
    return apiClient.request<TimeModeLeaderboardEntry[]>(`/api/leaderboard/daily/time-mode/${timeMode}?limit=${limit}`)
  },

  async getWeeklyXPLeaderboard(limit: number = 100): Promise<WeeklyXPLeaderboardEntry[]> {
    return apiClient.request<WeeklyXPLeaderboardEntry[]>(`/api/leaderboard/weekly-xp?limit=${limit}`)
  },
}
