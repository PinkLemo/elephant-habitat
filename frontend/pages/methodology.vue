<script setup lang="ts">
import { ref } from 'vue'
import PublicNavbar from '@/layouts/components/PublicNavbar.vue'
import Footer from "@/layouts/components/Footer.vue";

definePageMeta({
  path: '/methodology',
  layout: 'blank',
  public: true,
})

useHead({ title: 'Methodology — Elephant Habitat' })

// ─── Key Stats ──────────────────────────────────────────────────────────────
const stats = ref([
  { label: 'Occurrence Records', value: '3,067', icon: 'ri-database-2-line' },
  { label: 'DBSCAN Clusters', value: '12', icon: 'ri-focus-3-line' },
  { label: 'Spatial CV AUC', value: '0.885', icon: 'ri-line-chart-line' },
  { label: 'CWBI Imputation', value: '36.0%', icon: 'ri-percent-line' },
])

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

// ─── Study area details ────────────────────────────────────────────────────
const studyArea = ref({
  countries: ['Zimbabwe', 'Zambia', 'Mozambique', 'Botswana'],
  latRange: '8°S to 26°S',
  lonRange: '20°E to 36°E',
  keyFeature: 'KAZA Transfrontier Conservation Area',
})

// ─── Data sources ──────────────────────────────────────────────────────────
const dataSources = ref([
  {
    title: 'Elephant Occurrence Data',
    source: 'GBIF (Global Biodiversity Information Facility)',
    details: '3,067 georeferenced records, 1968–2026, human observations only',
    icon: 'ri-map-pin-2-line',
  },
  {
    title: 'Elevation Data',
    source: 'Open-Elevation API (SRTM 30m DEM)',
    details: 'Retrieved via API, 3.3% median-imputed',
    icon: 'ri-earth-line',
  },
  {
    title: 'Distance to Water',
    source: 'Haversine formula calculation',
    details: 'Seven major water features: Okavango Delta, Zambezi River, Lake Kariba, and others',
    icon: 'ri-drop-line',
  },
  {
    title: 'Vegetation Productivity (CWBI)',
    source: 'Open-Meteo API (precipitation/evapotranspiration ratio)',
    details: '36.0% median-imputed due to API timeouts',
    icon: 'ri-leaf-line',
  },
])

// ─── Environmental predictors ──────────────────────────────────────────────
const predictors = ref([
  {
    name: 'CWBI (Climatic Water Balance Index)',
    importance: '48.6%',
    description: 'Ratio of annual precipitation to potential evapotranspiration — measures moisture-driven vegetation productivity',
  },
  {
    name: 'Distance to Water',
    importance: '32.0%',
    description: 'Great-circle distance to nearest permanent water body — critical for daily drinking requirements',
  },
  {
    name: 'Elevation',
    importance: '18.9%',
    description: 'Elevation above sea level — reflects preference for lower-lying river valleys and floodplains',
  },
  {
    name: 'Season',
    importance: '0.4%',
    description: 'Binary wet/dry season encoding — negligible at regional scale',
  },
])

// ─── Limitations (Chapter 5.3) ──────────────────────────────────────────────
const limitations = ref([
  {
    title: 'Spatial Sampling Bias',
    detail: 'GBIF records carry systematic bias toward areas with high observer density — roads, tourist lodges, and urban centres — underrepresenting remote regions.',
    icon: 'ri-map-2-line',
  },
  {
    title: 'CWBI Data Quality',
    detail: '36.0% of CWBI values were median-imputed due to Open-Meteo API retrieval failures, compressing variance of the most important predictor.',
    icon: 'ri-cloud-off-line',
  },
  {
    title: 'Pseudo-Absence Uncertainty',
    detail: 'Pseudo-absence points may fall within genuinely suitable, unsampled habitat, introducing uncertainty in the negative training signal.',
    icon: 'ri-question-mark-line',
  },
  {
    title: 'Limited Feature Set',
    detail: 'Absent predictors include human population density, land cover type, soil type, and protected area status.',
    icon: 'ri-list-check-3',
  },
  {
    title: 'Static Modelling',
    detail: 'The model is a static snapshot — it does not account for climate change, land-use change, or human population growth over time.',
    icon: 'ri-time-line',
  },
])

// ─── Downloads ───────────────────────────────────────────────────────────────
const downloads = ref([
  { label: 'Full Dissertation (PDF)', icon: 'ri-file-pdf-2-line', href: '#' },
  { label: 'Jupyter Notebook (.ipynb)', icon: 'ri-code-s-slash-line', href: '#' },
  { label: 'Final Dataset (.csv)', icon: 'ri-file-excel-2-line', href: '#' },
  { label: 'Results Summary (.json)', icon: 'ri-file-code-line', href: '#' },
])
</script>

