import type { HorizontalNavItems } from '@layouts/types'

const navItems: HorizontalNavItems = [
  {
    title: 'Home',
    to: { name: 'index' },
    icon: { icon: 'ri-home-smile-2-line' },
  },
  {
    title: 'Dashboard',
    to: { name: 'dashboard' },
    icon: { icon: 'ri-map-2-line' },
  },
  {
    title: 'Explore Data',
    to: { name: 'explore-data' },
    icon: { icon: 'ri-bar-chart-2-line' },
  },
  {
    title: 'Habitat Model',
    to: { name: 'habitat-model' },
    icon: { icon: 'ri-cpu-line' },
  },
  {
    title: 'Methodology',
    to: { name: 'methodology' },
    icon: { icon: 'ri-file-list-3-line' },
  },
]

export default navItems
