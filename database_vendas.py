from sqlalchemy import create_engine, Column, String, Integer, Float
from sqlalchemy.orm import sessionmaker, declarative_base

from global_resources import *

db = create_engine("sqlite:///db_database_vendas.db")
Session = sessionmaker(bind=db)
session = Session()

Base = declarative_base()

class Produto(Base):
    __tablename__ = "produtos"

    id = Column("id", Integer, primary_key=True, autoincrement=True)
    nome_produto = Column("nome_produto", String)
    cod_produto = Column("cod_produto", Integer)
    preco_venda = Column("preco_venda", Float)
    preco_compra = Column("preco_compra", Float)
    lucro = Column("lucro", Float)  # Lucro agora é armazenado na tabela Produto

    def __init__(self, nome_produto, cod_produto, preco_venda, preco_compra):
        self.nome_produto = nome_produto
        self.cod_produto = cod_produto
        self.preco_venda = preco_venda
        self.preco_compra = preco_compra
        self.lucro = preco_venda - preco_compra  # Calcula o lucro e armazena

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
# produto_especifico.preco_venda = 14.00
# produto_especifico.lucro = produto_especifico.preco_venda - produto_especifico.preco_compra
# session.add(produto_especifico)
# session.commit()

# D - Delete
# session.delete(produto_especifico)
# session.commit()
