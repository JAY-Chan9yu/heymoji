import Vue from 'vue'
import axios from 'axios'
import VueAxios from 'vue-axios'
import App from './App'
import store from './store.js'
import vuetify from './plugins/vuetify';
import 'vuetify/dist/vuetify.min.css'

Vue.config.productionTip = false
Vue.use(VueAxios, axios);


new Vue({
  // <-- injecting the store for global access
  store,
  vuetify,
  render: h => h(App)
}).$mount('#app')
