from repository import ArticleRepository
from models import ProcessedArticle
import lorem


class ArticleService:
    def __init__(self):
        self.repository = ArticleRepository()

    def save_mock_data(self):
        mockdata = []
        sampleProcessedArticle = ProcessedArticle(
            title=f"{i} {lorem.text()[:50]}",
            headline=f"{i} {lorem.text()[:100]}",
            description=f"{i} {lorem.text()[:300]}",
            content=f"{i} {lorem.text()[:700]}",
            category=f"{i % 5}_Categorie",

        )
        mockdata.append(sampleProcessedArticle)

        if self.repository.add_articles(mockdata):
            print('Saved elements in db')
        else:
            print('Failed to save elements')
