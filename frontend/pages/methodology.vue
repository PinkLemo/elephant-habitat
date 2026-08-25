<script setup lang="ts">
import { ref } from 'vue'
import PublicNavbar from '@/layouts/components/PublicNavbar.vue'

definePageMeta({
  path: '/methodology',
  layout: 'blank',
  public: true,
})

useHead({ title: 'Methodology — Elephant Habitat' })

// ─── Methodological refinements (Chapter 3, in response to supervisor feedback) ──
const refinements = ref([
  {
    title: 'Pseudo-absence generation',
    before: 'Random points across the full bounding box',
    after: 'Targeted at four ecologically defined low-density regions',
    icon: 'ri-map-pin-range-line',
  },
  {
    title: 'Feature set',
    before: 'Raw latitude/longitude included as predictors',
    after: 'Coordinates removed to prevent spatial memorisation',
    icon: 'ri-crosshair-line',
  },
  {
    title: 'Model evaluation',
    before: 'Random 80/20 train-test split (AUC 0.9984)',
    after: 'Five-fold spatial block cross-validation (AUC 0.8850)',
    icon: 'ri-scales-3-line',
  },
  {
    title: 'Grid interpolation',
    before: 'Elevation/CWBI assigned by random sampling',
    after: 'KNN spatial interpolation from five nearest known points',
    icon: 'ri-grid-line',
  },
])

// ─── Limitations (Chapter 5.3) ──────────────────────────────────────────────
const limitations = ref([
  'GBIF records carry spatial sampling bias toward roads, lodges, and urban centres.',
  '36.0% of CWBI values were median-imputed due to Open-Meteo API retrieval failures.',
  'Pseudo-absence points may still fall within genuinely suitable, unsampled habitat.',
  'The model is a static snapshot — it does not account for climate or land-use change over time.',
])

// ─── Downloads ───────────────────────────────────────────────────────────────
const downloads = ref([
  { label: 'Full Dissertation (PDF)', icon: 'ri-file-pdf-2-line', href: '#' },
  { label: 'Jupyter Notebook (.ipynb)', icon: 'ri-code-s-slash-line', href: '#' },
  { label: 'Final Dataset (.csv)', icon: 'ri-file-excel-2-line', href: '#' },
])
</script>

<template>
  <div class="methodology-page-wrapper">
    <PublicNavbar />

    <VContainer class="py-10">
      <div class="mb-8">
        <VChip color="primary" variant="tonal" size="small" class="mb-3 text-uppercase font-weight-bold" label>
          Chapter 3 &amp; 5
        </VChip>
        <h1 class="text-h4 font-weight-bold mb-2">Methodology</h1>
        <p class="text-body-1 text-medium-emphasis" style="max-inline-size: 640px;">
          A quantitative, secondary-data design following the CRISP-DM framework, refined
          twice in response to supervisor feedback on spatial rigour.
        </p>
      </div>

      <!-- ── Refinement timeline ───────────────────────────────────────── -->
      <VCard flat border class="mb-8">
        <VCardText>
          <div class="text-overline text-medium-emphasis mb-4">Methodological Refinements</div>

          <VTimeline align="start" side="end" density="comfortable" line-inset="8">
            <VTimelineItem v-for="r in refinements" :key="r.title" dot-color="primary" size="small">
              <template #icon>
                <VIcon :icon="r.icon" size="16" color="white" />
              </template>
              <div class="mb-4">
                <div class="text-body-1 font-weight-semibold mb-1">{{ r.title }}</div>
                <div class="text-body-2 text-medium-emphasis">
                  <VIcon icon="ri-close-circle-line" size="14" color="error" class="me-1" />
                  {{ r.before }}
                </div>
                <div class="text-body-2 text-medium-emphasis">
                  <VIcon icon="ri-checkbox-circle-line" size="14" color="success" class="me-1" />
                  {{ r.after }}
                </div>
              </div>
            </VTimelineItem>
          </VTimeline>
        </VCardText>
      </VCard>

      <VRow>
        <!-- ── Limitations ────────────────────────────────────────────── -->
        <VCol cols="12" md="7">
          <VCard flat border class="h-100">
            <VCardText>
              <div class="text-overline text-medium-emphasis mb-4">Limitations</div>
              <div class="d-flex flex-column gap-y-3">
                <div v-for="(l, i) in limitations" :key="i" class="d-flex gap-x-3">
                  <VIcon icon="ri-alert-line" size="18" color="warning" class="mt-1 flex-shrink-0" />
                  <span class="text-body-2 text-medium-emphasis">{{ l }}</span>
                </div>
              </div>
            </VCardText>
          </VCard>
        </VCol>

        <!-- ── Downloads ──────────────────────────────────────────────── -->
        <VCol cols="12" md="5">
          <VCard flat border class="h-100">
            <VCardText>
              <div class="text-overline text-medium-emphasis mb-4">Downloads</div>
              <div class="d-flex flex-column gap-y-3">
                <VBtn
                  v-for="d in downloads" :key="d.label" :href="d.href" variant="outlined"
                  color="primary" class="justify-start" block
                >
                  <VIcon :icon="d.icon" start />
                  {{ d.label }}
                </VBtn>
              </div>
            </VCardText>
          </VCard>
        </VCol>
      </VRow>
    </VContainer>
  </div>
</template>
