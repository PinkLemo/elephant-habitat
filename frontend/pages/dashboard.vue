<script setup lang="ts">
import {onMounted, ref, watch} from 'vue'
import PublicNavbar from '@/layouts/components/PublicNavbar.vue'
import MapCanvas from '@/components/map/MapCanvas.vue'
import {useSightingsData} from '@/composables/useSightingsData'
import Footer from "@/layouts/components/Footer.vue";

definePageMeta({
  path: '/dashboard',
  layout: 'blank',
  public: true,
})

useHead({title: 'Dashboard — Elephant Habitat'})

// ─── Season toggle ─────────────────────────────────────────────────────────
const season = ref<'wet' | 'dry'>('wet')

// ─── Map layer toggles ─────────────────────────────────────────────────────
const layers = ref({
  sightings: true,
  clusters: false,
  heatmap: false,
  studyArea: true,
})

// ─── Point prediction state ──────────────────────────────────────────────
const selectedPoint = ref<{ lat: number; lon: number } | null>(null)
const prediction = ref<{
  suitability: number | null
  elevation: number | null
  ndvi: number | null
  distToWater: number | null
}>({
  suitability: null,
  elevation: null,
  ndvi: null,
  distToWater: null,
})

// ─── Load sightings data ──────────────────────────────────────────────────
const {sightings, loading, error, loadSightings} = useSightingsData()

onMounted(() => {
  loadSightings()
})

// ─── Handle point selection from map ──────────────────────────────────────
const {predictPoint, loading: predicting, error: predictError} = usePredictApi()

const fetchPrediction = async (lat: number, lon: number, seasonValue: 'wet' | 'dry') => {
  prediction.value = {suitability: null, elevation: null, ndvi: null, distToWater: null}

  try {
    const result = await predictPoint(lat, lon, seasonValue)
    prediction.value = {
      suitability: result.suitability,
      elevation: result.elevation,
      ndvi: result.ndvi_proxy,
      distToWater: result.dist_to_water_km,
    }
  } catch {
    // predictError.value is already set by the composable — surface it in the template below
  }
}

const handlePointSelected = (lat: number, lon: number) => {
  selectedPoint.value = {lat, lon}
  fetchPrediction(lat, lon, season.value)
}

// Toggling season with a point already selected re-scores that same point —
// no need to click the map again
watch(season, (newSeason) => {
  if (selectedPoint.value)
    fetchPrediction(selectedPoint.value.lat, selectedPoint.value.lon, newSeason)
})
</script>

