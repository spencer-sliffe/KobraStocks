<!-- Prologue
Component Name: ResultsPage
Path: src/views/ResultsPage.vue

Description:
Displays detailed stock information, a stock chart, and machine learning predictions for future stock performance based on user-selected indicators.
-->

<template>
  <div class="results-page">
    <h1 class="page-title center">Stock Chart for {{ name }} (${{ticker}})</h1>
    <div class="layout-grid">
      <!-- LEFT SIDEBAR -->
      <aside class="sidebar left-sidebar">
        <div class="card">
          <h2>Key Metrics</h2>
          <ul class="metrics-list">
            <li><strong>Market Cap:</strong> {{ market_cap }}</li>
            <li><strong>PE Ratio:</strong> {{ pe_ratio }}</li>
            <li><strong>Dividend Yield:</strong> {{ dividend_yield }}</li>
            <li><strong>50-Day Avg:</strong> {{ fifty_day_average }}</li>
            <li><strong>200-Day Avg:</strong> {{ two_hundred_day_average }}</li>
            <li><strong>Earnings Date:</strong> {{ earnings_date }}</li>
            <li><strong>Forward PE:</strong> {{ forward_pe }}</li>
            <li><strong>Beta:</strong> {{ beta }}</li>
          </ul>
        </div>
        <!-- Additional left-column suggestions:
             - Price Performance Sparkline
             - Average Volume, 52-Week Range
             - Key Financial Ratios -->
      </aside>

      <!-- CENTER COLUMN (MAIN CONTENT) -->
      <main class="main-content">
        <!-- Stock Chart -->
        <div class="card chart-container" ref="chart"></div>

        <!-- Today's Stats -->
        <div class="card">
          <h2>Today’s Stats</h2>
          <div class="stats-grid">
            <div><strong>Open:</strong> {{ popen }}</div>
            <div><strong>Close:</strong> {{ pclose }}</div>
            <div><strong>High:</strong> {{ phigh }}</div>
            <div><strong>Low:</strong> {{ plow }}</div>
            <div><strong>Volume:</strong> {{ volume }}</div>
          </div>
        </div>

        <!-- ML Predictions -->
        <div class="card">
          <h2>ML Predictions</h2>
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
          <h2>Stock Analysis</h2>
          <div v-if="analysisLoading" class="loading-container">
            <div class="spinner"></div>
            <p>Loading stock analysis...</p>
          </div>
          <div v-else-if="analysisError">
            <p class="error-text">{{ analysisError }}</p>
          </div>
          <div v-else-if="analysis">
            <p>{{ analysis }}</p>
          </div>
          <div v-else>
            <p>No analysis available at this time.</p>
          </div>
        </div>
      </main>

      <!-- RIGHT SIDEBAR -->
      <aside class="sidebar right-sidebar">
        <div class="card">
          <h2>Company Information</h2>
          <p><strong>CEO:</strong> {{ ceo }}</p>
          <p><strong>Industry:</strong> {{ industry }}</p>
          <p><strong>Sector:</strong> {{ sector }}</p>
          <p><strong>Address:</strong> {{ address }}</p>
          <p><strong>Website:</strong> <a :href="website" target="_blank">{{ website }}</a></p>
        </div>
        <div class="card" v-if="longBusinessSummary">
          <h2>Business Summary</h2>
          <p>{{ longBusinessSummary }}</p>
        </div>
        <!-- Additional right-column suggestions:
             - Analyst Ratings
             - Target Price (High, Mean, Low)
             - Recent News Headlines -->
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
      // Basic Stats
      popen: '',
      pclose: '',
      phigh: '',
      plow: '',
      volume: '',
      name: '',
      // Key Metrics
      market_cap: '',
      pe_ratio: '',
      dividend_yield: '',
      fifty_day_average: '',
      two_hundred_day_average: '',
      earnings_date: '',
      forward_pe: '',
      beta: '',
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
      // Company Info
      industry: '',
      sector: '',
      address: '',
      website: '',
      ceo: 'N/A',
      longBusinessSummary: '',
      companyOfficers: [],
      // Loading states
      loadingPredictions: false,
      analysisLoading: false,
      analysisError: null,
      analysis: null,
      indicators: {},
    };
  },
  computed: {
    foundCEO() {
      if (!this.companyOfficers || !this.companyOfficers.length) return 'N/A';
      const ceoOfficer = this.companyOfficers.find(officer =>
        officer.title && officer.title.toLowerCase().includes('ceo')
      );
      return ceoOfficer ? ceoOfficer.name : 'N/A';
    }
  },
  methods: {
    fetchStockData() {
      axios.get(`/api/stock_data?ticker=${this.ticker}`)
        .then((response) => {
          const data = response.data;
          // Today’s Stats
          this.popen = data.open?.toFixed(2) || 'N/A';
          this.pclose = data.close?.toFixed(2) || 'N/A';
          this.phigh = data.dayHigh?.toFixed(2) || 'N/A';
          this.plow = data.dayLow?.toFixed(2) || 'N/A';
          this.volume = data.volume || 'N/A';
          this.name = data.name || 'N/A';

          // Key Metrics
          this.market_cap = data.marketCap ? data.marketCap.toLocaleString() : 'N/A';
          this.pe_ratio = data.trailingPE ? data.trailingPE.toFixed(2) : 'N/A';
          this.dividend_yield = data.dividendYield
            ? (data.dividendYield * 100).toFixed(2) + '%'
            : 'N/A';
          this.fifty_day_average = data.fiftyDayAverage?.toFixed(2) || 'N/A';
          this.two_hundred_day_average = data.twoHundredDayAverage?.toFixed(2) || 'N/A';
          this.earnings_date = data.earningsDate || 'N/A';
          this.forward_pe = data.forwardPE ? data.forwardPE.toFixed(2) : 'N/A';
          this.beta = data.beta?.toFixed(2) || 'N/A';

          // Company Info
          this.industry = data.industryDisp || data.industry || 'N/A';
          this.sector = data.sectorDisp || data.sector || 'N/A';
          const addressParts = [data.address1, data.city, data.state, data.zip, data.country].filter(Boolean);
          this.address = addressParts.join(', ') || 'N/A';
          this.website = data.website || 'N/A';
          this.longBusinessSummary = data.longBusinessSummary || '';
          this.companyOfficers = data.companyOfficers || [];
          this.ceo = this.foundCEO;
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
      const { MACD, RSI, SMA, EMA, ATR, BBands, VWAP } = this.indicators;
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

      // If you have user data, pass it here. For now, just calling the endpoint:
      axios
        .get(`/api/stocks/${this.ticker}/analysis`) // Adjust endpoint and params if needed.
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
  padding: 20px;
  font-family: Arial, sans-serif;
}

.page-title {
  margin-bottom: 20px;
}

.layout-grid {
  display: grid;
  grid-template-columns: 200px 1fr 200px; /* Left narrow column, main wide column, right narrow column */
  gap: 20px;
}

/* Sidebar Styling */
.sidebar {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.card {
  background: #fff;
  border: 1px solid #e5e5e5;
  border-radius: 4px;
  padding: 15px;
  box-shadow: 0 1px 3px rgba(0,0,0,0.1);
}

/* Center Column (Main Content) */
.main-content {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

/* Styles for lists of metrics */
.metrics-list {
  list-style: none;
  padding: 0;
  margin: 0;
}

.metrics-list li {
  margin: 5px 0;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(100px, 1fr));
  gap: 10px;
}

.predictions-grid {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.center {
  text-align: center;
}

.error-text {
  color: #d9534f;
  font-weight: bold;
}

/* Loading Spinner Styles */
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
  width: 40px;
  height: 40px;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

/* Hover/Focus states for better UX */
a:hover {
  text-decoration: underline;
}
</style>
