<!-- SearchBar.vue -->

<template>
  <div class="search-container">
    <div class="search-wrapper">
      <span class="search-prefix">$</span>
      <input
        type="text"
        id="searchBar"
        placeholder="Search for stocks..."
        v-model="ticker"
        @input="onInputChange"
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

    <!-- Suggestions Dropdown -->
    <ul v-if="showSuggestions" class="suggestions-list">
      <li
        v-for="(suggestion, index) in suggestions"
        :key="index"
        @click="selectSuggestion(suggestion)"
        class="suggestion-item"
      >
        {{ suggestion.symbol }} - {{ suggestion.name }}
      </li>
      <li v-if="suggestions.length === 0" class="suggestion-item disabled">
        No suggestions available
      </li>
    </ul>

    <transition name="fade">
      <div class="advanced-options" :class="{ show: showAdvancedOptions }" v-show="showAdvancedOptions">
        <!-- Advanced options checkboxes -->
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
          Bollinger Bands
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
import axios from 'axios';
import debounce from 'lodash/debounce';

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
      suggestions: [],
      showSuggestions: false,
    };
  },
  computed: {
    isAnyIndicatorSelected() {
      return Object.values(this.localIndicators).some((val) => val);
    },
  },
  methods: {
    searchStock() {
      const params = {
        ticker: this.ticker.trim().toUpperCase(),
        MACD: this.localIndicators.MACD,
        RSI: this.localIndicators.RSI,
        SMA: this.localIndicators.SMA,
        EMA: this.localIndicators.EMA,
        ATR: this.localIndicators.ATR,
        BBands: this.localIndicators.BBands,
        VWAP: this.localIndicators.VWAP,
      };
      this.$router.push({ name: 'Results', query: params });
      this.showSuggestions = false;
    },
    advancedSearch() {
      if (this.isAnyIndicatorSelected) {
        this.searchStock();
      }
    },
    toggleAdvancedOptions() {
      this.showAdvancedOptions = !this.showAdvancedOptions;
    },
    onInputChange() {
      if (this.ticker.length >= 1) {
        this.fetchSuggestions();
      } else {
        this.suggestions = [];
        this.showSuggestions = false;
      }
    },
    fetchSuggestions: debounce(function () {
      const query = this.ticker.trim();
      if (query.length === 0) {
        this.suggestions = [];
        this.showSuggestions = false;
        return;
      }

      // Fetch suggestions from the backend
      axios
        .get('/api/suggestions', {
          params: {
            query: query,
          },
        })
        .then((response) => {
          // Filter out symbols ending with '=F' or '=X'
          this.suggestions = response.data.suggestions.filter((item) => {
            return !/.*=(F|X)$/i.test(item.symbol);
          });
          this.showSuggestions = true;
        })
        .catch((error) => {
          console.error('Error fetching suggestions:', error);
          this.suggestions = [];
          this.showSuggestions = false;
        });
    }, 300),
    selectSuggestion(suggestion) {
      this.ticker = suggestion.symbol;
      this.showSuggestions = false;
      this.searchStock();
    },
    handleClickOutside(event) {
      if (!this.$el.contains(event.target)) {
        this.showSuggestions = false;
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

<style scoped>
/* Existing styles */

.suggestions-list {
  position: absolute;
  top: calc(100% + var(--spacing-xs));
  left: 0;
  width: 100%;
  background-color: #ffffff;
  border: 1px solid #d1d5db;
  border-top: none;
  border-radius: 0 0 var(--border-radius) var(--border-radius);
  max-height: 200px;
  overflow-y: auto;
  z-index: 1000;
}

.suggestion-item {
  padding: var(--spacing-sm) var(--spacing-md);
  cursor: pointer;
  color: var(--color-text);
}

.suggestion-item:hover {
  background-color: var(--color-background);
}

.suggestion-item.disabled {
  color: var(--color-text-secondary);
  cursor: default;
}
</style>
