from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

db = create_engine("sqlite:///database_vendas.db")

Session = sessionmaker(bind=db)
session = Session()

Base = declarative_base()

# as tabelas
Base.metadata.create_all(bind=db)
