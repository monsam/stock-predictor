# Stock Predictor Web Application

A Flask-based web application that provides stock predictions and analysis using technical indicators and sentiment analysis.

## Features
- Real-time stock data analysis
- Technical indicators (RSI, MACD)
- Sentiment analysis from news
- Beautiful interactive UI
- Mock predictions as fallback

## Local Development
1. Create a virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Create a `.env` file with your Alpha Vantage API key:
```
ALPHA_VANTAGE_API_KEY=your_api_key_here
```

4. Run the application:
```bash
python app.py
```

## Deployment to Render.com
1. Create a Render.com account
2. Connect your GitHub repository
3. Create a new Web Service
4. Configure the following:
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `gunicorn app:app`
   - Add environment variable: `ALPHA_VANTAGE_API_KEY`

## Environment Variables
- `ALPHA_VANTAGE_API_KEY`: Your Alpha Vantage API key

## Dependencies
- Flask
- yfinance
- pandas
- numpy
- textblob
- ta
- requests
- python-dotenv
- gunicorn 