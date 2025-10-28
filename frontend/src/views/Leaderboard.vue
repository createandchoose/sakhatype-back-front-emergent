<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useTheme } from '@/composables/useTheme'
import { leaderboardApi, type TimeModeLeaderboardEntry, type WeeklyXPLeaderboardEntry } from '@/shared/api'
import { Card, CardContent } from '@/shared/ui/card'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/shared/ui/tabs'
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from '@/shared/ui/table'
import { Button } from '@/shared/ui/button'
import { Badge } from '@/shared/ui/badge'
import { Trophy, Medal, Clock } from 'lucide-vue-next'

const { isDark } = useTheme()

const isLoading = ref(true)
const activeTab = ref('all-time-15')
const selectedTimeMode = ref(15)

// All-time leaderboards
const allTime15 = ref<TimeModeLeaderboardEntry[]>([])
const allTime60 = ref<TimeModeLeaderboardEntry[]>([])

// Daily leaderboards
const daily15 = ref<TimeModeLeaderboardEntry[]>([])
const daily60 = ref<TimeModeLeaderboardEntry[]>([])

// Weekly XP leaderboard
const weeklyXP = ref<WeeklyXPLeaderboardEntry[]>([])

onMounted(async () => {
  await loadLeaderboards()
})

async function loadLeaderboards() {
  try {
    isLoading.value = true
    const [allTime15Data, allTime60Data, daily15Data, daily60Data, weeklyXPData] = await Promise.all([
      leaderboardApi.getLeaderboardByTimeMode(15, 100),
      leaderboardApi.getLeaderboardByTimeMode(60, 100),
      leaderboardApi.getDailyLeaderboardByTimeMode(15, 100),
      leaderboardApi.getDailyLeaderboardByTimeMode(60, 100),
      leaderboardApi.getWeeklyXPLeaderboard(100)
    ])
    allTime15.value = allTime15Data
    allTime60.value = allTime60Data
    daily15.value = daily15Data
    daily60.value = daily60Data
    weeklyXP.value = weeklyXPData
  } catch (error) {
    console.error('Failed to load leaderboards:', error)
  } finally {
    isLoading.value = false
  }
}

const getMedalColor = (index: number) => {
  if (index === 0) return 'text-yellow-500'
  if (index === 1) return 'text-gray-400'
  if (index === 2) return 'text-orange-600'
  return 'text-gray-500'
}

const formatDate = (dateString: string) => {
  const date = new Date(dateString)
  const day = date.getDate().toString().padStart(2, '0')
  const month = (date.getMonth() + 1).toString().padStart(2, '0')
  const year = date.getFullYear()
  const hours = date.getHours().toString().padStart(2, '0')
  const minutes = date.getMinutes().toString().padStart(2, '0')
  return `${day}.${month}.${year} ${hours}:${minutes}`
}

const formatTime = (seconds: number) => {
  const hours = Math.floor(seconds / 3600)
  const minutes = Math.floor((seconds % 3600) / 60)
  const secs = seconds % 60
  if (hours > 0) {
    return `${hours}h ${minutes}m`
  } else if (minutes > 0) {
    return `${minutes}m ${secs}s`
  } else {
    return `${secs}s`
  }
}
</script>

