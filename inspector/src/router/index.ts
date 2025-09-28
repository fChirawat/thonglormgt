import { createRouter, createWebHistory, type RouteRecordRaw } from "vue-router";
import About from "../views/About.vue";
import authRoutes from './auth';
import Layout from "../views/Layout.vue";
import Index from "../views/Index.vue";
import InspectionMonth from "../views/InspectionMonth.vue";
import InspectionDay from "../views/InspectionDay.vue";
import history from "../views/history.vue";
import dataHistory from "../views/dataHistory.vue";


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
      {
        path: "InspectionMonth",
        name: "InspectionMonth",
        component: InspectionMonth,
      },
      {
        path: "InspectionDay",
        name: "InspectionDay",
        component: InspectionDay,
      },
      {
        path: "history",
        name: "history",
        component: history,
      },
      {
        path: "dataHistory.",
        name: "dataHistory",
        component: dataHistory,
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