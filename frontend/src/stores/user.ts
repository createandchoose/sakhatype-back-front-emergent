import { defineStore } from 'pinia'
import { ref } from 'vue'
import { userApi } from '@/shared/api'

export interface UserProfile {
  username: string
  level: number
  total_tests: number
  total_time_seconds: number
  best_wpm: number
  best_accuracy: number
  total_experience: number
  created_at: string
}

export const useUserStore = defineStore('user', () => {
  const profile = ref<UserProfile | null>(null)
  const isLoading = ref(false)

  async function fetchProfile(username: string) {
    try {
      isLoading.value = true
      const data = await userApi.getUserProfile(username)
      profile.value = data as UserProfile
      return data
    } catch (error) {
      console.error('Failed to fetch user profile:', error)
      throw error
    } finally {
      isLoading.value = false
    }
  }

  async function refreshProfile(username: string) {
    await fetchProfile(username)
  }

  function clearProfile() {
    profile.value = null
  }

  return {
    profile,
    isLoading,
    fetchProfile,
    refreshProfile,
    clearProfile
  }
})
