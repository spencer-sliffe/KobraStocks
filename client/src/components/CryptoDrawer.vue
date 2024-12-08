<!-- Prologue
Component Name: CryptoDrawer
Path: src/components/CryptoDrawer.vue

Description:
Displays detailed crypto information in a sliding drawer, allowing users to view crypto prices, volume, and add cryptos to their favorites or watchlist.
-->

<template>
  <transition name="slide">
    <div class="crypto-drawer" v-if="isVisible">
      <div class="drawer-header">
        <div class="link-button">
          <h2 @click="navigateToCryptoPage">
            ${{ cryptoData.ticker || 'N/A' }}
          </h2>
          <p v-if="cryptoData.name" class="company-name">{{ cryptoData.name }}</p>
        </div>
        <button @click="closeDrawer">Close</button>
      </div>

      <div class="drawer-content">
        <!-- Loading State -->
        <div v-if="isLoading">
          <p>Loading crypto data...</p>
        </div>

        <!-- Crypto Data -->
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

          <button @click="addToFavorites(cryptoData.crypto_id, cryptoData.ticker)" :disabled="isInFavorites">
            {{ isInFavorites ? 'In Favorites' : 'Add to Favorites' }}
          </button>
          <button @click="addToWatchlist(cryptoData.crypto_id, cryptoData.ticker)" :disabled="isInWatchlist">
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
    crypto_id: {
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
        crypto_id: "",
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
      return this.userFavorites.includes(this.crypto_id);
    },
    isInWatchlist() {
      return this.userWatchlist.includes(this.crypto_id);
    },
  },
  watch: {
    crypto_id: {
      immediate: true,
      handler(newVal) {
        if (newVal) {
          this.fetchCryptoData(newVal);
        }
      },
    },
    isVisible(newVal) {
      if (!newVal) {
        this.resetCryptoData();
      }
    },
  },
  methods: {
    navigateToCryptoPage() {
      const params = { crypto_id: this.cryptoData.crypto_id };
      this.$router.push({ name: "CryptoResults", query: params }).catch((err) => {
        if (err.name !== "NavigationDuplicated") {
          console.error("Navigation error:", err);
        }
      });
    },
    async fetchCryptoData(crypto_id) {
      this.isLoading = true;
      try {
        const response = await axios.get(`/api/crypto_data?crypto_id=${crypto_id}`);
        const data = response.data;

        this.cryptoData = {
          crypto_id: data.crypto_id || crypto_id,
          ticker: data.ticker || 'N/A',
          name: data.name || 'N/A',
          price: data.price,
          market_cap: data.market_cap,
          percentage_change_24h: data.percentage_change_24h,
          volume: data.volume,
        };
      } catch (error) {
        console.error("Error fetching crypto data:", error);
        alert("Failed to fetch crypto data. Please try again.");
      } finally {
        this.isLoading = false;
      }
    },
    async addToFavorites(crypto_id, ticker) {
      try {
        await axios.post("/api/crypto_favorites", { crypto_id, ticker});
        alert(`${crypto_id} added to favorites.`);
        this.$emit("update-favorites", crypto_id);
      } catch (error) {
        console.error("Error adding to favorites:", error);
        alert("Failed to add to favorites. Please try again.");
      }
    },
    async addToWatchlist(crypto_id, ticker) {
      try {
        await axios.post("/api/crypto_watchlist", { crypto_id, ticker });
        alert(`${crypto_id} added to watchlist.`);
        this.$emit("update-watchlist", crypto_id);
      } catch (error) {
        console.error("Error adding to watchlist:", error);
        alert("Failed to add to watchlist. Please try again.");
      }
    },
    closeDrawer() {
      this.$emit("close");
    },
    resetCryptoData() {
      this.cryptoData = {
        crypto_id: "",
        ticker: "",
        name: "",
        price: undefined,
        market_cap: undefined,
        percentage_change_24h: undefined,
        volume: undefined,
      };
      this.isLoading = false;
    }
  },
};
</script>


