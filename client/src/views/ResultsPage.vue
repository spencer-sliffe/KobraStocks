<template>
  <div>
    <SearchBar :indicators="indicators" :initialTicker="ticker" />
    <h1>Stock Chart for {{ ticker }}</h1>
    <div class="chart-container" ref="chart"></div>

    <div class="data-section">
      <h2>Open | Close | High | Low | Volume</h2>
      <h2>{{ popen }} | {{ pclose }} | {{ phigh }} | {{ plow }} | {{ volume }}</h2>
    </div>

    <div class="data-section">
      <div>
        <h2>ML Suggest | Strength</h2>
      </div>
      <div>
        <h2>Tomorrow</h2>
        <h4>{{ dprediction }} | {{ daccuracy }}</h4>
      </div>
      <div>
        <h2>Next Week</h2>
        <h4>{{ wprediction }} | {{ waccuracy }}</h4>
      </div>
      <div>
        <h2>Next Month</h2>
        <h4>{{ mprediction }} | {{ maccuracy }}</h4>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import Plotly from 'plotly.js-dist';
import SearchBar from '@/components/SearchBar.vue';

export default {
  name: 'ResultsPage',
  components: {
    SearchBar,
  },
  data() {
    return {
      ticker: '',
      figureData: null,
      popen: '',
      pclose: '',
      phigh: '',
      plow: '',
      volume: '',
      dprediction: '',
      wprediction: '',
      mprediction: '',
      daccuracy: '',
      waccuracy: '',
      maccuracy: '',
      indicators: {},
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
      axios
        .get(`/api/predictions?ticker=${this.ticker}`)
        .then((response) => {
          const data = response.data;
          this.dprediction = data.daily.prediction === 1 ? 'BUY' : 'SELL';
          this.daccuracy = (data.daily.accuracy * 100).toFixed(2) + '%';
          this.wprediction = data.weekly.prediction === 1 ? 'BUY' : 'SELL';
          this.waccuracy = (data.weekly.accuracy * 100).toFixed(2) + '%';
          this.mprediction = data.monthly.prediction === 1 ? 'BUY' : 'SELL';
          this.maccuracy = (data.monthly.accuracy * 100).toFixed(2) + '%';
        })
        .catch((error) => {
          console.error('Error fetching predictions:', error);
        });
    },
    fetchStockChart() {
      const { MA9, MA50, MACD, RSI } = this.indicators;
      axios
        .get(
          `/api/stock_chart?ticker=${this.ticker}&MA9=${MA9}&MA50=${MA50}&MACD=${MACD}&RSI=${RSI}`
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
        const query = this.$route.query;
        this.ticker = query.ticker || 'AAPL';
        this.indicators = {
          RSI: query.RSI === 'true',
          MACD: query.MACD === 'true',
          MA50: query.MA50 === 'true',
          MA9: query.MA9 === 'true',
        };
        this.fetchStockData();
        this.fetchPredictions();
        this.fetchStockChart();
      },
    },
  },
};
</script>


