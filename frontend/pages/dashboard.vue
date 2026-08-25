<script setup lang="ts">
import { ref } from 'vue'
import PublicNavbar from '@/layouts/components/PublicNavbar.vue'

definePageMeta({
  path: '/dashboard',
  layout: 'blank',
  public: true,
})

useHead({ title: 'Dashboard — Elephant Habitat' })

// ─── Season toggle ─────────────────────────────────────────────────────────
// Feeds season_encoded (1 = wet, 0 = dry) into the point prediction call
const season = ref<'wet' | 'dry'>('wet')

// ─── Map layer toggles ─────────────────────────────────────────────────────
// Sightings + clusters read from the static GeoJSON cache; heatmap reads the
// precomputed 100x100 suitability grid (see engine/build_geojson_cache.py)
const layers = ref({
  sightings: true,
  clusters: true,
  heatmap: false,
})

// ─── Point prediction result ────────────────────────────────────────────────
// Placeholder values until usePredictApi() wires this to POST /api/predict/point
const prediction = ref({
  suitability: 88,
  elevation: 450,
  ndvi: 0.34,
  distToWater: 12,
})

// TODO: replace with a real map instance (Mapbox GL / Vue-Leaflet)
// mounted into #map-canvas below. On map click, call usePredictApi()
// with { lat, lon, season } and update `prediction`.
const mapCanvas = ref<HTMLElement>()
</script>

<template>
  <div class="dashboard-page-wrapper">
    <PublicNavbar />

    <VContainer fluid class="py-6">
      <VRow>

        <!-- ── Sidebar controls ──────────────────────────────────────────── -->
        <VCol cols="12" md="3">
          <div class="d-flex flex-column gap-y-6">

            <VCard flat border>
              <VCardText>
                <div class="text-overline text-medium-emphasis mb-3">Season</div>
                <VBtnToggle v-model="season" mandatory color="primary" density="comfortable" divided class="w-100">
                  <VBtn value="wet" class="flex-grow-1">
                    <VIcon start icon="ri-drop-line" />
                    Wet
                  </VBtn>
                  <VBtn value="dry" class="flex-grow-1">
                    <VIcon start icon="ri-sun-line" />
                    Dry
                  </VBtn>
                </VBtnToggle>
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
                </div>
              </VCardText>
            </VCard>

            <VCard flat border color="primary" variant="tonal">
              <VCardText>
                <div class="text-overline text-medium-emphasis mb-2">Point Prediction</div>
                <div class="text-h3 font-weight-bold text-primary mb-3">
                  {{ prediction.suitability }}%
                </div>
                <div class="d-flex flex-column gap-y-2">
                  <div class="d-flex align-center gap-x-2 text-body-2">
                    <VIcon icon="ri-mountain-line" size="18" />
                    Elevation: {{ prediction.elevation }}m
                  </div>
                  <div class="d-flex align-center gap-x-2 text-body-2">
                    <VIcon icon="ri-leaf-line" size="18" />
                    NDVI proxy: {{ prediction.ndvi }}
                  </div>
                  <div class="d-flex align-center gap-x-2 text-body-2">
                    <VIcon icon="ri-drop-line" size="18" />
                    Distance to water: {{ prediction.distToWater }}km
                  </div>
                </div>
              </VCardText>
            </VCard>

          </div>
        </VCol>

        <!-- ── Map canvas ────────────────────────────────────────────────── -->
        <VCol cols="12" md="9">
          <VCard flat border class="map-card">
            <!-- Real map (Mapbox GL / Vue-Leaflet) mounts here -->
            <div id="map-canvas" ref="mapCanvas" class="map-canvas">

              <VChip class="map-overlay-chip top-left" size="small" variant="elevated">
                <VIcon start icon="ri-map-2-line" size="16" />
                Interactive map canvas
              </VChip>

              <!-- Placeholder hotspot markers — replace with real GeoJSON layer -->
              <div class="hotspot-blob" style="inset-block-start: 130px; inset-inline-start: 200px; inline-size: 70px; block-size: 70px; background: rgb(var(--v-theme-error)); opacity: 0.45;" />
              <div class="hotspot-blob" style="inset-block-start: 180px; inset-inline-start: 90px; inline-size: 40px; block-size: 40px; background: rgb(var(--v-theme-warning)); opacity: 0.55;" />
              <div class="hotspot-blob" style="inset-block-start: 60px; inset-inline-start: 300px; inline-size: 30px; block-size: 30px; background: rgb(var(--v-theme-warning)); opacity: 0.45;" />
              <div class="hotspot-dot" style="inset-block-start: 220px; inset-inline-start: 260px;" />
              <div class="hotspot-dot" style="inset-block-start: 150px; inset-inline-start: 150px;" />

              <VChip class="map-overlay-chip bottom-right" size="small" variant="elevated" color="primary">
                <VIcon start icon="ri-cursor-line" size="16" />
                Click to predict at point
              </VChip>
            </div>
          </VCard>
        </VCol>

      </VRow>
    </VContainer>
  </div>
</template>

<style lang="scss" scoped>
.map-card {
  overflow: hidden;
}

.map-canvas {
  position: relative;
  block-size: 640px;
  background: rgba(var(--v-theme-on-surface), 0.02);
}

.map-overlay-chip {
  position: absolute;

  &.top-left {
    inset-block-start: 12px;
    inset-inline-start: 12px;
  }

  &.bottom-right {
    inset-block-end: 12px;
    inset-inline-end: 12px;
  }
}

.hotspot-blob {
  position: absolute;
  border-radius: 50%;
  pointer-events: none;
}

.hotspot-dot {
  position: absolute;
  inline-size: 12px;
  block-size: 12px;
  border-radius: 50%;
  background: rgb(var(--v-theme-primary));
  pointer-events: none;
}
</style>
