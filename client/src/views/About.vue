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
      <h2>About Us</h2>
      <p>Here we can put the mission, vision, and planning of KobraStocks. We can put our team and values and why people should trust our site.</p>
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
