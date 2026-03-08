# 🤖 AI Stock Market Predictor

An intelligent stock market prediction system that analyzes multiple global factors including war events, tech advancements, resource scarcity, and natural disasters to predict stock price movements.

![Python](https://img.shields.io/badge/Python-3.11+-blue)
![Flask](https://img.shields.io/badge/Flask-3.0-red)
![License](https://img.shields.io/badge/License-MIT-green)

## ✨ Features

### 📊 Real-Time Stock Data
- **US Stocks**: Apple, Google, Microsoft, Amazon, Tesla, NVIDIA, Meta, and 20+ more
- **NSE (India)**: Reliance, TCS, HDFC Bank, Infosys, Wipro, and 20+ more
- **BSE (India)**: Tata Steel, Coal India, ONGC, Vedanta, and more

### 🧠 AI Prediction Engine
The AI analyzes multiple factors to predict stock movements:

1. **War & Conflict Events**
   - Geopolitical tensions
   - Regional conflicts
   - Trade wars

2. **Technology Events**
   - AI breakthroughs
   - Product launches
   - Semiconductor shortages

3. **Resource Scarcity**
   - Oil & Gas prices
   - Lithium & Rare earth metals
   - Copper & Gold

4. **Natural Events**
   - Climate disasters
   - Weather events
   - Supply chain impacts

### 📈 Interactive Dashboard
- Real-time stock price charts
- Probability gauge (UP/DOWN)
- 7-day price predictions
- Historical data visualization
- Impact factor analysis

## 🚀 Getting Started

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/stock-market-predictor.git
cd stock-market-predictor
```

2. **Create virtual environment** (optional but recommended)
```bash
python -m venv venv
# On Windows
venv\Scripts\activate
# On Linux/Mac
source venv/bin/activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Run the application**
```bash
python app.py
```

5. **Open in browser**
Navigate to: `http://127.0.0.1:5000`

## 📁 Project Structure

```
stock-market-predictor/
├── app.py                 # Flask backend with AI prediction engine
├── requirements.txt       # Python dependencies
├── README.md             # This file
├── SPEC.md               # Project specification
├── static/
│   ├── css/
│   │   └── style.css     # Modern dark-themed stylesheet
│   └── js/
│       └── main.js       # Frontend JavaScript with Chart.js
└── templates/
    └── index.html        # Main dashboard page
```

## 🔌 API Endpoints

| Endpoint | Description |
|----------|-------------|
| `/` | Main dashboard |
| `/api/stocks` | List all available stocks |
| `/api/stock/<symbol>` | Get stock data with prediction |
| `/api/events/all` | Get all global events |
| `/api/market/sentiment` | Get market sentiment |
| `/api/search/<query>` | Search stocks |

## 📱 Supported Stocks

### US Stocks (NASDAQ/NYSE)
AAPL, GOOGL, MSFT, AMZN, TSLA, NVDA, META, JPM, V, JNJ, WMT, PG, UNH, HD, MA, DIS, NFLX, ADBE, CRM, INTC, AMD, CSCO, PEP, KO, NKE, BA

### NSE Stocks (India)
RELIANCE, TCS, HDFCBANK, BHARTIARTL, ICICIBANK, SBIN, WIPRO, HINDUNILVR, INFOSYS, LT, SUNPHARMA, MARUTI, TITAN, BAJFINANCE, NTPC, POWERGRID, KOTAKBANK, AXISBANK, ADANIPORTS, ASIANPAINT

### BSE Stocks (India)
BSE, COALINDIA, ONGC, TATASTEEL, JSWSTEEL, HINDZINC, VEDL, TATAMOTORS, ITC, EICHERMOT

## ⚠️ Disclaimer

This is an AI-powered prediction tool for **educational purposes only**. Stock market investments involve significant risk. Past performance does not guarantee future results. Always consult with a qualified financial advisor before making investment decisions.

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 👨‍💻 Author

Your Name - [GitHub](https://github.com/yourusername)

---

**Note**: This project uses Yahoo Finance API for real-time stock data. Data is cached for 5 minutes to improve performance.

