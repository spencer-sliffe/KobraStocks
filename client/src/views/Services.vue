<template>
  <div>
    <header>
      <h1>KobraStocks</h1>
      <div class="hamburger" @click="toggleDropdown">☰</div>
      <nav>
        <ul id="nav-menu">
          <li><a href="/">Home</a></li>
          <li><a href="/about">About</a></li>
          <li><a href="/services">Services</a></li>
          <li><a href="/contact">Contact</a></li>
        </ul>
        <div id="nav-dropdown" class="nav-dropdown" v-if="dropdownVisible">
          <a href="/">Home</a>
          <a href="/about">About</a>
          <a href="/services">Services</a>
          <a href="/contact">Contact</a>
        </div>
      </nav>
    </header>

    <div class="main-content">
      <h2>Our Services</h2>
      <p>Detail the range of services KobraStocks offers, such as investment portfolio management, real-time stock alerts, financial advisory, etc.</p>
    </div>

    <footer>
      <p>&copy; 2024 KobraStocks All rights reserved.</p>
      <a href="#">Privacy Policy</a>
    </footer>
  </div>
</template>

<script>
export default {
  data() {
    return {
      dropdownVisible: false
    };
  },
  methods: {
    toggleDropdown() {
      this.dropdownVisible = !this.dropdownVisible;
    }
  }
};
</script>
