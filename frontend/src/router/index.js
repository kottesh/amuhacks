import { createRouter, createWebHistory } from 'vue-router';
import LandingPage from '../views/LandingPage.vue';
import LoginPage from '../views/LoginPage.vue';
import RegisterPage from '../views/RegisterPage.vue';
import Dashboard from '../views/Dashboard.vue'; // Ensure this path is correct
import { useAuthStore } from '@/stores/authStore'; // Adjust path if needed

const routes = [
  // Public routes
  {
    path: '/',
    name: 'Landing', 
    component: LandingPage,
    meta: { requiresGuest: true } 
  },
  {
    path: '/login',
    name: 'Login',
    component: LoginPage,
    meta: { requiresGuest: true }
  },
  {
    path: '/register',
    name: 'Register',
    component: RegisterPage,
    meta: { requiresGuest: true }
   },
  {
    path: '/dashboard',
    name: 'Dashboard', 
    component: Dashboard,
    meta: { requiresAuth: true }
  },

  {
    path: '/:pathMatch(.*)*',
    redirect: '/'
  }
];

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes
});

router.beforeEach((to, from, next) => {
    const authStore = useAuthStore();
    const requiresAuth = to.matched.some(record => record.meta.requiresAuth);
    const requiresGuest = to.matched.some(record => record.meta.requiresGuest);

    if (requiresAuth && !authStore.isAuthenticated) {
        next({ name: 'Login', query: { redirect: to.fullPath } });
    } else if (requiresGuest && authStore.isAuthenticated) {
        next({ name: 'Dashboard' });
    } else {
        next();
    }
});


export default router;

