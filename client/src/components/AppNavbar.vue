<!-- AppNavbar.vue -->
<template>
  <nav>
    <router-link to="/" class="logo">
      <img src="@/assets/logo.png" alt="KobraStocks Logo" />
    </router-link>
    <div class="nav-items">
      <ul :class="{ show: menuVisible }">
        <template v-if="authState.isAuthenticated">
          <li><router-link to="/homepage">Home</router-link></li>
          <li><router-link to="/about">About</router-link></li>
          <li><router-link to="/services">Services</router-link></li>
          <li><router-link to="/contact">Contact</router-link></li>
          <li><router-link to="/portfolio">Portfolio</router-link></li>
        </template>
        <template v-else>
          <li><router-link to="/signup">Sign Up</router-link></li>
          <li><router-link to="/">Login</router-link></li>
        </template>
      </ul>
      <!-- Account Button -->
      <div v-if="authState.isAuthenticated" class="account-icon">
        <button @click="toggleAccountDrawer">
          <!-- Display the user's first name instead of "Account" -->
          {{ user ? user.first_name : 'Account' }}
        </button>
      </div>
      <div class="hamburger" @click="toggleMenu">☰</div>
    </div>
    <!-- Account Drawer Component -->
    <AccountDrawer :isVisible="isAccountDrawerVisible" @close="toggleAccountDrawer" />
  </nav>
</template>

<script>
import axios from 'axios';
import { authState } from '@/auth';
import AccountDrawer from '@/components/AccountDrawer.vue';

export default {
  name: 'AppNavbar',
  components: {
    AccountDrawer,
  },
  data() {
    return {
      menuVisible: false,
      authState,
      isAccountDrawerVisible: false,
      user: null, // Added to store user details
    };
  },
  created() {
    if (this.authState.isAuthenticated) {
      this.fetchUserDetails();
    }
  },
  watch: {
    'authState.isAuthenticated'(newVal) {
      if (newVal) {
        this.fetchUserDetails();
      } else {
        this.user = null;
      }
    },
  },
  methods: {
    toggleMenu() {
      this.menuVisible = !this.menuVisible;
    },
    toggleAccountDrawer() {
      this.isAccountDrawerVisible = !this.isAccountDrawerVisible;
    },
    fetchUserDetails() {
      axios
        .get('/api/user')
        .then((response) => {
          this.user = response.data;
        })
        .catch((error) => {
          console.error('Error fetching user details:', error);
          // Optionally handle error (e.g., redirect to login)
        });
    },
  },
};
</script>