import { ref } from 'vue'

// This will load from a JSON file you'll export from your notebook
export const useSightingsData = () => {
  const sightings = ref<any[]>([])
  const loading = ref(true)
  const error = ref<string | null>(null)

  const loadSightings = async () => {
    try {
      // In development, this loads from your static JSON file
      // You'll generate this from your notebook data
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
