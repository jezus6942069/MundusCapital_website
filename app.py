import yfinance as yf
from flask import Flask, render_template

app = Flask(__name__)

STOCKS = ["AAPL", "MSFT", "GOOGL", "AMZN", "FB", "TSLA", "V", "JPM", "JNJ", "WMT"]
COMMODITIES = ["GC=F", "SI=F", "CL=F", "HG=F", "ZC=F", "ZS=F", "ZW=F", "SB=F", "CC=F", "KC=F"]  # e.g., GC=F is Gold futures
ETFS = ["SPY", "IVV", "VTI", "VOO", "QQQ", "VEA", "EFA", "IEFA", "AGG", "IJH"]
FOREX = ["EURUSD=X", "USDJPY=X", "GBPUSD=X", "USDCAD=X", "USDCHF=X", "AUDUSD=X", "NZDUSD=X", "EURJPY=X", "GBPJPY=X", "EURGBP=X"]
BONDS = ["^TNX", "^TYX", "^FVX", "^IRX", "^GS2", "^GS5", "^GS10", "^GS20", "^GSPC", "^US30Y"]  
CRYPTOS = ["BTC-USD", "ETH-USD", "BNB-USD", "ADA-USD", "XRP-USD", "DOGE-USD", "DOT1-USD", "UNI3-USD", "LTC-USD", "LINK-USD"]  # Examples: Bitcoin, Ethereum, Binance Coin, etc.




@app.route('/')  
def index():
    stocks_prices = fetch_prices(STOCKS)
    commodities_prices = fetch_prices(COMMODITIES)
    etfs_prices = fetch_prices(ETFS)
    forex_prices = fetch_prices(FOREX)
    bonds_prices = fetch_prices(BONDS)
    crypto_prices = fetch_prices(CRYPTOS)
    return render_template('index.html', stocks=stocks_prices, commodities=commodities_prices, etfs=etfs_prices, forex=forex_prices, bonds=bonds_prices, cryptos=crypto_prices)

def fetch_prices(tickers):
    data = yf.download(tickers, period="1d")
    closing_prices = data['Close']
    opening_prices = data['Open']

    price_data = {}

    for ticker in tickers:
        close_price = closing_prices[ticker].iloc[0]
        open_price = opening_prices[ticker].iloc[0]
        difference = close_price - open_price

        color = "black"
        if difference > 0:
            color = "green"
        elif difference < 0:
            color = "red"

        price_data[ticker] = {
            "price": f"{close_price:.2f}",
            "color": color
        }

    return price_data

if __name__ == "__main__":
    app.run(debug=True)