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
      <button @click="searchStock" v-if="!showAdvancedOptions">Search</button>
      <button @click="advancedSearch" v-if="showAdvancedOptions" :disabled="!isAnyIndicatorSelected">
        Advanced Search
      </button>
      <button @click="toggleAdvancedOptions" class="advanced-toggle-button">
        <span v-if="!showAdvancedOptions">▼</span>
        <span v-else>▲</span>
      </button>
    </div>
    <transition name="fade">
      <div class="advanced-options" v-if="showAdvancedOptions">
        <label>
          <input type="checkbox" v-model="localIndicators.RSI" />
          RSI (Relative Strength Index)
        </label>
        <label>
          <input type="checkbox" v-model="localIndicators.MACD" />
          MACD (Moving Average Convergence Divergence)
        </label>
        <label>
          <input type="checkbox" v-model="localIndicators.MA50" />
          MA50 (50-Day Moving Average)
        </label>
        <label>
          <input type="checkbox" v-model="localIndicators.MA9" />
          MA9 (9-Day Moving Average)
        </label>
      </div>
    </transition>
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
      showAdvancedOptions: false,
      localIndicators: { ...this.indicators },
    };
  },
  computed: {
    isAnyIndicatorSelected() {
      return (
        this.localIndicators.RSI ||
        this.localIndicators.MACD ||
        this.localIndicators.MA50 ||
        this.localIndicators.MA9
      );
    },
  },
  methods: {
    searchStock() {
      const params = {
        ticker: this.ticker,
        RSI: false,
        MACD: false,
        MA50: false,
        MA9: false,
      };
      this.$router.push({ name: 'Results', query: params });
    },
    advancedSearch() {
      if (this.isAnyIndicatorSelected) {
        const params = {
          ticker: this.ticker,
          RSI: this.localIndicators.RSI,
          MACD: this.localIndicators.MACD,
          MA50: this.localIndicators.MA50,
          MA9: this.localIndicators.MA9,
        };
        this.$router.push({ name: 'Results', query: params });
      }
    },
    toggleAdvancedOptions() {
      this.showAdvancedOptions = !this.showAdvancedOptions;
    },
    handleClickOutside(event) {
      const advancedOptions = this.$el.querySelector('.advanced-options');
      const toggleButton = this.$el.querySelector('.advanced-toggle-button');
      if (
        advancedOptions &&
        !advancedOptions.contains(event.target) &&
        !toggleButton.contains(event.target)
      ) {
        this.showAdvancedOptions = false;
      }
    },
  },
  mounted() {
    document.addEventListener('click', this.handleClickOutside);
  },
  beforeUnmount() {
    document.removeEventListener('click', this.handleClickOutside);
  },
};
</script>
