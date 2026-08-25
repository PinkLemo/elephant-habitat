<script lang="ts" setup>
import { useConfigStore } from '@core/stores/config'
import { AppContentLayoutNav } from '@layouts/enums'
import { switchToVerticalNavOnLtOverlayNavBreakpoint } from '@layouts/utils'

// Get userDetails from cookies

const DefaultLayoutWithHorizontalNav = defineAsyncComponent(() => import('./components/DefaultLayoutWithHorizontalNav.vue'))
// const DefaultLayoutWithVerticalNav = defineAsyncComponent(() => import('./components/DefaultLayoutWithVerticalNav.vue')) // No longer used

const configStore = useConfigStore()

// ℹ️ This will switch to vertical nav when define breakpoint is reached when in horizontal nav layout
// Remove below composable usage if you are not using horizontal nav layout in your app
//  switchToVerticalNavOnLtOverlayNavBreakpoint(); // Remove this line

const { layoutAttrs, injectSkinClasses } = useSkins()

injectSkinClasses()

// Force horizontal nav
configStore.appContentLayoutNav = AppContentLayoutNav.Horizontal
</script>

<template>
  <Component
    v-bind="layoutAttrs"
    :is="DefaultLayoutWithHorizontalNav"  >
    <slot />
  </Component>
</template>

<style lang="scss">
// As we are using `layouts` plugin we need its styles to be imported
@use "@layouts/styles/default-layout";
</style>
