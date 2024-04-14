from pinecone import Pinecone
import os, dotenv
from openai_service import OpenAiService
from repository import ArticleRepository
from models import SourceArticle


class Embedder:
    def __init__(self):
        dotenv.load_dotenv()
        self.openai_service = OpenAiService()
        self.PINECONE_API_KEY = os.getenv("PINECONE")
        self.index_name = "odeon"
        self.pc = Pinecone(api_key=self.PINECONE_API_KEY)
        self.index = self.pc.Index(self.index_name)
        self.article_repository = ArticleRepository()

    def embed_all(self):
        print("Embedding all articles...")
        articles = self.article_repository.session.query(SourceArticle).all()
        try:
            for article in articles:
                if article.embedding:
                    continue
                article_content = article.content
                pinecone_object = self.openai_service.create_embedding(article.id, article_content)
                self.index.upsert([pinecone_object])
                article.embedding = True
                self.article_repository.session.commit()
        except Exception as e:
            print(f"Error: {e}")
        finally:
            self.article_repository.session.close()
        print("Finished Embedding all articles...")
