<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { useUserStore } from '@/stores/user'
import { useTheme } from '@/composables/useTheme'
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/shared/ui/card'
import { Button } from '@/shared/ui/button'
import { Input } from '@/shared/ui/input'
import { Label } from '@/shared/ui/label'
import { Switch } from '@/shared/ui/switch'
import { Settings as SettingsIcon, User, Lock, Moon, Sun } from 'lucide-vue-next'

const { isDark, toggleTheme } = useTheme()
const authStore = useAuthStore()
const userStore = useUserStore()
const router = useRouter()

const displayName = ref('')
const currentPassword = ref('')
const newPassword = ref('')
const confirmPassword = ref('')
const isSaving = ref(false)
const message = ref('')

onMounted(() => {
  if (!authStore.isAuthenticated) {
    router.push('/')
    return
  }
  
  if (authStore.username) {
    displayName.value = authStore.username
  }
})

async function saveSettings() {
  isSaving.value = true
  message.value = ''
  
  try {
    // Here you would save settings to the backend
    // For now, just show success message
    message.value = 'Настройки сохранены!'
    setTimeout(() => {
      message.value = ''
    }, 3000)
  } catch (error) {
    message.value = 'Ошибка при сохранении настроек'
  } finally {
    isSaving.value = false
  }
}

async function changePassword() {
  if (newPassword.value !== confirmPassword.value) {
    message.value = 'Пароли не совпадают'
    return
  }
  
  if (newPassword.value.length < 6) {
    message.value = 'Пароль должен быть не менее 6 символов'
    return
  }
  
  isSaving.value = true
  message.value = ''
  
  try {
    // Here you would change password via backend API
    message.value = 'Пароль изменен! (функция в разработке)'
    currentPassword.value = ''
    newPassword.value = ''
    confirmPassword.value = ''
    setTimeout(() => {
      message.value = ''
    }, 3000)
  } catch (error) {
    message.value = 'Ошибка при изменении пароля'
  } finally {
    isSaving.value = false
  }
}
</script>

