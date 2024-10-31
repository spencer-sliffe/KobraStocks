<template>
  <div class="search-container">
    <div class="search-wrapper">
      <span class="search-prefix">$</span>
      <input
        type="text"
        id="searchBar"
        placeholder="Search for stocks..."
        v-model="ticker"
        @keyup.enter="searchStock"
        required
      />
      <button @click="searchStock">Search</button>
    </div>
  </div>
</template>

<script>
export default {
  name: 'SearchBar',
  props: {
    initialTicker: {
      type: String,
      default: '',
    },
    indicators: {
      type: Object,
      default: () => ({
        RSI: false,
        MACD: false,
        MA50: false,
        MA9: false,
      }),
    },
  },
  data() {
    return {
      ticker: this.initialTicker,
    };
  },
  methods: {
    searchStock() {
      const params = {
        ticker: this.ticker,
        RSI: this.indicators.RSI,
        MACD: this.indicators.MACD,
        MA50: this.indicators.MA50,
        MA9: this.indicators.MA9,
      };
      this.$router.push({ name: 'Results', query: params });
    },
  },
};
</script>
