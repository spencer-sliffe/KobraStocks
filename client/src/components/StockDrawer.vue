<template>
  <transition name="slide">
    <div class="stock-drawer" v-if="isVisible">
      <div class="drawer-header">
        <h2>{{ stockData.ticker }}</h2>
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
          <button @click="addToFavorites(stockData.ticker)">Add to Favorites</button>
          <button @click="addToWatchlist(stockData.ticker)">Add to Watchlist</button>
        </div>
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
    fetchStockData(ticker) {
      this.isLoading = true;
      axios
        .get(`/api/stock_data?ticker=${ticker}`)
        .then((response) => {
          console.log('Stock data received:', response.data);
          // Ensure all numeric values are converted to numbers
          this.stockData = {
            ticker: response.data.ticker || '',
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

