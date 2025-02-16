from ccxtread import data_retrieval_price # data retrieval for price data
from newsread import data_retrieval_news # data retrieval for news
from test import send_eth, w3connect # deployment
from trainRandomForest import fun_process_price

import pandas as pd
import numpy as np
from datetime import datetime

time = "2023-10-01 03:40:00"  # timestamp format

# data retrieval function (time) => data format in csv format
def fun_data_price(time):
    start_time = pd.to_datetime(time) - pd.Timedelta(days=10)
    date = time.split(" ")[0]
    start_time = start_time.strftime("%Y-%m-%d %H:%M:%S")
    start_date = start_time.split(" ")[0]
    df = data_retrieval_price(start_date, date)
    return df

def fun_data_news(time):
    start_time = pd.to_datetime(time) - pd.Timedelta(days=5)
    start_time = start_time.strftime("%Y-%m-%d %H:%M:%S")
    df = data_retrieval_news(start_time, time)
    return df

# data preprocessing function (data format in csv format) => [predicted value (float), r^2]
fun_process_news = ''

weight_price = 0.5
weight_news = 1 - weight_price

# prediction function (time) => predicted value (float)
def predict(time, w1, w2):
    price_predicted = fun_process_price(fun_data_price(time))[0]
    # return price_predicted
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
    predicted = predict(time, weight_price, weight_news)
    current_price = current(time)
    if predicted > current_price:
        return 1
    elif predicted == current_price:
        return 0
    else:
        return -1

def do_trx(action):
    if action is not None:
        if action == 1:
            print("🟢 Buying ETH...")
        elif action == -1:
            print("🔴 Selling ETH...")
        try:
            w3connect()
            send_eth(action)
        except Exception as e:
            print(f"❌ Error sending ETH: {e}")

def check_do_trx():
    current_time = datetime.now()
    current_time = current_time.strftime("%Y-%m-%d %H:%M:%S")
    time = "2023-10-01 03:40:00"  # timestamp format
    do_trx(decision(time))


# print(fun_process_price(fun_data_price("2025-01-27 16:00:00")))
print(decision("2025-02-06 16:00:00"))
# print(current(time))
# print(pd.to_datetime(time) - pd.Timedelta(days=10))

# print(fun_data_price(time).head())

# check_do_trx()
