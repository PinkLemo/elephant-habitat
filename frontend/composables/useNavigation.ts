import type { HorizontalNavItems } from '@layouts/types'
import index from '@/navigation/horizontal/index'

export const useNavigation = () => {
  const navItems: HorizontalNavItems = [
    ...index,
  ]

  return { navItems }
}
