import { createRouter, createWebHistory, type RouteRecordRaw } from "vue-router";
import About from "../views/About.vue";
import authRoutes from './auth';
import Layout from "../views/Layout.vue";
import Index from "../views/Index.vue";

33
const routes: RouteRecordRaw[] = [
  ...authRoutes,
  {
    path: "/",
    name: "Layout",
    component: Layout,
    children: [
      {
        path: "",
        name: "Index",
        component: Index,
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