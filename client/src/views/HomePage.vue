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
                    <img :src="stock.logoUrl" alt="Logo" v-if="stock.logoUrl"/>
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
      <!-- Favorite Cryptos Carousel -->
      <section class="favorite-cryptos">
        <h2 class="center">Your Favorite Cryptocurrencies</h2>
        <div v-if="favoriteCryptosData && favoriteCryptosData.length > 0">
          <carousel
              ref="favoriteCryptosCarousel"
              :items-to-show="itemsToShow"
              :wrap-around="true"
              :mouse-drag="true"
              :touch-drag="true"
              class="stock-carousel"
          >
            <template #addons>
              <button
                  @click="prev('favoriteCryptosCarousel')"
                  class="carousel-nav-button prev-button"
                  aria-label="Previous"
              >
                <i class="fas fa-chevron-left"></i>
              </button>
              <button
                  @click="next('favoriteCryptosCarousel')"
                  class="carousel-nav-button next-button"
                  aria-label="Next"
              >
                <i class="fas fa-chevron-right"></i>
              </button>
            </template>

            <slide
                v-for="crypto in favoriteCryptosData"
                :key="crypto.crypto_id"
                class="carousel-slide-item"
            >
              <div class="crypto-card" @click="openCryptoDrawer(crypto.crypto_id)">
                <div class="crypto-card-header">
                  <div class="crypto-card-icon">
                    <img :src="crypto.logoUrl" alt="Logo" v-if="crypto.logoUrl"/>
                    <div v-else class="crypto-initial">{{ crypto.ticker.charAt(0) }}</div>
                  </div>
                  <div class="crypto-card-info">
                    <h3>${{ crypto.ticker }}</h3>
                    <p class="crypto-name">{{ crypto.name }}</p>
                  </div>
                </div>
                <div class="crypto-card-body">
                  <div class="crypto-price">
                    $<span v-if="crypto.price !== undefined">{{ crypto.price.toFixed(2) }}</span><span v-else>N/A</span>
                  </div>
                  <div
                      class="crypto-change"
                      :class="{ positive: crypto.percentage_change_24h >= 0, negative: crypto.percentage_change_24h < 0 }"
                  >
                    <span v-if="crypto.percentage_change_24h !== undefined">{{ crypto.percentage_change_24h.toFixed(2) }}%</span><span v-else>N/A</span>
                  </div>
                </div>
              </div>
            </slide>
          </carousel>
        </div>
        <div v-else>
          <p class="center">No favorite cryptocurrencies in your list at this time.</p>
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
                    <img :src="stock.logoUrl" alt="Logo" v-if="stock.logoUrl"/>
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

      <!-- Hot Cryptos Carousel -->
      <section class="hot-cryptos">
        <h2 class="center">Trending Cryptocurrencies</h2>
        <div v-if="hotCryptos && hotCryptos.length > 0">
          <carousel
              ref="hotCryptosCarousel"
              :items-to-show="itemsToShow"
              :wrap-around="true"
              :mouse-drag="true"
              :touch-drag="true"
              class="stock-carousel"
          >
            <template #addons>
              <button
                  @click="prev('hotCryptosCarousel')"
                  class="carousel-nav-button prev-button"
                  aria-label="Previous"
              >
                <i class="fas fa-chevron-left"></i>
              </button>
              <button
                  @click="next('hotCryptosCarousel')"
                  class="carousel-nav-button next-button"
                  aria-label="Next"
              >
                <i class="fas fa-chevron-right"></i>
              </button>
            </template>

            <slide
                v-for="crypto in hotCryptos"
                :key="crypto.crypto_id"
                class="carousel-slide-item"
            >
              <div class="crypto-card" @click="openCryptoDrawer(crypto.crypto_id)">
                <div class="crypto-card-header">
                  <div class="crypto-card-icon">
                    <img :src="crypto.logoUrl" alt="Logo" v-if="crypto.logoUrl"/>
                    <div v-else class="crypto-initial">{{ crypto.ticker.charAt(0) }}</div>
                  </div>
                  <div class="crypto-card-info">
                    <h3>${{ crypto.ticker }}</h3>
                    <p class="crypto-name">{{ crypto.name }}</p>
                  </div>
                </div>
                <div class="crypto-card-body">
                  <div class="crypto-price">
                    $<span v-if="crypto.price !== undefined">{{ crypto.price.toFixed(2) }}</span><span v-else>N/A</span>
                  </div>
                  <div
                      class="crypto-change"
                      :class="{ positive: crypto.percentage_change_24h >= 0, negative: crypto.percentage_change_24h < 0 }"
                  >
                    <span v-if="crypto.percentage_change_24h !== undefined">{{ crypto.percentage_change_24h.toFixed(2) }}%</span><span v-else>N/A</span>
                  </div>
                </div>
              </div>
            </slide>
          </carousel>
        </div>
        <div v-else>
          <p class="center">No trending cryptocurrencies available at this time.</p>
        </div>
      </section>

      <!-- Watchlist Stocks Carousel -->
      <section class="watchlist-stocks">
        <h2 class="center">Your Stocks Watchlist</h2>
        <div v-if="watchlistStocksData && watchlistStocksData.length > 0">
          <carousel
              ref="watchlistCarousel"
              :items-to-show="itemsToShow"
              :wrap-around="true"
              :mouse-drag="true"
              :touch-drag="true"
              class="stock-carousel"
          >
            <!-- Add navigation buttons here as well -->
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
                    <img :src="stock.logoUrl" alt="Logo" v-if="stock.logoUrl"/>
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

      <!-- Watchlist Cryptos Carousel -->
      <section class="watchlist-cryptos">
        <h2 class="center">Your Cryptocurrency Watchlist</h2>
        <div v-if="watchlistCryptosData && watchlistCryptosData.length > 0">
          <carousel
              ref="watchlistCryptosCarousel"
              :items-to-show="itemsToShow"
              :wrap-around="true"
              :mouse-drag="true"
              :touch-drag="true"
              class="stock-carousel"
          >
            <template #addons>
              <button
                  @click="prev('watchlistCryptosCarousel')"
                  class="carousel-nav-button prev-button"
                  aria-label="Previous"
              >
                <i class="fas fa-chevron-left"></i>
              </button>
              <button
                  @click="next('watchlistCryptosCarousel')"
                  class="carousel-nav-button next-button"
                  aria-label="Next"
              >
                <i class="fas fa-chevron-right"></i>
              </button>
            </template>

            <slide
                v-for="crypto in watchlistCryptosData"
                :key="crypto.crypto_id"
                class="carousel-slide-item"
            >
              <div class="crypto-card" @click="openCryptoDrawer(crypto.crypto_id)">
                <div class="crypto-card-header">
                  <div class="crypto-card-icon">
                    <img :src="crypto.logoUrl" alt="Logo" v-if="crypto.logoUrl"/>
                    <div v-else class="crypto-initial">{{ crypto.ticker.charAt(0) }}</div>
                  </div>
                  <div class="crypto-card-info">
                    <h3>${{ crypto.ticker }}</h3>
                    <p class="crypto-name">{{ crypto.name }}</p>
                  </div>
                </div>
                <div class="crypto-card-body">
                  <div class="crypto-price">
                    $<span v-if="crypto.price !== undefined">{{ crypto.price.toFixed(2) }}</span><span v-else>N/A</span>
                  </div>
                  <div
                      class="crypto-change"
                      :class="{ positive: crypto.percentage_change_24h >= 0, negative: crypto.percentage_change_24h < 0 }"
                  >
                    <span v-if="crypto.percentage_change_24h !== undefined">{{ crypto.percentage_change_24h.toFixed(2) }}%</span><span v-else>N/A</span>
                  </div>
                </div>
              </div>
            </slide>
          </carousel>
        </div>
        <div v-else>
          <p class="center">You have no cryptocurrencies in your watchlist.</p>
        </div>
      </section>
    </div>

    <!-- Stock Drawer Component -->
    <StockDrawer
        v-if="showDrawer"
        :ticker="selectedTicker"
        :isVisible="showDrawer"
        :userFavorites="favoriteStocks"
        :userWatchlist="userWatchlist"
        @close="closeDrawer"
        @update-favorites="addTickerToFavorites"
        @update-watchlist="addTickerToWatchlist"
    />

    <!-- Crypto Drawer Component -->
    <CryptoDrawer
      v-if="showCryptoDrawer && selectedCryptoID"
      :crypto_id="selectedCryptoID"
      :isVisible="showCryptoDrawer"
      :userFavorites="favoriteCryptos"
      :userWatchlist="userCryptoWatchlist"
      @close="closeCryptoDrawer"
      @update-favorites="addCryptoToFavorites"
      @update-watchlist="addCryptoToWatchlist"
    />
  </div>
