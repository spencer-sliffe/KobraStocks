# KobraStocks

Predict the stock market with accurate machine learning models.

## Introduction

KobraStocks is a web-based application designed to predict the movement of stock prices. By entering a stock ticker into the search bar, users can view the graph, data, and price prediction of the searched stock. Predictions consist of whether the stock price is likely to move up or down, alongside the accuracy of the model's prediction.

## Features

- **Stock Search** - Enter a ticker symbol to view financial data and ML-powered predictions
- **Selectable Indicators** - Choose technical indicators (MACD, RSI, SMA, EMA, ATR, Bollinger Bands, VWAP) for personalized models
- **Visualization** - Interactive Plotly charts with price history and indicator overlays
- **Price Predictions** - RandomForest, LDA, and LSTM neural network models for forecasting
- **Portfolio Analysis** - Add stocks to your portfolio and get AI-powered analysis via OpenAI
- **Crypto Watcher** - Track cryptocurrencies and manage favorites
- **Stock Market News** - Latest market news via NewsAPI

## Technologies

- **Frontend:** Vue.js 3, Vue Router, Axios, Plotly.js, vue3-carousel
- **Backend:** Python Flask, SQLAlchemy, Flask-JWT-Extended, Flask-Migrate
- **Database:** PostgreSQL
- **ML:** Scikit-Learn, TensorFlow/Keras (LSTM)
- **APIs:** Yahoo Finance (yfinance), OpenAI, NewsAPI

## Prerequisites

- **Python 3.11+**
- **Node.js 18+** and **npm**
- **PostgreSQL** (or another SQL database)

### Installing Prerequisites

#### macOS

```bash
# Install Homebrew (if not installed)
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install Python, Node.js, and PostgreSQL
brew install python@3.11 node postgresql@16

# Start PostgreSQL
brew services start postgresql@16

# Create the database
createdb kobrastocks
```

#### Windows

1. **Python 3.11+** - Download from [python.org](https://www.python.org/downloads/). Check "Add Python to PATH" during install.
2. **Node.js 18+** - Download the LTS installer from [nodejs.org](https://nodejs.org/).
3. **PostgreSQL** - Download from [postgresql.org](https://www.postgresql.org/download/windows/). Remember the password you set during install.
4. Open **pgAdmin** or **psql** and create a database named `kobrastocks`.

## Setup

### 1. Clone the repository

```bash
git clone https://github.com/spencer-sliffe/KobraStocks.git
cd KobraStocks
```

### 2. Backend Setup

#### macOS / Linux

```bash
cd Backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

#### Windows (PowerShell)

```powershell
cd Backend
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

> **Note:** If you get an error about running scripts being disabled on Windows, run:
> `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser`

### 3. Configure Environment Variables

Create a `.env` file in the `Backend/` directory:

```env
SECRET_KEY=your_secret_key_here
SQLALCHEMY_DATABASE_URI=postgresql://username:password@localhost:5432/kobrastocks
JWT_SECRET_KEY=your_jwt_secret_here
OPENAI_API_KEY=your_openai_api_key_here
NEWS_API_KEY=your_newsapi_key_here
```

Replace `username` and `password` with your PostgreSQL credentials. On macOS with Homebrew, the default URI is typically `postgresql://localhost:5432/kobrastocks` (no username/password needed).

### 4. Initialize the Database

```bash
# From the Backend/ directory with the venv activated
flask db upgrade
```

### 5. Frontend Setup

```bash
cd client
npm install
```

## Running the Application

### Start the Backend

#### macOS / Linux

```bash
cd Backend
source venv/bin/activate
flask run
```

#### Windows (PowerShell)

```powershell
cd Backend
.\venv\Scripts\Activate.ps1
flask run
```

The backend API will be available at `http://127.0.0.1:5000`.

### Start the Frontend

In a separate terminal:

```bash
cd client
npm run serve
```

The frontend will be available at `http://localhost:8080`.

## API Keys

- **OpenAI** - Get an API key from [platform.openai.com](https://platform.openai.com/)
- **NewsAPI** - Get a free key from [newsapi.org](https://newsapi.org/)
- **Yahoo Finance** - No API key required (uses yfinance library)
