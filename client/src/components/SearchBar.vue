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
      <div class="advanced-options" :class="{ show: showAdvancedOptions }" v-show="showAdvancedOptions">
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
  data() {
    return {
      ticker: '',
      showAdvancedOptions: false,
      localIndicators: {
        RSI: false,
        MACD: false,
        MA50: false,
        MA9: false,
      },
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
  },
};
</script>

<style scoped>
/* Fade Transition */
.fade-enter-active,
.fade-leave-active {
  transition: opacity var(--transition-speed), transform var(--transition-speed);
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
  transform: translateY(-10px);
}

/* Advanced Options Styling */
.advanced-options {
  position: absolute;
  top: calc(100% + var(--spacing-sm));
  left: 0;
  width: 100%;
  background-color: #ffffff;
  border: 1px solid #d1d5db;
  border-radius: 8px;
  padding: var(--spacing-lg);
  box-shadow: 0 8px 12px rgba(0, 0, 0, 0.1);
  z-index: 1000;
  opacity: 0;
  visibility: hidden;
  transform: translateY(-10px);
  transition: opacity var(--transition-speed), visibility var(--transition-speed), transform var(--transition-speed);
}

.advanced-options.show {
  opacity: 1;
  visibility: visible;
  transform: translateY(0);
}
</style>
