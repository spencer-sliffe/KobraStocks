<!-- Prologue
Component Name: ResultsPage
Path: src/views/ResultsPage.vue

Description:
Displays detailed stock information, a stock chart, and machine learning predictions for future stock performance based on user-selected indicators.
-->

<template>
  <div class="results-page">
    <h1 class="page-title">Stock Chart for {{ name }} (${{ ticker }})</h1>
    <div class="layout-grid">
      <!-- LEFT SIDEBAR -->
      <aside class="sidebar left-sidebar">
        <div class="card">
          <h2 class="card-title">Key Metrics</h2>
          <ul class="metrics-list">
            <li><strong>Market Cap:</strong> {{ market_cap }}</li>
            <li><strong>Short Ratio:</strong> {{ short_ratio }}</li>
            <li><strong>Dividend Yield:</strong> {{ dividend_yield }}</li>
            <li><strong>50-Day Avg:</strong> {{ fifty_day_average }}</li>
            <li><strong>200-Day Avg:</strong> {{ two_hundred_day_average }}</li>
            <li><strong>Earnings Date:</strong> {{ earnings_date }}</li>
            <li><strong>Forward PE:</strong> {{ forward_pe }}</li>
            <li><strong>Beta:</strong> {{ beta }}</li>
            <li><strong>Open:</strong> {{ open }}</li>
            <li><strong>Close:</strong> {{ previous_close }}</li>
            <li><strong>High:</strong> {{ day_high }}</li>
            <li><strong>Low:</strong> {{ day_low }}</li>
            <li><strong>Volume:</strong> {{ volume }}</li>
            <li><strong>Cash Per Share:</strong> {{ cash_per_share }}</li>
            <li><strong>Currency:</strong> {{ currency }}</li>
            <li><strong>Price:</strong> {{ price }}</li>
            <li><strong>52-Week High:</strong> {{ fifty_two_week_high }}</li>
            <li><strong>52-Week Low:</strong> {{ fifty_two_week_low }}</li>
          </ul>
        </div>
      </aside>

      <!-- CENTER COLUMN (MAIN CONTENT) -->
      <main class="main-content">
        <!-- Stock Chart -->
        <div class="chart-container" ref="chart"></div>
        <!-- Today's Stats -->
        <div class="card">
          <h2 class="center">Stock Stats</h2>
          <div class="stats-grid">
            <div><strong>Book Value:</strong> {{ book_value }}</div>
            <div><strong>Date Short Interest:</strong> {{ date_short_interest }}</div>
            <div><strong>Debt To Equity:</strong> {{ debt_to_equity }}</div>
            <div><strong>Earnings Growth:</strong> {{ earnings_growth }}</div>
            <div><strong>Earnings Quarterly Growth:</strong> {{ earnings_quarterly_growth }}</div>
            <div><strong>EBITDA:</strong> {{ ebitda }}</div>
            <div><strong>EBITDA Margins:</strong> {{ ebitda_margins }}</div>
            <div><strong>Enterprise Value:</strong> {{ enterprise_value }}</div>
            <div><strong>Exchange:</strong> {{ exchange }}</div>
            <div><strong>Financial Currency:</strong> {{ financial_currency }}</div>
            <div><strong>Float Shares:</strong> {{ float_shares }}</div>
            <div><strong>Free Cashflow:</strong> {{ free_cashflow }}</div>
            <div><strong>Gross Margins:</strong> {{ gross_margins }}</div>
            <div><strong>Gross Profit:</strong> {{ gross_profit }}</div>
            <div><strong>Held Percent Insiders:</strong> {{ held_percent_insiders }}</div>
            <div><strong>Held Percent Institutions:</strong> {{ held_percent_institutions }}</div>
            <div><strong>Implied Shares Outstanding:</strong> {{ implied_shares_outstanding }}</div>
            <div><strong>Last Fiscal Year End:</strong> {{ last_fiscal_year_end }}</div>
            <div><strong>Last Split Date:</strong> {{ last_split_date }}</div>
            <div><strong>Last Split Factor:</strong> {{ last_split_factor }}</div>
            <div><strong>Market Cap:</strong> {{ market_cap }}</div>
            <div><strong>Most Recent Quarter:</strong> {{ most_recent_quarter }}</div>
            <div><strong>Next Fiscal Year End:</strong> {{ next_fiscal_year_end }}</div>
            <div><strong>Number of Analyst Opinions:</strong> {{ number_of_analyst_opinions }}</div>
            <div><strong>Operating Cashflow:</strong> {{ operating_cashflow }}</div>
            <div><strong>Operating Margins:</strong> {{ operating_margins }}</div>
            <div><strong>Price To Book:</strong> {{ price_to_book }}</div>
            <div><strong>Profit Margins:</strong> {{ profit_margins }}</div>
            <div><strong>Recommendation Key:</strong> {{ recommendation_key }}</div>
            <div><strong>Recommendation Mean:</strong> {{ recommendation_mean }}</div>
            <div><strong>Regular Market Price:</strong> {{ regular_market_price }}</div>
            <div><strong>Regular Market Volume:</strong> {{ regular_market_volume }}</div>
            <div><strong>Return On Assets:</strong> {{ return_on_assets }}</div>
            <div><strong>Return On Equity:</strong> {{ return_on_equity }}</div>
            <div><strong>Revenue:</strong> {{ revenue }}</div>
            <div><strong>Revenue Growth:</strong> {{ revenue_growth }}</div>
            <div><strong>Revenue Per Share:</strong> {{ revenue_per_share }}</div>
            <div><strong>Shares Outstanding:</strong> {{ shares_outstanding }}</div>
            <div><strong>Shares Short:</strong> {{ shares_short }}</div>
            <div><strong>Shares Short Prior Month:</strong> {{ shares_short_prior_month }}</div>
            <div><strong>Short Percent of Float:</strong> {{ short_percent_of_float }}</div>
            <div><strong>Target High Price:</strong> {{ target_high_price }}</div>
            <div><strong>Target Low Price:</strong> {{ target_low_price }}</div>
            <div><strong>Target Mean Price:</strong> {{ target_mean_price }}</div>
            <div><strong>Target Median Price:</strong> {{ target_median_price }}</div>
            <div><strong>Total Cash:</strong> {{ total_cash }}</div>
            <div><strong>Total Debt:</strong> {{ total_debt }}</div>
            <div><strong>Trailing PE:</strong> {{ trailing_pe }}</div>
          </div>
        </div>
        <br>
        <!-- ML Predictions -->
        <div class="card">
          <h2 class="card-title center">ML Predictions</h2>
          <div v-if="loadingPredictions" class="loading-container">
            <div class="spinner"></div>
            <p>Loading predictions...</p>
          </div>
          <div v-else class="predictions-grid">
            <div>
              <h3>Tomorrow</h3>
              <p>{{ dprediction }} | Accuracy: {{ daccuracy }} | Price: {{ dprice_change }}</p>
            </div>
            <div>
              <h3>Next Week</h3>
              <p>{{ wprediction }} | Accuracy: {{ waccuracy }} | Price: {{ wprice_change }}</p>
            </div>
            <div>
              <h3>Next Month</h3>
              <p>{{ mprediction }} | Accuracy: {{ maccuracy }} | Price: {{ mprice_change }}</p>
            </div>
          </div>
        </div>

        <!-- ChatGPT Stock Analysis -->
        <div class="card stock-analysis">
          <h2 class="card-title center">Stock Analysis</h2>
          <div v-if="analysisLoading" class="loading-container">
            <div class="spinner"></div>
            <p>Loading stock analysis...</p>
          </div>
          <div v-else-if="analysisError">
            <p class="error-text">{{ analysisError }}</p>
          </div>
          <div v-else-if="analysis" class="analysis-card">
            <div v-html="formatAnalysis(analysis)"></div>
          </div>
          <div v-else>
            <p>No analysis available at this time.</p>
          </div>
        </div>
      </main>

      <!-- RIGHT SIDEBAR -->
      <aside class="sidebar right-sidebar">
        <div class="card">
          <h2 class="card-title">Company Information</h2>
          <p><strong>Industry:</strong> {{ industry }}</p>
          <p><strong>Sector:</strong> {{ sector }}</p>
          <p><strong>Address:</strong> {{ address }}</p>
          <p><strong>Website:</strong> <a :href="website" target="_blank">{{ website }}</a></p>
        </div>
        <div class="card business-summary" v-if="long_business_summary">
          <h2 class="card-title">Business Summary</h2>
          <p>{{ long_business_summary }}</p>
        </div>
      </aside>

    </div>
  </div>
