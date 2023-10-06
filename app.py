from flask import Flask, render_template
import time
from flask_socketio import SocketIO, emit
import threading
from flask import Flask, request, redirect, url_for, flash
from flask import jsonify

# Import functions from yfinance_data
from fetch_data.yfinance_data import fetch_prices, STOCKS, COMMODITIES, ETFS, FOREX, BONDS, CRYPTOS
from fetch_data.news import fetch_bloomberg_news

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


@app.route('/home')  
def home():
    news_data = fetch_bloomberg_news()
    return render_template('home.html', 
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

@app.route('/search')
def search():
    query = request.args.get('query').upper()
    return jsonify({
        'results': [
            {'text': f'{query}', 'url': f'https://finance.yahoo.com/quote/{query}'},
        ]
    })

@app.route('/submit_email', methods=['POST'])
def submit_email():
    user_email = request.form['user_email']
    print("Received email:", user_email)
    flash('Email received successfully!', 'success')
    return redirect(url_for('home'))  

@app.route('/home')
def home_redirect():
    return render_template('home.html')

@app.route('/news')
def news():
    return render_template('news.html')

@app.route('/stocks')
def stocks():
    return render_template('stocks.html')

@app.route('/etfs')
def etfs():
    return render_template('etfs.html')

@app.route('/crypto')
def crypto():
    return render_template('crypto.html')

@app.route('/futures')
def futures():
    return render_template('futures.html')

@app.route('/bonds')
def bonds():
    return render_template('bonds.html')

@app.route('/forex')
def forex():
    return render_template('forex.html')

@app.route('/screener')
def screener():
    return render_template('screener.html')

@app.route('/portfolio')
def portfolio():
    return render_template('portfolio.html')

@app.route('/insider')
def insider():
    return render_template('insider.html')

@app.route('/maps')
def maps():
    return render_template('maps.html')

@app.route('/profile')
def profile():
    return render_template('profile.html')

if __name__ == "__main__":
    thread = threading.Thread(target=background_task)
    thread.start()
    socketio.run(app, debug=True)

