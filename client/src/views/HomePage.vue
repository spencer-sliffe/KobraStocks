<template>
  <div>
    <SearchBar :indicators="indicators"/>
    <div class="cards-container">
      <label class="card" :class="{ active: indicators.RSI }">
        <input type="checkbox" v-model="indicators.RSI" hidden/>
        <h2>RSI (Relative Strength Index)</h2>
        <p>A momentum oscillator that measures the speed and change of price movements.</p>
        <p>RSI is typically used to identify overbought or oversold conditions in a market.</p>
      </label>
      <label class="card" :class="{ active: indicators.MACD }">
        <input type="checkbox" v-model="indicators.MACD" hidden/>
        <h2>MACD (Moving Average Convergence Divergence)</h2>
        <p>A trend-following momentum indicator that shows the relationship between two moving averages of a security’s
          price.</p>
        <p>MACD is used to spot changes in the strength, direction, momentum, and duration of a trend in a stock's
          price.</p>
      </label>
      <label class="card" :class="{ active: indicators.MA50 }">
        <input type="checkbox" v-model="indicators.MA50" hidden/>
        <h2>MA50 (50-Day Moving Average)</h2>
        <p>An indicator that averages out the closing prices for the last 50 days and updates with each new closing
          price.</p>
        <p>It's used to analyze the mid-term trend and determine support or resistance levels.</p>
      </label>

      <label class="card" :class="{ active: indicators.MA9 }">
        <input type="checkbox" v-model="indicators.MA9" hidden/>
        <h2>MA9 (9-Day Moving Average)</h2>
        <p>A short-term moving average that averages the closing prices over the past 9 days.</p>
        <p>Often used by traders to spot short-term trend reversals and as a component of the MACD.</p>
      </label>
    </div>
    <section class="favorite-stocks">
      <h2>Your Favorite Stocks</h2>
      <carousel :items-to-show="3" :wrap-around="true">
        <slide
            v-for="stock in favoriteStocksData"
            :key="stock.ticker"
        >
          <div
              class="favorite-stock-card"
              @click="openDrawer(stock.ticker)"
          >
            <h3>{{ stock.ticker }}</h3>
            <p>
              Price: $
              <span v-if="stock.close_price !== undefined">
                {{ stock.close_price.toFixed(2) }}
              </span>
              <span v-else>N/A</span>
            </p>
            <p
                :class="{
                positive: stock.percentage_change >= 0,
                negative: stock.percentage_change < 0,
              }"
            >
              <span v-if="stock.percentage_change !== undefined">
                {{ stock.percentage_change.toFixed(2) }}%
              </span>
              <span v-else>N/A</span>
            </p>
          </div>
        </slide>
      </carousel>
    </section>
    <section class="hot-stocks">
      <h2>Hot Stocks</h2>
      <div v-if="hotStocks.length > 0">
        <carousel :items-to-show="3" :wrap-around="true">
          <slide v-for="stock in hotStocks" :key="stock.ticker">
            <div
                class="hot-stock-card"
                @click="openDrawer(stock.ticker)"
            >
              <h3>{{ stock.ticker }}</h3>
              <p>
                Price: $
                <span v-if="stock.close_price !== undefined">
                    {{ stock.close_price.toFixed(2) }}
                  </span>
                <span v-else>N/A</span>
              </p>
              <p
                  :class="{
                    positive: stock.percentage_change >= 0,
                    negative: stock.percentage_change < 0,
                  }"
              >
                  <span v-if="stock.percentage_change !== undefined">
                    {{ stock.percentage_change.toFixed(2) }}%
                  </span>
                <span v-else>N/A</span>
              </p>
            </div>
          </slide>
        </carousel>
      </div>
      <div v-else>
        <p>No hot stocks found within your budget.</p>
      </div>
    </section>
    <StockDrawer
        :ticker="selectedTicker"
        :isVisible="showDrawer"
        :userFavorites="favoriteStocks"
        :userWatchlist="userWatchlist"
        @close="closeDrawer"
        @update-favorites="addTickerToFavorites"
        @update-watchlist="addTickerToWatchlist"
    />
  </div>
</template>
<script>
import axios from 'axios';
import StockDrawer from '@/components/StockDrawer.vue';
import SearchBar from '@/components/SearchBar.vue';
import { Carousel, Slide } from 'vue3-carousel';
import 'vue3-carousel/dist/carousel.css';

export default {
  name: 'HomePage',
  components: {
    StockDrawer,
    SearchBar,
    Carousel,
    Slide,
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
      favoriteStocks: [],
      favoriteStocksData: [],
      userWatchlist: [],
      showDrawer: false,
      selectedTicker: '',
    };
  },
  methods: {
    addTickerToFavorites(ticker) {
      if (!this.favoriteStocks.includes(ticker)) {
        this.favoriteStocks.push(ticker);
        this.loadFavoriteStocksData();
      }
    },
    addTickerToWatchlist(ticker) {
      if (!this.userWatchlist.includes(ticker)) {
        this.userWatchlist.push(ticker);
      }
    },
    fetchFavoriteStocks() {
      axios
          .get('/api/user')
          .then((response) => {
            this.favoriteStocks = response.data.favorite_stocks;
            this.userWatchlist = response.data.watched_stocks;
            this.loadFavoriteStocksData();
          })
          .catch((error) => {
            console.error('Error fetching favorite stocks:', error);
          });
    },
    loadFavoriteStocksData() {
      const promises = this.favoriteStocks.map((ticker) => {
        return axios.get(`/api/stock_data?ticker=${ticker}`)
            .then((response) => response.data)
            .catch((error) => {
              console.error(`Error fetching data for ${ticker}:`, error);
              return null; // Return null to handle it later
            });
      });
      Promise.all(promises)
          .then((stocksData) => {
            // Filter out null entries where data wasn't fetched
            this.favoriteStocksData = stocksData.filter(data => data !== null);
          })
          .catch((error) => {
            console.error('Error loading favorite stocks data:', error);
          });
    },
    searchStock() {
      const params = {
        ticker: this.ticker,
        RSI: this.indicators.RSI,
        MACD: this.indicators.MACD,
        MA50: this.indicators.MA50,
        MA9: this.indicators.MA9,
      };
      this.$router.push({name: 'Results', query: params});
    },
    fetchHotStocks() {
      axios
        .get('/api/hot_stocks')
        .then((response) => {
          if (response.data.message) {
            alert(response.data.message);
            this.hotStocks = response.data.data;
          } else {
            this.hotStocks = response.data;
          }
        })
        .catch((error) => {
          console.error('Error fetching hot stocks:', error);
          alert('Failed to fetch hot stocks. Please try again later.');
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
    this.fetchFavoriteStocks();
  },
};
</script>