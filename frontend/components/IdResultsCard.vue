<template>
  <div class="bg-white rounded-xl shadow-md overflow-hidden transition-transform transform hover:scale-102 hover:shadow-lg">
    <div class="bg-gray-50 px-6 py-4 border-b border-gray-200 flex items-center">
      <span class="text-xl mr-3">{{ icon }}</span>
      <h3 class="text-lg font-semibold text-gray-900">
        {{ title }}
      </h3>
    </div>
    <div class="p-6">
      <slot></slot>
    </div>
  </div>
</template>

<script setup lang="ts">
defineProps<{
  title: string
  icon: string
}>()
</script>
