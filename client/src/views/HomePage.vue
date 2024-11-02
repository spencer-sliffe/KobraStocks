<template>
  <div>

    <!-- Search Bar Component -->
    <SearchBar :indicators="indicators" @search="handleSearch" />
    <section class="favorite-stocks">
      <h2>Your Favorite Stocks</h2>
      <carousel
        :items-to-show="itemsToShow"
        :wrap-around="true"
        :mouse-drag="true"
        :touch-drag="true"
        :navigation-enabled="true"
        class="stock-carousel"
      >
        <template #prev>
          <button class="carousel-nav-button prev-button">
            <i class="fas fa-chevron-left"></i>
          </button>
        </template>
        <template #next>
          <button class="carousel-nav-button next-button">
            <i class="fas fa-chevron-right"></i>
          </button>
        </template>

        <slide v-for="stock in favoriteStocksData" :key="stock.ticker">
          <div class="favorite-stock-card" @click="openDrawer(stock.ticker)">
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

    <!-- Hot Stocks Carousel -->
    <section class="hot-stocks">
      <h2>Hot Stocks</h2>
      <div v-if="hotStocks && hotStocks.length > 0">
        <carousel
          :items-to-show="itemsToShow"
          :wrap-around="true"
          :mouse-drag="true"
          :touch-drag="true"
          :navigation-enabled="true"
          class="stock-carousel"
        >
          <template #prev>
            <button class="carousel-nav-button prev-button">
              <i class="fas fa-chevron-left"></i>
            </button>
          </template>
          <template #next>
            <button class="carousel-nav-button next-button">
              <i class="fas fa-chevron-right"></i>
            </button>
          </template>

          <slide v-for="stock in hotStocks" :key="stock.ticker">
            <div class="hot-stock-card" @click="openDrawer(stock.ticker)">
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
        <p>No hot stocks available at this time.</p>
      </div>
    </section>

    <!-- Stock Drawer Component -->
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
import { Carousel, Slide } from 'vue3-carousel';
import 'vue3-carousel/dist/carousel.css';
import '@fortawesome/fontawesome-free/css/all.css';
import SearchBar from '@/components/SearchBar.vue';
import StockDrawer from '@/components/StockDrawer.vue';

export default {
  name: 'HomePage',
  components: {
    Carousel,
    Slide,
    SearchBar,
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
      favoriteStocks: [],
      favoriteStocksData: [],
      userWatchlist: [],
      showDrawer: false,
      selectedTicker: '',
      itemsToShow: 3,
    };
  },
  methods: {
    handleSearch(searchParams) {
      // Handle search parameters from SearchBar component
      // For example, fetch hot stocks based on searchParams
      console.log('Search Parameters:', searchParams);
      // Implement search functionality as needed
    },
    fetchHotStocks() {
      axios
        .get('/api/hot_stocks')
        .then((response) => {
          if (response.data.message) {
            // Handle the case where no hot stocks are found within the budget
            alert(response.data.message);
            this.hotStocks = response.data.data || [];
          } else {
            this.hotStocks = response.data || [];
          }
        })
        .catch((error) => {
          console.error('Error fetching hot stocks:', error);
          alert('Failed to fetch hot stocks. Please try again later.');
          this.hotStocks = [];
        });
    },
    loadFavoriteStocksData() {
      const promises = this.favoriteStocks.map((ticker) => {
        return axios.get(`/api/stock_data?ticker=${ticker}`)
            .then((response) => response.data)
            .catch((error) => {
              console.error(`Error fetching data for ${ticker}:`, error);
              return null;
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
    fetchUserWatchlist() {
      axios
        .get('/api/watchlist')
        .then((response) => {
          // Ensure the response data is an array
          if (Array.isArray(response.data)) {
            this.userWatchlist = response.data;
          } else if (response.data && Array.isArray(response.data.watchlist)) {
            this.userWatchlist = response.data.watchlist;
          } else {
            console.warn('Unexpected watchlist format:', response.data);
            this.userWatchlist = [];
          }
        })
        .catch((error) => {
          console.error('Error fetching watchlist:', error);
          this.userWatchlist = [];
        });
    },
    openDrawer(ticker) {
      this.selectedTicker = ticker;
      this.showDrawer = true;
    },
    closeDrawer() {
      this.showDrawer = false;
    },
    addTickerToFavorites(ticker) {
      if (!this.favoriteStocks.includes(ticker)) {
        this.favoriteStocks.push(ticker);
        this.fetchFavoriteStocksData();
      }
    },
    addTickerToWatchlist(ticker) {
      if (!this.userWatchlist.includes(ticker)) {
        this.userWatchlist.push(ticker);
      }
    },
    updateItemsToShow() {
      const width = window.innerWidth;
      if (width >= 1024) {
        this.itemsToShow = 3;
      } else if (width >= 768) {
        this.itemsToShow = 2;
      } else {
        this.itemsToShow = 1;
      }
    },
  },
  mounted() {
    this.fetchHotStocks();
    this.fetchFavoriteStocks();
    this.fetchUserWatchlist();
    this.updateItemsToShow();
    window.addEventListener('resize', this.updateItemsToShow);
  },
  beforeUnmount() {
    window.removeEventListener('resize', this.updateItemsToShow);
  },
};
</script>
