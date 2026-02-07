import { createRouter, createWebHistory } from 'vue-router'
import { useFamilyStore } from '@/stores/familyStore'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: () => import('../views/TreeVisualization.vue')
    },
    {
      path: '/login',
      name: 'login',
      component: () => import('../views/AdminLogin.vue')
    },
    {
      path: '/admin',
      name: 'admin',
      component: () => import('../views/AdminDashboard.vue'),
      beforeEnter: (to, from, next) => {
        const store = useFamilyStore();
        if (store.isAdmin) {
          next();
        } else {
          next('/login');
        }
      }
    }
  ],

})

export default router
