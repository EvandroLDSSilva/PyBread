from sqlalchemy import create_engine, Column, String, Integer, Float
from sqlalchemy.orm import sessionmaker, declarative_base

from global_resources import *

db = create_engine("sqlite:///db_database_users.db")
Session = sessionmaker(bind=db)
session = Session()

Base = declarative_base()

class User(Base):
    __tablename__ = "usuários"

    id = Column("id", Integer, primary_key=True, autoincrement=True)
    nome_user = Column("nome_user", String)
    senha = Column("senha", Integer)


    def __init__(self, nome_user, senha):
        self.nome_user = nome_user
        self.senha = senha

Base.metadata.create_all(bind=db)

# CRUD

# C - Create
#produto = Produto(nome_produto="Pão Hamburguer pc", cod_produto=7891, preco_venda=7.50, preco_compra=5.50)
#session.add(produto)
#session.commit()

# R - READ
# lista_produtos = session.query(Produto).all()
# produto_especifico = session.query(Produto).filter_by(nome_produto="Pão de Hambúrguer").first()
# print(produto_especifico.nome_produto, produto_especifico.lucro) 

# U - Update
# produto_especifico.preco_venda = 14.00 Q@ 
# produto_especifico.lucro = produto_especifico.preco_venda - produto_especifico.preco_compra
# session.add(produto_especifico)
# session.commit()

# D - Delete
# session.delete(produto_especifico)
# session.commit()