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
- **Database:** SQLite (dev) / PostgreSQL (production)
- **ML:** Scikit-Learn, TensorFlow/Keras (LSTM)
- **APIs:** Yahoo Finance (yfinance), OpenAI, NewsAPI

## Quick Start

### Prerequisites

- **Python 3.11, 3.12, or 3.13** (3.14+ is NOT supported — key packages lack wheels)
- **Node.js 18+** and **npm**

### macOS / Linux

```bash
git clone https://github.com/spencer-sliffe/KobraStocks.git
cd KobraStocks
chmod +x setup.sh
./setup.sh
```

### Windows (PowerShell)

```powershell
git clone https://github.com/spencer-sliffe/KobraStocks.git
cd KobraStocks
.\setup.ps1
```

> **Note:** If you get a script execution policy error, run:
> `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser`

The scripts will:
1. Verify Python and Node.js are installed (on macOS, installs via Homebrew if missing)
2. Create a Python virtual environment and install backend dependencies
3. Create a `.env` file with SQLite defaults (no PostgreSQL required for development)
4. Run database migrations
5. Install frontend npm packages
6. Start both the backend (http://127.0.0.1:5000) and frontend (http://localhost:8080)

Press `Ctrl+C` to stop both servers.

## Manual Setup

### Installing Prerequisites

#### macOS

```bash
brew install python@3.12 node
```

#### Windows

1. **Python 3.12** - Download from [python.org](https://www.python.org/downloads/). Check "Add Python to PATH" during install.
2. **Node.js 18+** - Download the LTS installer from [nodejs.org](https://nodejs.org/).

### Backend

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

### Environment Variables

Create `Backend/.env`:

```env
SECRET_KEY=your_secret_key_here
SQLALCHEMY_DATABASE_URI=sqlite:///kobrastocks.db
JWT_SECRET_KEY=your_jwt_secret_here
OPENAI_API_KEY=your_openai_api_key_here
NEWS_API_KEY=your_newsapi_key_here
```

For PostgreSQL, use: `SQLALCHEMY_DATABASE_URI=postgresql://user:pass@localhost:5432/kobrastocks`

### Initialize Database

```bash
flask db upgrade
```

### Frontend

```bash
cd client
npm install
```

### Run

Start the backend and frontend in separate terminals:

```bash
# Terminal 1 — Backend
cd Backend
source venv/bin/activate   # Windows: .\venv\Scripts\Activate.ps1
flask run

# Terminal 2 — Frontend
cd client
npm run serve
```

## API Keys

- **OpenAI** - [platform.openai.com](https://platform.openai.com/)
- **NewsAPI** - [newsapi.org](https://newsapi.org/)
- **Yahoo Finance** - No API key required (uses yfinance library)
