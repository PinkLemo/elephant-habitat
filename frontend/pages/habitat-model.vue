<script setup lang="ts">
import { ref } from 'vue'
import PublicNavbar from '@/layouts/components/PublicNavbar.vue'
import Footer from "@/layouts/components/Footer.vue";

definePageMeta({
  path: '/habitat-model',
  layout: 'blank',
  public: true,
})

useHead({ title: 'Habitat Model — Elephant Habitat' })

// ─── Model performance metrics ──────────────────────────────────────────────
const modelMetrics = ref([
  { label: 'Model Type', value: 'Random Forest Classifier' },
  { label: 'Number of Trees', value: '200' },
  { label: 'Max Depth', value: '12' },
  { label: 'Min Samples Split', value: '10' },
  { label: 'Training Records', value: '6,134' },
  { label: 'Test Records (per fold)', value: '~1,200' },
])

// ─── Spatial block CV results (Table 3) ─────────────────────────────────────
const blocks = ref([
  { block: 'Block 1 (Northernmost)', range: '~8°S to ~11°S', auc: 0.8976 },
  { block: 'Block 2', range: '~11°S to ~14°S', auc: 0.8840 },
  { block: 'Block 3', range: '~14°S to ~18°S', auc: 0.9704 },
  { block: 'Block 4', range: '~18°S to ~22°S', auc: 0.9302 },
  { block: 'Block 5 (Southernmost)', range: '~22°S to ~26°S', auc: 0.7425 },
])

// ─── Feature importance (Section 4.3.2) ─────────────────────────────────────
const features = ref([
  {
    name: 'CWBI (Climatic Water Balance Index)',
    importance: 0.4861,
    description: 'Ratio of annual precipitation to potential evapotranspiration — measures moisture-driven vegetation productivity',
    color: 'primary'
  },
  {
    name: 'Distance to Water',
    importance: 0.3204,
    description: 'Great-circle distance to nearest permanent water body — critical for daily drinking requirements',
    color: 'success'
  },
  {
    name: 'Elevation',
    importance: 0.1891,
    description: 'Elevation above sea level — reflects preference for lower-lying river valleys and floodplains',
    color: 'warning'
  },
  {
    name: 'Season',
    importance: 0.0044,
    description: 'Binary wet/dry season encoding — negligible impact at regional scale',
    color: 'grey'
  },
])

// ─── Block performance summary ─────────────────────────────────────────────
const blockSummary = ref({
  mean: 0.8850,
  stdDev: 0.0772,
  min: 0.7425,
  max: 0.9704,
})

// ─── Model interpretation ──────────────────────────────────────────────────
const modelInterpretation = ref([
  {
    title: 'CWBI Dominance',
    detail: 'The Climatic Water Balance Index accounts for 48.6% of predictive power, confirming that moisture-driven vegetation productivity is the primary determinant of elephant habitat suitability at regional scale.',
    icon: 'ri-leaf-line',
  },
  {
    title: 'Water Proximity',
    detail: 'Distance to water (32.0% importance) reflects elephants\' daily drinking requirements and the concentration of populations around permanent water sources, particularly during the dry season.',
    icon: 'ri-drop-line',
  },
  {
    title: 'Elevation Preference',
    detail: 'Elevation (18.9% importance) captures elephants\' preference for lower-lying river valleys, floodplains, and gentle terrain that facilitates movement and provides access to water and forage.',
    icon: 'ri-earth-line',
  },
  {
    title: 'Seasonal Insignificance',
    detail: 'Season contributes only 0.4% of predictive power at regional scale, suggesting that geographic variation in habitat quality outweighs seasonal variation within any given location.',
    icon: 'ri-sun-line',
  },
])

