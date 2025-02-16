from ccxtread import add

import pandas as pd
import numpy as np

time = "2025-01-26 03:40:00"  # timestamp format

# data retrieval function (time) => data format in csv format
fun_data_price = ''
fun_data_news = ''

# data preprocessing function (data format in csv format) => predicted value (float)
fun_process_price = ''
fun_process_news = ''

weight_price = 0.5
weight_news = 1 - weight_price

# prediction function (time) => predicted value (float)
def predict(time, w1, w2):
    price_predicted = fun_process_price(fun_data_price(time))
    news_predicted = fun_process_news(fun_data_news(time))
    return w1 * price_predicted + w2 * news_predicted

# current value (time) => current price (float)
def current(time):
    df = pd.read_csv("../ETH.csv")
    target_time = pd.to_datetime(time)
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    closest_index = (df["timestamp"] - target_time).abs().idxmin()
    return df.loc[closest_index, "close"]

def decision(time):
    return predict(time, weight_price, weight_news) > current(time)

print(current(time))
print(pd.to_datetime(time) - pd.Timedelta(days=10))
