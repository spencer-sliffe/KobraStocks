<template>
  <div>
    <div class="main-content">
      <h2>Our Services</h2>
      <p>Detail the range of services KobraStocks offers, such as investment portfolio management, real-time stock alerts, financial advisory, etc.</p>
    </div>
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
