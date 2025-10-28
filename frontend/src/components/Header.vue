<script setup lang="ts">
import { computed, ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { Trophy, User, LogOut, Volume2, VolumeX } from 'lucide-vue-next'
import { useTheme } from '@/composables/useTheme'
import { useAuthStore } from '@/stores/auth'
import { apiService } from '@/shared/api/api-service'
import { soundManager } from '@/shared/lib/sound-manager'
import LoginDialog from '@/components/LoginDialog.vue'
import { Button } from '@/components/ui/button'
import { Badge } from '@/components/ui/badge'
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from '@/components/ui/dropdown-menu'

const { isDark } = useTheme()
const authStore = useAuthStore()
const router = useRouter()

const userLevel = ref<number>(1)
const soundEnabled = ref(soundManager.isEnabled())

// Загрузка уровня пользователя
onMounted(async () => {
  if (authStore.isAuthenticated && authStore.username) {
    try {
      const profile = await apiService.getUserProfile(authStore.username)
      userLevel.value = profile.level
    } catch (error) {
      console.error('Failed to load user level:', error)
    }
  }
})

// Обновляем уровень при изменении авторизации
const handleLogout = () => {
  authStore.logout()
  router.push('/')
}

const toggleSound = () => {
  soundEnabled.value = !soundEnabled.value
  soundManager.setEnabled(soundEnabled.value)
  soundManager.play('click')
}
</script>

<template>
  <header class="py-5 flex items-center justify-between">
    <div class="flex items-center gap-8">
      <!-- Главная через router-link -->
      <router-link to="/" class="flex items-center gap-3 select-none cursor-pointer">
        <span class="text-2xl font-bold tracking-tight">Sakhatype</span>
      </router-link>

      <!-- Лидерборд -->
      <router-link
        to="/leaderboard"
        :class="[
          'flex items-center gap-2 transition-colors text-sm select-none cursor-pointer',
          isDark ? 'text-gray-400 hover:text-white' : 'text-gray-600 hover:text-gray-900',
        ]"
      >
        <Trophy :size="16" />
        <span>Лидерборд</span>
      </router-link>
    </div>

    <!-- Авторизация / Профиль -->
    <div class="flex items-center gap-3">
      <!-- Звук -->
      <Button 
        variant="ghost" 
        size="icon" 
        @click="toggleSound"
        class="cursor-pointer"
      >
        <Volume2 v-if="soundEnabled" :size="20" />
        <VolumeX v-else :size="20" />
      </Button>

      <!-- Пользователь -->
      <div v-if="authStore.isAuthenticated">
        <DropdownMenu>
          <DropdownMenuTrigger as-child>
            <Button variant="outline" class="flex items-center gap-2 cursor-pointer select-none">
              <User :size="16" />
              <span>{{ authStore.username }}</span>
              <Badge class="ml-1 bg-blue-500 hover:bg-blue-600 text-white px-2 py-0.5 text-xs">
                {{ userLevel }}
              </Badge>
            </Button>
          </DropdownMenuTrigger>
          <DropdownMenuContent align="end">
            <DropdownMenuItem @click="router.push('/profile')" class="cursor-pointer">
              <User :size="16" class="mr-2" />
              <span>Профиль</span>
            </DropdownMenuItem>
            <DropdownMenuSeparator />
            <DropdownMenuItem @click="handleLogout" class="cursor-pointer text-red-600">
              <LogOut :size="16" class="mr-2" />
              <span>Тахсыы (Выйти)</span>
            </DropdownMenuItem>
          </DropdownMenuContent>
        </DropdownMenu>
      </div>
      <LoginDialog v-else />
    </div>
  </header>
</template>
