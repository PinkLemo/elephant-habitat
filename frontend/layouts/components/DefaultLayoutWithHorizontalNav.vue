<script lang="ts" setup>
import navItems from '@/navigation/horizontal'

import { themeConfig } from '@themeConfig'

// Components
import Footer from '@/layouts/components/Footer.vue'
import NavbarThemeSwitcher from '@/layouts/components/NavbarThemeSwitcher.vue'
import UserProfile from '@/layouts/components/UserProfile.vue'
import NavBarI18n from '@core/components/I18n.vue'
import { HorizontalNavLayout } from '@layouts'
import { VNodeRenderer } from '@layouts/components/VNodeRenderer'

// const { navItems } = useNavigation()
</script>

<template>
  <HorizontalNavLayout :nav-items="navItems">
    <!-- navbar -->
    <template #navbar>
      <NuxtLink
        to="/"
        class="app-logo"
      >
        <VNodeRenderer :nodes="themeConfig.app.logo" />

        <h1 class="app-logo-title leading-normal">
          {{ themeConfig.app.title }}
        </h1>
      </NuxtLink>

      <VSpacer />

      <NavBarI18n
        v-if="themeConfig.app.i18n.enable && themeConfig.app.i18n.langConfig?.length"
        :languages="themeConfig.app.i18n.langConfig"
      />

      <NavbarThemeSwitcher class="me-2" />
      <UserProfile />
    </template>

    <!-- Pages -->
    <slot />

    <!-- Footer -->
    <template #footer>
      <Footer />
    </template>
  </HorizontalNavLayout>
</template>
