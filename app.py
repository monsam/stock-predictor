from flask import Flask, render_template, jsonify
import yfinance as yf
import numpy as np
from textblob import TextBlob
import requests
import os
from dotenv import load_dotenv
import ta
from datetime import datetime, timedelta
import time
import pandas as pd
import warnings

# Suppress RuntimeWarnings from technical analysis library
warnings.filterwarnings('ignore', category=RuntimeWarning, module='ta')

app = Flask(__name__)
load_dotenv()

# Enable CORS
@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response

# List of stocks to analyze
STOCKS = [
    {'symbol': 'AAPL', 'name': 'Apple Inc.'},
    {'symbol': 'MSFT', 'name': 'Microsoft Corporation'},
    {'symbol': 'GOOGL', 'name': 'Alphabet Inc.'},
    {'symbol': 'AMZN', 'name': 'Amazon.com Inc.'},
    {'symbol': 'NVDA', 'name': 'NVIDIA Corporation'},
    {'symbol': 'META', 'name': 'Meta Platforms Inc.'},
    {'symbol': 'TSLA', 'name': 'Tesla Inc.'},
    {'symbol': 'JPM', 'name': 'JPMorgan Chase & Co.'},
    {'symbol': 'V', 'name': 'Visa Inc.'},
    {'symbol': 'WMT', 'name': 'Walmart Inc.'}
]

def get_technical_indicators(data):
    """Calculate technical indicators for the stock"""
    try:
        # Check if we have enough data points
        if len(data) < 20:  # Need at least 20 data points for reliable indicators
            print(f"Not enough data points ({len(data)}) for technical indicators")
            return None
        
        # Clean the data by removing any NaN values
        data_clean = data.dropna()
        if len(data_clean) < 20:
            print(f"Not enough clean data points ({len(data_clean)}) for technical indicators")
            return None
        
        # Calculate RSI
        try:
            rsi = ta.momentum.RSIIndicator(data_clean['Close']).rsi().iloc[-1]
            if pd.isna(rsi):
                rsi = 50  # Default neutral value
        except Exception:
            rsi = 50
        
        # Calculate MACD
        try:
            macd = ta.trend.MACD(data_clean['Close'])
            macd_line = macd.macd().iloc[-1]
            if pd.isna(macd_line):
                macd_line = 0
        except Exception:
            macd_line = 0
        
        # Calculate Bollinger Bands
        try:
            bollinger = ta.volatility.BollingerBands(data_clean['Close'])
            upper_band = bollinger.bollinger_hband().iloc[-1]
            lower_band = bollinger.bollinger_lband().iloc[-1]
            if pd.isna(upper_band) or pd.isna(lower_band):
                upper_band = data_clean['Close'].iloc[-1] * 1.02
                lower_band = data_clean['Close'].iloc[-1] * 0.98
        except Exception:
            upper_band = data_clean['Close'].iloc[-1] * 1.02
            lower_band = data_clean['Close'].iloc[-1] * 0.98
        
        # Calculate ADX (requires more data points)
        try:
            # Ensure we have enough data for ADX calculation (typically needs 14+ periods)
            if len(data_clean) >= 14:
                adx_indicator = ta.trend.ADXIndicator(data_clean['High'], data_clean['Low'], data_clean['Close'])
                adx_series = adx_indicator.adx()
                # Get the last valid ADX value
                adx = adx_series.dropna().iloc[-1] if not adx_series.dropna().empty else 50
                if pd.isna(adx) or adx <= 0:
                    adx = 50  # Default neutral value if calculation fails
            else:
                adx = 50  # Not enough data for ADX
        except (IndexError, ValueError, Exception) as e:
            print(f"ADX calculation error: {e}")
            adx = 50  # Default neutral value if calculation fails
        
        # Calculate OBV
        try:
            obv = ta.volume.OnBalanceVolumeIndicator(data_clean['Close'], data_clean['Volume']).on_balance_volume().iloc[-1]
            if pd.isna(obv):
                obv = 0  # Default value if calculation fails
        except (IndexError, ValueError, Exception):
            obv = 0  # Default value if calculation fails
        
        return {
            'rsi': float(rsi),
            'macd': float(macd_line),
            'upper_band': float(upper_band),
            'lower_band': float(lower_band),
            'adx': float(adx),
            'obv': float(obv)
        }
    except Exception as e:
        print(f"Error calculating technical indicators: {str(e)}")
        return None

def get_news_sentiment(symbol):
    """Get news sentiment for the stock"""
    try:
        news_api_key = os.getenv('NEWS_API_KEY')
        if not news_api_key:
            return 0.5  # Neutral sentiment if no API key
        
        url = f'https://newsapi.org/v2/everything'
        params = {
            'q': f'{symbol} stock',
            'apiKey': news_api_key,
            'language': 'en',
            'sortBy': 'publishedAt',
            'pageSize': 10
        }
        
        response = requests.get(url, params=params)
        if response.status_code != 200:
            return 0.5
        
        articles = response.json().get('articles', [])
        if not articles:
            return 0.5
        
        sentiments = []
        for article in articles:
            if article.get('description'):
                blob = TextBlob(article['description'])
                sentiments.append(blob.sentiment.polarity)
        
        return np.mean(sentiments) if sentiments else 0.5
    except Exception as e:
        print(f"Error getting news sentiment: {str(e)}")
        return 0.5

