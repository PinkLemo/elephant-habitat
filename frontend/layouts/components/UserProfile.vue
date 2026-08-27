<script setup lang="ts">
import { PerfectScrollbar } from 'vue3-perfect-scrollbar'
import avatar1 from '@images/avatars/avatar-1.png'

const userProfileList = [
  { type: 'divider' },
  {
    type: 'navItem',
    icon: 'ri-global-line',
    title: 'Portfolio Website',
    href: 'https://my-portfolio-vue-steel.vercel.app/',
  },
  {
    type: 'navItem',
    icon: 'ri-github-line',
    title: 'GitHub Repository',
    href: 'https://github.com/PinkLemo/elephant-habitat',
  },
  {
    type: 'navItem',
    icon: 'ri-linkedin-box-line',
    title: 'LinkedIn',
    href: 'https://www.linkedin.com/in/daliso-miti-805b8323a/',
  },
]
</script>

<template>
  <VBadge
    dot
    bordered
    location="bottom right"
    offset-x="2"
    offset-y="2"
    color="success"
    class="user-profile-badge"
  >
    <VAvatar
      class="cursor-pointer"
      size="38"
    >
      <VImg :src="avatar1" />

      <!-- SECTION Menu -->
      <VMenu
        activator="parent"
        width="230"
        location="bottom end"
        offset="15px"
      >
        <VList>
          <VListItem class="px-4">
            <div class="d-flex gap-x-2 align-center">
              <VAvatar>
                <VImg :src="avatar1" />
              </VAvatar>

              <div>
                <div class="text-body-2 font-weight-medium text-high-emphasis">
                  Daliso Rumbi Miti
                </div>
                <div class="text-capitalize text-caption text-disabled">
                  Data Science Researcher and Full Stack Software Engineer
                </div>
              </div>
            </div>
          </VListItem>

          <PerfectScrollbar :options="{ wheelPropagation: false }">
            <template
              v-for="item in userProfileList"
              :key="item.title"
            >
              <VListItem
                v-if="item.type === 'navItem'"
                class="px-4"
                :href="item.href"
                target="_blank"
                rel="noopener noreferrer"
              >
                <template #prepend>
                  <VIcon
                    :icon="item.icon"
                    size="22"
                  />
                </template>

                <VListItemTitle>{{ item.title }}</VListItemTitle>
              </VListItem>

              <VDivider
                v-else
                class="my-1"
              />
            </template>
          </PerfectScrollbar>
        </VList>
      </VMenu>
      <!-- !SECTION -->
    </VAvatar>
  </VBadge>
</template>

<style lang="scss">
.user-profile-badge {
  &.v-badge--bordered.v-badge--dot .v-badge__badge::after {
    color: rgb(var(--v-theme-background));
  }
}
</style>
