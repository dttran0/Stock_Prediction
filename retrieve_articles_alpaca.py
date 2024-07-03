from alpaca_trade_api import REST, Stream
import pandas as pd
from datetime import date


def load_api_key(filepath):
    """Load and return the API key from a file."""
    with open(filepath, 'r') as file:
        api_key = file.read().strip()  # .strip() removes any leading/trailing whitespace
    return api_key

def extract_headlines_and_dates(news_data):
    """Extract headlines and dates from the news data."""
    data = []
    for news_item in news_data:
        headline = news_item.headline
        date = str(news_item.created_at).split(' ')[0]  # Extract date part
        data.append({ 'date': date, 'headline': headline})
    return data

def save_to_csv(stock_data, stock_symbol):
    
    if not stock_data.empty:
        save_file = f'data/{stock_symbol}/{stock_symbol}_articles.csv'
        stock_data.to_csv(save_file, index=False)
        print(f'{save_file} succesfully saved')
    else:
        print("Fail to save")



if __name__ == '__main__':
    API_KEY= load_api_key('./key/Alpaca key.txt')
    API_SECRET= load_api_key('./key/Alpaca secret key.txt')


    symbol  = input("What comapny do you want to query: ")
    rest_client = REST(API_KEY, API_SECRET)

    current_year = int(str(date.today()).split('-')[0])

    all_dfs = [] 
    for i in range(2015, current_year+1):
        from_date = str(i) + "-01-01"
        to_date = str(i) + "-12-31"
        news = rest_client.get_news(symbol, from_date,to_date, limit =10000)

        news_data = extract_headlines_and_dates(news)

        # Create a DataFrame
        df = pd.DataFrame(news_data)

        # Convert date column to datetime
        df['date'] = pd.to_datetime(df['date'])

        # Sort DataFrame by date
        df_sorted = df.sort_values(by='date')

        all_dfs.append(df)
    full_df = pd.concat(all_dfs)

    full_df_sorted = full_df.sort_values(by='date')

    save_to_csv(full_df_sorted, symbol)

    #print(type(date.today()))