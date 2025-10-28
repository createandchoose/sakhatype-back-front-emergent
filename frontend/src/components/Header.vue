<script setup lang="ts">
import { computed } from 'vue'
import { useRouter } from 'vue-router'
import { Trophy, User, LogOut } from 'lucide-vue-next'
import { useTheme } from '@/composables/useTheme'
import { useAuthStore } from '@/stores/auth'
import LoginDialog from './LoginDialog.vue'
import { Button } from '@/components/ui/button'
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

const handleLogout = () => {
  authStore.logout()
  router.push('/')
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
    <div v-if="authStore.isAuthenticated">
      <DropdownMenu>
        <DropdownMenuTrigger as-child>
          <Button variant="outline" class="flex items-center gap-2 cursor-pointer select-none">
            <User :size="16" />
            <span>{{ authStore.username }}</span>
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
  </header>
</template>
