from ccxtread import data_retrieval_price # data retrieval for price data
from newsread import data_retrieval_news # data retrieval for news
from test import send_eth, w3connect # deployment
from trainRandomForest import fun_process_price
from analyze import fun_process_news

import pandas as pd
import numpy as np
from datetime import datetime

# time = "2023-10-01 03:40:00"  # timestamp format

# data retrieval function (time) => data format in csv format
def fun_data_price(time):
    start_time = pd.to_datetime(time) - pd.Timedelta(days=10)
    date = time.split(" ")[0]
    start_time = start_time.strftime("%Y-%m-%d %H:%M:%S")
    start_date = start_time.split(" ")[0]
    start_time = start_time.split(" ")[1]
    df = data_retrieval_price(start_date, date, start_time)
    return df

def fun_data_news(time):
    start_time = pd.to_datetime(time) - pd.Timedelta(days=1)
    start_time = start_time.strftime("%Y-%m-%d %H:%M:%S")
    df = data_retrieval_news(start_time, time)
    return df

weight_price = 0.9
weight_news = 1 - weight_price

# prediction function (time) => predicted value (float)
def predict(time, w1, w2):
    price_predicted = fun_process_price(fun_data_price(time))[0]
    # return price_predicted
    news_average = fun_process_news(fun_data_news(time))
    return (weight_news * news_average + 1) * price_predicted

def current_price(time):
    # get the data for the current day
    start_date = time.split(" ")[0]
    end_time = pd.to_datetime(time) + pd.Timedelta(days=1)
    end_time = end_time.strftime("%Y-%m-%d %H:%M:%S")
    end_date = end_time.split(" ")[0]
    return data_retrieval_price(start_date, end_date, "00:00:00")

# current value (time) => current price (float)
def current(time):
    df = current_price(time)
    target_time = pd.to_datetime(time)
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    closest_index = (df["timestamp"] - target_time).abs().idxmin()
    value = df.loc[closest_index, "close"]
    print(f"@@@ Recent Price for time {time}: {value} @@@")
    return value

def decision(time):
    predicted = predict(time, weight_price, weight_news)
    current_price = current(time)
    print(f"@@@ Final Predicted Price for time {time} (weighted): {predicted} @@@")
    if abs(predicted - current_price) <= 0.01 * current_price:
        return 0
    elif predicted > current_price:
        return 1
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
    time = "2023-09-28 20:15:00"  # buying
    time = "2023-09-28 18:00:00"  # selling
    time = "2023-09-30 04:00:00" # no action
    action = decision(time)
    do_trx(action)

check_do_trx()
