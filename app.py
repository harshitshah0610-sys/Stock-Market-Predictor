from flask import Flask, jsonify, render_template, request
from flask_cors import CORS
import random
from datetime import datetime, timedelta
import yfinance as yf

app = Flask(__name__)
CORS(app)

# Major US Stocks
US_STOCKS = {
    'AAPL': {'name': 'Apple Inc.', 'yahoo_symbol': 'AAPL', 'exchange': 'NASDAQ'},
    'GOOGL': {'name': 'Alphabet Inc.', 'yahoo_symbol': 'GOOGL', 'exchange': 'NASDAQ'},
    'MSFT': {'name': 'Microsoft Corp.', 'yahoo_symbol': 'MSFT', 'exchange': 'NASDAQ'},
    'AMZN': {'name': 'Amazon.com Inc.', 'yahoo_symbol': 'AMZN', 'exchange': 'NASDAQ'},
    'TSLA': {'name': 'Tesla Inc.', 'yahoo_symbol': 'TSLA', 'exchange': 'NASDAQ'},
    'NVDA': {'name': 'NVIDIA Corp.', 'yahoo_symbol': 'NVDA', 'exchange': 'NASDAQ'},
    'META': {'name': 'Meta Platforms', 'yahoo_symbol': 'META', 'exchange': 'NASDAQ'},
    'JPM': {'name': 'JPMorgan Chase', 'yahoo_symbol': 'JPM', 'exchange': 'NYSE'},
    'V': {'name': 'Visa Inc.', 'yahoo_symbol': 'V', 'exchange': 'NYSE'},
    'JNJ': {'name': 'Johnson & Johnson', 'yahoo_symbol': 'JNJ', 'exchange': 'NYSE'},
    'WMT': {'name': 'Walmart Inc.', 'yahoo_symbol': 'WMT', 'exchange': 'NYSE'},
    'PG': {'name': 'Procter & Gamble', 'yahoo_symbol': 'PG', 'exchange': 'NYSE'},
    'UNH': {'name': 'UnitedHealth Group', 'yahoo_symbol': 'UNH', 'exchange': 'NYSE'},
    'HD': {'name': 'Home Depot', 'yahoo_symbol': 'HD', 'exchange': 'NYSE'},
    'MA': {'name': 'Mastercard Inc.', 'yahoo_symbol': 'MA', 'exchange': 'NYSE'},
    'DIS': {'name': 'Walt Disney Co.', 'yahoo_symbol': 'DIS', 'exchange': 'NYSE'},
    'NFLX': {'name': 'Netflix Inc.', 'yahoo_symbol': 'NFLX', 'exchange': 'NASDAQ'},
    'ADBE': {'name': 'Adobe Inc.', 'yahoo_symbol': 'ADBE', 'exchange': 'NASDAQ'},
    'CRM': {'name': 'Salesforce Inc.', 'yahoo_symbol': 'CRM', 'exchange': 'NYSE'},
    'INTC': {'name': 'Intel Corp.', 'yahoo_symbol': 'INTC', 'exchange': 'NASDAQ'},
    'AMD': {'name': 'Advanced Micro Devices', 'yahoo_symbol': 'AMD', 'exchange': 'NASDAQ'},
    'CSCO': {'name': 'Cisco Systems', 'yahoo_symbol': 'CSCO', 'exchange': 'NASDAQ'},
    'PEP': {'name': 'PepsiCo Inc.', 'yahoo_symbol': 'PEP', 'exchange': 'NASDAQ'},
    'KO': {'name': 'Coca-Cola Co.', 'yahoo_symbol': 'KO', 'exchange': 'NYSE'},
    'NKE': {'name': 'Nike Inc.', 'yahoo_symbol': 'NKE', 'exchange': 'NYSE'},
    'BA': {'name': 'Boeing Co.', 'yahoo_symbol': 'BA', 'exchange': 'NYSE'}
}

