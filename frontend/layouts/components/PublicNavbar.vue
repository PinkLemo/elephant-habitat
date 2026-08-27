<script setup lang="ts">
import { ref } from 'vue'
import { useDisplay } from 'vuetify'
import navItems from '@/navigation/horizontal'
import NavbarThemeSwitcher from '@/layouts/components/NavbarThemeSwitcher.vue'
import { VNodeRenderer } from '@layouts/components/VNodeRenderer'
import { themeConfig } from '@themeConfig'
import UserProfile from "@/layouts/components/UserProfile.vue";

const display = useDisplay()
const route = useRoute()
const sidebar = ref(false)
</script>

<template>
  <div>
    <!-- Mobile drawer -->
    <VNavigationDrawer v-model="sidebar" data-allow-mismatch disable-resize-watcher>
      <div class="h-100" style="overflow-y: auto;">
        <div class="d-flex flex-column gap-y-4 pa-4 pt-8">
          <NuxtLink
            v-for="item in navItems" :key="item.title" :to="item.to"
            class="d-flex align-center gap-x-3 font-weight-medium"
            :class="route.name === item.to.name ? 'active-link' : 'text-high-emphasis'"
          >
            <VIcon :icon="item.icon.icon" size="20" />
            {{ item.title }}
          </NuxtLink>
        </div>
        <VIcon id="navigation-drawer-close-btn" icon="ri-close-line" size="20" @click="sidebar = !sidebar" />
      </div>
    </VNavigationDrawer>

    <!-- Desktop navbar -->
    <div class="front-page-navbar">
      <VAppBar elevation="0" class="rounded-b-xl" height="62" border="1px solid rgba(var(--v-theme-surface), 0.78)">
        <VAppBarNavIcon
          :class="display.mdAndUp.value ? 'd-none' : 'd-inline-block'" class="ms-0 me-1"
          color="high-emphasis" @click="sidebar = !sidebar"
        />

        <div class="d-flex align-center">
          <VAppBarTitle class="me-3 me-sm-6">
            <NuxtLink to="/frontend/public" class="d-flex gap-x-3 align-center text-decoration-none">
              <VNodeRenderer :nodes="themeConfig.app.logo" />
              <span class="nav-title">Elephant Habitat</span>
            </NuxtLink>
          </VAppBarTitle>

          <div :class="display.mdAndUp.value ? 'd-flex' : 'd-none'" class="text-base align-center gap-x-2">
            <NuxtLink
              v-for="item in navItems" :key="item.title" :to="item.to"
              class="nav-link font-weight-medium"
              :class="route.name === item.to.name ? 'active-link' : ''"
            >
              {{ item.title }}
            </NuxtLink>
          </div>
        </div>

        <VSpacer />

        <div class="d-flex gap-x-3 align-center">
          <NavbarThemeSwitcher class="me-0 me-sm-1" />
          <UserProfile />
        </div>
      </VAppBar>
    </div>
  </div>
</template>

<style lang="scss" scoped>
.nav-title {
  color: rgba(var(--v-theme-on-surface), var(--v-high-emphasis-opacity));
  font-size: 1.125rem;
  font-weight: 600;
  letter-spacing: 0.2px;
}

.nav-link {
  padding-inline: 0.625rem;

  &:not(:hover) {
    color: rgba(var(--v-theme-on-surface), var(--v-high-emphasis-opacity));
  }
}

.active-link {
  color: rgb(var(--v-theme-primary)) !important;
}
</style>

<style lang="scss">
.front-page-navbar {
  .v-toolbar__content {
    padding-inline: 2rem !important;
  }

  @media (max-width: 600px) {
    .v-toolbar__content {
      padding-inline: 0.75rem !important;
    }
  }
}

#navigation-drawer-close-btn {
  position: absolute;
  cursor: pointer;
  inset-block-start: 0.5rem;
  inset-inline-end: 1rem;
}
</style>
