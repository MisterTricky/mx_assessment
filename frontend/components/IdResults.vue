<template>
  <div class="w-full max-w-7xl mx-auto">
    <!-- Alert for No Holidays -->
    <div v-if="!results.holidays?.length" class="mx-8 mb-4 bg-yellow-50 border-l-4 border-yellow-400 text-yellow-700 p-3 text-sm" role="alert">
      <p class="font-medium">No Public Holidays</p>
      <p>There are no public holidays available for the selected date.</p>
    </div>

    <!-- Special Messages Banner -->
    <div v-if="results.special_messages?.length" class="mx-8 mb-4">
      <div class="bg-blue-50 border border-blue-100 rounded-lg p-4">
        <div class="flex flex-col space-y-1">
          <p v-for="(message, index) in results.special_messages" :key="index" 
             class="text-sm text-blue-700">
            {{ message }}
          </p>
        </div>
      </div>
    </div>

    <!-- Results Grid -->
    <div class="flex flex-wrap gap-8 p-8">
      <!-- Personal Information -->
      <IdResultsCard title="Personal Information" icon="👤" class="flex-grow min-w-[350px] basis-[calc(33.333%-2rem)]">
        <dl class="grid grid-cols-2 gap-4">
          <div class="col-span-2 sm:col-span-1">
            <dt class="text-sm font-medium text-gray-500">Date of Birth</dt>
            <dd class="mt-1 text-sm text-gray-900">{{ results.id_info.date_of_birth }}</dd>
          </div>
          <div class="col-span-2 sm:col-span-1">
            <dt class="text-sm font-medium text-gray-500">Gender</dt>
            <dd class="mt-1 text-sm text-gray-900 capitalize">{{ results.id_info.gender }}</dd>
          </div>
          <div class="col-span-2 sm:col-span-1">
            <dt class="text-sm font-medium text-gray-500">Citizenship</dt>
            <dd class="mt-1 text-sm text-gray-900">{{ results.id_info.citizen_status }}</dd>
          </div>
          <div class="col-span-2 sm:col-span-1">
            <dt class="text-sm font-medium text-gray-500">Age</dt>
            <dd class="mt-1 text-sm text-gray-900">{{ results.id_info.age }} years old</dd>
          </div>
        </dl>
      </IdResultsCard>
      <!-- Birth Day Info -->
      <IdResultsCard title="Birth Day Information" icon="📅" class="flex-grow min-w-[350px] basis-[calc(33.333%-2rem)]">
        <dl class="grid grid-cols-2 gap-4">
          <div class="col-span-2 sm:col-span-1">
            <dt class="text-sm font-medium text-gray-500">Day of Week</dt>
            <dd class="mt-1 text-sm text-gray-900">{{ results.birth_insights.day_of_week }}</dd>
          </div>
          <div class="col-span-2 sm:col-span-1">
            <dt class="text-sm font-medium text-gray-500">Next Birthday</dt>
            <dd class="mt-1 text-sm text-gray-900">
              {{ results.birth_insights.birthday_countdown.days_remaining }} days away
            </dd>
          </div>
        </dl>
      </IdResultsCard>
      <!-- Birthday Holiday Information -->
      <IdResultsCard v-if="results.last_birthday || results.next_birthday" title="Birthday Holidays" icon="🎊" class="flex-grow min-w-[350px] basis-[calc(33.333%-2rem)]">
        <dl class="space-y-3">
          <div v-if="results.last_birthday">
            <dt class="text-sm font-medium text-gray-500">Last Birthday</dt>
            <dd class="mt-1 text-sm text-gray-900">{{ formatDate(results.last_birthday.date) }}</dd>
            <dd v-if="results.last_birthday.holiday" class="mt-1 text-sm text-green-600">
              Fell on {{ results.last_birthday.holiday.name }}
            </dd>
            <dd v-else class="mt-1 text-sm text-gray-600">Not a public holiday</dd>
          </div>
          <div v-if="results.next_birthday" class="mt-4">
            <dt class="text-sm font-medium text-gray-500">Next Birthday</dt>
            <dd class="mt-1 text-sm text-gray-900">{{ formatDate(results.next_birthday.date) }}</dd>
            <dd v-if="results.next_birthday.holiday" class="mt-1 text-sm text-green-600">
              Will fall on {{ results.next_birthday.holiday.name }}
            </dd>
            <dd v-else class="mt-1 text-sm text-gray-600">Not a public holiday</dd>
          </div>
        </dl>
      </IdResultsCard>

      <!-- Birth Stone -->
      <IdResultsCard title="Birth Stone" icon="💎" class="flex-grow min-w-[350px] basis-[calc(33.333%-2rem)]">
        <dl class="space-y-3">
          <div>
            <dt class="text-sm font-medium text-gray-500">Name</dt>
            <dd class="mt-1 text-sm text-gray-900">{{ results.birth_insights.birth_symbols.stone.name }}</dd>
          </div>
          <div>
            <dt class="text-sm font-medium text-gray-500">Meaning</dt>
            <dd class="mt-1 text-sm text-gray-900">{{ results.birth_insights.birth_symbols.stone.meaning }}</dd>
          </div>
          <div>
            <dt class="text-sm font-medium text-gray-500">Color</dt>
            <dd class="mt-1 text-sm text-gray-900">{{ results.birth_insights.birth_symbols.stone.color }}</dd>
          </div>
        </dl>
      </IdResultsCard>

      <!-- Birth Flower -->
      <IdResultsCard title="Birth Flower" icon="🌸" class="flex-grow min-w-[350px] basis-[calc(33.333%-2rem)]">
        <dl class="space-y-3">
          <div>
            <dt class="text-sm font-medium text-gray-500">Name</dt>
            <dd class="mt-1 text-sm text-gray-900">{{ results.birth_insights.birth_symbols.flower.name }}</dd>
          </div>
          <div>
            <dt class="text-sm font-medium text-gray-500">Meaning</dt>
            <dd class="mt-1 text-sm text-gray-900">{{ results.birth_insights.birth_symbols.flower.meaning }}</dd>
          </div>
          <div>
            <dt class="text-sm font-medium text-gray-500">Colors</dt>
            <dd class="mt-1 text-sm text-gray-900">{{ results.birth_insights.birth_symbols.flower.colors.join(', ') }}</dd>
          </div>
        </dl>
      </IdResultsCard>

      <!-- Western Zodiac -->
      <IdResultsCard title="Western Zodiac" icon="♈" class="flex-grow min-w-[350px] basis-[calc(33.333%-2rem)]">
        <dl class="space-y-3">
          <div>
            <dt class="text-sm font-medium text-gray-500">Sign</dt>
            <dd class="mt-1 text-sm text-gray-900">{{ results.birth_insights.zodiac.western }}</dd>
          </div>
        </dl>
      </IdResultsCard>

      <!-- Chinese Zodiac -->
      <IdResultsCard title="Chinese Zodiac" icon="🐲" class="flex-grow min-w-[350px] basis-[calc(33.333%-2rem)]">
        <dl class="space-y-3">
          <div>
            <dt class="text-sm font-medium text-gray-500">Sign</dt>
            <dd class="mt-1 text-sm text-gray-900">{{ results.birth_insights.zodiac.chinese }}</dd>
          </div>
        </dl>
      </IdResultsCard>

      <!-- Numerology -->
      <IdResultsCard title="Numerology" icon="🔢" class="flex-grow min-w-[350px] basis-[calc(33.333%-2rem)]">
        <dl class="space-y-3">
          <div>
            <dt class="text-sm font-medium text-gray-500">Life Path Number</dt>
            <dd class="mt-1 text-sm text-gray-900">{{ results.birth_insights.numerology.life_path_number }}</dd>
          </div>
          <div>
            <dt class="text-sm font-medium text-gray-500">Meaning</dt>
            <dd class="mt-1 text-sm text-gray-900">{{ results.birth_insights.numerology.meaning }}</dd>
          </div>
        </dl>
      </IdResultsCard>

      <!-- Shared Birthdays -->
      <IdResultsCard title="Shared Birthdays" icon="🎂" class="flex-grow min-w-[350px] basis-[calc(33.333%-2rem)]">
        <p class="text-sm text-gray-900">{{ results.birth_insights.shared_birthdays.join(', ') }}</p>
      </IdResultsCard>

      <!-- Holidays -->
      <IdResultsCard v-if="results.holidays?.length" title="Public Holidays" icon="🎉" class="flex-grow min-w-[350px] basis-[calc(33.333%-2rem)]">
        <div class="space-y-3">
          <div v-for="holiday in results.holidays" :key="holiday.date" class="border-b border-gray-200 pb-3 last:border-b-0 last:pb-0">
            <div class="flex flex-col">
              <div class="flex items-center justify-between">
                <h4 class="text-sm font-medium text-gray-900">{{ holiday.name }}</h4>
                <span class="text-sm text-gray-500">{{ holiday.date }}</span>
              </div>
              <p class="text-sm text-gray-600 mt-1">{{ holiday.description }}</p>
            </div>
          </div>
        </div>
      </IdResultsCard>
    </div>

    <!-- Holidays Around Birthday - Full Width -->
    <div class="mt-8 px-8">
      <IdResultsCard v-if="results.holidays_around_birthday?.length" title="Holidays Around Birthday" icon="🎉">
        <div class="flex flex-wrap gap-8">
          <div v-for="holiday in results.holidays_around_birthday" :key="holiday.date" 
               class="flex-grow min-w-[350px] basis-[calc(33.333%-2rem)] bg-white rounded-xl shadow-md overflow-hidden transition-transform transform hover:scale-102 hover:shadow-lg">
            <div class="bg-gray-50 px-6 py-4 border-b border-gray-200 flex items-center justify-between">
              <div class="flex items-center">
                <span class="text-xl mr-3">🎈</span>
                <h4 class="text-lg font-semibold text-gray-900 break-words">{{ holiday.name }}</h4>
              </div>
              <span class="text-sm text-gray-500 whitespace-nowrap">{{ holiday.date }}</span>
            </div>
            <div class="p-6">
              <p class="text-sm text-gray-600 break-words">{{ holiday.description }}</p>
            </div>
          </div>
        </div>
      </IdResultsCard>
    </div>
  </div>
</template>

<script setup lang="ts">
import { useIdStore } from '~/stores/id'
import { computed } from 'vue'
import IdResultsCard from './IdResultsCard.vue'

const idStore = useIdStore()
const results = computed(() => idStore.results)

const formatDate = (dateStr: string) => {
  return new Date(dateStr).toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  })
}
</script>