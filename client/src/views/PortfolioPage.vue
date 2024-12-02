<!-- Prologue
Component Name: PortfolioPage
Path: src/views/PortfolioPage.vue

Description:
Provides the "Portfolio" section for the KobraStocks application.

Collaborators: Spencer Sliffe
-->

<!-- PortfolioPage.vue -->
<template>
  <div class="portfolio-page">
    <h2>My Portfolio</h2>

    <!-- Portfolio Metrics -->
    <div class="portfolio-metrics" v-if="portfolioMetrics">
      <div class="metric-card">
        <h3>Expected Return</h3>
        <p>{{ (portfolioMetrics.expected_return * 100).toFixed(2) }}%</p>
      </div>
      <div class="metric-card">
        <h3>Risk</h3>
        <p>{{ (portfolioMetrics.risk * 100).toFixed(2) }}%</p>
      </div>
      <div class="metric-card">
        <h3>Sharpe Ratio</h3>
        <p>{{ portfolioMetrics.sharpe_ratio.toFixed(2) }}</p>
      </div>
      <div class="metric-card">
        <h3>Diversification Ratio</h3>
        <p>{{ portfolioMetrics.diversification_ratio.toFixed(2) }}</p>
      </div>
    </div>

    <!-- Portfolio Analysis -->
    <div class="portfolio-analysis" v-if="portfolioAnalysis">
      <h3>Analysis</h3>
      <div class="analysis-card" v-for="(response, index) in portfolioAnalysis.chat_responses" :key="index">
        <p>{{ response }}</p>
      </div>
    </div>

    <!-- Add Stock Form -->
    <form @submit.prevent="addStock" class="add-stock-form">
      <h3>Add a Stock</h3>
      <div class="form-group">
        <label for="ticker">Stock Ticker:</label>
        <input type="text" id="ticker" v-model="newStock.ticker" required />
      </div>

      <div class="form-group">
        <label for="amount">Amount Invested ($):</label>
        <input type="number" id="amount" v-model.number="newStock.amount_invested" min="0" step="0.01" required />
      </div>

      <button type="submit">Add to Portfolio</button>
    </form>

    <!-- Portfolio Stocks Table -->
    <div v-if="portfolioStocks.length > 0" class="stocks-table">
      <table>
        <thead>
          <tr>
            <th>Ticker</th>
            <th>Name</th>
            <th>Amount Invested</th>
            <th>Current Price</th>
            <th>Change (%)</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="stock in portfolioStocks" :key="stock.ticker">
            <td>{{ stock.ticker }}</td>
            <td>{{ stock.name }}</td>
            <td>${{ stock.amount_invested.toFixed(2) }}</td>
            <td>${{ stock.close_price.toFixed(2) }}</td>
            <td :class="{'positive': stock.percentage_change >= 0, 'negative': stock.percentage_change < 0}">
              {{ stock.percentage_change.toFixed(2) }}%
            </td>
            <td>
              <button class="secondary-button" @click="removeStock(stock.ticker)">Remove</button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
    <p v-else>Your portfolio is empty. Start by adding some stocks!</p>

    <!-- Loading and Error Messages -->
    <div v-if="loading" class="loading-container">
      <div class="spinner"></div>
      <p>Loading portfolio...</p>
    </div>
    <p v-if="error" class="error-message">{{ error }}</p>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'PortfolioPage',
  data() {
    return {
      newStock: {
        ticker: '',
        amount_invested: null,
      },
      portfolioStocks: [],
      portfolioMetrics: null,
      portfolioAnalysis: null,
      loading: false,
      error: null,
    };
  },
  created() {
    this.fetchPortfolio();
  },
  methods: {
    fetchPortfolio() {
      this.loading = true;
      axios
        .get('/api/portfolio')
        .then((response) => {
          this.portfolioStocks = response.data.stocks;
          // Fetch portfolio analysis after loading stocks
          if (this.portfolioStocks.length > 0) {
            this.fetchPortfolioAnalysis();
          } else {
            this.portfolioMetrics = null;
            this.portfolioAnalysis = null;
          }
        })
        .catch((error) => {
          console.error('Error fetching portfolio:', error);
          this.error = 'Failed to load portfolio.';
        })
        .finally(() => {
          this.loading = false;
        });
    },
    fetchPortfolioAnalysis() {
      axios
        .get('/api/portfolio/analysis')
        .then((response) => {
          this.portfolioMetrics = response.data.metrics;
          this.portfolioAnalysis = response.data.analysis;
        })
        .catch((error) => {
          console.error('Error fetching portfolio analysis:', error);
          this.error = 'Failed to load portfolio analysis.';
        });
    },
    addStock() {
      const payload = {
        ticker: this.newStock.ticker.trim().toUpperCase(),
        amount_invested: this.newStock.amount_invested,
      };
      axios
        .post('/api/portfolio', payload)
        .then((response) => {
          console.log(response.data.message);
          this.newStock.ticker = '';
          this.newStock.amount_invested = null;
          this.fetchPortfolio();
        })
        .catch((error) => {
          console.error('Error adding stock:', error);
          alert('Failed to add stock to portfolio.');
        });
    },
    removeStock(ticker) {
      axios
        .delete(`/api/portfolio/${ticker}`)
        .then((response) => {
          console.log(response.data.message);
          this.fetchPortfolio();
        })
        .catch((error) => {
          console.error('Error removing stock:', error);
          alert('Failed to remove stock from portfolio.');
        });
    },
  },
};
</script>
