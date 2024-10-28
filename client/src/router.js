import { createRouter, createWebHistory } from 'vue-router';
import Home from './views/HomePage.vue';
import About from './views/AboutPage.vue';
import Services from './views/ServicesPage.vue';
import Contact from './views/ContactPage.vue';
import Results from './views/ResultsPage.vue';

const routes = [
  { path: '/', name: 'Home', component: Home },
  { path: '/about', name: 'About', component: About },
  { path: '/services', name: 'Services', component: Services },
  { path: '/contact', name: 'Contact', component: Contact },
  { path: '/results', name: 'Results', component: Results }
];

const router = createRouter({
  history: createWebHistory(),
  routes
});

export default router;
