<!-- AppNavbar.vue -->
<template>
  <nav>
    <!-- Logo -->
    <router-link to="/" class="logo">
      <img src="@/assets/logo.png" alt="KobraStocks Logo" />
    </router-link>

    <!-- Conditionally Render SearchBar -->
    <div v-if="authState.isAuthenticated" class="search-bar-container">
      <SearchBar :indicators="indicators" @search="handleSearch" />
    </div>

    <!-- Navigation Items -->
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

      <!-- Account Icon Button -->
      <div v-if="authState.isAuthenticated" class="account-icon">
        <button @click="toggleAccountDrawer">
          <!-- Account SVG Icon -->
          <svg
            xmlns="http://www.w3.org/2000/svg"
            class="account-svg-icon"
            viewBox="0 0 24 24"
            fill="currentColor"
          >
            <path
              d="M12 12c2.7 0 5-2.3 5-5s-2.3-5-5-5-5 2.3-5 5 2.3 5 5 5zm0 2c-3.3 0-10 1.7-10 5v3h20v-3c0-3.3-6.7-5-10-5z"
            />
          </svg>
        </button>
      </div>

      <!-- Hamburger Menu -->
      <div class="hamburger" @click="toggleMenu">☰</div>
    </div>

    <!-- Account Drawer Component -->
    <AccountDrawer
      :isVisible="isAccountDrawerVisible"
      @close="toggleAccountDrawer"
    />
  </nav>
</template>

<script>
import axios from 'axios';
import { authState } from '@/auth';
import AccountDrawer from '@/components/AccountDrawer.vue';
import SearchBar from '@/components/SearchBar.vue';

export default {
  name: 'AppNavbar',
  components: {
    SearchBar,
    AccountDrawer,
  },
  data() {
    return {
      menuVisible: false,
      authState,
      isAccountDrawerVisible: false,
      user: null,
      ticker: '',
      indicators: {
        RSI: false,
        MACD: false,
        SMA: false,
        EMA: false,
        ATR: false,
        BBands: false,
        VWAP: false,
      },
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
        });
    },
    handleSearch(searchParams) {
      // Handle search parameters from SearchBar component
      this.$router.push({ name: 'Results', query: searchParams });
    },
  },
};
</script>