// ─── Conservation implications ─────────────────────────────────────────────
const conservationImplications = ref([
  'The dominance of CWBI (48.6%) highlights the vulnerability of elephant habitat to climate-driven changes in water balance, with projected warming and drying trends potentially contracting high-suitability zones.',
  'The 80.6% combined importance of CWBI and distance to water confirms that conservation planning must prioritise protecting both productive vegetation zones and the permanent water sources that sustain them.',
  'The spatial block CV variation (0.7425–0.9704) suggests that model transferability is strongest in the KAZA core and weakest in the arid Kalahari periphery — informing where predictions are most reliable.',
])
</script>

<template>
  <div class="model-page-wrapper">
    <PublicNavbar class="mb-12" />

    <VContainer class="py-10">
      <!-- ── Header ────────────────────────────────────────────────────── -->
      <div class="mb-8">
        <VChip color="primary" variant="tonal" size="small" class="mb-3 text-uppercase font-weight-bold" label>
          Chapter 4.3
        </VChip>
        <h1 class="text-h4 font-weight-bold mb-2">Habitat Suitability Model</h1>
        <p class="text-body-1 text-medium-emphasis" style="max-inline-size: 680px;">
          A Random Forest classifier trained on environmental predictors only, evaluated with
          five-fold spatial block cross-validation to avoid the inflation caused by spatial autocorrelation.
          The model achieves a mean AUC of <strong>0.8850</strong> — a credible, generalisable estimate
          of predictive skill.
        </p>
      </div>

      <!-- ── Model Configuration ───────────────────────────────────────── -->
      <VCard flat border class="mb-8" style="background: rgba(var(--v-theme-primary), 0.04);">
        <VCardText>
          <div class="d-flex align-center gap-x-2 mb-4">
            <VIcon icon="ri-settings-3-line" color="primary" size="24" />
            <div class="text-overline text-medium-emphasis mb-0">Model Configuration</div>
          </div>

          <VRow>
            <VCol v-for="metric in modelMetrics" :key="metric.label" cols="6" md="4" lg="3">
              <div class="text-caption text-medium-emphasis">{{ metric.label }}</div>
              <div class="text-body-2 font-weight-bold">{{ metric.value }}</div>
            </VCol>
          </VRow>
        </VCardText>
      </VCard>

      <!-- ── AUC comparison ─────────────────────────────────────────────── -->
      <VRow class="mb-8">
        <VCol cols="12" md="6">
          <VCard flat border color="warning" variant="tonal" class="h-100">
            <VCardText>
              <div class="d-flex align-center gap-x-2 mb-2">
                <VIcon icon="ri-alert-line" color="warning" size="20" />
                <span class="text-overline text-medium-emphasis">Random Split (inflated)</span>
              </div>
              <div class="text-h3 font-weight-bold text-warning">0.9984</div>
              <p class="text-caption text-medium-emphasis mt-2 mb-0">
                Overestimated due to spatial leakage between nearby train/test points.
                This demonstrates why spatial cross-validation is essential.
              </p>
            </VCardText>
          </VCard>
        </VCol>
        <VCol cols="12" md="6">
          <VCard flat border color="info" variant="tonal" class="h-100">
            <VCardText>
              <div class="d-flex align-center gap-x-2 mb-2">
                <VIcon icon="ri-checkbox-circle-line" color="info" size="20" />
                <span class="text-overline text-medium-emphasis">Spatial Block CV (reported)</span>
              </div>
              <div class="text-h3 font-weight-bold text-info">0.8850</div>
              <p class="text-caption text-medium-emphasis mt-2 mb-0">
                Std. dev. <strong>0.0772</strong> — the honest, generalisable estimate of model skill.
                <span class="d-block mt-1">Difference: <strong>0.1134</strong> AUC units of inflation avoided.</span>
              </p>
            </VCardText>
          </VCard>
        </VCol>
      </VRow>

      <!-- ── Spatial Block Table & Feature Importance ──────────────────── -->
      <VRow>
        <!-- ── Spatial block table ───────────────────────────────────────── -->
        <VCol cols="12" md="6">
          <VCard flat border class="h-100">
            <VCardText>
              <div class="d-flex align-center gap-x-2 mb-4">
                <VIcon icon="ri-table-line" color="primary" size="20" />
                <div class="text-overline text-medium-emphasis mb-0">AUC by Spatial Block</div>
              </div>

              <VTable density="comfortable">
                <thead>
                <tr>
                  <th>Block</th>
                  <th>Latitude Range</th>
                  <th class="text-end">AUC</th>
                  <th class="text-end">Performance</th>
                </tr>
                </thead>
                <tbody>
                <tr v-for="b in blocks" :key="b.block">
                  <td class="text-body-2">{{ b.block }}</td>
                  <td class="text-body-2 text-medium-emphasis">{{ b.range }}</td>
                  <td class="text-body-2 text-end font-weight-medium">{{ b.auc.toFixed(4) }}</td>
                  <td class="text-end">
                    <VChip
                      :color="b.auc >= 0.9 ? 'success' : b.auc >= 0.8 ? 'primary' : 'warning'"
                      size="x-small"
                      variant="tonal"
                      label
                    >
                      {{ b.auc >= 0.9 ? 'Excellent' : b.auc >= 0.8 ? 'Good' : 'Moderate' }}
                    </VChip>
                  </td>
                </tr>
                </tbody>
                <tfoot>
                <tr>
                  <td colspan="2" class="text-body-2 font-weight-bold">Mean</td>
                  <td class="text-body-2 text-end font-weight-bold text-primary">
                    {{ blockSummary.mean.toFixed(4) }}
                  </td>
                  <td></td>
                </tr>
                <tr>
                  <td colspan="2" class="text-body-2 text-medium-emphasis">Std. Deviation</td>
                  <td class="text-body-2 text-end text-medium-emphasis">
                    {{ blockSummary.stdDev.toFixed(4) }}
                  </td>
                  <td></td>
                </tr>
                </tfoot>
              </VTable>

              <VDivider class="my-4" />
              <div class="d-flex justify-space-between text-caption text-medium-emphasis">
                <span>Min AUC: <strong>{{ blockSummary.min.toFixed(4) }}</strong> (Block 5)</span>
                <span>Max AUC: <strong>{{ blockSummary.max.toFixed(4) }}</strong> (Block 3)</span>
                <span>Range: <strong>{{ (blockSummary.max - blockSummary.min).toFixed(4) }}</strong></span>
              </div>
            </VCardText>
          </VCard>
        </VCol>

        <!-- ── Feature importance ────────────────────────────────────────── -->
        <VCol cols="12" md="6">
          <VCard flat border class="h-100">
            <VCardText>
              <div class="d-flex align-center gap-x-2 mb-4">
                <VIcon icon="ri-bar-chart-2-line" color="primary" size="20" />
                <div class="text-overline text-medium-emphasis mb-0">Feature Importance</div>
              </div>

              <p class="text-caption text-medium-emphasis mb-4">
                Variable importance scores from the Random Forest model showing the relative
                contribution of each environmental predictor to habitat suitability predictions.
              </p>

              <div class="d-flex flex-column gap-y-4">
                <div v-for="f in features" :key="f.name">
                  <div class="d-flex justify-space-between mb-1">
                    <span class="text-body-2 font-weight-medium">{{ f.name }}</span>
                    <span class="text-body-2 font-weight-bold" :class="f.color === 'grey' ? 'text-medium-emphasis' : `text-${f.color}`">
                      {{ (f.importance * 100).toFixed(1) }}%
                    </span>
                  </div>
                  <VProgressLinear
                    :model-value="f.importance * 100"
                    :color="f.color === 'grey' ? 'grey' : f.color"
                    height="8"
                    rounded
                    bg-color="rgba(var(--v-theme-on-surface), 0.06)"
                  />
                  <p class="text-caption text-medium-emphasis mt-1">{{ f.description }}</p>
                </div>
              </div>

              <VDivider class="my-4" />
              <div class="text-caption text-medium-emphasis">
                <strong>Combined importance:</strong> CWBI and distance to water together account for
                <strong>80.6%</strong> of the model's predictive power.
              </div>
            </VCardText>
          </VCard>
        </VCol>
      </VRow>

      <!-- ── Model Interpretation ───────────────────────────────────────── -->
      <VRow class="mt-8">
        <VCol cols="12">
          <VCard flat border>
            <VCardText>
              <div class="d-flex align-center gap-x-2 mb-4">
                <VIcon icon="ri-lightbulb-line" color="primary" size="24" />
                <div class="text-overline text-medium-emphasis mb-0">Model Interpretation</div>
              </div>

              <p class="text-body-2 text-medium-emphasis mb-4">
                The model reveals a coherent ecological story: elephant habitat suitability in Southern Africa
                is fundamentally structured by food and water availability. The findings confirm established
                ecological theory while providing quantitative, spatially explicit predictions.
              </p>

              <VRow>
                <VCol v-for="item in modelInterpretation" :key="item.title" cols="12" md="6">
                  <div class="d-flex gap-x-3 pa-3 rounded" style="background: rgba(var(--v-theme-primary), 0.04);">
                    <VIcon :icon="item.icon" size="20" color="primary" class="flex-shrink-0" />
                    <div>
                      <div class="text-body-2 font-weight-bold">{{ item.title }}</div>
                      <div class="text-caption text-medium-emphasis">{{ item.detail }}</div>
                    </div>
                  </div>
                </VCol>
              </VRow>
            </VCardText>
          </VCard>
        </VCol>
      </VRow>

      <!-- ── Conservation Implications ───────────────────────────────────── -->
      <VRow class="mt-8">
        <VCol cols="12">
          <VCard flat border color="info" variant="tonal">
            <VCardText>
              <div class="d-flex align-center gap-x-2 mb-4">
                <VIcon icon="ri-earth-line" color="info" size="24" />
                <div class="text-overline text-medium-emphasis mb-0">Conservation Implications</div>
              </div>

              <div class="d-flex flex-column gap-y-3">
                <div v-for="(item, index) in conservationImplications" :key="index" class="d-flex gap-x-3">
                  <VIcon icon="ri-arrow-right-s-line" size="16" color="primary" class="flex-shrink-0 mt-1" />
                  <span class="text-body-2">{{ item }}</span>
                </div>
              </div>

              <VDivider class="my-4" />

              <div class="text-caption text-medium-emphasis">
                <strong>Key insight:</strong> The spatial block cross-validation results demonstrate that model
                performance varies geographically — strongest in the KAZA core (Block 3: 0.9704) and weakest
                in the arid southern periphery (Block 5: 0.7425) — providing guidance on where predictions
                are most reliable for conservation planning.
              </div>
            </VCardText>
          </VCard>
        </VCol>
      </VRow>

      <!-- ── Model Summary ───────────────────────────────────────────────── -->
      <VCard flat border class="mt-8" color="success" variant="tonal">
        <VCardText class="text-center py-4">
          <div class="d-flex align-center justify-center gap-x-2 flex-wrap">
            <VIcon icon="ri-check-line" color="success" size="24" />
            <span class="text-body-1 font-weight-medium">
              The model achieves a robust AUC of <strong>0.8850</strong> under spatial block cross-validation,
              confirming its utility for regional conservation planning.
            </span>
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
.model-page-wrapper {
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

:deep(.v-table) {
  tfoot {
    border-top: 2px solid rgba(var(--v-theme-on-surface), 0.08);

    tr {
      background: rgba(var(--v-theme-primary), 0.04);
    }
  }

  .v-table__wrapper {
    border-radius: 8px;
  }
}

@media (max-width: 600px) {
  .model-page-wrapper {
    padding-bottom: 2rem;
  }
}
</style>
