import requests
from bs4 import BeautifulSoup
from models import SourceArticle
from repository import ArticleRepository
from datetime import datetime
import pprint


class RealitateaParser:
    def __init__(self):
        self.url = "https://rss.realitatea.net/stiri.xml"

    def parse(self):
        print('Starting Realitatea Parser')
        response = requests.get(self.url)
        content = response.content

        soup = BeautifulSoup(content, 'xml')

        items = soup.find_all('item')
        news_items = []
        repo = ArticleRepository()
        urls = [x[0] for x in repo.get_source_urls()]
        counter = 1
        for item in items:
            news = {}
            for key in ['title', 'description', 'thumbnail', 'content']:
                otherOption = key + ":encoded" if not item.find(key) else key
                news[key] = item.find(otherOption).text if item.find(otherOption) else f'No {key}'
                # if "encoded" in keyOption: break
            news['date_uploaded'] = item.find('pubDate').text if item.find('pubDate') else datetime.now()
            news['url'] = item.find('link').text if item.find('link') else None
            news['content'] = f"<title>{news['title']}</title>{news['description']}"
            if news['url'] in urls:
                continue  # remove if loc changes to accept updatable articles
            news_items.append(news)
            print(f"#{counter} : {news['url']}")
            counter += 1

        source_articles = [SourceArticle(
            url=news.get('url'),
            content=news.get('content'),
            date_uploaded=news.get('date_uploaded')
        ) for news in news_items]
        #
        repo = ArticleRepository()
        success_insert, result = repo.add_articles(source_articles)
        print('Finished Realitatea Parser')
        return result if not success_insert else None
