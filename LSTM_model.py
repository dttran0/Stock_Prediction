from keras.models import Sequential
from keras.layers import LSTM, Dropout, Dense
from keras.callbacks import ModelCheckpoint, EarlyStopping
import numpy as np


def split_data(data, training_split, features):
    split_row = int(data.shape[0]*training_split)
    training_set = data[features].iloc[:split_row].values
    testing_set = data[features].iloc[split_row:].values
    return training_set, testing_set


def get_x_y(dataset, window_size, label_feature, feature_count):
    X, y = [], []
    for i in range(window_size, len(dataset)):
        X.append(dataset[i-window_size:i])
        y.append(dataset[i, label_feature])

    X, y = np.array(X), np.array(y)
    X = np.reshape(X, (X.shape[0], window_size, feature_count))
    return X, y



def build_model(window_size, feature_count):
    d = 0.1
    model = Sequential()
    model.add(LSTM(128, input_shape=(window_size, feature_count), return_sequences=True))
    model.add(LSTM(32, input_shape=(window_size, feature_count)))
    model.add(Dropout(d))
    model.add(Dense(16, activation="relu", kernel_initializer="uniform"))
    model.add(Dense(1, activation="relu", kernel_initializer="uniform"))
    model.compile(loss='mse',optimizer='adam',metrics=['mae'])
    return model