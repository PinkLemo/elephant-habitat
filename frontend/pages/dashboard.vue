<script setup lang="ts">
import { onMounted, ref, watch } from 'vue'
import PublicNavbar from '@/layouts/components/PublicNavbar.vue'
import MapCanvas from '@/components/map/MapCanvas.vue'
import Footer from '@/layouts/components/Footer.vue'
import { useSightingsData } from '@/composables/useSightingsData'
import { useCountryColors } from '@/composables/useCountryColors'

definePageMeta({
  path: '/dashboard',
  layout: 'blank',
  public: true,
})

useHead({ title: 'Dashboard — Elephant Habitat' })

// ─── Season toggle ─────────────────────────────────────────────────────────
const season = ref<'wet' | 'dry'>('wet')

// ─── Map layer toggles ─────────────────────────────────────────────────────
const layers = ref({
  sightings: true,
  clusters: false,
  heatmap: false,
  studyArea: true,
})

// ─── Legend data — same source MapCanvas uses, so colors always match ──────
const { COUNTRY_COLORS, COUNTRY_NAMES } = useCountryColors()

// ─── Point prediction state ──────────────────────────────────────────────
const selectedPoint = ref<{ lat: number, lon: number } | null>(null)
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
const { sightings, loading, error, loadSightings } = useSightingsData()

onMounted(() => {
  loadSightings()
})

// ─── Handle point selection from map ──────────────────────────────────────
const { predictPoint, loading: predicting, error: predictError } = usePredictApi()

const fetchPrediction = async (lat: number, lon: number, seasonValue: 'wet' | 'dry') => {
  prediction.value = { suitability: null, elevation: null, ndvi: null, distToWater: null }

  try {
    const result = await predictPoint(lat, lon, seasonValue)
    prediction.value = {
      suitability: result.suitability,
      elevation: result.elevation,
      ndvi: result.ndvi_proxy,
      distToWater: result.dist_to_water_km,
    }
  }
  catch {
    // predictError.value is already set by the composable — surface it in the template below
  }
}