</template>

<script>
import axios from 'axios';
import Plotly from 'plotly.js-dist';

export default {
  name: 'ResultsPage',
  data() {
    return {
      ticker: '',
      figureData: null,
      // Predictions
      dprediction: '',
      daccuracy: '',
      dprice_change: '',
      wprediction: '',
      waccuracy: '',
      wprice_change: '',
      mprediction: '',
      maccuracy: '',
      mprice_change: '',
      //Company
      address: '',
      beta: '',
      book_value: '',
      cash_per_share: '',
      currency: '',
      date_short_interest: '',
      day_high: '',
      day_low: '',
      debt_to_equity: '',
      dividend_yield: '',
      earnings_date: '',
      earnings_growth: '',
      earnings_quarterly_growth: '',
      ebitda: '',
      ebitda_margins: '',
      enterprise_value: '',
      exchange: '',
      fifty_day_average: '',
      fifty_two_week_high: '',
      fifty_two_week_low: '',
      financial_currency: '',
      float_shares: '',
      forward_pe: '',
      free_cashflow: '',
      full_time_employees: '',
      gross_margins: '',
      gross_profit: '',
      held_percent_insiders: '',
      held_percent_institutions: '',
      implied_shares_outstanding: '',
      industry: '',
      last_fiscal_year_end: '',
      last_split_date: '',
      last_split_factor: '',
      long_business_summary: '',
      long_name: '',
      market_cap: '',
      most_recent_quarter: '',
      name: '',
      next_fiscal_year_end: '',
      number_of_analyst_opinions: '',
      open: '',
      operating_cashflow: '',
      operating_margins: '',
      previous_close: '',
      price: '',
      price_to_book: '',
      profit_margins: '',
      quote_type: '',
      recommendation_key: '',
      recommendation_mean: '',
      regular_market_price: '',
      regular_market_volume: '',
      return_on_assets: '',
      return_on_equity: '',
      revenue: '',
      revenue_growth: '',
      revenue_per_share: '',
      sector: '',
      shares_outstanding: '',
      shares_short: '',
      shares_short_prior_month: '',
      short_percent_of_float: '',
      short_ratio: '',
      target_high_price: '',
      target_low_price: '',
      target_mean_price: '',
      target_median_price: '',
      total_cash: '',
      total_debt: '',
      trailing_pe: '',
      two_hundred_day_average: '',
      volume: '',
      website: '',
      // Loading states
      loadingPredictions: false,
      analysisLoading: false,
      analysisError: null,
      analysis: null,
      indicators: {},
    };
  },
  methods: {
    fetchStockData() {
      axios.get(`/api/stock_data?ticker=${this.ticker}`)
          .then((response) => {
            const data = response.data;
            this.name = data.name || 'N/A';
          })
          .catch((error) => {
            console.error('Error fetching stock data:', error);
          });
    },
    fetchStockResultsData() {
      axios.get(`/api/stock_results_data?ticker=${this.ticker}`)
          .then((response) => {
            const data = response.data;
            Object.keys(data).forEach(key => {
              this[key] = data[key] || 'N/A';
            });
          })
          .catch((error) => {
            console.error('Error fetching stock data:', error);
          });
    },
    fetchPredictions() {
      this.loadingPredictions = true;
      axios.get(`/api/predictions?ticker=${this.ticker}`)
          .then((response) => {
            const data = response.data;
            const tomorrowData = data['Tomorrow'];
            if (tomorrowData) {
              this.dprediction = tomorrowData.classification.today_prediction === 1 ? 'Sell' : 'Buy';
              this.daccuracy = (tomorrowData.classification.accuracy * 100).toFixed(0) + '%';
              const dtomorrow_price_prediction = tomorrowData.regression.prediction.toFixed(2);
              this.dprice_change = '$' + dtomorrow_price_prediction;
            } else {
              this.dprediction = 'N/A';
              this.daccuracy = 'N/A';
              this.dprice_change = 'N/A';
            }

            const weekData = data['Week'];
            if (weekData) {
              this.wprediction = weekData.classification.today_prediction === 1 ? 'Sell' : 'Buy';
              this.waccuracy = (weekData.classification.accuracy * 100).toFixed(0) + '%';
              const wweek_price_prediction = weekData.regression.prediction.toFixed(2);
              this.wprice_change = '$' + wweek_price_prediction;
            } else {
              this.wprediction = 'N/A';
              this.waccuracy = 'N/A';
              this.wprice_change = 'N/A';
            }

            const monthData = data['Month'];
            if (monthData) {
              this.mprediction = monthData.classification.today_prediction === 1 ? 'Sell' : 'Buy';
              this.maccuracy = (monthData.classification.accuracy * 100).toFixed(0) + '%';
              const mmonth_price_prediction = monthData.regression.prediction.toFixed(2);
              this.mprice_change = '$' + mmonth_price_prediction;
            } else {
              this.mprediction = 'N/A';
              this.maccuracy = 'N/A';
              this.mprice_change = 'N/A';
            }
          })
          .catch((error) => {
            console.error('Error fetching predictions:', error);
            this.dprediction = 'Error';
            this.daccuracy = 'Error';
            this.dprice_change = 'Error';
            this.wprediction = 'Error';
            this.waccuracy = 'Error';
            this.wprice_change = 'Error';
            this.mprediction = 'Error';
            this.maccuracy = 'Error';
            this.mprice_change = 'Error';
          })
          .finally(() => {
            this.loadingPredictions = false;
          });
    },
    fetchStockChart() {
      const {MACD, RSI, SMA, EMA, ATR, BBands, VWAP} = this.indicators;
      axios
          .get(
              `/api/stock_chart?ticker=${this.ticker}&MACD=${MACD}&RSI=${RSI}&SMA=${SMA}&EMA=${EMA}&ATR=${ATR}&BBands=${BBands}&VWAP=${VWAP}`
          )
          .then((response) => {
            this.figureData = response.data;
            this.renderChart();
          })
          .catch((error) => {
            console.error('Error fetching stock chart:', error);
          });
    },
    fetchStockAnalysis() {
      this.analysisLoading = true;
      this.analysisError = null;
      axios
          .get(`/api/stocks/${this.ticker}/analysis`)
          .then((response) => {
            const data = response.data;
            if (data.analysis) {
              this.analysis = data.analysis;
            } else {
              this.analysisError = 'No analysis available.';
            }
          })
          .catch((error) => {
            console.error('Error fetching analysis:', error);
            this.analysisError = 'Error fetching analysis.';
          })
          .finally(() => {
            this.analysisLoading = false;
          });
    },
    renderChart() {
      if (this.figureData) {
        const chartElement = this.$refs.chart;
        Plotly.react(chartElement, this.figureData.data, this.figureData.layout);
      }
    },
    formatAnalysis(response) {
      let formattedResponse = response
          .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
          .replace(/\*(.*?)\*/g, '<em>$1</em>')
          .replace(/^- (.*?)(\n|$)/gm, '<li>$1</li>')
          .replace(/\n\d+\.\s(.*?)(\n|$)/g, '<li>$1</li>')
          .replace(/\n/g, '<br>');

      formattedResponse = formattedResponse.replace(
          /(<li>.*<\/li>)/g,
          '<ul>$1</ul>'
      );
      return formattedResponse;
    },
  },
  watch: {
    '$route.query': {
      immediate: true,
      handler() {
        const query = this.$route.query;
        this.ticker = query.ticker || 'AAPL';
        this.indicators = {
          RSI: query.RSI === 'true',
          MACD: query.MACD === 'true',
          SMA: query.SMA === 'true',
          EMA: query.EMA === 'true',
          ATR: query.ATR === 'true',
          BBands: query.BBands === 'true',
          VWAP: query.VWAP === 'true',
        };
        this.fetchStockResultsData();
        this.fetchStockData();
        this.fetchPredictions();
        this.fetchStockChart();
        this.fetchStockAnalysis();
      },
    },
  },
};
</script>

