import yfinance as yf

STOCKS = ["AAPL"]
COMMODITIES = ["GC=F", ]  
ETFS = ["SPY"]
FOREX = ["EURUSD=X"]
BONDS = ["^TNX" ]  
CRYPTOS = ["BTC-USD"]  

def fetch_prices(tickers):
    data = yf.download(tickers, period="1d")
    closing_prices = data['Close']
    opening_prices = data['Open']

    price_data = {}
    for ticker in tickers:
        # Check if we're dealing with a single ticker or multiple tickers
        if len(tickers) == 1:
            close_price = closing_prices.iloc[0]
            open_price = opening_prices.iloc[0]
        else:
            close_price = closing_prices[ticker].iloc[0]
            open_price = opening_prices[ticker].iloc[0]

        difference = close_price - open_price

        color = "white"
        if difference > 0:
            color = "green"
        elif difference < 0:
            color = "red"

        price_data[ticker] = {
            "price": f"{close_price:.2f}",
            "color": color
        }

    return price_data