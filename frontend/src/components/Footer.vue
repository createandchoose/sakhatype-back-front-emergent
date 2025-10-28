<template>
  <footer class="px-8 py-5 flex items-center justify-between">
    <Button class="select-none cursor-pointer" variant="outline">
      <Disc :size="14" /><span>Сделана командой DotX</span>
    </Button>

    <div class="flex items-center gap-2">
      <!-- Кнопка звука с переключением -->
      <Button
        class="select-none cursor-pointer flex items-center gap-1"
        variant="outline"
        @click="toggleSound"
      >
        <component :is="soundEnabled ? Volume2 : VolumeX" :size="14" />
        <span>{{ soundEnabled ? 'Үөн күүстээх' : 'Үөн суох' }}</span>
      </Button>

      <DropdownMenu>
        <DropdownMenuTrigger as-child>
          <Button class="select-none cursor-pointer" variant="outline">
            <Palette />
            <span>{{ isDark ? 'Хара' : 'Үрүҥ' }}</span>
          </Button>
        </DropdownMenuTrigger>
        <DropdownMenuContent class="w-56">
          <DropdownMenuItem
            @click="toggleDark()"
            :disabled="!isDark"
            class="select-none cursor-pointer"
          >
            <span>Үрүҥ баар</span>
          </DropdownMenuItem>
          <DropdownMenuItem
            @click="toggleDark()"
            :disabled="isDark"
            class="select-none cursor-pointer"
          >
            <span>Хара баар</span>
          </DropdownMenuItem>
        </DropdownMenuContent>
      </DropdownMenu>
    </div>
  </footer>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useTheme } from '@/composables/useTheme'
import { soundManager } from '@/shared/lib/sound-manager'
import { Disc, Volume2, VolumeX, Palette } from 'lucide-vue-next'
import { Button } from '@/components/ui/button'
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuTrigger,
} from '@/components/ui/dropdown-menu'

const { isDark, toggleDark } = useTheme()

// Состояние звука
const soundEnabled = ref(soundManager.isEnabled())
const toggleSound = () => {
  soundEnabled.value = !soundEnabled.value
  soundManager.setEnabled(soundEnabled.value)
  soundManager.play('click')
}
</script>
