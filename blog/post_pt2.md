# Smart Life Dashboard Pt. 2: Frontend
In my previous post I went over how to create the an API to handle all my daily to do's and help me keep a daily log.  
In this post I'll go over how I generated the front end of the system, both a bulk data entry system and a nice dashboard to go on a touch screen Raspberry Pi 3.

## Setup
To handle the frontend I chose to go with Vue to keep it simple. This [excellent tutorial](https://testdriven.io/blog/developing-a-single-page-app-with-flask-and-vuejs/) explains most of what I needed to do.

The most important parts are insalling vue and its cli:
```
$ npm install -g @vue/cli@4.5.11
```

Now we can create a skeleton of a vue app with the following command:
```
$ vue create client
```

We select the following features:
* Vue 2.x
* ESLint + Airbnb config
* Lint on save
* In package.json

This will create project for us. We will create the folder structure as follows:

```
client
    -src
        -assets
        -components
            -mixins
        -router
        -views
        App.vue
        main.js
```
Additionally we will be using `bootstrap` and `axios` for style and api calls. To install we just need to do
```
$ npm install axios@0.21.1 --save
$ npm install bootstrap@4.5.0 --save
```
We can check that everything is working so far by doing
```
cd client
npm run serve
```
The sample Vue page will then be available at localhost:8080

## Creating the Router
Now that we have a basic setup we can start working on our website. Setting up the router is pretty straight forward.

First we modify our main.js file as follows
```js
import BootstrapVue from 'bootstrap-vue';
import Vue from 'vue';
import App from './App.vue';
import router from './router';
import 'bootstrap/dist/css/bootstrap.css';

Vue.use(BootstrapVue);

Vue.config.productionTip = false;

new Vue({
  router,
  render: (h) => h(App),
}).$mount('#app');
```
This just tells our app to use Boostrap and tells it where the css is. Imports the App we created and imports the router.

App.vue will just contain our header to be used for navigation and define our fonts to be used.
```html
<template>
  <div id="app">
    <div id="nav">
      <router-link to="/water">Water</router-link> |
    </div>
    <router-view/>
  </div>
</template>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  color: #2c3e50;
  margin-top: 60px;
}

#nav {
  padding: 30px;
}

#nav a {
  font-weight: bold;
  color: #2c3e50;
}

#nav a.router-link-exact-active {
  color: #42b983;
}
</style>
```
We define a router link to each of out different components that we defined for the API in this case the water component.
Now we can handle each of our components and assign a data entry page for each of them by modifying index.js.
```js
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
```
For each of our routers we define its name and the component to import. This will handle all the navigation for us.

