<script setup lang="ts">
import { ref } from 'vue'
import PublicNavbar from '@/layouts/components/PublicNavbar.vue'

definePageMeta({
  path: '/',
  layout: 'blank',
  public: true,
})

useHead({ title: 'Elephant Habitat — MSc Dissertation' })

// ─── Stat data (from the dissertation results_summary.json) ──────────────────
const statData = ref([
  { title: 'DBSCAN Clusters', value: '12', icon: 'ri-focus-3-line', color: 'primary' },
  { title: 'Spatial CV AUC', value: '0.885', icon: 'ri-line-chart-line', color: 'success' },
  { title: 'Occurrence Records', value: '3,067', icon: 'ri-map-pin-line', color: 'warning' },
  { title: 'Countries Covered', value: '4', icon: 'ri-earth-line', color: 'info' },
])
</script>

<template>
  <div class="landing-page-wrapper">
    <PublicNavbar />

    <!-- ═══════════════════════════════════════════════════════════ HERO ═══ -->
    <section id="home" class="hero-section" :style="{ 'background-color': 'rgb(var(--v-theme-surface))' }">
      <div class="landing-hero">
        <VContainer>
          <div class="text-center pt-10 pb-16">
            <VChip color="primary" variant="tonal" size="small" class="mb-4 text-uppercase font-weight-bold" label>
              MSc Data Science Dissertation
            </VChip>

            <div class="mb-4 landing-page-title">
              <div>Predicting Elephant Habitat</div>
              Across the KAZA Landscape
            </div>

            <p class="text-body-1 font-weight-medium text-high-emphasis pb-8 mx-auto" style="max-inline-size: 560px;">
              Machine learning and spatial data science applied to 3,067 GBIF occurrence records
              across Zimbabwe, Zambia, Mozambique, and Botswana.
            </p>

            <div class="d-flex gap-4 justify-center flex-wrap">
              <VBtn size="large" color="primary" :to="{ name: 'dashboard' }">
                Explore the Dashboard
                <VIcon end icon="ri-arrow-right-line" class="flip-in-rtl" />
              </VBtn>
              <VBtn size="large" variant="outlined" color="primary" :to="{ name: 'methodology' }">
                Read the Methodology
              </VBtn>
            </div>
          </div>
        </VContainer>
      </div>
    </section>

    <!-- ═══════════════════════════════════════════════════════════ STATS ═══ -->
    <div :style="{ 'background-color': 'rgb(var(--v-theme-surface))' }">
      <VContainer>
        <div class="py-14">
          <VRow>
            <VCol v-for="(stat, index) in statData" :key="index" cols="12" sm="6" md="3">
              <VCard flat border>
                <VCardText class="text-center">
                  <VAvatar size="56" :color="stat.color" variant="tonal" class="mb-4" rounded>
                    <VIcon :icon="stat.icon" size="28" />
                  </VAvatar>
                  <div class="product-stat-text">{{ stat.value }}</div>
                  <div class="text-body-2 font-weight-medium text-medium-emphasis mt-1">{{ stat.title }}</div>
                </VCardText>
              </VCard>
            </VCol>
          </VRow>
        </div>
      </VContainer>
    </div>
  </div>
</template>

<style lang="scss" scoped>
.hero-section {
  display: block;
  padding-block-end: 4rem;
}

.landing-hero {
  padding-block-start: 5.5rem;
}

.landing-page-title {
  color: rgb(var(--v-theme-primary));
  font-size: 2.375rem;
  font-weight: 800;
  line-height: 2.75rem;
}

.product-stat-text {
  color: rgba(var(--v-theme-on-surface), var(--v-high-emphasis-opacity));
  font-size: 2rem;
  font-weight: 700;
  line-height: 2.5rem;
}

@media (max-width: 600px) {
  .hero-section {
    padding-block-end: 2.5rem;
  }

  .landing-page-title {
    font-size: 1.75rem;
    line-height: 2.25rem;
  }
}
</style>