def get_stock_data(symbol):
    """Get comprehensive stock data"""
    try:
        stock = yf.Ticker(symbol)
        info = stock.info
        
        # Get historical data
        end_date = datetime.now()
        start_date = end_date - timedelta(days=60)
        hist = stock.history(start=start_date, end=end_date)
        
        if hist.empty:
            return None
        
        # Calculate technical indicators
        indicators = get_technical_indicators(hist)
        if not indicators:
            return None
        
        # Get news sentiment
        sentiment = get_news_sentiment(symbol)
        
        # Calculate price change
        current_price = hist['Close'].iloc[-1]
        prev_price = hist['Close'].iloc[-2]
        price_change = ((current_price - prev_price) / prev_price) * 100
        
        return {
            'symbol': symbol,
            'name': info.get('longName', symbol),
            'price': float(current_price),
            'change': float(price_change),
            'volume': int(hist['Volume'].iloc[-1]),
            'sector': info.get('sector', 'Unknown'),
            'industry': info.get('industry', 'Unknown'),
            'market_cap': int(info.get('marketCap', 0)),
            'pe_ratio': float(info.get('trailingPE', 0)),
            'rsi': float(indicators['rsi']),
            'macd': float(indicators['macd']),
            'sentiment': float(sentiment)
        }
    except Exception as e:
        print(f"Error getting stock data for {symbol}: {str(e)}")
        return None

def analyze_stocks():
    """Analyze stocks and return recommendations"""
    recommendations = []
    
    for stock in STOCKS:
        data = get_stock_data(stock['symbol'])
        if not data:
            continue
        
        # Calculate technical score
        technical_score = 0
        if data['rsi'] < 30:  # Oversold
            technical_score += 1
        elif data['rsi'] > 70:  # Overbought
            technical_score -= 1
        
        if data['macd'] > 0:  # Bullish MACD
            technical_score += 1
        else:  # Bearish MACD
            technical_score -= 1
        
        # Calculate sentiment score
        sentiment_score = (data['sentiment'] + 1) / 2  # Normalize to 0-1
        
        # Calculate momentum score
        momentum_score = 1 if data['change'] > 0 else 0
        
        # Calculate final score (weighted average)
        final_score = (
            technical_score * 0.4 +
            sentiment_score * 0.3 +
            momentum_score * 0.3
        )
        
        # Determine trading signal
        if final_score > 0.6:
            signal = "Strong Buy"
        elif final_score > 0.4:
            signal = "Buy"
        elif final_score < 0.4:
            signal = "Sell"
        else:
            signal = "Hold"
        
        data['signal'] = signal
        data['score'] = final_score
        recommendations.append(data)
        
        # Add a delay to avoid hitting API rate limits
        time.sleep(5)
    
    # Sort by score and return top 5
    recommendations.sort(key=lambda x: x['score'], reverse=True)
    return recommendations[:5]

def get_mock_predictions():
    """Return mock predictions when API calls fail"""
    return [
        {
            'symbol': 'AAPL',
            'name': 'Apple Inc.',
            'price': 185.92,
            'change': 1.2,
            'volume': 50000000,
            'sector': 'Technology',
            'industry': 'Consumer Electronics',
            'market_cap': 2900000000000,
            'pe_ratio': 30.5,
            'rsi': 55,
            'macd': 2.5,
            'sentiment': 0.3,
            'score': 0.75,
            'signal': 'Buy'
        },
        {
            'symbol': 'MSFT',
            'name': 'Microsoft Corporation',
            'price': 415.32,
            'change': 0.8,
            'volume': 25000000,
            'sector': 'Technology',
            'industry': 'Software',
            'market_cap': 3100000000000,
            'pe_ratio': 35.2,
            'rsi': 58,
            'macd': 3.2,
            'sentiment': 0.4,
            'score': 0.72,
            'signal': 'Buy'
        },
        {
            'symbol': 'GOOGL',
            'name': 'Alphabet Inc.',
            'price': 175.28,
            'change': -0.5,
            'volume': 15000000,
            'sector': 'Technology',
            'industry': 'Internet Services',
            'market_cap': 2200000000000,
            'pe_ratio': 28.5,
            'rsi': 45,
            'macd': -1.5,
            'sentiment': 0.2,
            'score': 0.65,
            'signal': 'Hold'
        },
        {
            'symbol': 'AMZN',
            'name': 'Amazon.com Inc.',
            'price': 178.75,
            'change': 1.5,
            'volume': 35000000,
            'sector': 'Consumer Cyclical',
            'industry': 'Internet Retail',
            'market_cap': 1850000000000,
            'pe_ratio': 60.2,
            'rsi': 62,
            'macd': 2.8,
            'sentiment': 0.35,
            'score': 0.68,
            'signal': 'Buy'
        },
        {
            'symbol': 'NVDA',
            'name': 'NVIDIA Corporation',
            'price': 950.02,
            'change': 2.1,
            'volume': 45000000,
            'sector': 'Technology',
            'industry': 'Semiconductors',
            'market_cap': 2350000000000,
            'pe_ratio': 75.5,
            'rsi': 65,
            'macd': 4.2,
            'sentiment': 0.45,
            'score': 0.80,
            'signal': 'Strong Buy'
        }
    ]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_predictions')
def get_predictions():
    try:
        recommendations = analyze_stocks()
        if not recommendations:
            print("No recommendations found, using mock data")
            return jsonify(get_mock_predictions())
        return jsonify(recommendations)
    except Exception as e:
        print(f"Error getting predictions: {str(e)}")
        print("Using mock data as fallback")
        return jsonify(get_mock_predictions())

@app.route('/get_prediction')
def get_prediction():
    return get_predictions()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5050) 