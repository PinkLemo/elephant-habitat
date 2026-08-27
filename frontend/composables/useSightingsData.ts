import { ref } from 'vue'

export interface Sighting {
  decimalLatitude: number
  decimalLongitude: number
  countryCode: string
  year: number
  cluster?: number
}

export const useSightingsData = () => {
  const sightings = ref<Sighting[]>([])
  const loading = ref(true)
  const error = ref<string | null>(null)

  const loadSightings = async () => {
    loading.value = true
    error.value = null

    try {
      // In development, this loads from your static JSON file
      const data = await import('~/public/data/sightings.json')
      sightings.value = data.default || data
      loading.value = false
    } catch (err) {
      error.value = 'Failed to load sighting data'
      loading.value = false
      console.error(err)
    }
  }

  return { sightings, loading, error, loadSightings }
}
