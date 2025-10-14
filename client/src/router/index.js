import { createRouter, createWebHistory } from 'vue-router'
// import HomeView from '../views/HomeView.vue'


const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: () => import('../components/CertificatesList.vue'),
    },
    {
      path: '/host/:host/:port',
      name: 'hostview',
      component: () => import('../components/HostView.vue')
    },
    {
      path: '/certificate/:host/:port',
      name: 'certificateview',
      component: () => import('../components/CertificateView.vue'),
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
      component: () => import('../components/Ping.vue'),
    }
  ],
})

export default router
