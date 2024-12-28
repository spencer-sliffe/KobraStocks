<template>
  <div class="crypto-results">
    <h1 class="center">Crypto Details for {{ ticker }}</h1>
    <h2 class="center">{{ cryptoTitle }}</h2>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "CryptoResultsPage",
  data() {
    return {
      ticker: "",
      cryptoTitle: "Loading...",
    };
  },
  methods: {
    fetchCryptoTitle() {
      axios
        .get(`/api/crypto_data?ticker=${this.ticker}`)
        .then((response) => {
          const data = response.data;
          this.cryptoTitle = data.name || "N/A";
        })
        .catch((error) => {
          console.error("Error fetching crypto data:", error);
          this.cryptoTitle = "Error fetching data";
        });
    },
  },
  watch: {
    "$route.query": {
      immediate: true,
      handler() {
        this.ticker = this.$route.query.ticker || "BTC";
        this.fetchCryptoTitle();
      },
    },
  },
};
</script>
