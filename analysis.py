"""
Analyse the sentiment of news articles
"""
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import pandas as pd
from news_api import get_news

def get_sentiment(articles):
    """
    Get the sentiment value for each article
    
    :param articles: list of articles
    """
    date_sentiments = {}
    date_sentiments_list = []
    sia = SentimentIntensityAnalyzer()
    for article in articles:
        article_content = str(article['title']) + '. ' + str(article['description'])
        sentiment = sia.polarity_scores(article_content)['compound']
        date = article['publishedAt'].split('T')[0]
        date_sentiments.setdefault(date, []).append(sentiment)
        date_sentiments_list.append((date, sentiment, article_content))
    return date_sentiments_list

def analyse_sentiment(date_sentiments):
    """
    Turns the sentiment score into Positve, Negative or Neutral.
    :param date_sentiments: list of sentiments
    """
    scores_df = pd.DataFrame(date_sentiments, columns=['Date', 'Sentiment', 'Content'])
    scores_df["Judged Sentiment"] = "Neutral"
    scores_df.loc[scores_df["Sentiment"] > 0.05, "Judged Sentiment"] = "Positive"
    scores_df.loc[scores_df["Sentiment"] < -0.05, "Judged Sentiment"] = "Negative"

    return scores_df

if __name__ == '__main__':
    response = get_news('Microsoft', 7)

    scores = get_sentiment(response)

    analyse_sentiment(scores)
