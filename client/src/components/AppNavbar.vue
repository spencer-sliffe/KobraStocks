<template>
  <nav v-if="authState.isAuthenticated">
    <h1>KobraStocks</h1>
    <div class="hamburger" @click="toggleMenu">☰</div>
    <ul :class="{ show: menuVisible }">
      <li><router-link to="/homepage">Home</router-link></li>
      <li><router-link to="/about">About</router-link></li>
      <li><router-link to="/services">Services</router-link></li>
      <li><router-link to="/contact">Contact</router-link></li>
      <li><router-link to="/account">Account</router-link></li>
      <li><button @click="logout">Logout</button></li>

      <li v-if="authState.isAuthenticated">
      </li>
      <li v-else>

      </li>
    </ul>
  </nav>
  <nav v-else>
    <h1>KobraStocks</h1>
    <div class="hamburger" @click="toggleMenu">☰</div>
    <ul :class="{ show: menuVisible }">
      <li ><router-link to="/signup">Sign Up</router-link></li>
      <li ><router-link to="/">Login</router-link></li>
    </ul>
  </nav>
</template>

<script>
import axios from 'axios';
import { authState } from '@/auth';

export default {
  name: 'AppNavbar',
  setup() {
    return { authState };
  },
  methods: {
    logout() {
      localStorage.removeItem('token');
      delete axios.defaults.headers.common['Authorization'];
      authState.isAuthenticated = false; // Update the reactive state
      this.$router.push({ name: 'Login' });
    },
    toggleMenu() {
      // Implement your menu toggle logic here
    },
  },
};
</script>
