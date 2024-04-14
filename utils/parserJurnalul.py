import requests
from bs4 import BeautifulSoup
from models import SourceArticle
from repository import ArticleRepository
from datetime import datetime
import json


class JurnalulParser:
    def __init__(self):
        self.url = "https://jurnalul.ro/rss/stiri.xml"
        self.repository = ArticleRepository()

    def parse(self):
        print("Parsing Jurnalul")
        response = requests.get(self.url)
        content = response.content

        soup = BeautifulSoup(content, 'xml')

        items = soup.find_all('guid')

        news_items = []
        counter = 1
        urls = [x[0] for x in self.repository.get_source_urls()]
        for index, item in enumerate(items):
            new_url = item.getText()
            responseArticle = requests.get(new_url)
            bs_content = BeautifulSoup(responseArticle.content, features="lxml")
            paragraphs = bs_content.find_all('p')
            news = {}
            for json_ld in bs_content.find_all("script", type="application/ld+json"):
                json_content = json_ld.getText()
                json_load = json.loads(json_content)
                if json_load.get('type') != 'NewsArticle': continue
                news['headline'] = json_load.get('headline')
                news['date_uploaded'] = datetime.strptime(json_load.get('datePublished'), "%Y-%m-%dT%H:%M:%S%z")

            news['title'] = bs_content.find('title').getText()
            news['content'] = f"<title>{news['title']}</title> ".join(paragraph.getText() for paragraph in paragraphs)
            news['url'] = new_url
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

        result = self.repository.add_articles(source_articles)
        print("Finished Parsing Jurnalul")
        return result
