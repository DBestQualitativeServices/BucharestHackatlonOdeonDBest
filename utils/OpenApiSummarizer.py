from models import ProcessedArticle
from openai_service import OpenAiService
from repository import ArticleRepository
import random


def summarize_new_articles():
    openai_service = OpenAiService()
    repo = ArticleRepository()

    unprocessed_messages = repo.get_source_articles_with_no_processed_articles()

    generated_articles = []
    for message in unprocessed_messages[0:4]:
        result_object = openai_service.create_summary(message.content)
        processed_article = ProcessedArticle(
            content=result_object.get('articol'),
            headline=result_object.get('antet'),
            title=result_object.get('titlu'),
            price=result_object.get('price'),
            category=f"Categoria {random.randint(0, 5)}",
            model_name=result_object.get('model'),
            source_article=message
        )
        generated_articles.append(processed_article)
        print(processed_article.title)
    success_insert, result = repo.add_articles(generated_articles)
    print('DONE !')
    return result if not success_insert else None


summarize_new_articles()
