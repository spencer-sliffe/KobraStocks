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
          <!-- Account and Logout links removed -->
        </template>
        <template v-else>
          <li><router-link to="/signup">Sign Up</router-link></li>
          <li><router-link to="/">Login</router-link></li>
        </template>
      </ul>
      <!-- Account Button -->
      <div v-if="authState.isAuthenticated" class="account-icon">
        <button @click="toggleAccountDrawer">
          <!-- You can use an icon here instead of text -->
          Account
        </button>
      </div>
      <div class="hamburger" @click="toggleMenu">☰</div>
    </div>
    <!-- Account Drawer Component -->
    <AccountDrawer :isVisible="isAccountDrawerVisible" @close="toggleAccountDrawer" />
  </nav>
</template>

<script>
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
    };
  },
  methods: {
    toggleMenu() {
      this.menuVisible = !this.menuVisible;
    },
    toggleAccountDrawer() {
      this.isAccountDrawerVisible = !this.isAccountDrawerVisible;
    },
  },
};
</script>