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

    <h1>Stock Chart for {{ ticker }}</h1>
    <div v-html="graphHtml"></div>

    <div class="data-1">
      <h2>Open | Close | High | Low | Vol</h2>
      <h2>{{ popen }} | {{ pclose }} | {{ phigh }} | {{ plow }} | {{ volume }}</h2>
    </div>

    <div class="data">
      <div>
        <h2>ML Suggest | Strength</h2>
      </div>
      <div>
        <h2>Tomorrow</h2>
        <h4>{{ dprediction }} | {{ daccuracy }}</h4>
      </div>
      <div>
        <h2>Next Week</h2>
        <h4>{{ wprediction }} | {{ waccuracy }}</h4>
      </div>
      <div>
        <h2>Next Month</h2>
        <h4>{{ mprediction }} | {{ maccuracy }}</h4>
      </div>
    </div>

    <footer>
      <p>&copy; 2024 KobraStocks All rights reserved.</p>
    </footer>
  </div>
</template>

<script>
export default {
  data() {
    return {
      dropdownVisible: false,
      ticker: 'AAPL',
      graphHtml: '', // You can fetch this from an API later
      popen: '',
      pclose: '',
      phigh: '',
      plow: '',
      volume: '',
      dprediction: '',
      wprediction: '',
      mprediction: '',
      daccuracy: '',
      waccuracy: '',
      maccuracy: ''
    };
  },
  methods: {
    toggleDropdown() {
      this.dropdownVisible = !this.dropdownVisible;
    },
    fetchStockData() {
      // Fetch stock data from Flask API
      // Example of an API call using axios to retrieve the graph and other data
    }
  }
};
</script>
