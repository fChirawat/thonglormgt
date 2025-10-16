import { createRouter, createWebHistory, type RouteRecordRaw } from "vue-router";
import About from "../views/About.vue";
import authRoutes from './auth';
import Layout from "../views/Layout.vue";
import Index from "../views/Index.vue";
import InspectionDay from "../views/InspectionDay.vue";
import history from "../views/history.vue";
import EquipmentInspectorList from "../views/EquipmentInspectorList.vue";
import editinspection from "../views/editinspection.vue";
import inspectionbacktest from "../views/inspectionbacktest.vue";


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
        path: "EquipmentInspectorList",
        name: "EquipmentInspectorList",
        component: EquipmentInspectorList,
      },
      {
        path: "editinspection",
        name: "editinspection",
        component: editinspection,
      },
      {
        path: "inspectionbacktest",
        name: "inspectionbacktest",
        component: inspectionbacktest,
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