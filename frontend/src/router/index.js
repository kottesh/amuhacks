import { createRouter, createWebHistory } from 'vue-router'
import LandingPage from '../views/LandingPage.vue'
import LoginPage from '../views/LoginPage.vue'
import RegisterPage from '../views/RegisterPage.vue'
// Import your authenticated routes/layout as well
// import DashboardLayout from '../layouts/DashboardLayout.vue'
// import DashboardView from '../views/DashboardView.vue'
import { useAuthStore } from '@/stores/authStore';

const routes = [
  { path: '/', name: 'Quid', component: LandingPage },
  { path: '/login', name: 'Login', component: LoginPage, meta: { requiresGuest: true } },
  { path: '/register', name: 'Register', component: RegisterPage, meta: { requiresGuest: true } },
  // Example protected route:
  // {
  //   path: '/dashboard',
  //   component: DashboardLayout, // Or directly the view
  //   meta: { requiresAuth: true },
  //   children: [
  //     { path: '', name: 'Dashboard', component: DashboardView },
  //     // other authenticated routes
  //   ]
  // },
  // Redirect root path or add a 404 page
   { path: '/:pathMatch(.*)*', redirect: '/' }
]

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes
})

router.beforeEach((to, from, next) => {
    const authStore = useAuthStore();
    const requiresAuth = to.matched.some(record => record.meta.requiresAuth);
    const requiresGuest = to.matched.some(record => record.meta.requiresGuest);

    if (requiresAuth && !authStore.isAuthenticated) {
        // Redirect to login if trying to access protected route without auth
        next({ name: 'Login', query: { redirect: to.fullPath } });
    } else if (requiresGuest && authStore.isAuthenticated) {
        // Redirect to dashboard if trying to access login/register page while authenticated
        next('/dashboard');
    } else {
        next();
    }
});


export default router

