import { createRouter, createWebHistory } from 'vue-router'
// import HomeView from '../views/HomeView.vue'


const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/certificates',
      name: 'certificateslist',
      component: () => import('../views/CertificatesList.vue'),
    },
    {
      path: '/hosts',
      alias: '/',
      name: 'hostslist',
      component: () => import('../views/HostsList.vue'),
    },
    {
      path: '/host/:host/:port',
      name: 'hostview',
      component: () => import('../views/HostView.vue')
    },
    {
      path: '/certificate/:cert_serial',
      name: 'certificateview',
      component: () => import('../views/CertificateView.vue'),
    },
    {
      path: '/about',
      name: 'about',
      // route level code-splitting
      // this generates a separate chunk (About.[hash].js) for this route
      // which is lazy-loaded when the route is visited.
      component: () => import('../views/AboutView.vue'),
    },
    {
      path: '/ping',
      name: 'ping',
      component: () => import('../views/Ping.vue'),
    },
    {
      path: '/datatable',
      name: 'datatable',
      component: () => import('../components/datatable.vue'),
    }
  ],
})

export default router
