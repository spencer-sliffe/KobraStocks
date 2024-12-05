<!-- Prologue
Component Name: PortfolioPage
Path: src/views/PortfolioPage.vue

Description:
Provides the "Portfolio" section for the KobraStocks application.

Collaborators: Spencer Sliffe
-->

<!-- PortfolioPage.vue -->
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
    <div class="portfolio-analysis">
      <h3>Analysis</h3>
      <div v-if="loadingAnalysis" class="loading-container">
        <div class="spinner"></div>
        <p>Loading analysis...</p>
      </div>
      <div v-else>
        <div class="analysis-card" v-for="(response, index) in portfolioAnalysis.chat_responses" :key="index">
          <p>{{ response }}</p>
        </div>
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
        <label for="num_shares">Number of Shares:</label>
        <input type="number" id="num_shares" v-model.number="newStock.num_shares" min="1" step="1" required />
      </div>

      <div class="form-group">
        <label for="purchase_date">Purchase Date and Time:</label>
        <input type="datetime-local" id="purchase_date" v-model="newStock.purchase_date" />
      </div>

      <button type="submit">Add to Portfolio</button>
    </form>

    <!-- Portfolio Stocks Table -->
    <div v-if="portfolioStocks.length > 0" class="stocks-table">
      <!-- Manual Refresh Button -->
      <table>
        <thead>
          <tr>
            <th>Ticker</th>
            <th>Name</th>
            <th>Number of Shares</th>
            <th>Price per Share (at Purchase)</th>
            <th>Total Invested (Purchase Price x Shares)</th>
            <th>Current Value (Current Price x Shares)</th>
            <th>Profit/Loss (Current Value - Total Invested)</th>
            <th>Profit/Loss (%)</th>
            <th>Current Price</th>
            <th>Change Since Yesterday (%)</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="stock in portfolioStocks" :key="stock.ticker">
            <td>{{ stock.ticker }}</td>
            <td>{{ stock.name }}</td>
            <td>{{ stock.number_of_shares }}</td>
            <td>${{ stock.pps_at_purchase.toFixed(2) }}</td>
            <td>${{ stock.total_invested.toFixed(2) }}</td>
            <td>${{ stock.current_value.toFixed(2) }}</td>
            <td :class="{'positive': stock.profit_loss >= 0, 'negative': stock.profit_loss < 0}">
              ${{ stock.profit_loss.toFixed(2) }}
            </td>
            <td :class="{'positive': stock.profit_loss_percentage >= 0, 'negative': stock.profit_loss_percentage < 0}">
              {{ stock.profit_loss_percentage.toFixed(2) }}%
            </td>
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
        num_shares: null,
        purchase_date: '', 
      },
      portfolioStocks: [],
      portfolioMetrics: null,
      portfolioAnalysis: null,
      loading: false,
      error: null,
      loadingAnalysis: false, // Added loadingAnalysis
      refreshInterval: null,
    };
  },
  created() {
    this.fetchPortfolio();
    // Set up auto-refresh every 60 seconds
    this.refreshInterval = setInterval(() => {
      this.fetchPortfolio();
    }, 60000); // 60000 milliseconds = 60 seconds
  },
  beforeUnmount() {
    // Clear the interval when the component is destroyed
    if (this.refreshInterval) {
      clearInterval(this.refreshInterval);
    }
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
      this.loadingAnalysis = true;
      axios
        .get('/api/portfolio/analysis')
        .then((response) => {
          this.portfolioMetrics = response.data.metrics;
          this.portfolioAnalysis = response.data.analysis;
        })
        .catch((error) => {
          console.error('Error fetching portfolio analysis:', error);
          this.error = 'Failed to load portfolio analysis.';
        })
        .finally(() => {
          this.loadingAnalysis = false;
        });
    },
    addStock() {
      const payload = {
        ticker: this.newStock.ticker.trim().toUpperCase(),
        num_shares: this.newStock.num_shares,
        purchase_date: this.newStock.purchase_date || null, // Include purchase_date
      };
      axios
        .post('/api/portfolio', payload)
        .then((response) => {
          console.log(response.data.message);
          // Reset form fields
          this.newStock.ticker = '';
          this.newStock.num_shares = null;
          this.newStock.purchase_date = ''; // Reset purchase_date
          this.fetchPortfolio();
        })
        .catch((error) => {
          console.error('Error adding stock:', error);
          alert(error.response.data.message || 'Failed to add stock to portfolio.');
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
