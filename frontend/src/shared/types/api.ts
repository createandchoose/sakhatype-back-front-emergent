// API типы
export interface User {
  username: string
  total_tests: number
  total_time_seconds: number
  best_wpm: number
  best_accuracy: number
  total_experience: number
  level: number
  created_at: string
}

export interface TestResult {
  id: number
  username: string
  wpm: number
  raw_wpm: number
  accuracy: number
  burst_wpm: number
  total_errors: number
  time_mode: number
  test_duration: number
  consistency: number
  created_at: string
}

export interface TestResultCreate {
  wpm: number
  raw_wpm: number
  accuracy: number
  burst_wpm: number
  total_errors: number
  time_mode: number
  test_duration: number
  consistency: number
}

export interface LeaderboardEntry {
  username: string
  best_wpm: number
  best_accuracy: number
  total_tests: number
  level: number
}

export interface TokenResponse {
  access_token: string
  token_type: string
  username: string
}
