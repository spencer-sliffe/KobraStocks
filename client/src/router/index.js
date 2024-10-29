// client/src/router/index.js

import { createRouter, createWebHistory } from 'vue-router';
import HomePage from '@/views/HomePage.vue';
import LoginPage from '@/views/LoginPage.vue';
import SignUpPage from '@/views/SignUpPage.vue';
import AboutPage from '@/views/AboutPage.vue';
import ServicesPage from '@/views/ServicesPage.vue';
import ResultsPage from '@/views/ResultsPage.vue';
import ContactPage from '@/views/ContactPage.vue';
import AccountPage from '@/views/AccountPage.vue';

const routes = [
    {
        path: '/',
        name: 'Login',
        component: LoginPage,
    },
    {
        path: '/signup',
        name: 'Signup',
        component: SignUpPage,
    },
    {
        path: '/homepage',
        name: 'Home',
        component: HomePage,
        meta: { requiresAuth: true },
    },
    {
        path: '/contact',
        name: 'Contact',
        component: ContactPage,
        meta: { requiresAuth: true },
    },
    {
        path: '/about',
        name: 'About',
        component: AboutPage,
        meta: { requiresAuth: true },
    },
    {
        path: '/services',
        name: 'Services',
        component: ServicesPage,
        meta: { requiresAuth: true },
    },
    {
        path: '/results',
        name: 'Results',
        component: ResultsPage,
        meta: { requiresAuth: true },
    },
    {
        path: '/account',
        name: 'Account',
        component: AccountPage,
        meta: { requiresAuth: true },
    },
];

const router = createRouter({
    history: createWebHistory(),
    routes,
});

// Navigation Guard
router.beforeEach((to, from, next) => {
    const isAuthenticated = !!localStorage.getItem('token');
    if (to.matched.some((record) => record.meta.requiresAuth) && !isAuthenticated) {
        next({ name: 'Login' });
    } else if ((to.name === 'Login' || to.name === 'Signup') && isAuthenticated) {
        next({ name: 'Home' });
    } else {
        next();
    }
});

export default router;