import math
import pandas_datareader as web
import numpy as np
import pandas as pd

from keras.models import Sequential
from keras.layers import Dense, LSTM


def build_dataset(df):

    x = []
    y = []
    df = np.array(df)
    for i in range(60, len(df)):
        x.append(df[i - 60:i])
        y.append(df[i])
    x = np.asarray(x)
    y = np.asarray(y)
    return x, y


def build_lstm():

    model = Sequential()
    model.add(LSTM(units=50, return_sequences=True, input_shape=(60, 1)))
    model.add(LSTM(units=50, return_sequences=False))
    model.add(Dense(units=25))
    model.add(Dense(units=1))

    return model






