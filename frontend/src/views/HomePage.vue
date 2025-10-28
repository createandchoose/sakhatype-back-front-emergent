<script setup lang="ts">
import { ref, watch, onMounted, onUnmounted, computed, type Ref } from 'vue'
import { RotateCcw } from 'lucide-vue-next'
import { useTheme } from '@/composables/useTheme'
import { useSound } from '@/shared/composables/useSound'
import { useControlStore } from '@/stores/control'
import { useTypingStore } from '@/stores/typingStore.ts'
import Control from '@/components/Control.vue'
import ResultsView from '@/components/ResultsView.vue'

const { isDark } = useTheme()
const { playKeypress, playCorrect, playIncorrect } = useSound()
const control = useControlStore()
const store = useTypingStore()

const selectedTime = ref(control.selectedTime)
const displayTime = ref(control.selectedTime)
const isAnimating = ref(false)
const hiddenInput = ref<HTMLInputElement | null>(null)
const inputValue = ref('')
const hasFocus = ref(false)
const showResults = ref(false)
const currentLineIndex = ref(0)
const textDisplayRef = ref<HTMLDivElement | null>(null)
const lineOffset = ref(0)
const wordsPerLine = ref<number[][]>([]) // Array of word indices for each line
const visibleLines = ref<number[]>([0, 1, 2]) // Indices of the 3 visible lines

// Функция анимации чисел как в GTA
const animateNumber = (from: number, to: number) => {
  if (from === to) return
  isAnimating.value = true
  const duration = 200
  const steps = 30
  const increment = (to - from) / steps
  let current = from
  let step = 0
  const timer = setInterval(() => {
    step++
    current += increment
    if (step >= steps) {
      displayTime.value = to
      isAnimating.value = false
      clearInterval(timer)
    } else {
      displayTime.value = Math.round(current)
    }
  }, duration / steps)
}

// 🧩 следим за изменениями store → родитель с анимацией
watch(
  () => control.selectedTime,
  (newVal, oldVal) => {
    if (newVal !== undefined && oldVal !== undefined) {
      selectedTime.value = newVal
      animateNumber(oldVal, newVal)
      setTime(newVal)
    }
  },
)

// 🔁 следим за изменениями родителя → store
watch(selectedTime, (val) => {
  if (val !== undefined) {
    control.setTime(val)
  }
})

// Отображаемое время (таймер или выбранное)
const timeDisplay = computed(() => {
  return store.isTestActive ? store.timeLeft : displayTime.value
})

const setTime = (time: number) => {
  store.setTime(time)
  restartTest()
}

const restartTest = () => {
  store.initTest()
  inputValue.value = ''
  showResults.value = false
  lineOffset.value = 0
  calculateWordsPerLine()
  visibleLines.value = [0, 1, 2]
  currentLineIndex.value = 0
}

// Calculate which words belong to each line
const calculateWordsPerLine = () => {
  const containerWidth = textDisplayRef.value?.offsetWidth || 800
  const words = store.words
  const lines: number[][] = []
  let currentLine: number[] = []
  let currentWidth = 0
  
  // Approximate character width for monospace font at text-3xl (1.875rem)
  const charWidth = 18 // pixels per character at this font size
  const spaceWidth = 10 // space between words
  
  words.forEach((word, index) => {
    const wordWidth = word.length * charWidth + spaceWidth
    
    if (currentWidth + wordWidth > containerWidth && currentLine.length > 0) {
      // Start new line
      lines.push([...currentLine])
      currentLine = [index]
      currentWidth = wordWidth
    } else {
      currentLine.push(index)
      currentWidth += wordWidth
    }
  })
  
  // Push the last line
  if (currentLine.length > 0) {
    lines.push(currentLine)
  }
  
  wordsPerLine.value = lines
}

// Get the line index for a given word index
const getLineForWord = (wordIndex: number): number => {
  for (let i = 0; i < wordsPerLine.value.length; i++) {
    if (wordsPerLine.value[i].includes(wordIndex)) {
      return i
    }
  }
  return 0
}

// Update visible lines when user progresses
const updateVisibleLines = () => {
  const lineIndex = getLineForWord(store.currentWordIndex)
  
  // Keep current line in the middle (index 1 of visible lines)
  if (lineIndex > currentLineIndex.value) {
    currentLineIndex.value = lineIndex
    visibleLines.value = [
      Math.max(0, lineIndex - 1),
      lineIndex,
      Math.min(wordsPerLine.value.length - 1, lineIndex + 1)
    ]
  }
}

