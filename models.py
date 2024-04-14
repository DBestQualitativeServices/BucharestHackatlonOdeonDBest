from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, UniqueConstraint, ForeignKeyConstraint, Float, \
    Boolean
from sqlalchemy.orm import declarative_base, relationship
import datetime

Base = declarative_base()


class ProcessedArticle(Base):
    __tablename__ = 'processed_article'
    id = Column(Integer, primary_key=True, autoincrement=True)
    version = Column(Integer, primary_key=True, default=0)
    title = Column(String)
    content = Column(String)
    category = Column(String)
    date_uploaded = Column(DateTime, default=datetime.datetime.now)
    model_name = Column(String)
    price = Column(Float)
    headline = Column(String)
    # Reverse relationship from ProcessedArticle to SourceArticle
    source_article = relationship("SourceArticle", back_populates="processed_article", uselist=False)


class SourceArticle(Base):
    __tablename__ = 'source_article'
    id = Column(Integer, primary_key=True, autoincrement=True)
    url = Column(String, unique=True)
    content = Column(String)
    document_type = Column(String, default='html')
    date_uploaded = Column(DateTime, default=datetime.datetime.now)
    price = Column(Float, default=0)
    # Composite foreign key definition
    processed_article_id = Column(Integer)
    processed_article_version = Column(Integer)
    embedding = Column(Boolean, default=False)
    __table_args__ = (
        ForeignKeyConstraint(
            ['processed_article_id', 'processed_article_version'],
            ['processed_article.id', 'processed_article.version']
        ),
    )

    # Relationship to access the processed article linked to this source article
    processed_article = relationship("ProcessedArticle", back_populates="source_article")