# Major NSE (India) Stocks - Use .NS suffix for Yahoo Finance
NSE_STOCKS = {
    'RELIANCE': {'name': 'Reliance Industries Ltd.', 'yahoo_symbol': 'RELIANCE.NS', 'exchange': 'NSE'},
    'TCS': {'name': 'Tata Consultancy Services', 'yahoo_symbol': 'TCS.NS', 'exchange': 'NSE'},
    'HDFCBANK': {'name': 'HDFC Bank Ltd.', 'yahoo_symbol': 'HDFCBANK.NS', 'exchange': 'NSE'},
    'BHARTIARTL': {'name': 'Bharti Airtel Ltd.', 'yahoo_symbol': 'BHARTIARTL.NS', 'exchange': 'NSE'},
    'ICICIBANK': {'name': 'ICICI Bank Ltd.', 'yahoo_symbol': 'ICICIBANK.NS', 'exchange': 'NSE'},
    'SBIN': {'name': 'State Bank of India', 'yahoo_symbol': 'SBIN.NS', 'exchange': 'NSE'},
    'WIPRO': {'name': 'Wipro Ltd.', 'yahoo_symbol': 'WIPRO.NS', 'exchange': 'NSE'},
    'HINDUNILVR': {'name': 'Hindustan Unilever Ltd.', 'yahoo_symbol': 'HINDUNILVR.NS', 'exchange': 'NSE'},
    'INFOSYS': {'name': 'Infosys Ltd.', 'yahoo_symbol': 'INFY.NS', 'exchange': 'NSE'},
    'LT': {'name': 'Larsen & Toubro Ltd.', 'yahoo_symbol': 'LT.NS', 'exchange': 'NSE'},
    'SUNPHARMA': {'name': 'Sun Pharmaceutical', 'yahoo_symbol': 'SUNPHARMA.NS', 'exchange': 'NSE'},
    'MARUTI': {'name': 'Maruti Suzuki India', 'yahoo_symbol': 'MARUTI.NS', 'exchange': 'NSE'},
    'TITAN': {'name': 'Titan Company Ltd.', 'yahoo_symbol': 'TITAN.NS', 'exchange': 'NSE'},
    'BAJFINANCE': {'name': 'Bajaj Finance Ltd.', 'yahoo_symbol': 'BAJFINANCE.NS', 'exchange': 'NSE'},
    'NTPC': {'name': 'NTPC Ltd.', 'yahoo_symbol': 'NTPC.NS', 'exchange': 'NSE'},
    'POWERGRID': {'name': 'Power Grid Corp.', 'yahoo_symbol': 'POWERGRID.NS', 'exchange': 'NSE'},
    'KOTAKBANK': {'name': 'Kotak Mahindra Bank', 'yahoo_symbol': 'KOTAKBANK.NS', 'exchange': 'NSE'},
    'AXISBANK': {'name': 'Axis Bank Ltd.', 'yahoo_symbol': 'AXISBANK.NS', 'exchange': 'NSE'},
    'ADANIPORTS': {'name': 'Adani Ports & SEZ', 'yahoo_symbol': 'ADANIPORTS.NS', 'exchange': 'NSE'},
    'ASIANPAINT': {'name': 'Asian Paints Ltd.', 'yahoo_symbol': 'ASIANPAINT.NS', 'exchange': 'NSE'},
    'SHRIRAMFIN': {'name': 'Shriram Finance', 'yahoo_symbol': 'SHRIRAMFIN.NS', 'exchange': 'NSE'},
    'DLF': {'name': 'DLF Ltd.', 'yahoo_symbol': 'DLF.NS', 'exchange': 'NSE'},
    'GRASIM': {'name': 'Grasim Industries', 'yahoo_symbol': 'GRASIM.NS', 'exchange': 'NSE'},
    'ADANIGREEN': {'name': 'Adani Green Energy', 'yahoo_symbol': 'ADANIGREEN.NS', 'exchange': 'NSE'},
    'ADANIENSOL': {'name': 'Adani Energy Solutions', 'yahoo_symbol': 'ADANIENSOL.NS', 'exchange': 'NSE'}
}

# Major BSE (India) Stocks - Use .BO suffix for Yahoo Finance
BSE_STOCKS = {
    'BSE': {'name': 'BSE Ltd.', 'yahoo_symbol': 'BSE.BO', 'exchange': 'BSE'},
    'COALINDIA': {'name': 'Coal India Ltd.', 'yahoo_symbol': 'COALINDIA.BO', 'exchange': 'BSE'},
    'ONGC': {'name': 'Oil & Natural Gas Corp.', 'yahoo_symbol': 'ONGC.BO', 'exchange': 'BSE'},
    'TATASTEEL': {'name': 'Tata Steel Ltd.', 'yahoo_symbol': 'TATASTEEL.BO', 'exchange': 'BSE'},
    'JSWSTEEL': {'name': 'JSW Steel Ltd.', 'yahoo_symbol': 'JSWSTEEL.BO', 'exchange': 'BSE'},
    'HINDZINC': {'name': 'Hindustan Zinc Ltd.', 'yahoo_symbol': 'HINDZINC.BO', 'exchange': 'BSE'},
    'VEDL': {'name': 'Vedanta Ltd.', 'yahoo_symbol': 'VEDL.BO', 'exchange': 'BSE'},
    'TATAMOTORS': {'name': 'Tata Motors Ltd.', 'yahoo_symbol': 'TATAMOTORS.BO', 'exchange': 'BSE'},
    'ITC': {'name': 'ITC Ltd.', 'yahoo_symbol': 'ITC.BO', 'exchange': 'BSE'},
    'EICHERMOT': {'name': 'Eicher Motors Ltd.', 'yahoo_symbol': 'EICHERMOT.BO', 'exchange': 'BSE'}
}