<template>
  <div class="container mx-auto px-4 py-8 max-w-4xl">
    <!-- Header -->
    <div class="flex items-center gap-3 mb-6">
      <SettingsIcon :size="32" :class="isDark ? 'text-blue-500' : 'text-blue-600'" />
      <h1 :class="['text-4xl font-bold', isDark ? 'text-white' : 'text-gray-900']">
        Настройки
      </h1>
    </div>

    <!-- Message -->
    <div v-if="message" :class="['mb-4 p-3 rounded-lg', isDark ? 'bg-blue-900/50 text-blue-200' : 'bg-blue-100 text-blue-800']">
      {{ message }}
    </div>

    <div class="space-y-6">
      <!-- Profile Settings -->
      <Card>
        <CardHeader>
          <CardTitle class="flex items-center gap-2">
            <User :size="20" />
            <span>Профиль</span>
          </CardTitle>
          <CardDescription>Управление информацией профиля</CardDescription>
        </CardHeader>
        <CardContent class="space-y-4">
          <div class="space-y-2">
            <Label for="username">Имя пользователя</Label>
            <Input 
              id="username"
              v-model="displayName" 
              type="text"
              placeholder="Ваше имя"
            />
            <p :class="['text-xs', isDark ? 'text-gray-400' : 'text-gray-500']">
              Ваше текущее имя: {{ authStore.username }}
            </p>
          </div>
          
          <div class="space-y-2">
            <Label>Уровень</Label>
            <div class="flex items-center gap-2">
              <span :class="['text-2xl font-bold', isDark ? 'text-white' : 'text-gray-900']">
                Таһым {{ userStore.profile?.level || 1 }}
              </span>
              <span :class="['text-sm', isDark ? 'text-gray-400' : 'text-gray-600']">
                ({{ userStore.profile?.total_experience || 0 }} XP)
              </span>
            </div>
          </div>

          <div class="space-y-2">
            <Label>Статистика</Label>
            <div :class="['grid grid-cols-2 gap-4 p-4 rounded-lg', isDark ? 'bg-gray-800' : 'bg-gray-50']">
              <div>
                <p :class="['text-xs', isDark ? 'text-gray-400' : 'text-gray-600']">Всего тестов</p>
                <p :class="['text-lg font-bold', isDark ? 'text-white' : 'text-gray-900']">
                  {{ userStore.profile?.total_tests || 0 }}
                </p>
              </div>
              <div>
                <p :class="['text-xs', isDark ? 'text-gray-400' : 'text-gray-600']">Лучший WPM</p>
                <p :class="['text-lg font-bold', isDark ? 'text-white' : 'text-gray-900']">
                  {{ Math.round(userStore.profile?.best_wpm || 0) }}
                </p>
              </div>
              <div>
                <p :class="['text-xs', isDark ? 'text-gray-400' : 'text-gray-600']">Лучшая точность</p>
                <p :class="['text-lg font-bold', isDark ? 'text-white' : 'text-gray-900']">
                  {{ Math.round(userStore.profile?.best_accuracy || 0) }}%
                </p>
              </div>
              <div>
                <p :class="['text-xs', isDark ? 'text-gray-400' : 'text-gray-600']">Время набора</p>
                <p :class="['text-lg font-bold', isDark ? 'text-white' : 'text-gray-900']">
                  {{ Math.floor((userStore.profile?.total_time_seconds || 0) / 60) }}м
                </p>
              </div>
            </div>
          </div>
        </CardContent>
      </Card>

      <!-- Password Settings -->
      <Card>
        <CardHeader>
          <CardTitle class="flex items-center gap-2">
            <Lock :size="20" />
            <span>Безопасность</span>
          </CardTitle>
          <CardDescription>Изменить пароль</CardDescription>
        </CardHeader>
        <CardContent class="space-y-4">
          <div class="space-y-2">
            <Label for="current-password">Текущий пароль</Label>
            <Input 
              id="current-password"
              v-model="currentPassword" 
              type="password"
              placeholder="Введите текущий пароль"
            />
          </div>
          
          <div class="space-y-2">
            <Label for="new-password">Новый пароль</Label>
            <Input 
              id="new-password"
              v-model="newPassword" 
              type="password"
              placeholder="Введите новый пароль"
            />
          </div>

          <div class="space-y-2">
            <Label for="confirm-password">Подтвердите пароль</Label>
            <Input 
              id="confirm-password"
              v-model="confirmPassword" 
              type="password"
              placeholder="Повторите новый пароль"
            />
          </div>

          <Button 
            @click="changePassword" 
            :disabled="isSaving || !currentPassword || !newPassword || !confirmPassword"
          >
            {{ isSaving ? 'Сохранение...' : 'Изменить пароль' }}
          </Button>
        </CardContent>
      </Card>

      <!-- Appearance Settings -->
      <Card>
        <CardHeader>
          <CardTitle class="flex items-center gap-2">
            <component :is="isDark ? Moon : Sun" :size="20" />
            <span>Внешний вид</span>
          </CardTitle>
          <CardDescription>Настройка темы приложения</CardDescription>
        </CardHeader>
        <CardContent class="space-y-4">
          <div class="flex items-center justify-between">
            <div class="space-y-0.5">
              <Label>Темная тема</Label>
              <p :class="['text-xs', isDark ? 'text-gray-400' : 'text-gray-500']">
                Переключить между светлой и темной темой
              </p>
            </div>
            <Switch :checked="isDark" @update:checked="toggleTheme" />
          </div>
        </CardContent>
      </Card>

      <!-- Back Button -->
      <div class="flex justify-end">
        <Button variant="outline" @click="router.push('/')">
          Вернуться к печати
        </Button>
      </div>
    </div>
  </div>
</template>