<style scoped>
.results-page {
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Oxygen, Ubuntu, Cantarell, "Open Sans", "Helvetica Neue", sans-serif;
  color: #333;
  background: #f9f9f9;
  padding: 40px 20px;
}

/* Title Styling */
.page-title {
  text-align: center;
  font-size: 3rem; /* Keep the header large */
  margin-bottom: 10px;
  margin-top: -40px;
  font-weight: 600;
  color: #333;
}

/* Layout Grid: Prioritize Chart */
.layout-grid {
  display: grid;
  grid-template-columns: 250px minmax(200px, 1fr) 250px;
  gap: 30px;
  max-width: 1800px;
  margin: 0 auto;
  padding: 0 20px;
  width: 100%;
}

/* Center Column: Chart Scaling */
.chart-container {
  min-height: 500px; /* Set a taller minimum height for the chart */
  height: 40vh; /* Allow the chart to dynamically scale */
  width: 100%; /* Fill the available space */
}

/* Responsive Adjustments */
@media (max-width: 1200px) {
  .layout-grid {
    grid-template-columns: 180px 1fr 180px; /* Further reduce sidebar sizes */
  }
}

@media (max-width: 992px) {
  .layout-grid {
    grid-template-columns: 1fr; /* Collapse to a single column */
  }

  .chart-container {
    height: 30vh; /* Scale the chart appropriately for smaller screens */
  }
}

