<script setup lang="ts">
import { computed } from 'vue'

interface Props {
  checked?: boolean
}

const props = defineProps<Props>()
const emit = defineEmits<{
  'update:checked': [value: boolean]
}>()

const handleToggle = () => {
  emit('update:checked', !props.checked)
}
</script>

<template>
  <button
    type="button"
    role="switch"
    :aria-checked="checked"
    @click="handleToggle"
    :class="[
      'relative inline-flex h-6 w-11 items-center rounded-full transition-colors focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2',
      checked ? 'bg-blue-600' : 'bg-gray-300 dark:bg-gray-700'
    ]"
  >
    <span
      :class="[
        'inline-block h-4 w-4 transform rounded-full bg-white transition-transform',
        checked ? 'translate-x-6' : 'translate-x-1'
      ]"
    />
  </button>
</template>
