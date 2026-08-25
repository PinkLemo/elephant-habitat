<!-- eslint-disable import/extensions -->
<script setup lang="ts">
import { useBreadcrumbs } from '@/composables/useBreadcrumbs';

const { getBreadcrumbs } = useBreadcrumbs()
</script>

<template>
  <div class="d-flex justify-space-between align-center">
    <VBreadcrumbs
        class="px-0 pb-2 pt-0 flex-wrap"
        :items="getBreadcrumbs"
    >
      <template #item="{ item, index }">
        <NuxtLink
            v-if="item.to && index !== getBreadcrumbs.length - 1"
            :to="item.to"
            class="text-body-1 text-medium-emphasis breadcrumb-link"
        >
          <VIcon v-if="item.icon" :icon="item.icon.icon" size="small" class="mr-1" />
          {{ item.title }}
        </NuxtLink>
        <span
            v-else
            class="text-body-1"
            :class="index === getBreadcrumbs.length - 1 ? 'text-high-emphasis' : 'text-medium-emphasis'"
        >
          <VIcon v-if="item.icon" :icon="item.icon.icon" size="small" class="mr-1" />
          {{ item.title }}
        </span>
      </template>
      <template #divider>
        <VIcon icon="ri-arrow-right-s-line" size="small" />
      </template>
    </VBreadcrumbs>
  </div>
</template>

<style scoped>
.breadcrumb-link {
  text-decoration: none; /* Remove underline from NuxtLink */
}
.breadcrumb-link:hover {
  text-decoration: underline; /* Add underline on hover for better UX */
}
</style>
