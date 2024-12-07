<!-- Prologue
Component Name: HomePage
Path: src/views/HomePage.vue

Description:
Displays the main page for KobraStocks, including search functionality, favorite stocks, hot stocks, and watchlist carousels, with a detailed stock drawer for viewing individual stock data.
-->

<template>
  <div class="homepage-layout">
    <!-- News Column -->
    <div class="news-column">
      <section class="stock-news">
        <h3 class="center">Latest Stock Market News</h3>
        <div v-if="loadingNews" class="loading-container">
          <div class="spinner"></div>
          <p>Loading news...</p>
        </div>
        <div v-else-if="newsArticles.length > 0">
          <div class="news-article" v-for="article in newsArticles" :key="article.url">
            <a :href="article.url" target="_blank" class="news-title">{{ article.title }}</a>
            <p class="news-description">{{ article.description }}</p>
            <small class="news-source">Source: {{ article.source.name }}</small>
          </div>
        </div>
        <div v-else>
          <p>No news articles found.</p>
        </div>
      </section>
    </div>

    <!-- Main Content Column -->
    <div class="content-column">
      <!-- Favorite Stocks Carousel -->
      <section class="favorite-stocks">
        <h2 class="center">Your Favorite Stocks</h2>
        <div v-if="favoriteStocksData && favoriteStocksData.length > 0">
          <carousel
            ref="favoriteCarousel"
            :items-to-show="itemsToShow"
            :wrap-around="true"
            :mouse-drag="true"
            :touch-drag="true"
            class="stock-carousel"
          >
            <!-- Custom Navigation -->
            <template #addons>
              <button
                @click="prev('favoriteCarousel')"
                class="carousel-nav-button prev-button"
                aria-label="Previous"
              >
                <i class="fas fa-chevron-left"></i>
              </button>
              <button
                @click="next('favoriteCarousel')"
                class="carousel-nav-button next-button"
                aria-label="Next"
              >
                <i class="fas fa-chevron-right"></i>
              </button>
            </template>

            <slide
              v-for="stock in favoriteStocksData"
              :key="stock.ticker"
              class="carousel-slide-item"
            >
              <div class="stock-card" @click="openDrawer(stock.ticker)">
                <div class="stock-card-header">
                  <div class="stock-card-icon">
                    <img :src="stock.logoUrl" alt="Logo" v-if="stock.logoUrl" />
                    <div v-else class="stock-initial">{{ stock.ticker.charAt(0) }}</div>
                  </div>
                  <div class="stock-card-info">
                    <h3>${{ stock.ticker }}</h3>
                    <p class="company-name">{{ stock.name }}</p>
                  </div>
                </div>
                <div class="stock-card-body">
                  <div class="stock-price">
                    $<span v-if="stock.close_price !== undefined">{{ stock.close_price.toFixed(2) }}</span><span v-else>N/A</span>
                  </div>
                  <div
                    class="stock-change"
                    :class="{ positive: stock.percentage_change >= 0, negative: stock.percentage_change < 0 }"
                  >
                    <span v-if="stock.percentage_change !== undefined">{{ stock.percentage_change.toFixed(2) }}%</span><span v-else>N/A</span>
                  </div>
                </div>
              </div>
            </slide>
          </carousel>
        </div>
        <div v-else>
          <p class="center">No favorite stocks in your list at this time.</p>
        </div>
      </section>

      <!-- Hot Stocks Carousel -->
      <section class="hot-stocks">
        <h2 class="center">Hot Stocks</h2>
        <div v-if="hotStocks && hotStocks.length > 0">
          <carousel
            ref="hotStocksCarousel"
            :items-to-show="itemsToShow"
            :wrap-around="true"
            :mouse-drag="true"
            :touch-drag="true"
            class="stock-carousel"
          >
            <!-- Custom Navigation -->
            <template #addons>
              <button
                @click="prev('hotStocksCarousel')"
                class="carousel-nav-button prev-button"
                aria-label="Previous"
              >
                <i class="fas fa-chevron-left"></i>
              </button>
              <button
                @click="next('hotStocksCarousel')"
                class="carousel-nav-button next-button"
                aria-label="Next"
              >
                <i class="fas fa-chevron-right"></i>
              </button>
            </template>

            <slide
              v-for="stock in hotStocks"
              :key="stock.ticker"
              class="carousel-slide-item"
            >
              <div class="stock-card" @click="openDrawer(stock.ticker)">
                <div class="stock-card-header">
                  <div class="stock-card-icon">
                    <img :src="stock.logoUrl" alt="Logo" v-if="stock.logoUrl" />
                    <div v-else class="stock-initial">{{ stock.ticker.charAt(0) }}</div>
                  </div>
                  <div class="stock-card-info">
                    <h3>${{ stock.ticker }}</h3>
                    <p class="company-name">{{ stock.name }}</p>
                  </div>
                </div>
                <div class="stock-card-body">
                  <div class="stock-price">
                    $<span v-if="stock.close_price !== undefined">{{ stock.close_price.toFixed(2) }}</span><span v-else>N/A</span>
                  </div>
                  <div
                    class="stock-change"
                    :class="{ positive: stock.percentage_change >= 0, negative: stock.percentage_change < 0 }"
                  >
                    <span v-if="stock.percentage_change !== undefined">{{ stock.percentage_change.toFixed(2) }}%</span><span v-else>N/A</span>
                  </div>
                </div>
              </div>
            </slide>
          </carousel>
        </div>
        <div v-else>
          <p class="center">No hot stocks available at this time.</p>
        </div>
      </section>

      <!-- Watchlist Stocks Carousel -->
      <section class="watchlist-stocks">
        <h2 class="center">Your Watchlist</h2>
        <div v-if="watchlistStocksData && watchlistStocksData.length > 0">
          <carousel
            ref="watchlistCarousel"
            :items-to-show="itemsToShow"
            :wrap-around="true"
            :mouse-drag="true"
            :touch-drag="true"
            class="stock-carousel"
          >
            <!-- Custom Navigation -->
            <template #addons>
              <button
                @click="prev('watchlistCarousel')"
                class="carousel-nav-button prev-button"
                aria-label="Previous"
              >
                <i class="fas fa-chevron-left"></i>
              </button>
              <button
                @click="next('watchlistCarousel')"
                class="carousel-nav-button next-button"
                aria-label="Next"
              >
                <i class="fas fa-chevron-right"></i>
              </button>
            </template>

            <slide
              v-for="stock in watchlistStocksData"
              :key="stock.ticker"
              class="carousel-slide-item"
            >
              <div class="stock-card" @click="openDrawer(stock.ticker)">
                <div class="stock-card-header">
                  <div class="stock-card-icon">
                    <img :src="stock.logoUrl" alt="Logo" v-if="stock.logoUrl" />
                    <div v-else class="stock-initial">{{ stock.ticker.charAt(0) }}</div>
                  </div>
                  <div class="stock-card-info">
                    <h3>${{ stock.ticker }}</h3>
                    <p class="company-name">{{ stock.name }}</p>
                  </div>
                </div>
                <div class="stock-card-body">
                  <div class="stock-price">
                    $<span v-if="stock.close_price !== undefined">{{ stock.close_price.toFixed(2) }}</span><span v-else>N/A</span>
                  </div>
                  <div
                    class="stock-change"
                    :class="{ positive: stock.percentage_change >= 0, negative: stock.percentage_change < 0 }"
                  >
                    <span v-if="stock.percentage_change !== undefined">{{ stock.percentage_change.toFixed(2) }}%</span><span v-else>N/A</span>
                  </div>
                </div>
              </div>
            </slide>
          </carousel>
        </div>
        <div v-else>
          <p class="center">You have no stocks in your watchlist.</p>
        </div>
      </section>
    </div>

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
import StockDrawer from '@/components/StockDrawer.vue';

