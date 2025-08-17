import { createRouter, createWebHistory, type RouteRecordRaw } from "vue-router";
import Home from "../views/Home.vue";
import About from "../views/About.vue";
import authRoutes from './auth';
import Layout from "../views/Layout.vue";

const routes: RouteRecordRaw[] = [
  ...authRoutes,
  {
    path: "/",
    name: "Layout",
    component: Layout,
    children: [
      {
        path: "",
        name: "Home",
        component: Home,
      },
      {
        path: "about",
        name: "About",
        component: About,
      },
    ]
  },

];

const router = createRouter({
  base: "/inspector/",
  history: createWebHistory(),
  routes,
});

export default router;
