<template>
  <div>
    <SearchBar :indicators="indicators"/>
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
              this.hotStocks = [];
              alert(response.data.message);
              this.$router.push({name: 'Account'});
            } else {
              this.hotStocks = response.data;
            }
          })
          .catch((error) => {
            console.error('Error fetching hot stocks:', error);
            if (error.response && error.response.data && error.response.data.error) {
              alert(error.response.data.error);
              if (error.response.data.error.includes('set your budget')) {
                this.$router.push({name: 'Account'});
              }
            } else {
              alert('Failed to fetch hot stocks. Please try again later.');
            }
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