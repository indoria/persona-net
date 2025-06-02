from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()

class Journalist(Base):
    __tablename__ = 'journalists'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    interests = Column(Text, nullable=False)
    style = Column(Text, nullable=False)
    sample_articles = Column(Text, nullable=True)

class Interaction(Base):
    __tablename__ = 'interactions'
    id = Column(Integer, primary_key=True)
    journalist_id = Column(Integer, ForeignKey('journalists.id'))
    pitch = Column(Text)
    response = Column(Text)
    journalist = relationship("Journalist")