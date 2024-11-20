import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

interface BirthSymbol {
  name: string
  meaning: string
  color?: string
  colors?: string[]
}

interface BirthInsights {
  day_of_week: string
  zodiac: {
    western: string
    chinese: string
  }
  birth_symbols: {
    stone: BirthSymbol
    flower: BirthSymbol
  }
  numerology: {
    life_path_number: number
    meaning: string
  }
  birthday_countdown: {
    days_remaining: number
    is_today: boolean
  }
  shared_birthdays: string[]
}

interface IdInfo {
  date_of_birth: string
  gender: string
  citizen_status: string
  age: number
}

interface Holiday {
  name: string
  description: string
  date: string
}

interface ValidationResults {
  id_info: IdInfo
  birth_insights: BirthInsights
  holidays: Holiday[]
  holidays_around_birthday: Holiday[]
  special_messages?: string[]
}

export const useIdStore = defineStore('id', () => {
  const results = ref<ValidationResults | null>(null)
  const loading = ref(false)
  const error = ref<string | null>(null)

  const hasResults = computed(() => !!results.value)
  const isLoading = computed(() => loading.value)

  function isValidId(idNumber: string): boolean {
    // Basic validation for 13 digits
    if (!/^\d{13}$/.test(idNumber)) {
      return false
    }

    // Check birth date validity
    const year = parseInt(idNumber.substring(0, 2))
    const month = parseInt(idNumber.substring(2, 4))
    const day = parseInt(idNumber.substring(4, 6))

    if (month < 1 || month > 12) return false
    if (day < 1 || day > 31) return false

    // Validate using Luhn algorithm
    return validateLuhn(idNumber)
  }

  function validateLuhn(idNumber: string): boolean {
    let sum = 0
    let alternate = false

    // Loop through values starting from the rightmost side
    for (let i = idNumber.length - 1; i >= 0; i--) {
      let n = parseInt(idNumber.charAt(i))
      if (alternate) {
        n *= 2
        if (n > 9) {
          n = (n % 10) + 1
        }
      }
      sum += n
      alternate = !alternate
    }

    return (sum % 10 === 0)
  }

  async function searchId(idNumber: string) {
    loading.value = true
    error.value = null
    
    try {
      const config = useRuntimeConfig()
      const formData = new FormData()
      formData.append('id_number', idNumber)
      
      const response = await fetch(`${config.public.apiBaseUrl}/api/id/validate`, {
        method: 'POST',
        body: formData
      })

      if (!response.ok) {
        const errorData = await response.json()
        throw new Error(errorData.detail || 'Failed to fetch ID information')
      }

      results.value = await response.json()
    } catch (err) {
      error.value = err instanceof Error ? err.message : 'An error occurred'
      results.value = null
    } finally {
      loading.value = false
    }
  }

  return {
    results,
    loading,
    error,
    hasResults,
    isLoading,
    isValidId,
    searchId
  }
})
