import Vue from "vue";
import VueRouter from "vue-router";
import About from "./views/About.vue";
import Contact from "./views/Contact.vue";
import Services from "./views/Services.vue";
import Results from "./views/Results.vue";

Vue.use(VueRouter);

const routes = [
  { path: "/", component: Home },
  { path: "/about", component: About },
  { path: "/contact", component: Contact },
  { path: "/services", component: Services },
  { path: "/results", component: Results },
];

const router = new VueRouter({
  mode: "history",
  routes,
});

export default router;
