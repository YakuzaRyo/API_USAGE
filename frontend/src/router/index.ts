import { createRouter, createWebHistory } from 'vue-router'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: '/',
      redirect: '/dashboard',
    },
    {
      path: '/dashboard',
      name: 'dashboard',
      component: () => import('../views/DashboardView.vue'),
    },
    {
      path: '/providers',
      name: 'providers',
      component: () => import('../views/ProviderView.vue'),
    },
    {
      path: '/categories',
      name: 'categories',
      component: () => import('../views/CategoryManager.vue'),
    },
    {
      path: '/spotlight',
      name: 'spotlight',
      component: () => import('../views/SpotlightView.vue'),
    },
  ],
})

export default router
