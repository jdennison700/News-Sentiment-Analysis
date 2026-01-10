"""
Analyse the sentiment of news articles
"""
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
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
        sentiment_score = sia.polarity_scores(article_content)['compound']
        date = article['publishedAt'].split('T')[0]
        date_sentiments.setdefault(date, []).append(sentiment_score)
        date_sentiments_list.append((date, sentiment_score, article_content))
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

def plot_sentiment_overall_bar(scores_df, keyword):
    """
    Plots the sentiment analysis
    """
    sentiment_counts = scores_df["Judged Sentiment"].value_counts()

    plt.bar(sentiment_counts.index, sentiment_counts.values)
    plt.title(f"Sentiment Analysis for {keyword}")
    plt.ylabel("Count")
    plt.xlabel("Sentiment")
    plt.show()

def plot_sentiment_by_date_grouped_bar(scores_df, keyword):
    """
    Plots the sentiment analysis by date
    """
    grouped_df = scores_df.groupby(["Date", "Judged Sentiment"]).size().unstack(fill_value=0)

    sentiment_order = ["Positive", "Neutral", "Negative"]

    available_sentiments= [s for s in sentiment_order if s in grouped_df.columns]

    grouped_df = grouped_df[sentiment_order]

    dates = grouped_df.index
    x = np.arange(len(dates)) * 1.5
    width = 0.25

    _, ax = plt.subplots(figsize=(10, 6))

    colours = {'Positive': '#4CAF50', 'Neutral': '#9E9E9E', 'Negative': '#F44336'}

    for i, sentiment in enumerate(available_sentiments):
        offset = (i - len(available_sentiments)/2 + 0.5) * width
        rects = ax.bar(x + offset, grouped_df[sentiment], width, label=sentiment,
                       color=colours.get(sentiment, '#000000'))


        ax.bar_label(rects, padding=3)

    ax.set_ylabel('Count')
    ax.set_xlabel('Date')
    ax.set_title('Sentiment Count by Date for ' + keyword)
    ax.set_xticks(x)
    ax.set_xticks(x)
    ax.set_xticklabels(dates)
    ax.legend(title='Sentiment')

    plt.show()

def main():
    """
    Main function
    """
    search = input("Enter a search term: ")
    days_searched = 7
    response = get_news(search, days_searched)

    scores = get_sentiment(response)
    scores_df = analyse_sentiment(scores)
    plot_sentiment_by_date_grouped_bar(scores_df = scores_df, keyword=search)

if __name__ == '__main__':

    main()
