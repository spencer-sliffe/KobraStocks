<!-- Prologue
Component Name: ResultsPage
Path: src/views/ResultsPage.vue

Description:
Displays detailed stock information, a stock chart, and machine learning predictions for future stock performance based on user-selected indicators.
-->

<template>
  <div>
    <h1>Stock Chart for {{ ticker }}</h1>
    <div class="chart-container" ref="chart"></div>

    <!-- Loading indicator for predictions -->
    <div v-if="loadingPredictions" class="loading-container">
      <div class="spinner"></div>
      <p>Loading predictions...</p>
    </div>
    <div v-else>
      <!-- Data sections displaying predictions -->
      <div class="data-section">
        <h2>Open | Close | High | Low | Volume</h2>
        <h2>{{ popen }} | {{ pclose }} | {{ phigh }} | {{ plow }} | {{ volume }}</h2>
      </div>

      <div class="data-section">
        <div>
          <h2>ML Suggest | Accuracy | Price Prediction</h2>
        </div>
        <div>
          <h2>Tomorrow</h2>
          <h4>{{ dprediction }} | {{ daccuracy }} | {{ dprice_change }}</h4>
        </div>
        <div>
          <h2>Next Week</h2>
          <h4>{{ wprediction }} | {{ waccuracy }} | {{ wprice_change }}</h4>
        </div>
        <div>
          <h2>Next Month</h2>
          <h4>{{ mprediction }} | {{ maccuracy }} | {{ mprice_change }}</h4>
        </div>
      </div>
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
      popen: '',
      pclose: '',
      phigh: '',
      plow: '',
      volume: '',
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
      indicators: {},
      // Loading state
      loadingPredictions: false,
    };
  },
  methods: {
    fetchStockData() {
      axios
          .get(`/api/stock_data?ticker=${this.ticker}`)
          .then((response) => {
            const data = response.data;
            this.popen = data.open_price.toFixed(2);
            this.pclose = data.close_price.toFixed(2);
            this.phigh = data.high_price.toFixed(2);
            this.plow = data.low_price.toFixed(2);
            this.volume = data.volume;
          })
          .catch((error) => {
            console.error('Error fetching stock data:', error);
          });
    },
    fetchPredictions() {
      this.loadingPredictions = true;
      axios
          .get(`/api/predictions?ticker=${this.ticker}`)
          .then((response) => {
            const data = response.data;
            // Tomorrow
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

            // Week
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

            // Month
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
            // Optionally set default values or error messages
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
        console.log('Route query updated:', this.$route.query); // Debugging log
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
      },
    },
  },
};
</script>

<style scoped>
/* General Styles */
.chart-container {
  width: 100%;
  height: 600px;
}

.data-section {
  margin-top: 20px;
}

/* Loading Spinner Styles */
.loading-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin-top: 20px;
}

.spinner {
  margin: 20px;
  border: 8px solid #f3f3f3; /* Light gray */
  border-top: 8px solid #3498db; /* Blue */
  border-radius: 50%;
  width: 60px;
  height: 60px;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  0% {
    transform: rotate(0deg);
  }
  100% {
    transform: rotate(360deg);
  }
}

/* Optional: Styling for the data display */
.data-section h2 {
  margin: 10px 0;
}

.data-section h4 {
  margin: 5px 0;
}
</style>
