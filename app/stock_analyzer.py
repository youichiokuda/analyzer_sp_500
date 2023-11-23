import yfinance as yf
import pandas as pd
import pandas_datareader as pdr
from datetime import datetime, timedelta
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor
import os

# ユーザー入力
days = int(input('何日さかのぼる?'))
drop = int(input('下落率は？'))
jump = int(input('上昇率は?'))
pernumber = int(input('PERは幾つ以下にする？'))

# 日付設定
end_date = datetime.now()
start_date = end_date - timedelta(days=days)

# S&P 500株のリストを取得またはキャッシュから読み込み
sp500_url = 'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies'
sp500_file = 'sp500_tickers.csv'

if os.path.exists(sp500_file):
    sp500_tickers = pd.read_csv(sp500_file)['Symbol'].tolist()
else:
    sp500_table = pd.read_html(sp500_url)
    sp500_tickers = sp500_table[0]['Symbol'].tolist()
    pd.DataFrame(sp500_tickers, columns=['Symbol']).to_csv(sp500_file, index=False)

# 株価の分析とPER取得を行う関数
def analyze_stock(ticker):
    try:
        stock = yf.Ticker(ticker)
        stock_data = stock.history(start=start_date, end=end_date)

        if stock_data.empty:
            return None

        high_price = stock_data['High'].max()
        low_price = stock_data['Low'].min()
        current_price = stock_data['Close'].iloc[-1]

        drop_percentage = ((high_price - low_price) / high_price) * 100
        recovery_percentage = ((current_price - low_price) / low_price) * 100

        # PERデータの取得
        per_data = pdr.get_quote_yahoo(ticker)['trailingPE']
        per = per_data[ticker]

        if drop_percentage >= drop and recovery_percentage >= jump and per <= pernumber:
            # 企業概要とYahoo FinanceのURLを取得
            company_info = stock.info.get('longBusinessSummary', '情報なし')
            yahoo_finance_url = f"https://finance.yahoo.com/quote/{ticker}"
            return ticker, per, company_info, yahoo_finance_url
        else:
            return None
    except Exception as e:
        return None

# 並列処理で株価の分析を行う関数
def analyze_stocks(tickers):
    with ThreadPoolExecutor(max_workers=10) as executor:
        results = list(tqdm(executor.map(analyze_stock, tickers), total=len(tickers)))
    return [result for result in results if result is not None]

# 条件に合致する株を探す
matching_stocks = analyze_stocks(sp500_tickers)

# 結果の表示
print(matching_stocks)

# CSVファイルに保存
if matching_stocks:
    df = pd.DataFrame(matching_stocks, columns=['Ticker', 'PER', 'CompanyInfo', 'YahooFinanceURL'])
    df.to_csv('matching_stocks.csv', index=False)
    print("結果を 'matching_stocks.csv' に保存しました。")
else:
    print("条件に合致する株が見つかりませんでした。")
