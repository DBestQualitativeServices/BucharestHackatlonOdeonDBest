from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os
import dotenv
from models import Base, SourceArticle
from pprint import pprint


class ArticleRepository:
    def __init__(self):
        dotenv.load_dotenv()
        DB_USER = os.getenv('DB_USER')
        DB_PASSWORD = os.getenv('DB_PASSWORD')
        DB_NAME = os.getenv('DB_NAME')
        DB_HOST = os.getenv('DB_HOST')
        DB_PORT = os.getenv('DB_PORT')
        DATABASE_URI = f'postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'
        self.engine = create_engine(DATABASE_URI)  # Make engine an instance variable
        Session = sessionmaker(bind=self.engine)
        self.session = Session()

    def start(self):
        Base.metadata.create_all(self.engine)  # Use the instance variable engine

    def add_articles(self, articles):
        if not articles:
            return True, []  # If the list is empty, return success with no failures

        def try_insert(articles):
            if len(articles) == 1:  # Base case: Only one article
                try:
                    self.session.add(articles[0])
                    self.session.commit()
                    return [], []
                except Exception as e:
                    self.session.rollback()
                    print({'message': 'Error saving the article', 'error': str(e), 'article': str(articles[0])})
                    return articles, [{'article': str(articles[0]), 'error': str(e)}]
            try:
                self.session.add_all(articles)
                self.session.commit()
                return [], []
            except Exception:
                self.session.rollback()
                mid_point = len(articles) // 2
                left_half, left_errors = try_insert(articles[:mid_point])
                right_half, right_errors = try_insert(articles[mid_point:])
                return left_half + right_half, left_errors + right_errors

        negative_results, error_logs = try_insert(articles)
        if negative_results:
            return False, error_logs  # Return False and error logs if there are failures
        return True, []  # Return True and an empty list if all articles were inserted successfully

    def add_article(self, article):
        try:
            self.session.add(article)
            self.session.commit()
            return True
        except Exception as e:
            self.session.rollback()
            pprint({'message': 'Error saving the article', 'error': str(e)})
            return False

    def get_source_articles_with_no_processed_articles(self):
        from models import SourceArticle  # Importing here to avoid circular dependencies if needed
        result = (self.session.query(SourceArticle)
                  .filter(SourceArticle.processed_article_id == None)
                  .all())
        return result

    def add_embedding(self, source_article_id, embedding):
        try:
            original = (self.session.query(SourceArticle)
                        .filter(SourceArticle.id == source_article_id)
                        .first())
            original.embedding = 1 if embedding else None
            self.session.commit()
        except Exception as e:
            self.session.rollback()
            pprint({'message': 'Error updating error in article', 'error': str(e)})
            return False

    def get_source_urls(self):
        return self.session.query(SourceArticle.url).all()


