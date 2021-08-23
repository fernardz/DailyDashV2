import Vue from 'vue';
import VueRouter from 'vue-router';
import Water from '../components/Water.vue';
import Task from '../components/Task.vue';
import Strava from '../components/Strava.vue';
import Vitamin from '../components/Vitamin.vue';
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
    path: '/strava',
    name: 'Strava',
    component: Strava,
  },
  {
    path: '/task',
    name: 'Task',
    component: Task,
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
