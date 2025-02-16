import openai
import pandas as pd
import time
from transformers import pipeline
# Load dataset
df = pd.read_csv(r"/Users/hanxu/Desktop/TreeHack/TreeHack2025/Output.csv")  # Replace with your actual file
# Load FinBERT model for financial sentiment analysis
sentiment_pipeline = pipeline("sentiment-analysis", model="ProsusAI/finbert")

def get_sentiment_score(text):
    """Analyze sentiment using FinBERT and assign a continuous score between -1 and 1."""
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
# Apply sentiment analysis
df['Sentiment_Score'] = df.iloc[:, 0].apply(lambda text: get_sentiment_score(str(text)))
# Keep only date and sentiment score columns
df = df[[df.columns[0], 'Sentiment_Score']]
# Save updated dataset
df.to_csv("/Users/hanxu/Desktop/TreeHack/TreeHack2025/NewsAnalyzer/output_with_sentiment.csv", index=False)
print("Sentiment analysis completed using FinBERT and saved to output_with_sentiment.csv")


