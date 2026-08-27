// composables/usePredictApi.ts
import { ref } from 'vue'

type Season = 'wet' | 'dry'

interface PredictResponse {
  suitability: number
  elevation: number
  dist_to_water_km: number
  ndvi_proxy: number
}

export const usePredictApi = () => {
  const loading = ref(false)
  const error = ref<string | null>(null)

  const config = useRuntimeConfig()

  const predictPoint = async (lat: number, lon: number, season: Season) => {
    loading.value = true
    error.value = null

    try {
      const response = await $fetch<PredictResponse>('/api/predict/point', {
        baseURL: config.public.apiBase,
        method: 'POST',
        body: { lat, lon, season },
      })
      return response
    } catch (err: any) {
      // $fetch throws FetchError — status lives at err.response?.status / err.statusCode
      const status = err?.response?.status ?? err?.statusCode

      if (status === 429)
        error.value = 'Too many requests — wait a moment and try again.'
      else if (status === 422)
        error.value = 'That point is outside the study area.'
      else
        error.value = 'Prediction failed — is the backend running?'

      throw err
    } finally {
      loading.value = false
    }
  }

  return { predictPoint, loading, error }
}
