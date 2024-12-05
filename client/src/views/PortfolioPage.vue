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

    <!-- Actions Section: Add Stock Form and Stocks Table at the top -->
    <div class="portfolio-actions">
      <!-- Add Stock Form -->
      <div class="add-stock-column">
        <form @submit.prevent="addStock" class="add-stock-form">
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
      </div>

      <!-- Portfolio Stocks Table -->
      <div class="stocks-column" v-if="portfolioStocks.length > 0">
        <div class="stocks-table">
          <table>
            <thead>
              <tr>
                <th>Ticker</th>
                <th>Name</th>
                <th>Shares</th>
                <th>Price/Share</th>
                <th>Invested</th>
                <th>Value</th>
                <th>Profit/Loss</th>
                <th>Profit/Loss(%)</th>
                <th>Price(now)</th>
                <th>Change(24h%)</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="stock in portfolioStocks" :key="stock.ticker">
                <td>{{ stock.ticker }}</td>
                <td>{{ stock.name.substring(0, 15) }}</td>
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
                  <button class="secondary-button" @click="analyzeStock(stock.ticker)">Analyze</button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
      <div class="stocks-column" v-else>
        <p>Your portfolio is empty. Start by adding some stocks!</p>
      </div>
    </div>

    <!-- Stock Chart Row (If you have a chart to show, place it here) -->
    <div class="chart-container" v-if="showChart">
      <!-- Insert your chart component or code here -->
      <!-- e.g., <chart-component :data="chartData" /> -->
    </div>

    <!-- Stock Analysis (Individual Stock) -->
    <div class="stock-analysis">
      <div v-if="loadingStockAnalysis" class="loading-container">
        <div class="spinner"></div>
        <p>Loading stock analysis...</p>
      </div>
      <div class="analysis-card" v-else-if="stockAnalysis">
        <h3 class="center">Stock Analysis</h3>
        <p>{{ stockAnalysis }}</p>
      </div>
    </div>
    <h3 class="center">Portfolio Analysis</h3>

    <!-- Portfolio Overview (Metrics + Portfolio Analysis) now below everything else -->
    <div class="portfolio-overview">
      <!-- Portfolio Metrics -->
      <div class="metrics-container" v-if="portfolioMetrics">
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
      <div class="analysis-container">
        <div v-if="loadingAnalysis" class="loading-container">
          <div class="spinner"></div>
          <p>Loading analysis...</p>
        </div>
        <div v-else-if="portfolioAnalysis && portfolioAnalysis.chat_responses && portfolioAnalysis.chat_responses.length">
          <div class="analysis-card" v-for="(response, index) in portfolioAnalysis.chat_responses" :key="index">
            <p>{{ response }}</p>
          </div>
        </div>
        <div v-else>
          <p>No analysis available.</p>
        </div>
      </div>
    </div>

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
      loadingAnalysis: false,
      refreshInterval: null,
      stockAnalysis: null,
      loadingStockAnalysis: false,
      showChart: false, // Toggle this if you have a chart to display
    };
  },
  created() {
    this.fetchPortfolio();
    // Set up auto-refresh every 60 seconds
    this.refreshInterval = setInterval(() => {
      this.fetchStocks();
    }, 60000);
  },
  beforeUnmount() {
    if (this.refreshInterval) {
      clearInterval(this.refreshInterval);
    }
  },
  methods: {
    fetchStocks() {
      axios.get('/api/portfolio')
        .then((response) => {
          this.portfolioStocks = response.data.stocks;
        })
        .catch((error) => console.error('Error fetching stocks:', error));
    },
    fetchPortfolio() {
      this.loading = true;
      axios.get('/api/portfolio')
        .then((response) => {
          this.portfolioStocks = response.data.stocks;
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
      axios.get('/api/portfolio/analysis')
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
        purchase_date: this.newStock.purchase_date || null,
      };
      axios.post('/api/portfolio', payload)
        .then((response) => {
          console.log(response.data.message);
          this.newStock.ticker = '';
          this.newStock.num_shares = null;
          this.newStock.purchase_date = '';
          this.fetchPortfolio();
        })
        .catch((error) => {
          console.error('Error adding stock:', error);
          alert(error.response.data.message || 'Failed to add stock to portfolio.');
        });
    },
    removeStock(ticker) {
      axios.delete(`/api/portfolio/${ticker}`)
        .then((response) => {
          console.log(response.data.message);
          this.fetchPortfolio();
        })
        .catch((error) => {
          console.error('Error removing stock:', error);
          alert('Failed to remove stock from portfolio.');
        });
    },
    analyzeStock(ticker) {
      this.loadingStockAnalysis = true;
      this.stockAnalysis = null;

      // Find the user's stock data for the specified ticker
      const userStockData = this.portfolioStocks.find(
        s => s.ticker.toLowerCase() === ticker.toLowerCase()
      );

      if (!userStockData) {
        alert('User stock data not found for the selected ticker.');
        this.loadingStockAnalysis = false;
        return;
      }

      // Pass user-specific data as query parameters
      axios.get(`/api/stocks/${ticker}/analysis`, {
          params: {
            user_shares: userStockData.number_of_shares,
            user_pps_at_purchase: userStockData.pps_at_purchase,
            user_total_invested: userStockData.total_invested,
            user_current_value: userStockData.current_value,
            user_profit_loss: userStockData.profit_loss,
            user_profit_loss_percentage: userStockData.profit_loss_percentage
          }
        })
        .then((response) => {
          this.stockAnalysis = response.data.analysis;
        })
        .catch((error) => {
          console.error('Error fetching stock analysis:', error);
          alert('Failed to load stock analysis.');
        })
        .finally(() => {
          this.loadingStockAnalysis = false;
        });
    },
  },
};
</script>

