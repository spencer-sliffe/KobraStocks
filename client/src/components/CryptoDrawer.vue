<!-- Prologue
Component Name: CryptoDrawer
Path: src/components/CryptoDrawer.vue

Description:
Displays detailed crypto information in a sliding drawer, allowing users to view crypto prices, volume, and add cryptos to their favorites or watchlist.
-->

<template>
  <transition name="slide">
    <div class="stock-drawer" v-if="isVisible">
      <div class="drawer-header">
        <div class="link-button">
          <h2 @click="navigateToCryptoPage">
            ${{ cryptoData.ticker }}
          </h2>
          <p v-if="cryptoData.name" class="company-name">{{ cryptoData.name }}</p>
        </div>
        <button @click="closeDrawer">Close</button>
      </div>
      <div class="drawer-content">
        <div v-if="isLoading">
          <p>Loading crypto data...</p>
        </div>
        <div v-else>
          <p v-if="cryptoData.price !== undefined">
            Price: ${{ cryptoData.price.toFixed(2) }}
          </p>
          <p v-else>
            Price: Data not available
          </p>
          <p v-if="cryptoData.market_cap !== undefined">
            Market Cap: ${{ cryptoData.market_cap.toLocaleString() }}
          </p>
          <p v-else>
            Market Cap: Data not available
          </p>
          <p v-if="cryptoData.percentage_change_24h !== undefined">
            24h Change: {{ cryptoData.percentage_change_24h.toFixed(2) }}%
          </p>
          <p v-else>
            24h Change: Data not available
          </p>
          <p v-if="cryptoData.volume !== undefined">
            Volume: ${{ cryptoData.volume.toLocaleString() }}
          </p>
          <p v-else>
            Volume: Data not available
          </p>
          <button @click="addToFavorites(cryptoData.ticker)" :disabled="isInFavorites">
            {{ isInFavorites ? 'In Favorites' : 'Add to Favorites' }}
          </button>
          <button @click="addToWatchlist(cryptoData.ticker)" :disabled="isInWatchlist">
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
  name: "CryptoDrawer",
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
      cryptoData: {
        ticker: "",
        name: "",
        price: undefined,
        market_cap: undefined,
        percentage_change_24h: undefined,
        volume: undefined,
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
          this.fetchCryptoData(newVal);
        }
      },
    },
    isVisible(newVal) {
      if (!newVal) {
        this.cryptoData = {
          ticker: "",
          name: "",
          price: undefined,
          market_cap: undefined,
          percentage_change_24h: undefined,
          volume: undefined,
        };
      }
    },
  },
  methods: {
    navigateToCryptoPage() {
      const params = {
        ticker: this.cryptoData.ticker.trim().toUpperCase(),
      };

      this.$router.push({ name: "CryptoResults", query: params }).catch((err) => {
        if (err.name !== "NavigationDuplicated") {
          console.error("Navigation error:", err);
        }
      });
    },
    fetchCryptoData(ticker) {
      this.isLoading = true;
      axios
        .get(`/api/crypto_data?ticker=${ticker}`)
        .then((response) => {
          const data = response.data;
          this.cryptoData = {
            ticker: data.ticker || ticker,
            name: data.name || "N/A",
            price: data.price,
            market_cap: data.market_cap,
            percentage_change_24h: data.percentage_change_24h,
            volume: data.volume,
          };
          this.isLoading = false;
        })
        .catch((error) => {
          console.error("Error fetching crypto data:", error);
          this.isLoading = false;
          this.closeDrawer();
          alert("Failed to fetch crypto data. Please try again later.");
        });
    },
    addToFavorites(ticker) {
      axios
        .post("/api/crypto_favorites", { ticker })
        .then(() => {
          alert(`${ticker} added to favorites.`);
          this.$emit("update-favorites", ticker);
        })
        .catch((error) => {
          console.error("Error adding to favorites:", error);
          alert("Failed to add to favorites. Please try again.");
        });
    },
    addToWatchlist(ticker) {
      axios
        .post("/api/crypto_watchlist", { ticker })
        .then(() => {
          alert(`${ticker} added to watchlist.`);
          this.$emit("update-watchlist", ticker);
        })
        .catch((error) => {
          console.error("Error adding to watchlist:", error);
          alert("Failed to add to watchlist. Please try again.");
        });
    },
    closeDrawer() {
      this.$emit("close");
    },
  },
};
</script>
