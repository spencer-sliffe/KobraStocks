<!-- Prologue
Component Name: PortfolioPage
Path: src/views/PortfolioPage.vue

Description:
Provides the "Portfolio" section for the KobraStocks application.

Collaborators: Spencer Sliffe
-->

<template>
  <div class="main-content">
    <h2>My Portfolio</h2>

    <!-- Add Stock Form -->
    <form @submit.prevent="addStock">
      <label for="ticker">Stock Ticker:</label>
      <input type="text" id="ticker" v-model="newStock.ticker" required />

      <label for="amount">Amount Invested ($):</label>
      <input type="number" id="amount" v-model.number="newStock.amount_invested" min="0" step="0.01" required />

      <button type="submit">Add to Portfolio</button>
    </form>

    <!-- Portfolio Stocks Table -->
    <table v-if="portfolioStocks.length > 0">
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
            <button @click="removeStock(stock.ticker)">Remove</button>
          </td>
        </tr>
      </tbody>
    </table>
    <p v-else>Your portfolio is empty. Start by adding some stocks!</p>
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
        })
        .catch((error) => {
          console.error('Error fetching portfolio:', error);
          this.error = 'Failed to load portfolio.';
        })
        .finally(() => {
          this.loading = false;
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
          this.fetchPortfolio();
          this.newStock.ticker = '';
          this.newStock.amount_invested = null;
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

<style scoped>
.main-content {
  max-width: var(--max-width);
  margin: 0 auto;
}

form {
  margin-bottom: var(--spacing-lg);
}

form label {
  display: block;
  margin-top: var(--spacing-md);
}

form input {
  width: 100%;
  padding: var(--spacing-sm);
  margin-top: var(--spacing-xs);
}

table {
  width: 100%;
  border-collapse: collapse;
  margin-top: var(--spacing-lg);
}

table th,
table td {
  padding: var(--spacing-sm);
  text-align: left;
  border-bottom: 1px solid #e0e0e0;
}

table th {
  background-color: var(--color-background);
  font-weight: 600;
}

.positive {
  color: var(--color-success);
}

.negative {
  color: var(--color-danger);
}

button {
  margin-top: var(--spacing-md);
}

</style>
