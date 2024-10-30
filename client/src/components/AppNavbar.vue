<template>
  <nav>
    <router-link to="/" class="logo">
      <img src="@/assets/logo.png" alt="KobraStocks Logo" />
    </router-link>
    <div class="hamburger" @click="toggleMenu">☰</div>
    <ul :class="{ show: menuVisible }">
      <template v-if="authState.isAuthenticated">
        <li><router-link to="/homepage">Home</router-link></li>
        <li><router-link to="/about">About</router-link></li>
        <li><router-link to="/services">Services</router-link></li>
        <li><router-link to="/contact">Contact</router-link></li>
        <li><router-link to="/account">Account</router-link></li>
        <li><a @click.prevent="logout">Logout</a></li>
      </template>
      <template v-else>
        <li><router-link to="/signup">Sign Up</router-link></li>
        <li><router-link to="/">Login</router-link></li>
      </template>
    </ul>
  </nav>
</template>

<script>
import axios from 'axios';
import { authState } from '@/auth';

export default {
  name: 'AppNavbar',
  data() {
    return {
      menuVisible: false,
      authState,
    };
  },
  methods: {
    logout() {
      localStorage.removeItem('token');
      delete axios.defaults.headers.common['Authorization'];
      this.authState.isAuthenticated = false; 
      this.$router.push({ name: 'Login' });
    },
    toggleMenu() {
      this.menuVisible = !this.menuVisible;
    },
  },
};
</script>