export default {
  name: 'HomePage',
  components: {
    Carousel,
    Slide,
    StockDrawer,
  },
  data() {
    return {
      ticker: '',
      indicators: {
        RSI: false,
        MACD: false,
        SMA: false,
        EMA: false,
        ATR: false,
        BBands: false,
        VWAP: false,
      },
      hotStocks: [],
      favoriteStocks: [],
      favoriteStocksData: [],
      userWatchlist: [],
      watchlistStocksData: [],
      showDrawer: false,
      selectedTicker: '',
      itemsToShow: 3,
      newsArticles: [],
      loadingNews: false,
    };
  },
  methods: {
    fetchHotStocks() {
      axios
        .get('/api/hot_stocks')
        .then((response) => {
          if (response.data.message) {
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
        return axios
          .get(`/api/stock_data?ticker=${ticker}`)
          .then((response) => {
            const data = response.data;
            data.name = data.name || 'Company Name';
            data.logoUrl = data.logoUrl || '';
            return data;
          })
          .catch((error) => {
            console.error(`Error fetching data for ${ticker}:`, error);
            return null;
          });
      });
      Promise.all(promises)
        .then((stocksData) => {
          this.favoriteStocksData = stocksData.filter((data) => data !== null);
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
    fetchStockNews() {
      this.loadingNews = true;
      axios
        .get('/api/news', { params: { query: 'stock market' } })
        .then((response) => {
          this.newsArticles = response.data.articles || [];
        })
        .catch((error) => {
          console.error('Error fetching news:', error);
          this.newsArticles = [];
        })
        .finally(() => {
          this.loadingNews = false;
        });
    },
    fetchUserWatchlist() {
      axios
        .get('/api/user')
        .then((response) => {
          this.userWatchlist = response.data.watched_stocks;
          this.loadWatchlistStocksData();
        })
        .catch((error) => {
          console.error('Error fetching user watchlist:', error);
        });
    },
    loadWatchlistStocksData() {
      const promises = this.userWatchlist.map((ticker) => {
        return axios
          .get(`/api/stock_data?ticker=${ticker}`)
          .then((response) => {
            const data = response.data;
            data.name = data.name || 'Company Name';
            data.logoUrl = data.logoUrl || '';
            return data;
          })
          .catch((error) => {
            console.error(`Error fetching data for ${ticker}:`, error);
            return null;
          });
      });
      Promise.all(promises)
        .then((stocksData) => {
          this.watchlistStocksData = stocksData.filter((data) => data !== null);
        })
        .catch((error) => {
          console.error('Error loading watchlist stocks data:', error);
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
        this.loadFavoriteStocksData();
      }
    },
    addTickerToWatchlist(ticker) {
      if (!this.userWatchlist.includes(ticker)) {
        this.userWatchlist.push(ticker);
        this.loadWatchlistStocksData();
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
    prev(carouselRef) {
      this.$refs[carouselRef].prev();
    },
    next(carouselRef) {
      this.$refs[carouselRef].next();
    },
  },
  mounted() {
    this.fetchHotStocks();
    this.fetchFavoriteStocks();
    this.fetchUserWatchlist();
    this.updateItemsToShow();
    this.fetchStockNews();
    window.addEventListener('resize', this.updateItemsToShow);
  },
  beforeUnmount() {
    window.removeEventListener('resize', this.updateItemsToShow);
  },
};
</script>
