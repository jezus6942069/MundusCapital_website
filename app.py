import yfinance as yf
from flask import Flask, render_template
import time
from flask_socketio import SocketIO, emit
import threading

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")  


STOCKS = ["AAPL"]
COMMODITIES = ["GC=F", ]  
ETFS = ["SPY"]
FOREX = ["EURUSD=X"]
BONDS = ["^TNX" ]  
CRYPTOS = ["BTC-USD"]  


CACHE_TIMEOUT = 9 
cache = {}
last_fetch_time = 0

def background_task():
    global cache
    while True:
        print("Fetching new data...")
        cache['stocks'] = fetch_prices(STOCKS)
        cache['commodities'] = fetch_prices(COMMODITIES)
        cache['etfs'] = fetch_prices(ETFS)
        cache['forex'] = fetch_prices(FOREX)
        cache['bonds'] = fetch_prices(BONDS)
        cache['cryptos'] = fetch_prices(CRYPTOS)
        print("Emitting data:", cache)
        socketio.emit('data_update', cache)
        time.sleep(CACHE_TIMEOUT)




@app.route('/')  
def index():
    return render_template('index.html', 
                           stocks=cache.get('stocks', {}), 
                           commodities=cache.get('commodities', {}),
                           etfs=cache.get('etfs', {}),
                           forex=cache.get('forex', {}),
                           bonds=cache.get('bonds', {}),
                           cryptos=cache.get('cryptos', {}))

def fetch_prices(tickers):
    data = yf.download(tickers, period="1d")
    closing_prices = data['Close']
    opening_prices = data['Open']

    price_data = {}
    print(data)
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

@socketio.on('request_data')
def send_current_data():
    emit('data_update', cache)



if __name__ == "__main__":
    thread = threading.Thread(target=background_task)
    thread.start()
    socketio.run(app, debug=True)