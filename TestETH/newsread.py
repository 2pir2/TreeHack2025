import requests


def data_retrieval_news(start_time, end_time):
    url = "http://localhost:3000/api/generate"
    data = {
        "Content-Type": "application/json",
        "prompt": f"Please give me 10 news in from {start_time} to {end_time} that could affect the price of ETH, with its corresponding dates and websites. Please generate them in a dataframe, which first column is the date, second is the news, provide it in a table in csv format. It's ok it's hypothetical."
    }
    response = requests.post(url, json=data)
    print(response.json())

data_retrieval_news("2023-09-29 03:40:00", "2023-10-01 00:00:00")