/* Sidebars */
.sidebar {
  display: flex;
  flex-direction: column;
  gap: 30px; /* Spacing between cards */
  margin-top: 21px;
}

.card {
  background: #fff;
  border: 1px solid #ddd;
  border-radius: 8px;
  padding: 25px;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.1);
}

/* Card Title */
.card-title {
  margin-top: 0;
  margin-bottom: 20px;
  font-size: 1.5rem;
  font-weight: bold;
  color: #333;
  border-bottom: 2px solid #f0f0f0;
  padding-bottom: 10px;
}

.business-summary p {
  font-size: 0.8rem; /* Reduce font size */
  line-height: 1.4; /* Adjust line height for readability */
  color: #555; /* Optional: soften the color for better aesthetics */
}

/* Metrics and Stats */
.metrics-list {
  list-style: none;
  padding: 0;
  margin: 0;
  font-size: 1.1rem;
}

.metrics-list li {
  margin: 10px 0;
  line-height: 1.6;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(180px, 1fr));
  gap: 20px;
  font-size: 1.1rem;
}

.stats-grid div {
  background: #fdfdfd;
  border-radius: 6px;
  padding: 15px;
  border: 1px solid #eee;
}

/* Predictions Section */
.predictions-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 30px;
}

.predictions-grid h3 {
  margin-bottom: 10px;
  font-size: 1.25rem;
  font-weight: 600;
}

/* Analysis Section */
.analysis-card {
  font-size: 1.1rem;
  line-height: 1.7;
}

/* Loading Spinner */
.loading-container {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.spinner {
  margin: 20px;
  border: 8px solid #f3f3f3;
  border-top: 8px solid #3498db;
  border-radius: 50%;
  width: 50px;
  height: 50px;
  animation: spin 1s linear infinite;
}

/* Hover and Focus States */
a {
  color: #3498db;
  text-decoration: none;
  transition: color 0.3s;
}

a:hover, a:focus {
  text-decoration: underline;
}

/* Keyframes */
@keyframes spin {
  0% {
    transform: rotate(0deg);
  }
  100% {
    transform: rotate(360deg);
  }
}

/* Responsive Design */
@media (max-width: 768px) {
  .card {
    padding: 20px;
  }

  .card-title {
    font-size: 1.25rem;
  }

  .stats-grid div {
    padding: 10px;
  }

  .predictions-grid {
    grid-template-columns: 1fr;
  }
}

</style>


