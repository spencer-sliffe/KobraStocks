<!-- Prologue
Component Name: ServicesPage
Path: src/views/ServicesPage.vue

Description:
Outlines the services provided by KobraStocks, such as portfolio management, real-time alerts, and financial advisory.
-->

<template>
  <div>
    <div class="main-content">
      <h2 class="center">Our Services</h2>
      <p class="center">KobraStocks provides a suite of powerful tools and services designed to empower users in their investment journey.</p>
      <p class="center">From real-time stock alerts to advanced financial advisory, we offer everything you need to stay ahead of the market.</p>
      <div class="service-section">
        <div class="service-card">
          <h3 class="center">📈 Investment Portfolio Management</h3>
          <p class="center">
            Monitor, track, and optimize your investments in one place. Our portfolio management system offers a clear overview of your assets, personalized insights, and real-time performance tracking.
          </p>
        </div>

        <div class="service-card">
          <h3 class="center">🔔 Real-Time Stock Alerts</h3>
          <p class="center">
            Stay ahead of the market with real-time alerts. Receive instant notifications on significant price movements, news updates, and changes in your watched stocks.
          </p>
        </div>

        <div class="service-card">
          <h3 class="center">📊 Stock Price Predictions</h3>
          <p class="center">
            Our state-of-the-art machine learning models analyze market trends and predict future stock movements, helping you make informed investment decisions with confidence.
          </p>
        </div>

        <div class="service-card">
          <h3 class="center">📡 Real-Time Market Data</h3>
          <p class="center">
            Access real-time data on stock prices, financial indicators, and other key metrics. Stay connected to live market movements and never miss an opportunity.
          </p>
        </div>

        <div class="service-card">
          <h3 class="center">💡 Personalized Financial Advisory</h3>
          <p class="center">
            Tailored financial advice based on your goals, preferences, and risk tolerance. Our AI-powered advisory system guides you through personalized investment strategies.
          </p>
        </div>

        <div class="service-card">
          <h3 class="center">🧮 Customizable Financial Indicators</h3>
          <p class="center">
            Select from a wide range of financial indicators to create a model that fits your strategy. Customize technical indicators, moving averages, and other market signals.
          </p>
        </div>

        <div class="service-card">
          <h3 class="center">📅 Investment Planning Tools</h3>
          <p class="center">
            Plan your investment goals with our easy-to-use planning tools. From goal setting to risk analysis, our tools help you stay on track toward achieving your financial objectives.
          </p>
        </div>

        <div class="service-card">
          <h3 class="center">🔍 Stock Search & Analysis</h3>
          <p class="center">
            Instantly search for any stock and access comprehensive analysis, price history, and predictions. Our stock search tool provides all the data you need to make quick decisions.
          </p>
        </div>
      </div>
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
