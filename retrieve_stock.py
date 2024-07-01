import numpy as np
import matplotlib.pyplot as plt
import os
import pandas as pd
from datetime import date

def get_stock(file_path, stock_symbol):

    """Load and return the API key from a file."""
    with open(file_path, 'r') as file:
        api_key = file.read().strip()  # .strip() removes any leading/trailing whitespace
    url = f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={stock_symbol}&outputsize=full&datatype=csv&apikey={api_key}'
    try:
        data = pd.read_csv(url)
        data = data.iloc[::-1]
        return data #in df 
    except Exception as e:
        print("Unable to retrieve stock for the current input symbol")
        return None

def save_to_csv(stock_data, stock_symbol):
    
    if not stock_data.empty:
        get_date = date.today()
        save_file = f'data/{stock_symbol}_{get_date}.csv'
        stock_data.to_csv(save_file, index=False)
        print(f'{save_file} succesfully saved')
    else:
        print("Fail to save")

def plot_stock_data(stock_data, stock_symbol):
    plt.figure(figsize=(14, 7))
    plt.plot(stock_data['timestamp'], stock_data['open'], label='Open', color='blue', alpha=0.7)
    plt.plot(stock_data['timestamp'], stock_data['high'], label='High', color='green', alpha=0.7)
    plt.plot(stock_data['timestamp'], stock_data['low'], label='Low', color='red', alpha=0.7)
    plt.plot(stock_data['timestamp'], stock_data['close'], label='Close', color='orange', alpha=0.7)
    plt.xlabel('Date')
    plt.ylabel('Stock Prices')
    plt.title(f'Stock Prices for {stock_symbol}')
    plt.legend()
    plt.xticks(rotation=45)  
    plt.gca().xaxis.set_major_locator(plt.MaxNLocator(nbins=10))  # Set the number of x-axis labels to show
    #plt.grid(True)

    ax = plt.gca()
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    plt.tight_layout()

    os.makedirs('plots', exist_ok=True)
    plot_file = f'plots/{stock_symbol}_{date.today()}.png'
    plt.savefig(plot_file)
    return

if __name__ == '__main__':
    symbol = input("Please enter the stock symbol you want to retrieve: ")
    data_df = get_stock('C:/Users/trand/CS-172B-Project/key/Alpha Vantage API Key.txt', symbol)
    if data_df is not None:
        save_to_csv(data_df, symbol)
        plot_stock_data(data_df, symbol)
  
