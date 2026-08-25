import { ref, computed } from 'vue';
import type { RouteLocationRaw } from 'vue-router';

export interface BreadcrumbItem {
  title: string;
  to?: RouteLocationRaw;
  icon?: { icon: string };
}

const breadcrumbItems = ref<BreadcrumbItem[]>([]);

export function useBreadcrumbs() {
  const setBreadcrumbs = (items: BreadcrumbItem[]) => {
    breadcrumbItems.value = items;
  };

  const addBreadcrumb = (item: BreadcrumbItem) => {
    breadcrumbItems.value.push(item);
  };

  const clearBreadcrumbs = () => {
    breadcrumbItems.value = [];
  };

  const getBreadcrumbs = computed(() => breadcrumbItems.value);

  return {
    setBreadcrumbs,
    addBreadcrumb,
    clearBreadcrumbs,
    getBreadcrumbs,
  };
}
