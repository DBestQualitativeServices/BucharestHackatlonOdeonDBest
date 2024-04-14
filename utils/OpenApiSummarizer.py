from models import ProcessedArticle, SourceArticle
from openai_service import OpenAiService
from repository import ArticleRepository
import random


def summarize_new_articles():
    openai_service = OpenAiService()
    repo = ArticleRepository()

    source_articles = repo.get_source_articles_with_no_processed_articles()
    generated_articles = []
    for article in source_articles:
        result_object = openai_service.create_summary(article.content[0:3000])
        processed_article = ProcessedArticle(
            content=result_object.get('articol'),
            headline=result_object.get('antet'),
            title=result_object.get('titlu'),
            price=result_object.get('price'),
            category=openai_service.create_category(article),
            model_name=result_object.get('model'),
            source_article=article
        )
        repo.add_article(processed_article)
        print(processed_article.title)
    # success_insert, result = repo.add_articles(generated_articles)
    print('DONE !')
    # return result if not success_insert else None


summarize_new_articles()
