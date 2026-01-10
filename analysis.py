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


if __name__ == '__main__':
    response = get_news('Microsoft', 7)

    scores = get_sentiment(response)

    scores_df = pd.DataFrame(scores, columns = ['Date', 'Sentiment', 'Content'])
    scores_df.to_csv('scores.csv')