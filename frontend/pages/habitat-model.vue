<script setup lang="ts">
import { ref } from 'vue'
import PublicNavbar from '@/layouts/components/PublicNavbar.vue'

definePageMeta({
  path: '/habitat-model',
  layout: 'blank',
  public: true,
})

useHead({ title: 'Habitat Model — Elephant Habitat' })

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
  { name: 'CWBI (Climatic Water Balance Index)', importance: 0.4861 },
  { name: 'Distance to Water', importance: 0.3204 },
  { name: 'Elevation', importance: 0.1891 },
  { name: 'Season', importance: 0.0044 },
])
</script>

<template>
  <div class="model-page-wrapper">
    <PublicNavbar />

    <VContainer class="py-10">
      <div class="mb-8">
        <VChip color="primary" variant="tonal" size="small" class="mb-3 text-uppercase font-weight-bold" label>
          Chapter 4.3
        </VChip>
        <h1 class="text-h4 font-weight-bold mb-2">Habitat Suitability Model</h1>
        <p class="text-body-1 text-medium-emphasis" style="max-inline-size: 640px;">
          A Random Forest classifier trained on environmental predictors only, evaluated with
          five-fold spatial block cross-validation to avoid the inflation caused by spatial autocorrelation.
        </p>
      </div>

      <!-- ── AUC comparison ─────────────────────────────────────────────── -->
      <VRow class="mb-2">
        <VCol cols="12" md="6">
          <VCard flat border>
            <VCardText>
              <div class="d-flex align-center gap-x-2 mb-2">
                <VIcon icon="ri-error-warning-line" color="warning" size="20" />
                <span class="text-overline text-medium-emphasis">Random Split (inflated)</span>
              </div>
              <div class="text-h3 font-weight-bold text-medium-emphasis">0.9984</div>
              <p class="text-caption text-medium-emphasis mt-2 mb-0">
                Overestimated due to spatial leakage between nearby train/test points.
              </p>
            </VCardText>
          </VCard>
        </VCol>
        <VCol cols="12" md="6">
          <VCard flat border color="primary" variant="tonal">
            <VCardText>
              <div class="d-flex align-center gap-x-2 mb-2">
                <VIcon icon="ri-checkbox-circle-line" color="primary" size="20" />
                <span class="text-overline text-medium-emphasis">Spatial Block CV (reported)</span>
              </div>
              <div class="text-h3 font-weight-bold text-primary">0.8850</div>
              <p class="text-caption text-medium-emphasis mt-2 mb-0">
                Std. dev. 0.0772 — the honest, generalisable estimate of model skill.
              </p>
            </VCardText>
          </VCard>
        </VCol>
      </VRow>

      <VRow>
        <!-- ── Spatial block table ───────────────────────────────────────── -->
        <VCol cols="12" md="6">
          <VCard flat border class="h-100">
            <VCardText>
              <div class="text-overline text-medium-emphasis mb-4">AUC by Spatial Block</div>
              <VTable density="comfortable">
                <thead>
                  <tr>
                    <th>Block</th>
                    <th>Latitude Range</th>
                    <th class="text-end">AUC</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="b in blocks" :key="b.block">
                    <td class="text-body-2">{{ b.block }}</td>
                    <td class="text-body-2 text-medium-emphasis">{{ b.range }}</td>
                    <td class="text-body-2 text-end font-weight-medium">{{ b.auc.toFixed(4) }}</td>
                  </tr>
                </tbody>
              </VTable>
            </VCardText>
          </VCard>
        </VCol>

        <!-- ── Feature importance ────────────────────────────────────────── -->
        <VCol cols="12" md="6">
          <VCard flat border class="h-100">
            <VCardText>
              <div class="text-overline text-medium-emphasis mb-4">Feature Importance</div>
              <div class="d-flex flex-column gap-y-4">
                <div v-for="f in features" :key="f.name">
                  <div class="d-flex justify-space-between mb-1">
                    <span class="text-body-2">{{ f.name }}</span>
                    <span class="text-body-2 font-weight-medium">{{ f.importance.toFixed(4) }}</span>
                  </div>
                  <VProgressLinear
                    :model-value="f.importance * 100" color="primary" height="8"
                    rounded bg-color="rgba(var(--v-theme-on-surface), 0.06)"
                  />
                </div>
              </div>
            </VCardText>
          </VCard>
        </VCol>
      </VRow>
    </VContainer>
  </div>
</template>
