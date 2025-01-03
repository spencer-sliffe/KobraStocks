// Prologue
// File Name: auth.js
// Path: client/src/auth.js
//
// Description:
// Defines a reactive authentication state, setting `isAuthenticated` based on the presence of a token in localStorage.


import { createApp } from 'vue';
import App from './App.vue';
import router from './router';
import './assets/css/style.css';
import axios from 'axios';

axios.defaults.baseURL = 'http://127.0.0.1:5000';

const token = localStorage.getItem('token');
if (token) {
  axios.defaults.headers.common['Authorization'] = `Bearer ${token}`;
}

createApp(App)
  .use(router)
  .mount('#app');