# Combine all stocks
ALL_STOCKS = {**US_STOCKS, **NSE_STOCKS, **BSE_STOCKS}

# Event databases
WAR_EVENTS = [
    {'id': 1, 'title': 'Israel-Hamas Conflict', 'location': 'Middle East', 'intensity': 0.7, 'impact': 'negative'},
    {'id': 2, 'title': 'Russia-Ukraine War', 'location': 'Europe', 'intensity': 0.6, 'impact': 'negative'},
    {'id': 3, 'title': 'US-China Tensions', 'location': 'Global', 'intensity': 0.5, 'impact': 'negative'},
    {'id': 4, 'title': 'India-Pakistan Standoff', 'location': 'South Asia', 'intensity': 0.3, 'impact': 'negative'},
    {'id': 5, 'title': 'Taiwan Strait Crisis', 'location': 'Asia Pacific', 'intensity': 0.8, 'impact': 'negative'}
]

TECH_EVENTS = [
    {'id': 1, 'title': 'AI Breakthrough - GPT-5', 'category': 'AI', 'intensity': 0.9, 'impact': 'positive'},
    {'id': 2, 'title': 'Quantum Computing Milestone', 'category': 'Computing', 'intensity': 0.7, 'impact': 'positive'},
    {'id': 3, 'title': 'Chip Export Restrictions', 'category': 'Semiconductors', 'intensity': 0.8, 'impact': 'negative'},
    {'id': 4, 'title': 'Apple Product Launch', 'category': 'Consumer', 'intensity': 0.6, 'impact': 'positive'},
    {'id': 5, 'title': 'Tesla Autopilot Update', 'category': 'Automotive', 'intensity': 0.5, 'impact': 'positive'},
    {'id': 6, 'title': 'Cloud Computing Expansion', 'category': 'Infrastructure', 'intensity': 0.7, 'impact': 'positive'}
]

RESOURCE_SCARcity = [
    {'id': 1, 'name': 'Crude Oil (WTI)', 'shortage_level': 0.6, 'unit': '$78.45/bbl', 'trend': 'rising', 'price': 78.45},
    {'id': 2, 'name': 'Natural Gas', 'shortage_level': 0.5, 'unit': '$2.85/MMBtu', 'trend': 'rising', 'price': 2.85},
    {'id': 3, 'name': 'Semiconductors', 'shortage_level': 0.7, 'unit': 'chips', 'trend': 'stable', 'price': 0},
    {'id': 4, 'name': 'Lithium', 'shortage_level': 0.8, 'unit': '$22,500/mt', 'trend': 'rising', 'price': 22500},
    {'id': 5, 'name': 'Rare Earth Metals', 'shortage_level': 0.65, 'unit': '$150/kg', 'trend': 'rising', 'price': 150},
    {'id': 6, 'name': 'Copper', 'shortage_level': 0.4, 'unit': '$4.25/lb', 'trend': 'rising', 'price': 4.25},
    {'id': 7, 'name': 'Gold', 'shortage_level': 0.3, 'unit': '$2,340/oz', 'trend': 'stable', 'price': 2340},
    {'id': 8, 'name': 'Wheat', 'shortage_level': 0.55, 'unit': '$5.65/bushel', 'trend': 'rising', 'price': 5.65}
]

NATURAL_EVENTS = [
    {'id': 1, 'title': 'Hurricane Season Active', 'location': 'Atlantic', 'severity': 0.6, 'type': 'weather'},
    {'id': 2, 'title': 'California Drought', 'location': 'USA', 'severity': 0.7, 'type': 'climate'},
    {'id': 3, 'title': 'Japan Earthquake Warning', 'location': 'Japan', 'severity': 0.4, 'type': 'geological'},
    {'id': 4, 'title': 'European Flooding', 'location': 'Europe', 'severity': 0.5, 'type': 'weather'},
    {'id': 5, 'title': 'Australian Wildfires', 'location': 'Australia', 'severity': 0.6, 'type': 'climate'}
]

