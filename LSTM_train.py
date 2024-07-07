import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import keras
seed = 43
keras.utils.set_random_seed(seed)
from LSTM_model import split_data, get_x_y, build_model
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.callbacks import ModelCheckpoint



if __name__ == '__main__':
    stock_data = pd.read_csv('./data/AAPL/AAPL_2024-07-02.csv')
    sentiment_data = pd.read_csv('./data/AAPL/AAPL_articles_sentiment.csv')

    merged_data = pd.merge(stock_data, sentiment_data, left_on='timestamp', right_on='date')

    feature = ['open', 'high', 'low', 'close', 'volume', 'pos','neu','neg', 'compound']
    #print(merged_data.columns.tolist())
    training_set, testing_set = split_data(merged_data, 0.85, feature)
    # print("training_set: ", training_set.shape)
    # print("testing_set: ", testing_set.shape)


    #scaling 
    sc_train = MinMaxScaler()
    training_set = sc_train.fit_transform(training_set)
    testing_set = sc_train.fit_transform(testing_set)

    #print(training_set)

    # Get X and y from training set
    X_train, y_train = get_x_y(training_set, 14, 0, len(feature))

    # Split training into train and val
    val_split_row = int(X_train.shape[0]*0.85) # 15% will be used for validation
    X_train, X_val = X_train[:val_split_row], X_train[val_split_row:]
    y_train, y_val = y_train[:val_split_row], y_train[val_split_row:]
    # print("X_train: ", X_train.shape)
    # print("y_train: ", y_train.shape)
    # print("X_val: ", X_val.shape)
    # print("y_val: ", y_val.shape)


    model = build_model(14, len(feature))
    #print(model.summary())
    

    checkpointer = ModelCheckpoint(
        filepath='best_model.weights.h5',
        monitor='val_loss',
        verbose=1,
        save_best_only=True,
        save_weights_only=True,
        mode='min'
    )

    history = model.fit(X_train,
                    y_train,
                    batch_size=32,
                    epochs=100,
                    validation_data=(X_val, y_val),
                    callbacks=[checkpointer])
    
