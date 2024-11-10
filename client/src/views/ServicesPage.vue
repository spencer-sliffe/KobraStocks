<!-- Prologue
Component Name: ServicesPage
Path: src/views/ServicesPage.vue

Description:
Outlines the services provided by KobraStocks, such as portfolio management, real-time alerts, and financial advisory.
-->

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