</template>

<script>
import axios from 'axios';
import {Carousel, Slide} from 'vue3-carousel';
import 'vue3-carousel/dist/carousel.css';
import '@fortawesome/fontawesome-free/css/all.css';
import StockDrawer from '@/components/StockDrawer.vue';
import CryptoDrawer from '@/components/CryptoDrawer.vue';

export default {
  name: 'HomePage',
  components: {
    Carousel,
    Slide,
    StockDrawer,
    CryptoDrawer,
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
      hotCryptos: [],
      favoriteStocks: [],
      favoriteCryptos: [],
      favoriteStocksData: [],
      favoriteCryptosData: [],
      userWatchlist: [],
      userCryptoWatchlist: [],
      watchlistStocksData: [],
      watchlistCryptosData: [],
      showDrawer: false,
      showCryptoDrawer: false,
      selectedTicker: '',
      itemsToShow: 3,
      newsArticles: [],
      loadingNews: false,
      loading: false,
      selectedCryptoID: '',
    };
  },
  methods: {
    fetchUserData() {
      this.loading = true;
      axios
          .get('/api/user')
          .then((response) => {
            const data = response.data;
            this.favoriteStocks = data.favorite_stocks || [];
            this.favoriteCryptos = data.favorite_cryptos || [];
            this.userWatchlist = data.watched_stocks || [];
            this.userCryptoWatchlist = data.watched_cryptos || [];
            this.loadFavoriteStocksData();
            this.loadFavoriteCryptosData();
            this.loadWatchlistStocksData();
            this.loadWatchlistCryptosData();
          })
          .catch((error) => {
            console.error('Error fetching user data:', error);
          })
          .finally(() => {
            this.loading = false;
          });
    },
    fetchHotStocks() {
      axios
          .get('/api/hot_stocks')
          .then((response) => {
            this.hotStocks = response.data.message ? response.data.data || [] : response.data || [];
          })
          .catch((error) => {
            console.error('Error fetching hot stocks:', error);
            alert('Failed to fetch hot stocks. Please try again later.');
          });
    },
    loadFavoriteStocksData() {
      const promises = this.favoriteStocks.map((ticker) =>
          this.fetchStockData(ticker).catch((error) => {
            console.error(`Error fetching data for ${ticker}:`, error);
            return null;
          })
      );
      Promise.all(promises).then((stocksData) => {
        this.favoriteStocksData = stocksData.filter((data) => data !== null);
      });
    },
    loadWatchlistStocksData() {
      const promises = this.userWatchlist.map((ticker) =>
          this.fetchStockData(ticker).catch((error) => {
            console.error(`Error fetching data for ${ticker}:`, error);
            return null;
          })
      );
      Promise.all(promises).then((stocksData) => {
        this.watchlistStocksData = stocksData.filter((data) => data !== null);
      });
    },
    fetchStockData(ticker) {
      return axios.get(`/api/stock_data?ticker=${ticker}`).then((response) => {
        const data = response.data;
        data.name = data.name || 'Company Name';
        data.logoUrl = data.logoUrl || '';
        return data;
      });
    },
    fetchStockNews() {
      this.loadingNews = true;
      axios
          .get('/api/news', {params: {query: 'stock market'}})
          .then((response) => {
            this.newsArticles = response.data.articles || [];
          })
          .catch((error) => {
            console.error('Error fetching news:', error);
          })
          .finally(() => {
            this.loadingNews = false;
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
      this.itemsToShow = width >= 1024 ? 3 : width >= 768 ? 2 : 1;
    },
    prev(carouselRef) {
      this.$refs[carouselRef].prev();
    },
    next(carouselRef) {
      this.$refs[carouselRef].next();
    },
    fetchHotCryptos() {
      axios
        .get('/api/hot_crypto')
        .then((response) => {
          this.hotCryptos = response.data;
        })
        .catch((error) => {
          console.error('Error fetching hot cryptos:', error);
        });
    },
    loadFavoriteCryptosData() {
      const promises = this.favoriteCryptos.map((crypto_id) =>
        this.fetchCryptoData(crypto_id).catch((error) => {
          console.error(`Error fetching data for ${crypto_id}:`, error);
          return null;
        })
      );
      Promise.all(promises).then((cryptosData) => {
        this.favoriteCryptosData = cryptosData.filter((data) => data !== null);
      });
    },
    loadWatchlistCryptosData() {
      const promises = this.userCryptoWatchlist.map((crypto_id) =>
        this.fetchCryptoData(crypto_id).catch((error) => {
          console.error(`Error fetching data for ${crypto_id}:`, error);
          return null;
        })
      );
      Promise.all(promises).then((cryptosData) => {
        this.watchlistCryptosData = cryptosData.filter((data) => data !== null);
      });
    },
    fetchCryptoData(crypto_id) {
      return axios.get(`/api/crypto_data?crypto_id=${crypto_id}`).then((response) => {
        const data = response.data;
        data.name = data.name || 'Crypto Name';
        data.logoUrl = data.logoUrl || '';
        return data;
      });
    },
    openCryptoDrawer(cryptoID) {
      console.log(cryptoID)
      this.selectedCryptoID = cryptoID;
      this.showCryptoDrawer = true;
    },
    closeCryptoDrawer() {
      this.showCryptoDrawer = false;
    },
    addCryptoToFavorites(crypto_id) {
      if (!this.favoriteCryptos.includes(crypto_id)) {
        this.favoriteCryptos.push(crypto_id);
        this.loadFavoriteCryptosData();
      }
    },
    addCryptoToWatchlist(crypto_id) {
      if (!this.userCryptoWatchlist.includes(crypto_id)) {
        this.userCryptoWatchlist.push(crypto_id);
        this.loadWatchlistCryptosData();
      }
    },
  },
  mounted() {
    this.fetchUserData();
    this.fetchHotStocks();
    this.fetchHotCryptos();
    this.fetchStockNews();
    this.updateItemsToShow();
    window.addEventListener('resize', this.updateItemsToShow);
  },
  beforeUnmount() {
    window.removeEventListener('resize', this.updateItemsToShow);
  },
};
</script>
