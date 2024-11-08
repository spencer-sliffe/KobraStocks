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
        <h2>ML Suggest | Strength | Price Prediction</h2>
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
          // Tomorrow
          this.dprediction = data.tomorrow.classification_prediction === 1 ? 'Buy' : 'Sell';
          this.daccuracy = (data.tomorrow.classification_accuracy * 100).toFixed(0) + '%';
          const dtomorrow_price_change = data.tomorrow.price_change.toFixed(2);
          this.dprice_change = (dtomorrow_price_change >= 0 ? '+ $' : '- $') + Math.abs(dtomorrow_price_change);
          // Next Week
          this.wprediction = data.next_week.classification_prediction === 1 ? 'Buy' : 'Sell';
          this.waccuracy = (data.next_week.classification_accuracy * 100).toFixed(0) + '%';
          const wnextweek_price_change = data.next_week.price_change.toFixed(2);
          this.wprice_change = (wnextweek_price_change >= 0 ? '+ $' : '- $') + Math.abs(wnextweek_price_change);
          // Next Month
          this.mprediction = data.next_month.classification_prediction === 1 ? 'Buy' : 'Sell';
          this.maccuracy = (data.next_month.classification_accuracy * 100).toFixed(0) + '%';
          const mnextmonth_price_change = data.next_month.price_change.toFixed(2);
          this.mprice_change = (mnextmonth_price_change >= 0 ? '+ $' : '- $') + Math.abs(mnextmonth_price_change);
        })
        .catch((error) => {
          console.error('Error fetching predictions:', error);
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
      },
    },
  },
};
</script>
