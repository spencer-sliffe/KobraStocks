<!-- Prologue
Component Name: SearchBar
Path: src/components/SearchBar.vue

Description:
Provides a search interface for KobraStocks, allowing users to search for stocks by ticker with optional advanced technical indicators.
-->

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
          <input type="checkbox" v-model="localIndicators.MACD" />
          MACD
        </label>
        <label>
          <input type="checkbox" v-model="localIndicators.RSI" />
          RSI
        </label>
        <label>
          <input type="checkbox" v-model="localIndicators.SMA" />
          SMA
        </label>
        <label>
          <input type="checkbox" v-model="localIndicators.EMA" />
          EMA
        </label>
        <label>
          <input type="checkbox" v-model="localIndicators.ATR" />
          ATR
        </label>
        <label>
          <input type="checkbox" v-model="localIndicators.BBands" />
          BBands
        </label>
        <label>
          <input type="checkbox" v-model="localIndicators.VWAP" />
          VWAP
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
        MACD: false,
        RSI: false,
        SMA: false,
        EMA: false,
        ATR: false,
        BBands: false,
        VWAP: false,
      },
    };
  },
  computed: {
    isAnyIndicatorSelected() {
      return (
        this.localIndicators.MACD||
        this.localIndicators.RSI ||
        this.localIndicators.SMA ||
        this.localIndicators.EMA ||
        this.localIndicators.ATR ||
        this.localIndicators.BBands ||
        this.localIndicators.VWAP
      );
    },
  },
  methods: {
    searchStock() {
      const params = {
        ticker: this.ticker,
        MACD: false,
        RSI: false,
        SMA: false,
        EMA: false,
        ATR: false,
        BBands: false,
        VWAP: false,
      };
      this.$router.push({ name: 'Results', query: params });
    },
    advancedSearch() {
      if (this.isAnyIndicatorSelected) {
        const params = {
          ticker: this.ticker,
          MACD: this.localIndicators.MACD,
          RSI: this.localIndicators.RSI,
          SMA: this.localIndicators.SMA,
          EMA: this.localIndicators.EMA,
          ATR: this.localIndicators.ATR,
          BBands: this.localIndicators.BBands,
          VWAP: this.localIndicators.VWAP,
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
