import requests
import pandas as pd



def load_api_key(filepath):
    """Load and return the API key from a file."""
    with open(filepath, 'r') as file:
        api_key = file.read().strip()  # .strip() removes any leading/trailing whitespace
    return api_key

def fetch_news(api_key, query):
    """Fetch news articles from the News API based on a query and date range."""
    url = 'https://newsapi.org/v2/everything'
    params = {
        'q': query,
        'apiKey': api_key,
        'sortBy': 'publishedAt',  # Sort by publication date
        'language': 'en'  # Assuming you want articles in English
    }
    response = requests.get(url, params=params)
    return response.json()


def convert_to_df(news_data):
    data = []
    for article in news_data['articles']:
        if article['title'] != "[Removed]":
            date_only = article['publishedAt'].split('T')[0]
            data.append({'title': article['title'], 'publishedAt': date_only})

    df = pd.DataFrame(data, columns=['publishedAt', 'title'])
    return df 


if __name__ == '__main__':
    api_key = load_api_key('./key/NewsAPI key.txt')
    query_word = input("Please input the keyword for article search: ")
    news_articles = fetch_news(api_key, query_word)
    news_df = convert_to_df(news_articles)
    print(news_df)