# Cache for stock data
stock_cache = {}
cache_timeout = 300  # 5 minutes

def fetch_real_stock_data(symbol, period='1mo'):
    """Fetch real stock data from Yahoo Finance"""
    try:
        ticker = yf.Ticker(symbol)
        hist = ticker.history(period=period)
        
        if hist.empty:
            return None
        
        data = []
        for idx, row in hist.iterrows():
            data.append({
                'date': idx.strftime('%Y-%m-%d'),
                'open': round(row['Open'], 2),
                'high': round(row['High'], 2),
                'low': round(row['Low'], 2),
                'close': round(row['Close'], 2),
                'volume': int(row['Volume'])
            })
        
        return data
    except Exception as e:
        print(f"Error fetching data for {symbol}: {e}")
        return None

def fetch_current_price(symbol):
    """Fetch current stock price from Yahoo Finance"""
    try:
        ticker = yf.Ticker(symbol)
        info = ticker.info
        if 'currentPrice' in info:
            return info['currentPrice']
        elif 'regularMarketPrice' in info:
            return info['regularMarketPrice']
        else:
            # Try getting from history
            hist = ticker.history(period='1d')
            if not hist.empty:
                return round(hist['Close'].iloc[-1], 2)
        return None
    except Exception as e:
        print(f"Error fetching price for {symbol}: {e}")
        return None

def calculate_probability_factors(stock_symbol):
    """Calculate probability factors based on various events"""
    factors = {
        'war_impact': 0,
        'tech_impact': 0,
        'resource_impact': 0,
        'natural_impact': 0,
        'sentiment': 0
    }
    
    # War events impact (typically negative)
    war_impact = sum([e['intensity'] * -0.15 for e in WAR_EVENTS[:3]])
    factors['war_impact'] = war_impact
    
    # Tech events impact (typically positive for tech stocks)
    tech_stocks = ['AAPL', 'GOOGL', 'MSFT', 'NVDA', 'META', 'TSLA', 'AMZN', 'INFY', 'TCS', 'WIPRO', 'INFO', 'ADBE', 'CRM']
    if stock_symbol in tech_stocks:
        tech_impact = sum([e['intensity'] * 0.12 for e in TECH_EVENTS if e['impact'] == 'positive'])
        tech_impact += sum([e['intensity'] * -0.08 for e in TECH_EVENTS if e['impact'] == 'negative'])
    else:
        tech_impact = sum([e['intensity'] * 0.05 for e in TECH_EVENTS if e['impact'] == 'positive'])
    factors['tech_impact'] = tech_impact
    
    # Resource scarcity impact
    avg_scarcity = sum([r['shortage_level'] for r in RESOURCE_SCARcity]) / len(RESOURCE_SCARcity)
    factors['resource_impact'] = avg_scarcity * -0.08
    
    # Natural events impact
    natural_impact = sum([e['severity'] * -0.05 for e in NATURAL_EVENTS])
    factors['natural_impact'] = natural_impact
    
    # Overall market sentiment
    factors['sentiment'] = (factors['tech_impact'] + factors['war_impact'] + 
                          factors['resource_impact'] + factors['natural_impact'])
    
    return factors

def generate_prediction(stock_symbol, current_price, historical_data):
    """Generate AI prediction based on factors"""
    factors = calculate_probability_factors(stock_symbol)
    
    if not historical_data or current_price is None:
        return None
    
    last_price = current_price
    base_change = factors['sentiment']
    
    # Generate predictions for next 7 days
    predictions = []
    current_pred = last_price
    
    for i in range(7):
        day_change = base_change + random.uniform(-0.02, 0.02)
        current_pred = current_pred * (1 + day_change)
        
        predictions.append({
            'day': i + 1,
            'predicted_price': round(current_pred, 2),
            'confidence': round(75 + factors['sentiment'] * 20, 1),
            'direction': 'up' if day_change > 0 else 'down'
        })
    
    # Calculate overall probability
    prob_up = 50 + (factors['sentiment'] * 100)
    prob_up = max(15, min(85, prob_up))  # Clamp between 15-85%
    
    return {
        'probability_up': round(prob_up, 1),
        'probability_down': round(100 - prob_up, 1),
        'factors': factors,
        'predictions': predictions,
        'prediction_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/stocks')
