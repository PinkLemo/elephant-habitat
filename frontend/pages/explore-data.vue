<script setup lang="ts">
import { computed, onMounted } from 'vue'
import PublicNavbar from '@/layouts/components/PublicNavbar.vue'
import MapCanvas from '@/components/map/MapCanvas.vue'
import { useSightingsData } from '@/composables/useSightingsData'
import { COUNTRY_NAMES, COUNTRY_THEME_COLORS, COUNTRY_COLORS } from '@/composables/useCountryColors'

definePageMeta({
  path: '/explore-data',
  layout: 'blank',
  public: true,
})

useHead({ title: 'Explore Data — Elephant Habitat' })

// ─── Load sightings data ──────────────────────────────────────────────────
const { sightings, loading, error, loadSightings } = useSightingsData()

onMounted(() => {
  loadSightings()
})

// ─── Country breakdown from real data ─────────────────────────────────────
const countryBreakdown = computed(() => {
  if (!sightings.value || sightings.value.length === 0) return []

  const counts: Record<string, number> = {}
  sightings.value.forEach(s => {
    if (s.countryCode) {
      counts[s.countryCode] = (counts[s.countryCode] || 0) + 1
    }
  })

  const total = sightings.value.length
  return Object.entries(counts)
    .map(([code, count]) => ({
      code,
      name: COUNTRY_NAMES[code] || code,
      records: count,
      pct: (count / total) * 100,
      color: COUNTRY_THEME_COLORS[code] || 'grey',
      hexColor: COUNTRY_COLORS[code] || '#888888',
    }))
    .sort((a, b) => b.records - a.records)
})

// ─── Sightings per year from real data ────────────────────────────────────
const yearlyData = computed(() => {
  if (!sightings.value || sightings.value.length === 0) return []

  const yearCounts: Record<number, number> = {}
  sightings.value.forEach(s => {
    if (s.year && s.year >= 1990) {
      yearCounts[s.year] = (yearCounts[s.year] || 0) + 1
    }
  })

  return Object.entries(yearCounts)
    .map(([year, count]) => ({
      year: parseInt(year),
      count,
    }))
    .sort((a, b) => a.year - b.year)
})

const maxCount = computed(() => {
  if (yearlyData.value.length === 0) return 1
  return Math.max(...yearlyData.value.map(y => y.count))
})

// For display, show a sample of years or all years if under ~30
const displayYears = computed(() => {
  if (yearlyData.value.length <= 30) return yearlyData.value
  // If too many years, show every 5th year
  return yearlyData.value.filter((_, i) => i % 5 === 0)
})

// ─── Stats for the header ──────────────────────────────────────────────────
const totalRecords = computed(() => sightings.value?.length || 0)
const countryCount = computed(() => countryBreakdown.value.length)
const yearRange = computed(() => {
  if (!sightings.value || sightings.value.length === 0) return 'N/A'
  const years = sightings.value.map(s => s.year).filter(y => y)
  if (years.length === 0) return 'N/A'
  return `${Math.min(...years)} – ${Math.max(...years)}`
})
</script>

