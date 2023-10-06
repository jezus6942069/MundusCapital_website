# news.py

import requests

API_KEY = 'ab7081e129c2494cb72552366d3f7b23'  # Replace with your actual API key

def fetch_bloomberg_news():
    endpoint = 'https://newsapi.org/v2/top-headlines'
    parameters = {
        'apiKey': API_KEY,
        'sources': 'bloomberg',  # Specify Bloomberg as the source
        'pageSize': 1  # Fetch the latest 10 articles (change this as needed)
    }
    
    response = requests.get(endpoint, params=parameters)
    data = response.json()

    articles = []

    if response.status_code == 200 and data['status'] == 'ok':
        for article in data['articles']:
            articles.append({
                'title': article['title'],
                'description': article['description'],
                'url': article['url'],
                'thumbnail': article['urlToImage']  # Thumbnail URL
            })
    else:
        print("Error fetching news:", data.get('message'))

    return articles