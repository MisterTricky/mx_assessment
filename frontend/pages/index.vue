<!-- Main page for ID number validation and results -->
<template>
  <div class="min-h-screen bg-gray-50">
    <div class="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
      <!-- Input Card -->
      <div class="max-w-3xl mx-auto">
        <div class="rounded-2xl bg-white p-8 shadow-lg ring-1 ring-gray-200">
          <div class="space-y-6">
            <div>
              <label for="idNumber" class="block text-sm font-medium leading-6 text-gray-900">
                South African ID Number
              </label>
              <div class="mt-2">
                <input
                  id="idNumber"
                  v-model="idNumber"
                  type="text"
                  class="block w-full rounded-md border-0 py-2.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-blue-600 sm:text-sm sm:leading-6"
                  placeholder="Enter your 13-digit ID number"
                  @input="validateIdNumber"
                />
              </div>
              <!-- Validation Message -->
              <div v-if="validationMessage" class="mt-2">
                <p :class="[
                  'text-sm',
                  validationMessage.type === 'error' ? 'text-red-600' : 'text-green-600'
                ]">
                  {{ validationMessage.text }}
                </p>
              </div>
            </div>

            <div class="pt-4">
              <button
                @click="searchId"
                :disabled="!isValidId"
                :class="[
                  'w-full rounded-md px-3.5 py-2.5 text-sm font-semibold text-white shadow-sm focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2',
                  isValidId
                    ? 'bg-blue-600 hover:bg-blue-500 focus-visible:outline-blue-600'
                    : 'bg-gray-400 cursor-not-allowed'
                ]"
              >
                <span v-if="idStore.isLoading" class="flex items-center justify-center">
                  <svg class="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                    <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                    <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                  </svg>
                  Processing...
                </span>
                <span v-else>Search</span>
              </button>
            </div>
          </div>
        </div>
      </div>

      <!-- Error Alert -->
      <div v-if="idStore.error" class="mt-6">
        <div class="rounded-md bg-red-50 p-4">
          <div class="flex">
            <div class="flex-shrink-0">
              <svg class="h-5 w-5 text-red-400" viewBox="0 0 20 20" fill="currentColor">
                <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.28 7.22a.75.75 0 00-1.06 1.06L8.94 10l-1.72 1.72a.75.75 0 101.06 1.06L10 11.06l1.72 1.72a.75.75 0 101.06-1.06L11.06 10l1.72-1.72a.75.75 0 00-1.06-1.06L10 8.94 8.28 7.22z" clip-rule="evenodd" />
              </svg>
            </div>
            <div class="ml-3">
              <h3 class="text-sm font-medium text-red-800">Error</h3>
              <div class="mt-2 text-sm text-red-700">
                <p>{{ idStore.error }}</p>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Results Section -->
      <IdResults v-if="hasResults" class="mt-8" />
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { useIdStore } from '~/stores/id'

const idStore = useIdStore()
const idNumber = ref('')
const validationMessage = ref<{ type: 'error' | 'success', text: string } | null>(null)

const isValidId = computed(() => {
  return idStore.isValidId(idNumber.value)
})

const hasResults = computed(() => idStore.hasResults)

const validateIdNumber = () => {
  if (idNumber.value.length === 0) {
    validationMessage.value = null
    return
  }

  if (isValidId.value) {
    validationMessage.value = {
      type: 'success',
      text: 'Valid ID number'
    }
  } else {
    validationMessage.value = {
      type: 'error',
      text: 'Please enter a valid South African ID number'
    }
  }
}

const searchId = async () => {
  if (isValidId.value) {
    await idStore.searchId(idNumber.value)
  }
}
</script>
