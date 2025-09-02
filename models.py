from sqlalchemy import create_engine, Column, Integer, String, Text, ForeignKey, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

Base = declarative_base()

class Author(Base):
    __tablename__ = 'authors'
    
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    affiliation = Column(String)
    email = Column(String)
    total_papers = Column(Integer, default=0)
    
    papers = relationship("Paper", back_populates="author")

class Paper(Base):
    __tablename__ = 'papers'
    
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    publication_year = Column(Integer)
    journal = Column(String)
    author_id = Column(Integer, ForeignKey('authors.id'))
    is_favorite = Column(Integer, default=0)  # 0 = False, 1 = True
    
    author = relationship("Author", back_populates="papers")
    topics = relationship("PaperTopic", back_populates="paper")
    content = relationship("PaperContent", back_populates="paper", uselist=False)

class Topic(Base):
    __tablename__ = 'topics'
    
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(Text)
    
    papers = relationship("PaperTopic", back_populates="topic")

class PaperTopic(Base):
    __tablename__ = 'paper_topics'
    
    id = Column(Integer, primary_key=True)
    paper_id = Column(Integer, ForeignKey('papers.id'))
    topic_id = Column(Integer, ForeignKey('topics.id'))
    
    paper = relationship("Paper", back_populates="topics")
    topic = relationship("Topic", back_populates="papers")

class PaperContent(Base):
    __tablename__ = 'paper_contents'
    
    id = Column(Integer, primary_key=True)
    paper_id = Column(Integer, ForeignKey('papers.id'))
    content = Column(Text)
    
    paper = relationship("Paper", back_populates="content")

engine = create_engine('sqlite:///research_papers.db')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()