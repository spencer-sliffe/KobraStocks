# KobraStocks

KobraStocks is a web-based application designed to help users predict the movement of stock prices intuitively. By simply entering a stock ticker symbol, users can view detailed financial graphs, data insights, and the model's price movement prediction. Additionally, the application provides options for a personalized portfolio and tracks hot stocks/crypto.


---

## Features

KobraStocks offers the following features:

1. **Stock Search**:  
   Search stocks by entering their ticker symbols and view key financial data, stock price graphs, and predictions.

2. **Custom Machine Learning Model**:  
   Selectable indicators (e.g., moving averages, RSI) which are used within the model's training to predict price movements for the next day, week, and year.

3. **Visualization**:  
   View detailed stock/graphs powered by **Matplotlib** and **Plotly.js**, which plot stock price data alongside selected indicators. 

4. **Data Insights**:  
   Access key data points related to stock performance and predictions for future price trends, including accuracies of the machine learning models.

5. **Personalized Stock Portfolio Analysis**:  
   Add stocks you own to your portfolio, and an AI will analyze your portfolio to provide suggestions and predictions unique to your holdings.

6. **Crypto Watcher**:  
   Explore trending cryptocurrencies, add them to your favorites, and track their performance in real time.

7. **Stock Market News**:  
   Stay updated with the latest news affecting the stock market integrated into the user interface.

---

## Technologies Used

The application leverages the following technologies:

### Frontend:
- **Vue.js**: The framework used for building the app's UI.  
- **JavaScript & CSS**: To support an interactive UI and styling of the frontend. 

### Backend:
- **Python Flask**: Lightweight framework for routing and handling backend logic.  
- **APIs**:
  - **Yahoo Finance**: For fetching real-time stock and cryptocurrency data.  

### Machine Learning:
- **Python Scikit-Learn**: Used to train, test, and evaluate machine learning models for predicting stock price movements.

---

## Installation

Follow these steps to set up the application locally:

1. Clone the repository:

   ```bash
   git clone https://github.com/yourusername/KobraStocks.git
   cd KobraStocks
   ```

2. Install the required Python dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Install the required frontend dependencies using npm:

   ```bash
   npm install
   ```

4. Build the Vue.js frontend (if necessary):

   ```bash
   npm run build
   ```

5. Start the Flask server:

   ```bash
   python app.py
   ```

6. Open the app in your browser at:

   ```
   http://localhost:5000
   ```

---

## Usage

1. Enter a stock ticker in the search bar.  
2. View the detailed graph with selectable indicators to customize your analysis.  
3. Check the model's prediction for stock price movement (up or down).  
4. Explore additional features such as personalized portfolio analysis, crypto tracking, and market news aggregation.

---

## Future Plans

- **Enhanced Machine Learning Models**: Refine existing models with deep learning techniques for better accuracy.  
- **Real-Time Data Fetching**: Improve APIs for faster real-time updates.  
- **Mobile App Version**: Extend functionality to native mobile applications.

---
