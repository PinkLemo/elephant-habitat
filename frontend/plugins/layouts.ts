import type { PartialObjectDeep } from 'type-fest/source/partial-deep'
import { createLayouts } from '@layouts'

import { layoutConfig } from '@themeConfig'

// Styles
import '@layouts/styles/index.scss'

export default defineNuxtPlugin(nuxtApp => {
  // ℹ️ We generate layout config from our themeConfig so you don't have to write config twice
  nuxtApp.vueApp.use(createLayouts(layoutConfig as PartialObjectDeep<typeof layoutConfig, NonNullable<unknown>>))
})