const focusInput = () => {
  hiddenInput.value?.focus()
  hasFocus.value = true
}

const handleFocus = () => {
  hasFocus.value = true
}

const handleBlur = () => {
  hasFocus.value = false
}

const handleInput = (event: Event) => {
  const target = event.target as HTMLInputElement
  if (!store.isTestActive) {
    store.startTimer()
    if (!hasFocus.value) {
      hasFocus.value = true
    }
  }

  const prevWordIndex = store.currentWordIndex
  const prevInputLength = store.inputValue.length
  const newInput = target.value
  
  // Определяем, был ли добавлен символ
  if (newInput.length > prevInputLength) {
    playKeypress()
    
    // Проверяем правильность последнего введенного символа
    const lastChar = newInput[newInput.length - 1]
    const expectedChar = store.words[store.currentWordIndex]?.[newInput.length - 1]
    
    if (lastChar === expectedChar) {
      playCorrect()
    } else {
      playIncorrect()
    }
  }
  
  store.processInput(target.value)
  inputValue.value = store.inputValue

  // Проверяем, перешли ли мы на новое слово
  if (store.currentWordIndex > prevWordIndex) {
    updateVisibleLines()
  }
}

const updateLineOffset = () => {
  // This function is no longer needed with the 3-line approach
  // Keeping it as a placeholder in case it's called elsewhere
}

const getCharClass = (wordIdx: number, charIdx: number): string => {
  if (!hasFocus.value && !store.isTestActive) {
    return ''
  }

  if (wordIdx < store.currentWordIndex) {
    return store.wordHistory[wordIdx]?.[charIdx] || ''
  } else if (wordIdx === store.currentWordIndex) {
    if (charIdx < store.inputValue.length)
      return store.inputValue[charIdx] === store.words[wordIdx][charIdx] ? 'correct' : 'incorrect'
    else if (charIdx === store.inputValue.length && hasFocus.value && store.isTestActive)
      return 'current'
  }
  return ''
}

const handleKeyDown = (e: KeyboardEvent) => {
  if (e.key.length === 1 && !e.ctrlKey && !e.metaKey && !e.altKey) {
    focusInput()
  }
  if (e.ctrlKey && e.key === 'Backspace') {
    e.preventDefault()
    inputValue.value = ''
    store.inputValue = ''
  }
  if ((e.key === 'Tab' || e.key === 'Escape') && !showResults.value) {
    e.preventDefault()
    restartTest()
  }
}

// Исправленная типизация для обработчика действий store
const unsubscribe = store.$onAction(
  ({ name, after }: { name: string; after: (callback: () => void) => void }) => {
    if (name === 'endTest') after(() => (showResults.value = true))
  },
)

onMounted(() => {
  store.initTest()
  document.addEventListener('keydown', handleKeyDown)
  // Calculate initial lines after a short delay to ensure DOM is ready
  setTimeout(() => {
    calculateWordsPerLine()
  }, 100)
})

onUnmounted(() => {
  document.removeEventListener('keydown', handleKeyDown)
  unsubscribe()
})
</script>