<template>
  <div class="methodology-page-wrapper">
    <PublicNavbar class="mb-12" />

    <VContainer class="py-10">
      <!-- ── Header ────────────────────────────────────────────────────── -->
      <div class="mb-8">
        <VChip color="primary" variant="tonal" size="small" class="mb-3 text-uppercase font-weight-bold" label>
          Chapter 3 &amp; 5
        </VChip>
        <h1 class="text-h4 font-weight-bold mb-2">Methodology &amp; Research Design</h1>
        <p class="text-body-1 text-medium-emphasis" style="max-inline-size: 680px;">
          A quantitative, secondary-data design following the CRISP-DM framework, refined twice in
          response to supervisor feedback on spatial rigour. All analyses conducted using open-access
          data and freely available computational tools.
        </p>
      </div>

      <!-- ── Key Stats ──────────────────────────────────────────────────── -->
      <VRow class="mb-10">
        <VCol v-for="stat in stats" :key="stat.label" cols="6" md="3">
          <VCard flat border>
            <VCardText class="text-center py-3">
              <VIcon :icon="stat.icon" size="24" color="primary" class="mb-1" />
              <div class="text-h4 font-weight-bold text-primary">{{ stat.value }}</div>
              <div class="text-caption text-medium-emphasis">{{ stat.label }}</div>
            </VCardText>
          </VCard>
        </VCol>
      </VRow>

      <!-- ── Study Area ────────────────────────────────────────────────── -->
      <VCard flat border class="mb-8">
        <VCardText>
          <div class="d-flex align-center gap-x-2 mb-4">
            <VIcon icon="ri-earth-line" color="primary" size="24" />
            <div class="text-overline text-medium-emphasis mb-0">Study Area</div>
          </div>

          <p class="text-body-1 mb-3">
            The study area encompasses <strong>{{ studyArea.countries.join(', ') }}</strong>,
            spanning approximately latitudes <strong>{{ studyArea.latRange }}</strong> and
            longitudes <strong>{{ studyArea.lonRange }}</strong>. This region was deliberately
            chosen to capture the <strong>{{ studyArea.keyFeature }}</strong> — the world's
            largest transboundary conservation area and the single most critical elephant
            habitat complex on the continent, home to an estimated 220,000 elephants.
          </p>
          <p class="text-body-2 text-medium-emphasis">
            Botswana alone supports over 130,000 individuals, representing approximately
            one-third of the global African elephant population.
          </p>
        </VCardText>
      </VCard>

      <!-- ── Data Sources ───────────────────────────────────────────────── -->
      <VCard flat border class="mb-8">
        <VCardText>
          <div class="d-flex align-center gap-x-2 mb-4">
            <VIcon icon="ri-database-2-line" color="primary" size="24" />
            <div class="text-overline text-medium-emphasis mb-0">Data Sources &amp; Acquisition</div>
          </div>

          <VRow>
            <VCol v-for="source in dataSources" :key="source.title" cols="12" md="6">
              <div class="d-flex gap-x-3 pa-3 rounded" style="background: rgba(var(--v-theme-primary), 0.04);">
                <VIcon :icon="source.icon" size="24" color="primary" class="flex-shrink-0" />
                <div>
                  <div class="text-body-2 font-weight-bold">{{ source.title }}</div>
                  <div class="text-caption text-medium-emphasis">{{ source.source }}</div>
                  <div class="text-caption text-medium-emphasis">{{ source.details }}</div>
                </div>
              </div>
            </VCol>
          </VRow>
        </VCardText>
      </VCard>

      <!-- ── Analytical Pipeline ────────────────────────────────────────── -->
      <VCard flat border class="mb-8">
        <VCardText>
          <div class="d-flex align-center gap-x-2 mb-4">
            <VIcon icon="ri-flow-chart" color="primary" size="24" />
            <div class="text-overline text-medium-emphasis mb-0">Analytical Pipeline</div>
          </div>

          <p class="text-body-1 mb-3">
            The analysis follows a two-stage analytical pipeline designed to address two
            identified gaps in the literature: the absence of combined clustering and
            Random Forest pipelines applied to GBIF data at the KAZA regional scale, and
            the widespread reliance on conventional random splitting that overestimates
            performance due to spatial autocorrelation.
          </p>

          <VRow>
            <VCol cols="12" md="6">
              <VCard flat color="primary" variant="tonal">
                <VCardText>
                  <div class="d-flex align-center gap-x-2">
                    <VIcon icon="ri-focus-3-line" size="20" color="primary" />
                    <span class="text-body-2 font-weight-bold">Stage 1: Spatial Clustering</span>
                  </div>
                  <p class="text-body-2 text-medium-emphasis mt-2 mb-0">
                    DBSCAN clustering identifies geographic hotspots with ε = 0.3 and MinPts = 5.
                    12 clusters identified, 82.7% of records in the KAZA core cluster.
                  </p>
                </VCardText>
              </VCard>
            </VCol>
            <VCol cols="12" md="6">
              <VCard flat color="info" variant="tonal">
                <VCardText>
                  <div class="d-flex align-center gap-x-2">
                    <VIcon icon="ri-tree-line" size="20" color="info" />
                    <span class="text-body-2 font-weight-bold">Stage 2: Habitat Suitability</span>
                  </div>
                  <p class="text-body-2 text-medium-emphasis mt-2 mb-0">
                    Random Forest classifier with spatial block cross-validation (5 latitudinal folds).
                    Mean AUC of 0.8850 using environmental predictors only.
                  </p>
                </VCardText>
              </VCard>
            </VCol>
          </VRow>
        </VCardText>
      </VCard>

      <!-- ── Model Evaluation ───────────────────────────────────────────── -->
      <VCard flat border class="mb-8">
        <VCardText>
          <div class="d-flex align-center gap-x-2 mb-4">
            <VIcon icon="ri-scales-3-line" color="primary" size="24" />
            <div class="text-overline text-medium-emphasis mb-0">Spatial Block Cross-Validation</div>
          </div>

          <p class="text-body-1 mb-3">
            Model performance was evaluated using the Area Under the Receiver Operating
            Characteristic Curve (AUC-ROC), reported separately for each of five spatial
            blocks. This approach divides the study area into five latitudinal geographic
            blocks, holding out each block as the test set while training on the remaining
            four — forcing the model to generalise across geographic space.
          </p>

          <VRow>
            <VCol cols="12" md="6">
              <VCard flat border color="error" variant="tonal">
                <VCardText class="text-center">
                  <div class="text-overline text-medium-emphasis">Random Split (inflated)</div>
                  <div class="text-h3 font-weight-bold text-error">0.9984</div>
                  <p class="text-caption text-medium-emphasis mt-1 mb-0">
                    Overestimated due to spatial leakage between nearby train/test points
                  </p>
                </VCardText>
              </VCard>
            </VCol>
            <VCol cols="12" md="6">
              <VCard flat border color="primary" variant="tonal">
                <VCardText class="text-center">
                  <div class="text-overline text-medium-emphasis">Spatial Block CV (reported)</div>
                  <div class="text-h3 font-weight-bold text-primary">0.8850</div>
                  <p class="text-caption text-medium-emphasis mt-1 mb-0">
                    Std. dev. 0.0772 — honest, generalisable estimate of model skill
                  </p>
                </VCardText>
              </VCard>
            </VCol>
          </VRow>
        </VCardText>
      </VCard>

      <!-- ── Environmental Predictors ───────────────────────────────────── -->
      <VCard flat border class="mb-8">
        <VCardText>
          <div class="d-flex align-center gap-x-2 mb-4">
            <VIcon icon="ri-bar-chart-2-line" color="primary" size="24" />
            <div class="text-overline text-medium-emphasis mb-0">Environmental Predictors</div>
          </div>

          <p class="text-body-2 text-medium-emphasis mb-4">
            Variable importance from the Random Forest model, showing the relative contribution
            of each predictor to habitat suitability predictions.
          </p>

          <div class="d-flex flex-column gap-y-3">
            <div v-for="p in predictors" :key="p.name">
              <div class="d-flex justify-space-between mb-1">
                <span class="text-body-2 font-weight-medium">{{ p.name }}</span>
                <span class="text-body-2 font-weight-bold text-primary">{{ p.importance }}</span>
              </div>
              <VProgressLinear
                :model-value="parseFloat(p.importance) * 100 / 48.6"
                :color="parseFloat(p.importance) > 30 ? 'primary' : 'grey'"
                height="6"
                rounded
                bg-color="rgba(var(--v-theme-on-surface), 0.06)"
              />
              <p class="text-caption text-medium-emphasis mt-1">{{ p.description }}</p>
            </div>
          </div>

          <VDivider class="my-4" />
          <p class="text-caption text-medium-emphasis">
            <strong>Combined importance:</strong> CWBI and distance to water together account for
            <strong>80.6%</strong> of the model's predictive power.
          </p>
        </VCardText>
      </VCard>

      <!-- ── Refinement Timeline ────────────────────────────────────────── -->
      <VCard flat border class="mb-8">
        <VCardText>
          <div class="d-flex align-center gap-x-2 mb-4">
            <VIcon icon="ri-git-branch-line" color="info" size="24" />
            <div class="text-overline text-medium-emphasis mb-0">Methodological Refinements</div>
          </div>

          <p class="text-body-2 text-medium-emphasis mb-4">
            Four key refinements were made during the research process in response to supervisor
            feedback, each improving the methodological rigour and ecological validity of the analysis.
          </p>

          <VTimeline align="start" side="end" density="comfortable" line-inset="8">
            <VTimelineItem v-for="r in refinements" :key="r.title" dot-color="info" size="small">
              <template #icon>
                <VIcon :icon="r.icon" size="16" color="white" />
              </template>
              <div class="mb-4">
                <VChip color="info" variant="tonal" size="small" class="mb-2 font-weight-bold" label>
                  {{ r.title }}
                </VChip>
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

      <!-- ── Limitations ────────────────────────────────────────────────── -->
      <VRow>
        <VCol cols="12" md="7">
          <VCard flat border color="warning" variant="tonal" class="h-100">
            <VCardText>
              <div class="d-flex align-center gap-x-2 mb-4">
                <VIcon icon="ri-alert-line" color="warning" size="24" />
                <div class="text-overline text-medium-emphasis mb-0">Limitations (Chapter 5.3)</div>
              </div>

              <div class="d-flex flex-column gap-y-4">
                <div v-for="l in limitations" :key="l.title" class="d-flex gap-x-3">
                  <VIcon :icon="l.icon" size="18" color="warning" class="mt-1 flex-shrink-0" />
                  <div>
                    <div class="text-body-2 font-weight-medium">{{ l.title }}</div>
                    <div class="text-body-2 text-medium-emphasis">{{ l.detail }}</div>
                  </div>
                </div>
              </div>
            </VCardText>
          </VCard>
        </VCol>

        <!-- ── Conservation Implications ────────────────────────────────── -->
        <VCol cols="12" md="5">
          <VCard flat border color="primary" variant="tonal" class="h-100">
            <VCardText>
              <div class="d-flex align-center gap-x-2 mb-4">
                <VIcon icon="ri-earth-fill" color="primary" size="24" />
                <div class="text-overline text-medium-emphasis mb-0">Conservation Implications</div>
              </div>

              <p class="text-body-2 mb-3">
                The identification of KAZA as the dominant elephant habitat cluster reinforces
                the importance of maintaining transboundary governance mechanisms across four
                national jurisdictions.
              </p>
              <p class="text-body-2 mb-3">
                The habitat suitability map provides a data-driven framework for prioritising
                protected area management and identifying potential human-elephant conflict
                hotspots requiring mitigation interventions.
              </p>
              <p class="text-body-2">
                <strong>Key insight:</strong> The finding that CWBI is the dominant predictor
                (48.6% importance) has implications for climate change adaptation planning, as
                projected warming and drying trends may cause high-suitability zones to contract
                or shift northward.
              </p>
            </VCardText>
          </VCard>
        </VCol>
      </VRow>

      <!-- ── Downloads ──────────────────────────────────────────────────── -->
      <VCard flat border class="mt-8">
        <VCardText>
          <div class="d-flex align-center gap-x-2 mb-4">
            <VIcon icon="ri-download-2-line" color="primary" size="24" />
            <div class="text-overline text-medium-emphasis mb-0">Downloads &amp; Further Resources</div>
          </div>

          <div class="d-flex flex-wrap gap-3">
            <VBtn
              v-for="d in downloads"
              :key="d.label"
              :href="d.href"
              variant="tonal"
              color="primary"
              class="flex-grow-1 flex-md-grow-0"
            >
              <VIcon :icon="d.icon" start />
              {{ d.label }}
            </VBtn>
          </div>
        </VCardText>
      </VCard>
    </VContainer>
  </div>
  <!-- ═══════════════════════════════════════════════════════════ FOOTER ═══ -->
  <section class="ma-6">
    <Footer />
  </section>
</template>

<style lang="scss" scoped>
.methodology-page-wrapper {
  background: rgb(var(--v-theme-surface));
  min-height: 100vh;
}

:deep(.v-card) {
  border-radius: 8px;
  transition: all 0.2s ease;

  &:hover {
    border-color: rgba(var(--v-theme-primary), 0.3);
  }
}

:deep(.v-timeline-item) {
  .v-timeline-item__dot {
    background: rgb(var(--v-theme-primary));
  }
}

@media (max-width: 600px) {
  .methodology-page-wrapper {
    padding-bottom: 2rem;
  }

  :deep(.v-row) {
    margin-bottom: 1rem;
  }
}
</style>