const handlePointSelected = (lat: number, lon: number) => {
  selectedPoint.value = { lat, lon }
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
    <PublicNavbar class="mb-15" />

    <VContainer fluid class="py-6">
      <VRow>
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
                    <VIcon start icon="ri-drop-line" />
                    Wet
                  </VTab>
                  <VTab value="dry">
                    <VIcon start icon="ri-sun-line" />
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
                    v-model="layers.sightings" color="info" density="compact" hide-details
                    label="Elephant sightings"
                  />
                  <VSwitch
                    v-model="layers.clusters" color="info" density="compact" hide-details
                    label="DBSCAN clusters"
                  />
                  <VSwitch
                    v-model="layers.heatmap" color="info" density="compact" hide-details
                    label="Suitability heatmap"
                  />
                  <VSwitch
                    v-model="layers.studyArea" color="info" density="compact" hide-details
                    label="Study area boundary"
                  />
                </div>
                <p class="text-caption text-medium-emphasis mt-3 mb-0">
                  Sightings are individual GBIF records; clusters group nearby sightings
                  using DBSCAN (Chapter 3.4).
                </p>
              </VCardText>
            </VCard>

            <!-- ── Map key — explains every color/symbol currently visible ── -->
            <VCard flat border>
              <VCardText>
                <div class="text-overline text-medium-emphasis mb-3">Map Key</div>
                <div class="d-flex flex-column gap-y-3">

                  <div v-if="layers.sightings">
                    <div class="text-caption font-weight-medium text-medium-emphasis mb-2">
                      Sightings by country
                    </div>
                    <div class="d-flex flex-column gap-y-1">
                      <div v-for="code in Object.keys(COUNTRY_NAMES)" :key="code" class="d-flex align-center gap-x-2">
                        <div class="legend-dot" :style="{ background: COUNTRY_COLORS[code] }" />
                        <span class="text-body-2">{{ COUNTRY_NAMES[code] }}</span>
                      </div>
                    </div>
                  </div>

                  <div v-if="layers.clusters">
                    <div class="text-caption font-weight-medium text-medium-emphasis mb-2">
                      DBSCAN clusters
                    </div>
                    <p class="text-body-2 text-medium-emphasis mb-0">
                      Each color marks a distinct cluster — hover a point to see its
                      cluster ID, country, and year.
                    </p>
                  </div>

                  <div v-if="layers.studyArea" class="d-flex align-center gap-x-2">
                    <div class="legend-line" />
                    <span class="text-body-2">Study area boundary</span>
                  </div>

                  <div class="d-flex align-center gap-x-2">
                    <div class="legend-dot legend-dot--selected" />
                    <span class="text-body-2">Your selected point</span>
                  </div>

                </div>
              </VCardText>
            </VCard>

            <!-- ── Point Prediction ── -->
<!--            <VCard flat border color="primary" variant="tonal">-->
<!--              <VCardText>-->
<!--                <div class="text-overline text-medium-emphasis mb-2">Point Prediction</div>-->
<!--                <VProgressCircular v-if="predicting" indeterminate size="20" class="mb-2" />-->
<!--                <VAlert v-else-if="predictError" type="error" variant="tonal" density="compact" class="mb-2">-->
<!--                  {{ predictError }}-->
<!--                </VAlert>-->

<!--                <div v-if="selectedPoint" class="mb-2">-->
<!--                  <div class="text-caption text-medium-emphasis">-->
<!--                    {{ selectedPoint.lat.toFixed(4) }}, {{ selectedPoint.lon.toFixed(4) }}-->
<!--                  </div>-->
<!--                </div>-->

<!--                <div-->
<!--                  v-if="prediction.suitability === null && selectedPoint"-->
<!--                  class="text-body-2 text-medium-emphasis py-2"-->
<!--                >-->
<!--                  <VIcon icon="ri-information-line" class="me-1" />-->
<!--                  Click a point on the map to get prediction-->
<!--                </div>-->

<!--                <div v-else-if="prediction.suitability !== null" class="d-flex flex-column gap-y-2">-->
<!--                  <div class="text-h3 font-weight-bold text-primary mb-2">-->
<!--                    {{ Math.round(prediction.suitability * 100) }}%-->
<!--                  </div>-->
<!--                  <div class="d-flex flex-column gap-y-2">-->
<!--                    <div class="d-flex align-center gap-x-2 text-body-2">-->
<!--                      <VIcon icon="ri-mountain-line" size="18" />-->
<!--                      Elevation: {{ prediction.elevation?.toFixed(0) || '&#45;&#45;' }}m-->
<!--                    </div>-->
<!--                    <div class="d-flex align-center gap-x-2 text-body-2">-->
<!--                      <VIcon icon="ri-leaf-line" size="18" />-->
<!--                      CWBI: {{ prediction.ndvi?.toFixed(3) || '&#45;&#45;' }}-->
<!--                    </div>-->
<!--                    <div class="d-flex align-center gap-x-2 text-body-2">-->
<!--                      <VIcon icon="ri-drop-line" size="18" />-->
<!--                      Distance to water: {{ prediction.distToWater?.toFixed(1) || '&#45;&#45;' }}km-->
<!--                    </div>-->
<!--                  </div>-->
<!--                </div>-->

<!--                <div v-else class="text-body-2 text-medium-emphasis py-2">-->
<!--                  <VIcon icon="ri-cursor-line" class="me-1" />-->
<!--                  Click the map to predict habitat suitability-->
<!--                </div>-->
<!--              </VCardText>-->
<!--            </VCard>-->

            <!-- Show loading state -->
            <VCard v-if="loading" flat border>
              <VCardText class="text-center py-3">
                <VProgressCircular indeterminate size="24" />
                <span class="text-body-2 text-medium-emphasis ms-2">Loading sightings...</span>
              </VCardText>
            </VCard>

            <!-- Show error state -->
            <VCard v-if="error" flat border color="error">
              <VCardText class="text-center py-3">
                <VIcon icon="ri-error-warning-line" color="error" />
                <span class="text-body-2 text-medium-emphasis ms-2">{{ error }}</span>
              </VCardText>
            </VCard>

          </div>
        </VCol>

        <!-- ── Map canvas ────────────────────────────────────────────────── -->
        <VCol cols="12" md="9">
          <VCard flat border class="map-card mb-4">
            <MapCanvas
              :sightings="sightings"
              :show-sightings="layers.sightings"
              :show-clusters="layers.clusters"
              :show-heatmap="layers.heatmap"
              :show-study-area="layers.studyArea"
              @point-selected="handlePointSelected"
            />
          </VCard>

          <!-- ── Point Prediction ── -->
          <VCard flat border color="primary" variant="tonal">
            <VCardText>
              <div class="text-overline text-medium-emphasis mb-2">Point Prediction</div>
              <VProgressCircular v-if="predicting" indeterminate size="20" class="mb-2" />
              <VAlert v-else-if="predictError" type="error" variant="tonal" density="compact" class="mb-2">
                {{ predictError }}
              </VAlert>

              <div v-if="selectedPoint" class="mb-2">
                <div class="text-caption text-medium-emphasis">
                  {{ selectedPoint.lat.toFixed(4) }}, {{ selectedPoint.lon.toFixed(4) }}
                </div>
              </div>

              <div
                v-if="prediction.suitability === null && selectedPoint"
                class="text-body-2 text-medium-emphasis py-2"
              >
                <VIcon icon="ri-information-line" class="me-1" />
                Click a point on the map to get prediction
              </div>

              <div v-else-if="prediction.suitability !== null" class="d-flex flex-column gap-y-2">
                <div class="text-h3 font-weight-bold text-primary mb-2">
                  {{ Math.round(prediction.suitability * 100) }}%
                </div>
                <div class="d-flex flex-column gap-y-2">
                  <div class="d-flex align-center gap-x-2 text-body-2">
                    <VIcon icon="ri-mountain-line" size="18" />
                    Elevation: {{ prediction.elevation?.toFixed(0) || '--' }}m
                  </div>
                  <div class="d-flex align-center gap-x-2 text-body-2">
                    <VIcon icon="ri-leaf-line" size="18" />
                    CWBI: {{ prediction.ndvi?.toFixed(3) || '--' }}
                  </div>
                  <div class="d-flex align-center gap-x-2 text-body-2">
                    <VIcon icon="ri-drop-line" size="18" />
                    Distance to water: {{ prediction.distToWater?.toFixed(1) || '--' }}km
                  </div>
                </div>
              </div>

              <div v-else class="text-body-2 text-medium-emphasis py-2">
                <VIcon icon="ri-cursor-line" class="me-1" />
                Click the map to predict habitat suitability
              </div>
            </VCardText>
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
  overflow: hidden;
}

.legend-dot {
  inline-size: 10px;
  block-size: 10px;
  border-radius: 50%;
  flex-shrink: 0;
}

.legend-dot--selected {
  background: #7367F0;
  border: 2px solid white;
  box-shadow: 0 0 0 1px rgba(var(--v-theme-on-surface), 0.15);
}

.legend-line {
  inline-size: 18px;
  block-size: 0;
  border-top: 2px dashed #7367F0;
  flex-shrink: 0;
}
</style>
