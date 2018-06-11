from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('sqlite:///people_and_numbers.db')
Base = declarative_base()


class Info(Base):

    __tablename__ = "info"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    surname = Column(String, nullable=False)
    number = Column(Integer, nullable=False)


Base.metadata.create_all(engine)