<template>
  <div class="explore-page-wrapper">
    <PublicNavbar class="mb-12"/>

    <VContainer class="py-10">
      <div class="mb-8">
        <VChip color="primary" variant="tonal" size="small" class="mb-3 text-uppercase font-weight-bold" label>
          Chapter 4.1
        </VChip>
        <h1 class="text-h4 font-weight-bold mb-2">Exploratory Data Analysis</h1>
        <p class="text-body-1 text-medium-emphasis" style="max-inline-size: 640px;">
          {{ totalRecords.toLocaleString() }} georeferenced elephant occurrence records across
          {{ countryCount }} countries, sourced from GBIF and filtered to human-observation
          records with valid coordinates.
        </p>
        <div class="d-flex gap-4 mt-2 flex-wrap">
          <VChip size="small" variant="outlined">
            <VIcon start icon="ri-calendar-line" size="14" />
            {{ yearRange }}
          </VChip>
          <VChip size="small" variant="outlined" color="primary">
            <VIcon start icon="ri-map-pin-line" size="14" />
            {{ totalRecords.toLocaleString() }} records
          </VChip>
        </div>
      </div>

      <!-- Show loading state -->
      <VRow v-if="loading">
        <VCol cols="12" class="text-center py-8">
          <VProgressCircular indeterminate size="48" />
          <p class="text-body-1 text-medium-emphasis mt-4">Loading sightings data...</p>
        </VCol>
      </VRow>

      <!-- Show error state -->
      <VRow v-else-if="error">
        <VCol cols="12">
          <VAlert type="error" variant="tonal">
            {{ error }}
          </VAlert>
        </VCol>
      </VRow>

      <!-- Show data -->
      <template v-else>
        <VRow>
          <!-- ── Country breakdown ─────────────────────────────────────────── -->
          <VCol cols="12" md="5">
            <VCard flat border class="h-100">
              <VCardText>
                <div class="text-overline text-medium-emphasis mb-4">Records by Country</div>

                <div class="stacked-bar mb-6">
                  <div
                    v-for="c in countryBreakdown" :key="c.code"
                    class="stacked-bar-segment"
                    :style="{
                      inlineSize: `${c.pct}%`,
                      background: c.hexColor
                    }"
                  />
                </div>

                <div class="d-flex flex-column gap-y-3">
                  <div v-for="c in countryBreakdown" :key="c.code" class="d-flex align-center justify-space-between">
                    <div class="d-flex align-center gap-x-2">
                      <div class="legend-dot" :style="{ background: c.hexColor }" />
                      <span class="text-body-2 font-weight-medium">{{ c.name }}</span>
                    </div>
                    <span class="text-body-2 text-medium-emphasis">{{ c.records.toLocaleString() }} · {{ c.pct.toFixed(1) }}%</span>
                  </div>
                </div>

                <VDivider class="my-4" />

                <div class="d-flex justify-space-between text-caption text-medium-emphasis">
                  <span>Total: {{ totalRecords.toLocaleString() }} records</span>
                  <span>{{ countryCount }} countries</span>
                </div>
              </VCardText>
            </VCard>
          </VCol>

          <!-- ── Sightings over time ───────────────────────────────────────── -->
          <VCol cols="12" md="7">
            <VCard flat border class="h-100">
              <VCardText>
                <div class="text-overline text-medium-emphasis mb-1">Sightings Per Year</div>
                <p class="text-caption text-medium-emphasis mb-6">
                  The post-2010 surge reflects citizen-science growth (iNaturalist),
                  not necessarily a biological signal. <strong>{{ yearlyData.length }} years</strong> of data.
                </p>

                <div v-if="yearlyData.length === 0" class="text-center py-8">
                  <p class="text-body-2 text-medium-emphasis">No year data available</p>
                </div>

                <div v-else class="year-bars">
                  <div
                    v-for="y in displayYears"
                    :key="y.year"
                    class="year-bar-col"
                    :title="`${y.year}: ${y.count} sightings`"
                  >
                    <div
                      class="year-bar"
                      :style="{
                        blockSize: `${Math.max((y.count / maxCount) * 140, 4)}px`
                      }"
                    />
                    <span class="text-caption text-medium-emphasis mt-2">{{ y.year }}</span>
                  </div>
                </div>

                <!-- Annotation for citizen science surge -->
                <div v-if="yearlyData.length > 0" class="mt-4">
                  <div class="d-flex align-center gap-x-2 text-caption text-medium-emphasis">
                    <VIcon icon="ri-information-line" size="14" color="warning" />
                    <span>Citizen-science inflection point: <strong>~2010</strong></span>
                  </div>
                </div>
              </VCardText>
            </VCard>
          </VCol>

          <!-- ── Spatial distribution (live map) ───────────────────────────── -->
          <VCol cols="12">
            <VCard flat border>
              <VCardText>
                <div class="text-overline text-medium-emphasis mb-4">Spatial Distribution</div>
                <div class="spatial-map-wrapper">
                  <MapCanvas
                    :sightings="sightings"
                    :show-sightings="true"
                    :show-clusters="false"
                    :show-heatmap="false"
                    :show-study-area="true"
                    :interactive="false"
                  />
                </div>
                <p class="text-caption text-medium-emphasis mt-3">
                  {{ totalRecords.toLocaleString() }} elephant sightings across the KAZA landscape.
                  Colours indicate country: Botswana (red), Zimbabwe (green), Zambia (blue), Mozambique (orange).
                </p>
              </VCardText>
            </VCard>
          </VCol>
        </VRow>
      </template>
    </VContainer>
  </div>
</template>

<style lang="scss" scoped>
.stacked-bar {
  display: flex;
  block-size: 12px;
  border-radius: 999px;
  overflow: hidden;
  background: rgba(var(--v-theme-on-surface), 0.06);
}

.stacked-bar-segment {
  block-size: 100%;
  transition: inline-size 0.3s ease;
}

.legend-dot {
  inline-size: 10px;
  block-size: 10px;
  border-radius: 50%;
  flex-shrink: 0;
}

.year-bars {
  display: flex;
  align-items: flex-end;
  justify-content: space-between;
  block-size: 170px;
  gap: 4px;
  padding-inline: 2px;
}

.year-bar-col {
  display: flex;
  flex-direction: column;
  align-items: center;
  flex: 1;
  min-inline-size: 12px;
}

.year-bar {
  inline-size: 100%;
  max-inline-size: 36px;
  min-block-size: 4px;
  border-radius: 4px 4px 0 0;
  background: rgb(var(--v-theme-primary));
  transition: block-size 0.5s ease;
}

.spatial-map-wrapper {
  block-size: 350px;
  border-radius: 8px;
  overflow: hidden;
  background: rgba(var(--v-theme-on-surface), 0.02);
  border: 1px solid rgba(var(--v-theme-on-surface), 0.08);

  :deep(.map-canvas-wrapper) {
    min-height: 350px;
    height: 100%;
  }
}

@media (max-width: 600px) {
  .year-bars {
    block-size: 120px;
    gap: 2px;
  }

  .spatial-map-wrapper {
    block-size: 250px;
  }
}
</style>
