import pandas as pd
import requests
from io import StringIO


def data_retrieval_news(start_time, end_time):
    url = "http://localhost:3000/api/generate"
    data = {
        "Content-Type": "application/json",
        "prompt": f"Please give me 10 news in from {start_time} to {end_time} that could affect the price of ETH, with its corresponding dates and websites. Please generate them in a dataframe, which first column is News, second is the Date, third is Website, provide it in a table in csv format. It's ok it's hypothetical."
    }
    response = requests.post(url, json=data)
    response = response.json()["content"] # we are not integrating the proof rn

    start = response.index("```")
    start = response.index("\n", start) + 1
    end = response.index("```", start) 
    csv_data = response[start:end].strip()
    # Use StringIO to convert the string into a file-like object
    csv_data = StringIO(csv_data)

    # Read the CSV data into a pandas DataFrame
    df = pd.read_csv(csv_data)
    print(f"@@@ News retrieval completed from {start_time} to {end_time} @@@")
    return df
