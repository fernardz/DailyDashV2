import Vue from 'vue';
import VueRouter from 'vue-router';
import Water from '../views/Water.vue';
import Task from '../views/Task.vue';
import Vitamin from '../views/Vitamin.vue';
import Activity from '../views/Activity.vue';
import Dashboard from '../views/Dashboard.vue';

Vue.use(VueRouter);

const routes = [
  {
    path: '/water',
    name: 'Water',
    component: Water,
  },
  {
    path: '/vitamin',
    name: 'Vitamin',
    component: Vitamin,
  },
  {
    path: '/task',
    name: 'Task',
    component: Task,
  },
  {
    path: '/activity',
    name: 'Activity',
    component: Activity,
  },
  {
    path: '/dashboard',
    name: 'Dashboard',
    component: Dashboard,
  },
];

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes,
});

export default router;
