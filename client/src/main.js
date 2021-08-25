import { BootstrapVue, BootstrapVueIcons } from 'bootstrap-vue';
import moment from 'moment';
import Vue from 'vue';
import App from './App.vue';
import router from './router';
import store from './store';
import 'bootstrap/dist/css/bootstrap.css';

Vue.use(BootstrapVue);
Vue.use(BootstrapVueIcons);

Vue.config.productionTip = false;

Vue.filter('formatDate', (value) => {
  if (value) {
    return moment(String(value)).format('MM/DD/YYYY hh:mm');
  }
  return value;
});

new Vue({
  router,
  store,
  render: (h) => h(App),
}).$mount('#app');
