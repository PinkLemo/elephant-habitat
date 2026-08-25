<script setup lang="ts">
import { ref } from 'vue'
import PublicNavbar from '@/layouts/components/PublicNavbar.vue'

definePageMeta({
  path: '/explore-data',
  layout: 'blank',
  public: true,
})

useHead({ title: 'Explore Data — Elephant Habitat' })

// ─── Country breakdown (Table 1) ────────────────────────────────────────────
const countries = ref([
  { name: 'Botswana', records: 1893, pct: 61.7, color: 'primary' },
  { name: 'Zimbabwe', records: 641, pct: 20.9, color: 'success' },
  { name: 'Zambia', records: 498, pct: 16.2, color: 'info' },
  { name: 'Mozambique', records: 76, pct: 2.5, color: 'warning' },
])

// ─── Sightings per year, representative sample ──────────────────────────────
// TODO: replace with the full 1990–2026 series from elephant_final_dataset.csv
const yearlySample = ref([
  { year: 1990, count: 4 },
  { year: 2000, count: 9 },
  { year: 2010, count: 103 },
  { year: 2015, count: 168 },
  { year: 2020, count: 226 },
  { year: 2023, count: 480 },
  { year: 2024, count: 365 },
])
const maxCount = Math.max(...yearlySample.value.map(y => y.count))
</script>

<template>
  <div class="explore-page-wrapper">
    <PublicNavbar />

    <VContainer class="py-10">
      <div class="mb-8">
        <VChip color="primary" variant="tonal" size="small" class="mb-3 text-uppercase font-weight-bold" label>
          Chapter 4.1
        </VChip>
        <h1 class="text-h4 font-weight-bold mb-2">Exploratory Data Analysis</h1>
        <p class="text-body-1 text-medium-emphasis" style="max-inline-size: 640px;">
          3,067 georeferenced elephant occurrence records across four countries, sourced from GBIF
          and filtered to human-observation records with valid coordinates.
        </p>
      </div>

      <VRow>
        <!-- ── Country breakdown ─────────────────────────────────────────── -->
        <VCol cols="12" md="5">
          <VCard flat border class="h-100">
            <VCardText>
              <div class="text-overline text-medium-emphasis mb-4">Records by Country</div>

              <div class="stacked-bar mb-6">
                <div
                  v-for="c in countries" :key="c.name" class="stacked-bar-segment"
                  :style="{ inlineSize: `${c.pct}%`, background: `rgb(var(--v-theme-${c.color}))` }"
                />
              </div>

              <div class="d-flex flex-column gap-y-3">
                <div v-for="c in countries" :key="c.name" class="d-flex align-center justify-space-between">
                  <div class="d-flex align-center gap-x-2">
                    <div class="legend-dot" :style="{ background: `rgb(var(--v-theme-${c.color}))` }" />
                    <span class="text-body-2 font-weight-medium">{{ c.name }}</span>
                  </div>
                  <span class="text-body-2 text-medium-emphasis">{{ c.records.toLocaleString() }} · {{ c.pct }}%</span>
                </div>
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
                The post-2010 surge reflects citizen-science growth (iNaturalist), not a biological signal.
              </p>

              <div class="year-bars">
                <div v-for="y in yearlySample" :key="y.year" class="year-bar-col">
                  <div class="year-bar" :style="{ blockSize: `${(y.count / maxCount) * 140}px` }" />
                  <span class="text-caption text-medium-emphasis mt-2">{{ y.year }}</span>
                </div>
              </div>
            </VCardText>
          </VCard>
        </VCol>

        <!-- ── Spatial distribution ──────────────────────────────────────── -->
        <VCol cols="12">
          <VCard flat border>
            <VCardText>
              <div class="text-overline text-medium-emphasis mb-4">Spatial Distribution</div>
              <div class="spatial-preview d-flex align-center justify-center">
                <div class="text-center">
                  <VIcon icon="ri-map-2-line" size="32" class="text-medium-emphasis mb-2" />
                  <p class="text-body-2 text-medium-emphasis mb-0">
                    Static preview of Figure 1 — swap for the live Leaflet/Mapbox layer
                  </p>
                </div>
              </div>
            </VCardText>
          </VCard>
        </VCol>
      </VRow>
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

.legend-dot {
  inline-size: 10px;
  block-size: 10px;
  border-radius: 50%;
}

.year-bars {
  display: flex;
  align-items: flex-end;
  justify-content: space-between;
  block-size: 170px;
  gap: 12px;
}

.year-bar-col {
  display: flex;
  flex-direction: column;
  align-items: center;
  flex: 1;
}

.year-bar {
  inline-size: 100%;
  max-inline-size: 36px;
  border-radius: 4px 4px 0 0;
  background: rgb(var(--v-theme-primary));
}

.spatial-preview {
  block-size: 220px;
  border-radius: 8px;
  background: rgba(var(--v-theme-on-surface), 0.02);
  border: 1px dashed rgba(var(--v-theme-on-surface), 0.12);
}
</style>
