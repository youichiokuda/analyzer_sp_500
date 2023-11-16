import yfinance as yf
import pandas as pd
import pandas_datareader as pdr
from datetime import datetime, timedelta

def analyze_stock(days, drop, jump, pernumber):
    # 日付設定
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days)

    # S&P 500株のリストを取得
    sp500_url = 'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies'
    sp500_table = pd.read_html(sp500_url)
    sp500_tickers = sp500_table[0]['Symbol'].tolist()

    matching_stocks = []

    for ticker in sp500_tickers:
        try:
            stock = yf.Ticker(ticker)
            stock_data = stock.history(start=start_date, end=end_date)

            if stock_data.empty:
                continue

            high_price = stock_data['High'].max()
            low_price = stock_data['Low'].min()
            current_price = stock_data['Close'].iloc[-1]

            drop_percentage = ((high_price - low_price) / high_price) * 100
            recovery_percentage = ((current_price - low_price) / low_price) * 100

            # PERデータの取得
            per_data = pdr.get_quote_yahoo(ticker)['trailingPE']
            per = per_data[ticker]

            if drop_percentage >= drop and recovery_percentage >= jump and per <= pernumber:
                matching_stocks.append((ticker, per))
        except Exception as e:
            continue

    return matching_stocks
