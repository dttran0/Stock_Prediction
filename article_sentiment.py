import pandas as pd
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import os, os.path

# def convert_df(csv_file):
#     data = []
#     for index, row in df.iterrows():
#         date_only = row['Date and Time'].split('T')[0]
#         data.append({'title': row['Article Title'], 'publishedAt': date_only})

#     df = pd.DataFrame(data, columns=['title', 'publishedAt'])
    
def avg_sentiment(sent_df):
    data_aggregated = []

    # Group by 'publishedAt' date
    grouped = sent_df.groupby('date')

    for date, group in grouped:
        # Initialize sentiment sums
        pos_sum = neu_sum = neg_sum = compound_sum = 0
        titles = []

        # Loop through each article in the group
        for _, article in group.iterrows():
            sentiment = get_sentiment(article['headline'])
            pos_sum += sentiment['pos']
            neu_sum += sentiment['neu']
            neg_sum += sentiment['neg']
            compound_sum += sentiment['compound']
            titles.append(article['headline'])

        # Calculate average sentiments for the group
        n = len(group)
        avg_pos = pos_sum / n
        avg_neu = neu_sum / n
        avg_neg = neg_sum / n
        avg_compound = compound_sum / n

        data_aggregated.append({
            "date": date,
            "article titles": titles,
            "pos": avg_pos,
            "neu": avg_neu,
            "neg": avg_neg,
            "compound": avg_compound
        })

    df_aggregated = pd.DataFrame(data_aggregated, columns=['date', 'article titles', 'pos', 'neu', 'neg', 'compound'])
    return df_aggregated

def save_to_csv(average_df, stock_symbol):
    
    if not average_df.empty:
        save_file = f'data/{stock_symbol}/{stock_symbol}_articles_sentiment.csv'
        average_df.to_csv(save_file, index=False)
        print(f'{save_file} succesfully saved')
    else:
        print("Fail to save")


if __name__ == '__main__':
    init_dir = './data'
    elems = os.listdir(init_dir)
    #print(elems)

    for elem_ in elems:
        full_path = init_dir + '/' + elem_
        if os.path.isdir(full_path):
            sub_elems = os.listdir(full_path)
            for elem in sub_elems:
                if 'articles.csv' in elem:
                    articles_df = pd.read_csv(full_path+'/'+elem)
                    #print(articles_df)
    
            # Initialize VADER
            analyzer = SentimentIntensityAnalyzer()

            # Function to get sentiments
            def get_sentiment(text):
                return analyzer.polarity_scores(text)

            # Apply sentiment analysis
            articles_df['sentiments'] = articles_df['headline'].apply(get_sentiment)
            articles_df = pd.concat([articles_df.drop(['sentiments'], axis=1), articles_df['sentiments'].apply(pd.Series)], axis=1)

            avg_df = avg_sentiment(articles_df)

            save_to_csv(avg_df, elem_)

            #print(avg_df)