def get_stocks():
    """Get list of all available stocks"""
    stock_list = {'US': {}, 'NSE': {}, 'BSE': {}}
    
    for symbol, info in US_STOCKS.items():
        stock_list['US'][symbol] = {'name': info['name'], 'exchange': info['exchange']}
    
    for symbol, info in NSE_STOCKS.items():
        stock_list['NSE'][symbol] = {'name': info['name'], 'exchange': info['exchange']}
    
    for symbol, info in BSE_STOCKS.items():
        stock_list['BSE'][symbol] = {'name': info['name'], 'exchange': info['exchange']}
    
    return jsonify(stock_list)

@app.route('/api/stock/<symbol>')
def get_stock(symbol):
    # Get timeframe parameter (default: 1mo)
    timeframe = request.args.get('period', '1mo')
    symbol = symbol.upper()
    
    # Validate timeframe
    valid_periods = ['1d', '5d', '1wk', '1mo', '3mo', '6mo', '1y', '2y', '5y', '10y', 'ytd', 'max']
    if timeframe not in valid_periods:
        timeframe = '1mo'
    
    # Map frontend timeframes to Yahoo Finance periods
    period_map = {
        '1D': '1d',
        '5D': '5d',
        '1W': '1wk',
        '1M': '1mo',
        '3M': '3mo',
        '6M': '6mo',
        '1Y': '1y',
        '2Y': '2y',
        '5Y': '5y'
    }
    yahoo_period = period_map.get(timeframe, timeframe)
    
    # Check if stock exists in any category
    stock_info = None
    if symbol in US_STOCKS:
        stock_info = US_STOCKS[symbol]
    elif symbol in NSE_STOCKS:
        stock_info = NSE_STOCKS[symbol]
    elif symbol in BSE_STOCKS:
        stock_info = BSE_STOCKS[symbol]
    
    if not stock_info:
        return jsonify({'error': 'Stock not found'}), 404
    
    # Fetch real data from Yahoo Finance
    yahoo_symbol = stock_info['yahoo_symbol']
    
    # Check cache with timeframe key
    cache_key = f"{yahoo_symbol}_{yahoo_period}"
    if cache_key in stock_cache:
        cached_data, timestamp = stock_cache[cache_key]
        if (datetime.now() - timestamp).total_seconds() < cache_timeout:
            return cached_data
    
    historical = fetch_real_stock_data(yahoo_symbol, period=yahoo_period)
    current_price = fetch_current_price(yahoo_symbol)
    
    if historical is None:
        current_price = 100.0
        historical = []
    
    if current_price is None:
        current_price = 100.0
    
    prediction = generate_prediction(symbol, current_price, historical)
    
    response_data = {
        'symbol': symbol,
        'name': stock_info['name'],
        'exchange': stock_info['exchange'],
        'current_price': current_price,
        'current_price_formatted': f"${current_price:.2f}" if stock_info['exchange'] != 'NSE' and stock_info['exchange'] != 'BSE' else f"₹{current_price:.2f}",
        'historical': historical,
        'prediction': prediction,
        'period': timeframe
    }
    
    # Cache the response
    stock_cache[cache_key] = (response_data, datetime.now())
    
    return jsonify(response_data)

@app.route('/api/stock/<symbol>/info')
def get_stock_info(symbol):
    """Get detailed stock info"""
    symbol = symbol.upper()
    
    stock_info = None
    if symbol in US_STOCKS:
        stock_info = US_STOCKS[symbol]
    elif symbol in NSE_STOCKS:
        stock_info = NSE_STOCKS[symbol]
    elif symbol in BSE_STOCKS:
        stock_info = BSE_STOCKS[symbol]
    
    if not stock_info:
        return jsonify({'error': 'Stock not found'}), 404
    
    return jsonify(stock_info)

@app.route('/api/events/war')
def get_war_events():
    return jsonify(WAR_EVENTS)

@app.route('/api/events/tech')
def get_tech_events():
    return jsonify(TECH_EVENTS)

@app.route('/api/events/resources')
def get_resource_events():
    return jsonify(RESOURCE_SCARcity)

@app.route('/api/events/natural')
def get_natural_events():
    return jsonify(NATURAL_EVENTS)

@app.route('/api/events/all')
def get_all_events():
    return jsonify({
        'war': WAR_EVENTS,
        'tech': TECH_EVENTS,
        'resources': RESOURCE_SCARcity,
        'natural': NATURAL_EVENTS
    })

