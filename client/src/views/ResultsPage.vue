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
            <li><strong>Short Ratio:</strong> {{ short_ratio }}</li>
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
            <div><strong>Open:</strong> {{ open }}</div>
            <div><strong>Close:</strong> {{ previous_close }}</div>
            <div><strong>High:</strong> {{ day_high }}</div>
            <div><strong>Low:</strong> {{ day_low }}</div>
            <div><strong>Volume:</strong> {{ volume }}</div>
            <div><strong>Address:</strong> {{ address }}</div>
            <div><strong>Book Value:</strong> {{ book_value }}</div>
            <div><strong>Cash Per Share:</strong> {{ cash_per_share }}</div>
            <div><strong>Currency:</strong> {{ currency }}</div>
            <div><strong>Date Short Interest:</strong> {{ date_short_interest }}</div>
            <div><strong>Debt To Equity:</strong> {{ debt_to_equity }}</div>
            <div><strong>Earnings Growth:</strong> {{ earnings_growth }}</div>
            <div><strong>Earnings Quarterly Growth:</strong> {{ earnings_quarterly_growth }}</div>
            <div><strong>EBITDA:</strong> {{ ebitda }}</div>
            <div><strong>EBITDA Margins:</strong> {{ ebitda_margins }}</div>
            <div><strong>Enterprise Value:</strong> {{ enterprise_value }}</div>
            <div><strong>Exchange:</strong> {{ exchange }}</div>
            <div><strong>52-Week High:</strong> {{ fifty_two_week_high }}</div>
            <div><strong>52-Week Low:</strong> {{ fifty_two_week_low }}</div>
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
            <div><strong>Price:</strong> {{ price }}</div>
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
          <h2>Company Information</h2>
          <p><strong>Industry:</strong> {{ industry }}</p>
          <p><strong>Sector:</strong> {{ sector }}</p>
          <p><strong>Address:</strong> {{ address }}</p>
          <p><strong>Website:</strong> <a :href="website" target="_blank">{{ website }}</a></p>
        </div>
        <div class="card" v-if="long_business_summary">
          <h2>Business Summary</h2>
          <p>{{ long_business_summary }}</p>
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
          console.log(data)
          // Today’s Stats
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
          console.log(data)
          this.address = data.address || 'N/A';
          this.beta = data.beta || 'N/A';
          this.book_value = data.book_value || 'N/A';
          this.cash_per_share = data.cash_per_share || 'N/A';
          this.currency = data.currency || 'N/A';
          this.date_short_interest = data.date_short_interest || 'N/A';
          this.day_high = data.day_high || 'N/A';
          this.day_low = data.day_low || 'N/A';
          this.debt_to_equity = data.debt_to_equity || 'N/A';
          this.dividend_yield = data.dividend_yield || 'N/A';
          this.earnings_date = data.earnings_date || 'N/A';
          this.earnings_growth = data.earnings_growth || 'N/A';
          this.earnings_quarterly_growth = data.earnings_quarterly_growth || 'N/A';
          this.ebitda = data.ebitda || 'N/A';
          this.ebitda_margins = data.ebitda_margins || 'N/A';
          this.enterprise_value = data.enterprise_value || 'N/A';
          this.exchange = data.exchange || 'N/A';
          this.fifty_day_average = data.fifty_day_average || 'N/A';
          this.fifty_two_week_high = data.fifty_two_week_high || 'N/A';
          this.fifty_two_week_low = data.fifty_two_week_low || 'N/A';
          this.financial_currency = data.financial_currency || 'N/A';
          this.float_shares = data.float_shares || 'N/A';
          this.forward_pe = data.forward_pe || 'N/A';
          this.free_cashflow = data.free_cashflow || 'N/A';
          this.full_time_employees = data.full_time_employees || 'N/A';
          this.gross_margins = data.gross_margins || 'N/A';
          this.gross_profit = data.gross_profit || 'N/A';
          this.held_percent_insiders = data.held_percent_insiders || 'N/A';
          this.held_percent_institutions = data.held_percent_institutions || 'N/A';
          this.implied_shares_outstanding = data.implied_shares_outstanding || 'N/A';
          this.industry = data.industry || 'N/A';
          this.last_fiscal_year_end = data.last_fiscal_year_end || 'N/A';
          this.last_split_date = data.last_split_date || 'N/A';
          this.last_split_factor = data.last_split_factor || 'N/A';
          this.long_business_summary = data.long_business_summary || 'N/A';
          this.long_name = data.long_name || 'N/A';
          this.market_cap = data.market_cap || 'N/A';
          this.most_recent_quarter = data.most_recent_quarter || 'N/A';
          this.next_fiscal_year_end = data.next_fiscal_year_end || 'N/A';
          this.number_of_analyst_opinions = data.number_of_analyst_opinions || 'N/A';
          this.open = data.open;
          this.operating_cashflow = data.operating_cashflow || 'N/A';
          this.operating_margins = data.operating_margins || 'N/A';
          this.previous_close = data.previous_close || 'N/A';
          this.price = data.price || 'N/A';
          this.price_to_book = data.price_to_book || 'N/A';
          this.profit_margins = data.profit_margins || 'N/A';
          this.quote_type = data.quote_type || 'N/A';
          this.recommendation_key = data.recommendation_key || 'N/A';
          this.recommendation_mean = data.recommendation_mean || 'N/A';
          this.regular_market_price = data.regular_market_price || 'N/A';
          this.regular_market_volume = data.regular_market_volume || 'N/A';
          this.return_on_assets = data.return_on_assets || 'N/A';
          this.return_on_equity = data.return_on_equity || 'N/A';
          this.revenue = data.revenue || 'N/A';
          this.revenue_growth = data.revenue_growth || 'N/A';
          this.revenue_per_share = data.revenue_per_share || 'N/A';
          this.sector = data.sector || 'N/A';
          this.shares_outstanding = data.shares_outstanding || 'N/A';
          this.shares_short = data.shares_short || 'N/A';
          this.shares_short_prior_month = data.shares_short_prior_month || 'N/A';
          this.short_percent_of_float = data.short_percent_of_float || 'N/A';
          this.short_ratio = data.short_ratio || 'N/A';
          this.target_high_price = data.target_high_price || 'N/A';
          this.target_low_price = data.target_low_price || 'N/A';
          this.target_mean_price = data.target_mean_price || 'N/A';
          this.target_median_price = data.target_median_price || 'N/A';
          this.total_cash = data.total_cash || 'N/A';
          this.total_debt = data.total_debt || 'N/A';
          this.trailing_pe = data.trailing_pe || 'N/A';
          this.two_hundred_day_average = data.two_hundred_day_average || 'N/A';
          this.volume = data.volume || 'N/A';
          this.website = data.website || 'N/A';
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
    formatAnalysis(response) {
      // Replace Markdown-style formatting with HTML tags
      let formattedResponse = response
        .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>') // Bold (**text**)
        .replace(/\*(.*?)\*/g, '<em>$1</em>')            // Italic (*text*)
        .replace(/^- (.*?)(\n|$)/gm, '<li>$1</li>')      // Bulleted list (- item)
        .replace(/\n\d+\.\s(.*?)(\n|$)/g, '<li>$1</li>') // Numbered list (1. item)
        .replace(/\n/g, '<br>');                         // Line breaks

      // Wrap bullet points or numbered list items in <ul> if applicable
      formattedResponse = formattedResponse.replace(
        /(<li>.*<\/li>)/g,
        '<ul>$1</ul>'
      );

      // Return the formatted and safe HTML string
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
