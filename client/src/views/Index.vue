<template>
  <div>
    <h1>KobraStocks</h1>
    <div>
      <input v-model="ticker" placeholder="Search for stocks..." />
      <button @click="fetchStockData">Search</button>
    </div>
    <div v-if="stockData">
      <h2>Stock Data for {{ ticker }}</h2>
      <p>Price: {{ stockData.Close }}</p>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      ticker: 'AAPL',
      stockData: null
    };
  },
  methods: {
    fetchStockData() {
      axios.get(`http://localhost:5000/api/stock_data?ticker=${this.ticker}`)
        .then(response => {
          this.stockData = response.data;
        });
    }
  }
};
</script>
