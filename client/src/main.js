import { createApp } from 'vue';
import App from './App.vue';
import router from './router';
import './assets/css/style.css';
import axios from 'axios';

axios.defaults.baseURL = 'http://127.0.0.1:5000/';

createApp(App)
  .use(router)
  .mount('#app');