<template>
  <div>
    <main class="flex-1 flex flex-col items-center justify-center py-16">
      <!-- Controls (только когда не активен тест и нет результатов) -->
      <div v-if="!store.isTestActive && !showResults" class="flex items-center gap-3 mb-20">
        <Control v-model="selectedTime" />
      </div>

      <!-- Typing Container -->
      <div v-if="!showResults" class="w-full">
        <!-- Timer -->
        <div
          :class="[
            'text-7xl font-bold mb-6 transition-all duration-300 select-none text-left',
            isDark ? 'text-[#2a2a2a]' : 'text-gray-300',
          ]"
          :style="{
            transform: isAnimating ? 'translateY(-5px)' : 'translateY(0)',
            opacity: isAnimating ? '0.7' : '1',
          }"
        >
          {{ timeDisplay }}
        </div>

        <!-- Text Display (Monkeytype-style) -->
        <div class="text-display-wrapper overflow-hidden relative mb-4" style="height: 10rem">
          <div
            ref="textDisplayRef"
            @click="focusInput"
            tabindex="0"
            :class="[
              'text-3xl leading-relaxed cursor-text select-none font-mono transition-transform duration-200',
              isDark ? 'text-gray-600' : 'text-gray-400',
            ]"
            :style="{
              transform: `translateY(${lineOffset}px)`,
            }"
          >
            <span
              v-for="(word, wordIdx) in store.words"
              :key="wordIdx"
              :class="[
                'word inline-block relative',
                wordIdx === store.currentWordIndex && hasFocus && store.isTestActive ? 'word-active' : ''
              ]"
              :style="{ marginRight: '0.5rem' }"
            >
              <span
                v-for="(char, charIdx) in word"
                :key="charIdx"
                :class="[
                  'char relative inline-block transition-all duration-75',
                  {
                    [isDark ? 'text-white' : 'text-gray-900']:
                      getCharClass(wordIdx, charIdx) === 'correct',
                    'text-red-500 char-incorrect': getCharClass(wordIdx, charIdx) === 'incorrect',
                    'char-cursor': getCharClass(wordIdx, charIdx) === 'current',
                  }
                ]"
              >
                {{ char }}
              </span>
              <!-- Показываем лишние символы если их напечатали -->
              <span
                v-if="wordIdx === store.currentWordIndex && store.inputValue.length > word.length"
                v-for="extraIdx in store.inputValue.length - word.length"
                :key="`extra-${extraIdx}`"
                class="char relative inline-block text-red-500 extra-char"
              >
                {{ store.inputValue[word.length + extraIdx - 1] }}
              </span>
            </span>
          </div>
        </div>

        <!-- Focus Message & Restart -->
        <div class="text-center">
          <p
            :class="[
              'text-xs mb-6 select-none transition-opacity duration-300',
              isDark ? 'text-gray-500' : 'text-gray-600',
              { 'opacity-0': hasFocus || store.isTestActive },
            ]"
          >
            Нажмите на текст и начните печатать
          </p>
          <div
            @click="restartTest"
            :class="[
              'inline-flex justify-center cursor-pointer rotate-icon',
              isDark ? 'text-gray-500 hover:text-white' : 'text-gray-400 hover:text-gray-900',
            ]"
          >
            <RotateCcw :size="24" />
          </div>
        </div>

        <!-- Hidden Input -->
        <input
          ref="hiddenInput"
          type="text"
          class="absolute opacity-0 pointer-events-none"
          v-model="inputValue"
          @input="handleInput"
          @focus="handleFocus"
          @blur="handleBlur"
          autocomplete="off"
          autocorrect="off"
          autocapitalize="off"
          spellcheck="false"
        />
      </div>

      <!-- Results View -->
      <ResultsView
        v-else
        :stats="store.finalStats"
        :wpm-history="store.wpmHistory"
        :raw-history="store.rawHistory"
        :burst-history="store.burstHistory"
        :error-timestamps="store.errorTimestamps"
        @restart="restartTest"
      />
    </main>
  </div>
</template>

<style scoped>
.rotate-icon {
  transition: transform 0.3s ease;
}
.rotate-icon:hover {
  transform: rotate(-260deg);
}

/* Monkeytype-style cursor */
.char-cursor::before {
  content: '';
  position: absolute;
  left: -2px;
  top: 2px;
  bottom: 2px;
  width: 2.5px;
  background: currentColor;
  animation: blink-smooth 1s infinite;
  border-radius: 2px;
}

@keyframes blink-smooth {
  0%, 49% {
    opacity: 1;
  }
  50%, 100% {
    opacity: 0;
  }
}

/* Active word styling (like monkeytype) */
.word-active {
  opacity: 1;
}

.word {
  margin-bottom: 10px;
  position: relative;
}

/* Incorrect character wobble */
.char-incorrect {
  animation: wobble 0.1s ease-in-out;
}

@keyframes wobble {
  0%, 100% {
    transform: translateX(0);
  }
  25% {
    transform: translateX(-2px);
  }
  75% {
    transform: translateX(2px);
  }
}

/* Extra characters styling */
.extra-char {
  opacity: 0.8;
  background: rgba(239, 68, 68, 0.2);
  border-radius: 2px;
}

.char {
  letter-spacing: 0.05em;
  position: relative;
  padding: 2px 0;
}

/* Smooth scrolling for text */
.text-display-wrapper {
  position: relative;
}
</style>
