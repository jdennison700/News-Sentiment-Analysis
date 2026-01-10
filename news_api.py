"""
Calls the NewsAPI
"""

import os
from datetime import date, timedelta
from newsapi import NewsApiClient
from dotenv import load_dotenv


load_dotenv()

def get_news(keyword, days):
    """
    Gets everything from the NewsAPI
    
    :param keyword: Word to search for
    :param days: Days to search back
    """
    newsapi = NewsApiClient(api_key=os.getenv('API_KEY'))
    searchdate = date.today() - timedelta(days=days)

    articles = newsapi.get_everything(qintitle = f"{keyword} AND NOT offer AND NOT deal",
    
                                      from_param = date.isoformat(searchdate),
                                      to = (searchdate + timedelta(days = days)).isoformat(),
                                      language="en",
                                      sort_by="publishedAt",
                                      page_size = 100)

    return articles['articles']

if __name__ == '__main__':

    news = get_news('Pittsburgh Steelers', 1)

    print(len(news))

    for article in news:
        print('Title')
        print(article['title'])
        print('Description')
        print(article['description'])
