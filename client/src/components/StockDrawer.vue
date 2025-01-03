<!-- Prologue
Component Name: StockDrawer
Path: src/components/StockDrawer.vue

Description:
Displays detailed stock information in a sliding drawer, allowing users to view stock prices, volume, and add stocks to their favorites or watchlist.
-->

<template>
  <transition name="slide">
    <div class="stock-drawer" v-if="isVisible">
      <div class="drawer-header">
        <div class="link-button">
          <h2 @click="navigateToStockPage">
            ${{ stockData.ticker }}
          </h2>
          <p v-if="stockData.name" class="company-name">{{ stockData.name }}</p>
        </div>
        <button @click="closeDrawer">Close</button>
      </div>
      <div class="drawer-content">
        <div v-if="isLoading">
          <p>Loading stock data...</p>
        </div>
        <div v-else>
          <p v-if="stockData.close_price !== undefined">
            Price: ${{ stockData.close_price.toFixed(2) }}
          </p>
          <p v-else>
            Price: Data not available
          </p>
          <p v-if="stockData.open_price !== undefined">
            Open: ${{ stockData.open_price.toFixed(2) }}
          </p>
          <p v-else>
            Open: Data not available
          </p>
          <p v-if="stockData.high_price !== undefined">
            High: ${{ stockData.high_price.toFixed(2) }}
          </p>
          <p v-else>
            High: Data not available
          </p>
          <p v-if="stockData.low_price !== undefined">
            Low: ${{ stockData.low_price.toFixed(2) }}
          </p>
          <p v-else>
            Low: Data not available
          </p>
          <p v-if="stockData.volume !== undefined">
            Volume: {{ stockData.volume }}
          </p>
          <p v-else>
            Volume: Data not available
          </p>
          <button @click="addToFavorites(stockData.ticker)" :disabled="isInFavorites">
            {{ isInFavorites ? 'In Favorites' : 'Add to Favorites' }}
          </button>
          <button @click="addToWatchlist(stockData.ticker)" :disabled="isInWatchlist">
            {{ isInWatchlist ? 'In Watchlist' : 'Add to Watchlist' }}
          </button>
        </div>
      </div>
    </div>
  </transition>
</template>


<script>
import axios from "axios";

export default {
  name: 'StockDrawer',
  props: {
    ticker: {
      type: String,
      required: true,
    },
    isVisible: {
      type: Boolean,
      required: true,
    },
    userFavorites: {
      type: Array,
      default: () => [],
    },
    userWatchlist: {
      type: Array,
      default: () => [],
    },
  },
  data() {
    return {
      stockData: {
        ticker: '',
        open_price: 0,
        close_price: 0,
        high_price: 0,
        low_price: 0,
        volume: 0,
        percentage_change: 0,
      },
      isLoading: false,
    };
  },
  computed: {
    isInFavorites() {
      return this.userFavorites.includes(this.ticker);
    },
    isInWatchlist() {
      return this.userWatchlist.includes(this.ticker);
    },
  },
  watch: {
    ticker: {
      immediate: true,
      handler(newVal) {
        if (newVal) {
          this.fetchStockData(newVal);
        }
      },
    },
    isVisible(newVal) {
      if (!newVal) {
        this.stockData = {
          ticker: '',
          open_price: 0,
          close_price: 0,
          high_price: 0,
          low_price: 0,
          volume: 0,
          percentage_change: 0,
        };
      }
    },
  },
  methods: {
    navigateToStockPage() {
      const params = {
        ticker: this.stockData.ticker.trim().toUpperCase(),
        MACD: false,
        RSI: false,
        SMA: false,
        EMA: false,
        ATR: false,
        BBands: false,
        VWAP: false,
      };

      console.log('Navigating to Results with params:', params); // Debugging log
      this.$router.push({ name: 'Results', query: params }).catch((err) => {
        if (err.name !== 'NavigationDuplicated') {
          console.error('Navigation error:', err);
        }
      });
    },
    fetchStockData(ticker) {
      this.isLoading = true;
      axios
          .get(`/api/stock_data?ticker=${ticker}`)
          .then((response) => {
            this.stockData = {
              ticker: response.data.ticker || '',
              name: response.data.name || 'Company Name',
              open_price: parseFloat(response.data.open_price) || 0,
              close_price: parseFloat(response.data.close_price) || 0,
              high_price: parseFloat(response.data.high_price) || 0,
              low_price: parseFloat(response.data.low_price) || 0,
              volume: parseInt(response.data.volume) || 0,
              percentage_change: parseFloat(response.data.percentage_change) || 0,
            };
            this.isLoading = false;
          })
          .catch((error) => {
            console.error('Error fetching stock data:', error);
            this.isLoading = false;
            this.closeDrawer();
            alert('Failed to fetch stock data. Please try again later.');
          });
    },
    addToFavorites(ticker) {
      axios
          .post('/api/favorites', { ticker })
          .then(() => {
            alert(`${ticker} added to favorites.`);
            this.$emit('update-favorites', ticker);
            this.isInFavorites = true;
          })
          .catch((error) => {
            console.error('Error adding to favorites:', error);
            alert('Failed to add to favorites. Please try again.');
          });
    },
    addToWatchlist(ticker) {
      axios
          .post('/api/watchlist', { ticker })
          .then(() => {
            alert(`${ticker} added to watchlist.`);
            this.$emit('update-watchlist', ticker);
            this.isInWatchlist = true;
          })
          .catch((error) => {
            console.error('Error adding to watchlist:', error);
            alert('Failed to add to watchlist. Please try again.');
          });
    },
    closeDrawer() {
      this.$emit('close');
    },
  },
};
</script>

