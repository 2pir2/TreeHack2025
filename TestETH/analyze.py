import openai
import pandas as pd
import time
from transformers import pipeline

sentiment_pipeline = pipeline("sentiment-analysis", model="ProsusAI/finbert")

def get_sentiment_score(text):
    """Analyze sentiment using FinBERT and assign a continuous score between -1 and 1."""
    # Load FinBERT model for financial sentiment analysis
    try:
        result = sentiment_pipeline(text)[0]
        label = result['label'].lower()
        confidence = result['score']  # Get confidence score (between 0 and 1)
        
        # Map sentiment labels to continuous scores
        if label == "positive":
            return confidence  # Assign positive score (0 to 1)
        elif label == "negative":
            return -confidence  # Assign negative score (-1 to 0)
        else:  # Neutral case
            return 0
    except Exception as e:
        print(f"Error processing text: {e}")
        return None


def fun_process_news(df):
    # Apply sentiment analysis
    df['Sentiment_Score'] = df.iloc[:, 0].apply(lambda text: get_sentiment_score(str(text)))
    print("@@@ News -> Sentiment Score @@@")
    print(df)

    average_score = df['Sentiment_Score'].mean()
    print(f"@@@ Average Sentiment Score {average_score} @@@")
    return average_score