@app.route('/api/market/sentiment')
def get_market_sentiment():
    """Get overall market sentiment"""
    factors = calculate_probability_factors('AAPL')
    
    sentiment_score = factors['sentiment'] * 100 + 50
    
    # Get market indices
    try:
        spy = yf.Ticker("SPY")
        spy_hist = spy.history(period="5d")
        sp_change = 0
        if not spy_hist.empty:
            sp_change = ((spy_hist['Close'].iloc[-1] - spy_hist['Close'].iloc[0]) / spy_hist['Close'].iloc[0]) * 100
    except:
        sp_change = 0
    
    return jsonify({
        'overall_sentiment': round(sentiment_score, 1),
        'interpretation': 'bullish' if sentiment_score > 55 else 'bearish' if sentiment_score < 45 else 'neutral',
        'volatility_index': round(random.uniform(15, 35), 1),
        'fear_greed_index': round(random.uniform(30, 70), 1),
        'sp500_change': round(sp_change, 2),
        'last_updated': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    })

@app.route('/api/search/<query>')
def search_stocks(query):
    """Search stocks by name or symbol"""
    query = query.upper()
    results = []
    
    for symbol, info in ALL_STOCKS.items():
        if query in symbol or query in info['name'].upper():
            results.append({
                'symbol': symbol,
                'name': info['name'],
                'exchange': info['exchange']
            })
    
    return jsonify(results[:20])

@app.route('/api/price/<symbol>')
def get_realtime_price(symbol):
    """Get real-time price for a single stock - optimized for fast polling (every second)"""
    symbol = symbol.upper()
    
    # Check if stock exists
    stock_info = None
    if symbol in US_STOCKS:
        stock_info = US_STOCKS[symbol]
    elif symbol in NSE_STOCKS:
        stock_info = NSE_STOCKS[symbol]
    elif symbol in BSE_STOCKS:
        stock_info = BSE_STOCKS[symbol]
    
    if not stock_info:
        return jsonify({'error': 'Stock not found'}), 404
    
    # Fast price fetch
    yahoo_symbol = stock_info['yahoo_symbol']
    current_price = fetch_current_price(yahoo_symbol)
    
    if current_price is None:
        return jsonify({'error': 'Could not fetch price'}), 500
    
    # Get market status
    is_market_open = is_indian_market_open() if stock_info['exchange'] in ['NSE', 'BSE'] else is_us_market_open()
    
    return jsonify({
        'symbol': symbol,
        'exchange': stock_info['exchange'],
        'current_price': current_price,
        'current_price_formatted': f"${current_price:.2f}" if stock_info['exchange'] not in ['NSE', 'BSE'] else f"₹{current_price:.2f}",
        'is_market_open': is_market_open,
        'last_updated': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    })

@app.route('/api/market/status')
def get_market_status():
    """Get current market status for all exchanges"""
    return jsonify({
        'us': is_us_market_open(),
        'nse': is_indian_market_open(),
        'bse': is_indian_market_open(),
        'current_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'ist_time': get_indian_time()
    })

def is_indian_market_open():
    """Check if Indian market (NSE/BSE) is open"""
    try:
        # Get current time in IST
        ist = get_indian_time()
        hour = ist.hour
        minute = ist.minute
        weekday = ist.weekday()
        
        # NSE/BSE Market Hours: 9:15 AM - 3:30 PM IST, Mon-Fri
        if weekday >= 5:
            return False
        
        market_open = (hour > 9) or (hour == 9 and minute >= 15)
        market_close = (hour < 15) or (hour == 15 and minute < 30)
        
        return market_open and market_close
    except:
        return False

def is_us_market_open():
    """Check if US market is open"""
    try:
        import pytz
        now_utc = datetime.now(pytz.UTC)
        est = pytz.timezone('US/Eastern')
        now_est = now_utc.astimezone(est)
        
        hour = now_est.hour
        minute = now_est.minute
        weekday = now_est.weekday()
        
        if weekday >= 5:
            return False
        
        market_open = (hour > 9) or (hour == 9 and minute >= 30)
        market_close = hour < 16
        
        return market_open and market_close
    except:
        now = datetime.now()
        return now.weekday() < 5 and 9 <= now.hour < 16

def get_indian_time():
    """Get current Indian Standard Time"""
    try:
        import pytz
        ist = pytz.timezone('Asia/Kolkata')
        return datetime.now(ist)
    except:
        return datetime.now() + timedelta(hours=5, minutes=30)

if __name__ == '__main__':
    app.run(debug=True, port=5000, host='0.0.0.0')