<template>
  <div>
    <!-- Header -->
    <header :class="[isDark ? 'border-gray-800' : 'border-gray-200']">
      <div class="container mx-auto py-6 flex items-center justify-between">
        <div class="flex items-center gap-3">
          <Trophy :size="32" :class="isDark ? 'text-yellow-500' : 'text-yellow-600'" />
          <h1 :class="['text-4xl font-bold', isDark ? 'text-white' : 'text-gray-900']">
            Лидерборд
          </h1>
        </div>
      </div>
    </header>

    <!-- Loading state -->
    <div v-if="isLoading" class="container mx-auto px-4 py-12 text-center">
      <p :class="['text-lg', isDark ? 'text-gray-400' : 'text-gray-600']">Күүтүү...</p>
    </div>

    <!-- Leaderboard Content -->
    <main v-else class="container mx-auto px-4 py-6">
      <Tabs v-model="activeTab" default-value="all-time-15" class="w-full">
        <TabsList class="grid w-full max-w-4xl mx-auto grid-cols-5 mb-6">
          <TabsTrigger value="all-time-15" class="flex items-center gap-1 text-xs md:text-sm">
            <Clock :size="14" />
            <span>15с Все</span>
          </TabsTrigger>
          <TabsTrigger value="all-time-60" class="flex items-center gap-1 text-xs md:text-sm">
            <Clock :size="14" />
            <span>60с Все</span>
          </TabsTrigger>
          <TabsTrigger value="daily-15" class="flex items-center gap-1 text-xs md:text-sm">
            <Clock :size="14" />
            <span>15с День</span>
          </TabsTrigger>
          <TabsTrigger value="daily-60" class="flex items-center gap-1 text-xs md:text-sm">
            <Clock :size="14" />
            <span>60с День</span>
          </TabsTrigger>
          <TabsTrigger value="weekly-xp" class="flex items-center gap-1 text-xs md:text-sm">
            <Trophy :size="14" />
            <span>Неделя XP</span>
          </TabsTrigger>
        </TabsList>

        <!-- All-time 15s Leaderboard -->
        <TabsContent value="all-time-15">
          <Card :class="[isDark ? '' : 'bg-white']">
            <CardContent class="p-0">
              <div class="overflow-x-auto">
                <Table>
                  <TableHeader>
                    <TableRow>
                      <TableHead class="w-16">#</TableHead>
                      <TableHead>Имя</TableHead>
                      <TableHead class="text-right">WPM</TableHead>
                      <TableHead class="text-right">Точность</TableHead>
                      <TableHead class="text-right">Raw</TableHead>
                      <TableHead class="text-right">Согласованность</TableHead>
                      <TableHead class="text-right">Дата</TableHead>
                    </TableRow>
                  </TableHeader>
                  <TableBody>
                    <TableRow
                      v-for="(entry, index) in allTime15"
                      :key="entry.username"
                      :class="[index < 3 && 'font-semibold']"
                    >
                      <TableCell class="font-medium">
                        <Medal v-if="index < 3" :size="20" :class="getMedalColor(index)" />
                        <span v-else>{{ index + 1 }}</span>
                      </TableCell>
                      <TableCell class="flex items-center gap-2">
                        <span>{{ entry.username }}</span>
                        <Badge variant="secondary" class="text-xs">Таһым {{ entry.level }}</Badge>
                      </TableCell>
                      <TableCell class="text-right font-bold">{{ Math.round(entry.wpm) }}</TableCell>
                      <TableCell class="text-right">{{ Math.round(entry.accuracy) }}%</TableCell>
                      <TableCell class="text-right">{{ Math.round(entry.raw) }}</TableCell>
                      <TableCell class="text-right">{{ Math.round(entry.consistency) }}%</TableCell>
                      <TableCell class="text-right text-sm">{{ formatDate(entry.date) }}</TableCell>
                    </TableRow>
                    
                    <!-- Empty state -->
                    <TableRow v-if="allTime15.length === 0">
                      <TableCell colspan="7" class="text-center py-8">
                        <p :class="isDark ? 'text-gray-500' : 'text-gray-400'">
                          Нет данных
                        </p>
                      </TableCell>
                    </TableRow>
                  </TableBody>
                </Table>
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        <!-- All-time 60s Leaderboard -->
        <TabsContent value="all-time-60">
          <Card :class="[isDark ? '' : 'bg-white']">
            <CardContent class="p-0">
              <div class="overflow-x-auto">
                <Table>
                  <TableHeader>
                    <TableRow>
                      <TableHead class="w-16">#</TableHead>
                      <TableHead>Имя</TableHead>
                      <TableHead class="text-right">WPM</TableHead>
                      <TableHead class="text-right">Точность</TableHead>
                      <TableHead class="text-right">Raw</TableHead>
                      <TableHead class="text-right">Согласованность</TableHead>
                      <TableHead class="text-right">Дата</TableHead>
                    </TableRow>
                  </TableHeader>
                  <TableBody>
                    <TableRow
                      v-for="(entry, index) in allTime60"
                      :key="entry.username"
                      :class="[index < 3 && 'font-semibold']"
                    >
                      <TableCell class="font-medium">
                        <Medal v-if="index < 3" :size="20" :class="getMedalColor(index)" />
                        <span v-else>{{ index + 1 }}</span>
                      </TableCell>
                      <TableCell class="flex items-center gap-2">
                        <span>{{ entry.username }}</span>
                        <Badge variant="secondary" class="text-xs">Таһым {{ entry.level }}</Badge>
                      </TableCell>
                      <TableCell class="text-right font-bold">{{ Math.round(entry.wpm) }}</TableCell>
                      <TableCell class="text-right">{{ Math.round(entry.accuracy) }}%</TableCell>
                      <TableCell class="text-right">{{ Math.round(entry.raw) }}</TableCell>
                      <TableCell class="text-right">{{ Math.round(entry.consistency) }}%</TableCell>
                      <TableCell class="text-right text-sm">{{ formatDate(entry.date) }}</TableCell>
                    </TableRow>
                    
                    <!-- Empty state -->
                    <TableRow v-if="allTime60.length === 0">
                      <TableCell colspan="7" class="text-center py-8">
                        <p :class="isDark ? 'text-gray-500' : 'text-gray-400'">
                          Нет данных
                        </p>
                      </TableCell>
                    </TableRow>
                  </TableBody>
                </Table>
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        <!-- Daily 15s Leaderboard -->
        <TabsContent value="daily-15">
          <Card :class="[isDark ? '' : 'bg-white']">
            <CardContent class="p-0">
              <div class="overflow-x-auto">
                <Table>
                  <TableHeader>
                    <TableRow>
                      <TableHead class="w-16">#</TableHead>
                      <TableHead>Имя</TableHead>
                      <TableHead class="text-right">WPM</TableHead>
                      <TableHead class="text-right">Точность</TableHead>
                      <TableHead class="text-right">Raw</TableHead>
                      <TableHead class="text-right">Согласованность</TableHead>
                      <TableHead class="text-right">Дата</TableHead>
                    </TableRow>
                  </TableHeader>
                  <TableBody>
                    <TableRow
                      v-for="(entry, index) in daily15"
                      :key="entry.username"
                      :class="[index < 3 && 'font-semibold']"
                    >
                      <TableCell class="font-medium">
                        <Medal v-if="index < 3" :size="20" :class="getMedalColor(index)" />
                        <span v-else>{{ index + 1 }}</span>
                      </TableCell>
                      <TableCell class="flex items-center gap-2">
                        <span>{{ entry.username }}</span>
                        <Badge variant="secondary" class="text-xs">Таһым {{ entry.level }}</Badge>
                      </TableCell>
                      <TableCell class="text-right font-bold">{{ Math.round(entry.wpm) }}</TableCell>
                      <TableCell class="text-right">{{ Math.round(entry.accuracy) }}%</TableCell>
                      <TableCell class="text-right">{{ Math.round(entry.raw) }}</TableCell>
                      <TableCell class="text-right">{{ Math.round(entry.consistency) }}%</TableCell>
                      <TableCell class="text-right text-sm">{{ formatDate(entry.date) }}</TableCell>
                    </TableRow>
                    
                    <!-- Empty state -->
                    <TableRow v-if="daily15.length === 0">
                      <TableCell colspan="7" class="text-center py-8">
                        <p :class="isDark ? 'text-gray-500' : 'text-gray-400'">
                          Нет данных за сегодня
                        </p>
                      </TableCell>
                    </TableRow>
                  </TableBody>
                </Table>
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        <!-- Daily 60s Leaderboard -->
        <TabsContent value="daily-60">
          <Card :class="[isDark ? '' : 'bg-white']">
            <CardContent class="p-0">
              <div class="overflow-x-auto">
                <Table>
                  <TableHeader>
                    <TableRow>
                      <TableHead class="w-16">#</TableHead>
                      <TableHead>Имя</TableHead>
                      <TableHead class="text-right">WPM</TableHead>
                      <TableHead class="text-right">Точность</TableHead>
                      <TableHead class="text-right">Raw</TableHead>
                      <TableHead class="text-right">Согласованность</TableHead>
                      <TableHead class="text-right">Дата</TableHead>
                    </TableRow>
                  </TableHeader>
                  <TableBody>
                    <TableRow
                      v-for="(entry, index) in daily60"
                      :key="entry.username"
                      :class="[index < 3 && 'font-semibold']"
                    >
                      <TableCell class="font-medium">
                        <Medal v-if="index < 3" :size="20" :class="getMedalColor(index)" />
                        <span v-else>{{ index + 1 }}</span>
                      </TableCell>
                      <TableCell class="flex items-center gap-2">
                        <span>{{ entry.username }}</span>
                        <Badge variant="secondary" class="text-xs">Таһым {{ entry.level }}</Badge>
                      </TableCell>
                      <TableCell class="text-right font-bold">{{ Math.round(entry.wpm) }}</TableCell>
                      <TableCell class="text-right">{{ Math.round(entry.accuracy) }}%</TableCell>
                      <TableCell class="text-right">{{ Math.round(entry.raw) }}</TableCell>
                      <TableCell class="text-right">{{ Math.round(entry.consistency) }}%</TableCell>
                      <TableCell class="text-right text-sm">{{ formatDate(entry.date) }}</TableCell>
                    </TableRow>
                    
                    <!-- Empty state -->
                    <TableRow v-if="daily60.length === 0">
                      <TableCell colspan="7" class="text-center py-8">
                        <p :class="isDark ? 'text-gray-500' : 'text-gray-400'">
                          Нет данных за сегодня
                        </p>
                      </TableCell>
                    </TableRow>
                  </TableBody>
                </Table>
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        <!-- Weekly XP Leaderboard -->
        <TabsContent value="weekly-xp">
          <Card :class="[isDark ? '' : 'bg-white']">
            <CardContent class="p-0">
              <div class="overflow-x-auto">
                <Table>
                  <TableHeader>
                    <TableRow>
                      <TableHead class="w-16">#</TableHead>
                      <TableHead>Имя</TableHead>
                      <TableHead class="text-right">XP получено</TableHead>
                      <TableHead class="text-right">Время набора</TableHead>
                      <TableHead class="text-right">Последняя активность</TableHead>
                    </TableRow>
                  </TableHeader>
                  <TableBody>
                    <TableRow
                      v-for="(entry, index) in weeklyXP"
                      :key="entry.username"
                      :class="[index < 3 && 'font-semibold']"
                    >
                      <TableCell class="font-medium">
                        <Medal v-if="index < 3" :size="20" :class="getMedalColor(index)" />
                        <span v-else>{{ index + 1 }}</span>
                      </TableCell>
                      <TableCell class="flex items-center gap-2">
                        <span>{{ entry.username }}</span>
                        <Badge variant="secondary" class="text-xs">Таһым {{ entry.level }}</Badge>
                      </TableCell>
                      <TableCell class="text-right font-bold">{{ entry.xp_gained }}</TableCell>
                      <TableCell class="text-right">{{ formatTime(entry.time_typed) }}</TableCell>
                      <TableCell class="text-right text-sm">{{ formatDate(entry.last_activity) }}</TableCell>
                    </TableRow>
                    
                    <!-- Empty state -->
                    <TableRow v-if="weeklyXP.length === 0">
                      <TableCell colspan="5" class="text-center py-8">
                        <p :class="isDark ? 'text-gray-500' : 'text-gray-400'">
                          Нет данных за неделю
                        </p>
                      </TableCell>
                    </TableRow>
                  </TableBody>
                </Table>
              </div>
            </CardContent>
          </Card>
        </TabsContent>
      </Tabs>
    </main>
  </div>
</template>
