<template>
  <nav v-if="isAuthenticated">
    <h1>KobraStocks</h1>
    <div class="hamburger" @click="toggleMenu">☰</div>
    <ul :class="{ show: menuVisible }">
      <li><router-link to="/homepage">Home</router-link></li>
      <li><router-link to="/about">About</router-link></li>
      <li><router-link to="/services">Services</router-link></li>
      <li><router-link to="/contact">Contact</router-link></li>
      <li >
        <router-link to="/account">Account</router-link>
        <button @click="logout">Logout</button>
      </li>
    </ul>
  </nav>
  <nav v-else>
    <h1>KobraStocks</h1>
    <div class="hamburger" @click="toggleMenu">☰</div>
    <ul :class="{ show: menuVisible }">
      <li><router-link to="/home">Home</router-link></li>
      <li><router-link to="/about">About</router-link></li>
      <li><router-link to="/services">Services</router-link></li>
      <li><router-link to="/contact">Contact</router-link></li>
      <li><router-link to="/">Login</router-link></li>
      <li><router-link to="/signup">Sign Up</router-link></li>
    </ul>
  </nav>
</template>

<script>
import axios from 'axios';

export default {
  name: 'AppNavbar',
  computed: {
    isAuthenticated() {
      return !!localStorage.getItem('token');
    },
  },
  methods: {
    logout() {
      localStorage.removeItem('token');
      delete axios.defaults.headers.common['Authorization'];
      this.$router.push({ name: 'Login' });
    },
  },
};
</script>