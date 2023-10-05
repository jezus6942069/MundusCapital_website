from flask import Flask, render_template
import time
from flask_socketio import SocketIO, emit
import threading

# Import functions from yfinance_data
from yfinance_data import fetch_prices, STOCKS, COMMODITIES, ETFS, FOREX, BONDS, CRYPTOS
from news import fetch_bloomberg_news

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")  

CACHE_TIMEOUT = 1000
cache = {}

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
    news_data = fetch_bloomberg_news()
    return render_template('index.html', 
                           news=news_data,
                           stocks=cache.get('stocks', {}), 
                           commodities=cache.get('commodities', {}),
                           etfs=cache.get('etfs', {}),
                           forex=cache.get('forex', {}),
                           bonds=cache.get('bonds', {}),
                           cryptos=cache.get('cryptos', {}))


@socketio.on('request_data')
def send_current_data():
    emit('data_update', cache)

if __name__ == "__main__":
    thread = threading.Thread(target=background_task)
    thread.start()
    socketio.run(app, debug=True)
