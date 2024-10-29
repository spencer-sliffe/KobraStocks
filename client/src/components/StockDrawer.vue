<template>
  <transition name="slide">
    <div class="stock-drawer" v-if="isVisible">
      <div class="drawer-header">
        <h2>{{ stockData.ticker }}</h2>
        <button @click="closeDrawer">Close</button>
      </div>
      <div class="drawer-content">
        <p>Price: ${{ stockData.close_price.toFixed(2) }}</p>
        <p>Open: ${{ stockData.open_price.toFixed(2) }}</p>
        <p>High: ${{ stockData.high_price.toFixed(2) }}</p>
        <p>Low: ${{ stockData.low_price.toFixed(2) }}</p>
        <p>Volume: {{ stockData.volume }}</p>
        <button @click="addToFavorites(stockData.ticker)">Add to Favorites</button>
        <button @click="addToWatchlist(stockData.ticker)">Add to Watchlist</button>
      </div>
    </div>
  </transition>
</template>

<script>
import axios from 'axios';

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
  },
  data() {
    return {
      stockData: {},
      isLoading: false,
    };
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
        this.stockData = {};
      }
    },
  },
  methods: {
    fetchStockData(ticker) {
      this.isLoading = true;
      axios
        .get(`/api/stock_data?ticker=${ticker}`)
        .then((response) => {
          this.stockData = response.data;
          this.isLoading = false;
        })
        .catch((error) => {
          console.error('Error fetching stock data:', error);
          this.isLoading = false;
          this.closeDrawer();
          alert('Failed to fetch stock data. Please try again later.');
        });
    },
    closeDrawer() {
      this.$emit('close');
    },
    addToFavorites(ticker) {
      axios
        .post('/api/favorites', { ticker })
        .then(() => {
          alert(`${ticker} added to favorites.`);
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
        })
        .catch((error) => {
          console.error('Error adding to watchlist:', error);
          alert('Failed to add to watchlist. Please try again.');
        });
    },
  },
};
</script>
