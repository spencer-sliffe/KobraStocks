<template>
  <div>
    <!-- Search Bar and Indicators -->
    <div class="search-container">
      <div class="search-wrapper">
        <span class="search-prefix">$</span>
        <input
          type="text"
          id="searchBar"
          placeholder="Search for stocks..."
          v-model="ticker"
          required
        />
        <button @click="searchStock">Search</button>
      </div>
    </div>

    <div class="cards-container">
      <label class="card" :class="{ active: indicators.RSI }">
        <input type="checkbox" v-model="indicators.RSI" hidden />
        <h2>RSI (Relative Strength Index)</h2>
        <p>A momentum oscillator that measures the speed and change of price movements.</p>
        <p>RSI is typically used to identify overbought or oversold conditions in a market.</p>
      </label>

      <label class="card" :class="{ active: indicators.MACD }">
        <input type="checkbox" v-model="indicators.MACD" hidden />
        <h2>MACD (Moving Average Convergence Divergence)</h2>
        <p>A trend-following momentum indicator that shows the relationship between two moving averages of a security’s price.</p>
        <p>MACD is used to spot changes in the strength, direction, momentum, and duration of a trend in a stock's price.</p>
      </label>

      <label class="card" :class="{ active: indicators.MA50 }">
        <input type="checkbox" v-model="indicators.MA50" hidden />
        <h2>MA50 (50-Day Moving Average)</h2>
        <p>An indicator that averages out the closing prices for the last 50 days and updates with each new closing price.</p>
        <p>It's used to analyze the mid-term trend and determine support or resistance levels.</p>
      </label>

      <label class="card" :class="{ active: indicators.MA9 }">
        <input type="checkbox" v-model="indicators.MA9" hidden />
        <h2>MA9 (9-Day Moving Average)</h2>
        <p>A short-term moving average that averages the closing prices over the past 9 days.</p>
        <p>Often used by traders to spot short-term trend reversals and as a component of the MACD.</p>
      </label>
    </div>

    <!-- Hot Stocks Section -->
    <section class="hot-stocks">
      <h2>Hot Stocks</h2>
      <div class="hot-stocks-container">
        <div
          v-for="stock in hotStocks"
          :key="stock.ticker"
          class="hot-stock-card"
          @click="openDrawer(stock.ticker)"
        >
          <h3>{{ stock.ticker }}</h3>
          <p>Price: ${{ stock.close_price.toFixed(2) }}</p>
          <p
            :class="{
              positive: stock.percentage_change >= 0,
              negative: stock.percentage_change < 0,
            }"
          >
            {{ stock.percentage_change.toFixed(2) }}%
          </p>
        </div>
      </div>
    </section>

    <!-- Stock Drawer Component -->
    <StockDrawer
      :ticker="selectedTicker"
      :isVisible="showDrawer"
      @close="closeDrawer"
    />
  </div>
</template>

<script>
import axios from 'axios';
import StockDrawer from '@/components/StockDrawer.vue';

export default {
  name: 'HomePage',
  components: {
    StockDrawer,
  },
  data() {
    return {
      ticker: '',
      indicators: {
        RSI: false,
        MACD: false,
        MA50: false,
        MA9: false,
      },
      hotStocks: [],
      showDrawer: false,
      selectedTicker: '',
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
    fetchHotStocks() {
      axios
        .get('/api/hot_stocks')
        .then((response) => {
          this.hotStocks = response.data;
        })
        .catch((error) => {
          console.error('Error fetching hot stocks:', error);
        });
    },
    openDrawer(ticker) {
      this.selectedTicker = ticker;
      this.showDrawer = true;
    },
    closeDrawer() {
      this.showDrawer = false;
      this.selectedTicker = '';
    },
  },
  created() {
    this.fetchHotStocks();
  },
};
</script>