<template>
  <div class="dashboard-page-wrapper">
    <PublicNavbar class="mb-15"/>

    <VContainer fluid class="py-6">
      <VRow>
        <!-- ── Sidebar controls ──────────────────────────────────────────── -->
        <!-- ── Sidebar controls ──────────────────────────────────────────── -->
        <VCol cols="12" md="3">
          <div class="d-flex flex-column gap-y-3">

            <VCard flat border>
              <VCardText class="pb-0">
                <div class="text-overline text-medium-emphasis mb-3">Interactive Habitat Suitability Dashboard</div>
                <p class="text-body-1 font-weight-medium">
                  Click any point to predict habitat
                  suitability, or toggle map layers to explore patterns.
                </p>
              </VCardText>
            </VCard>

            <VCard flat border>
              <VCardText>
                <div class="text-overline text-medium-emphasis mb-3">Season</div>
                <VTabs v-model="season" class="v-tabs-pill" density="comfortable" grow>
                  <VTab value="wet">
                    <VIcon start icon="ri-drop-line"/>
                    Wet
                  </VTab>
                  <VTab value="dry">
                    <VIcon start icon="ri-sun-line"/>
                    Dry
                  </VTab>
                </VTabs>
              </VCardText>
            </VCard>

            <VCard flat border>
              <VCardText>
                <div class="text-overline text-medium-emphasis mb-3">Map Layers</div>
                <div class="d-flex flex-column gap-y-1">
                  <VSwitch
                    v-model="layers.sightings" color="primary" density="compact" hide-details
                    label="Elephant sightings"
                  />
                  <VSwitch
                    v-model="layers.clusters" color="primary" density="compact" hide-details
                    label="DBSCAN clusters"
                  />
                  <VSwitch
                    v-model="layers.heatmap" color="primary" density="compact" hide-details
                    label="Suitability heatmap"
                  />
                  <VSwitch
                    v-model="layers.studyArea" color="primary" density="compact" hide-details
                    label="Study area boundary"
                  />
                </div>
              </VCardText>
            </VCard>

            <VCard flat border color="primary" variant="tonal">
              <VCardText>
                <div class="text-overline text-medium-emphasis mb-2">Point Prediction</div>
                <VProgressCircular v-if="predicting" indeterminate size="20" class="mb-2"/>
                <VAlert v-else-if="predictError" type="error" variant="tonal" density="compact" class="mb-2">
                  {{ predictError }}
                </VAlert>

                <div v-if="selectedPoint" class="mb-2">
                  <div class="text-caption text-medium-emphasis">
                    {{ selectedPoint.lat.toFixed(4) }}, {{ selectedPoint.lon.toFixed(4) }}
                  </div>
                </div>

                <div v-if="prediction.suitability === null && selectedPoint"
                     class="text-body-2 text-medium-emphasis py-2">
                  <VIcon icon="ri-information-line" class="me-1"/>
                  Click a point on the map to get prediction
                </div>

                <div v-else-if="prediction.suitability !== null" class="d-flex flex-column gap-y-2">
                  <div class="text-h3 font-weight-bold text-primary mb-2">
                    {{ Math.round(prediction.suitability * 100) }}%
                  </div>
                  <div class="d-flex flex-column gap-y-2">
                    <div class="d-flex align-center gap-x-2 text-body-2">
                      <VIcon icon="ri-mountain-line" size="18"/>
                      Elevation: {{ prediction.elevation?.toFixed(0) || '--' }}m
                    </div>
                    <div class="d-flex align-center gap-x-2 text-body-2">
                      <VIcon icon="ri-leaf-line" size="18"/>
                      CWBI: {{ prediction.ndvi?.toFixed(3) || '--' }}
                    </div>
                    <div class="d-flex align-center gap-x-2 text-body-2">
                      <VIcon icon="ri-drop-line" size="18"/>
                      Distance to water: {{ prediction.distToWater?.toFixed(1) || '--' }}km
                    </div>
                  </div>
                </div>

                <div v-else class="text-body-2 text-medium-emphasis py-2">
                  <VIcon icon="ri-cursor-line" class="me-1"/>
                  Click the map to predict habitat suitability
                </div>
              </VCardText>
            </VCard>

            <!-- Show loading state -->
            <VCard v-if="loading" flat border>
              <VCardText class="text-center py-3">
                <VProgressCircular indeterminate size="24"/>
                <span class="text-body-2 text-medium-emphasis ms-2">Loading sightings...</span>
              </VCardText>
            </VCard>

            <!-- Show error state -->
            <VCard v-if="error" flat border color="error">
              <VCardText class="text-center py-3">
                <VIcon icon="ri-error-warning-line" color="error"/>
                <span class="text-body-2 text-medium-emphasis ms-2">{{ error }}</span>
              </VCardText>
            </VCard>

          </div>
        </VCol>

        <!-- ── Map canvas ────────────────────────────────────────────────── -->
        <VCol cols="12" md="9">
          <VCard flat border class="map-card">
            <MapCanvas
              :sightings="sightings"
              :show-sightings="layers.sightings"
              :show-clusters="layers.clusters"
              :show-heatmap="layers.heatmap"
              :show-study-area="layers.studyArea"
              @point-selected="handlePointSelected"
            />
          </VCard>
        </VCol>

      </VRow>
    </VContainer>
  </div>
  <!-- ═══════════════════════════════════════════════════════════ FOOTER ═══ -->
  <section class="ma-6">
    <Footer />
  </section>
</template>

<style lang="scss" scoped>
.map-card {
  overflow: hidden;
  height: 640px;

  :deep(.v-card-text) {
    padding: 0;
    height: 100%;
  }
}

.map-canvas-wrapper {
  width: 100%;
  height: 100%;
  min-height: 600px;
}

.dashboard-page-wrapper {
  // Ensure the map card doesn't overflow
  overflow: hidden;
}
</style>
