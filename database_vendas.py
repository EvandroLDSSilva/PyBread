from sqlalchemy import create_engine, Column, Integer, String, Float, Text
from sqlalchemy.orm import sessionmaker, declarative_base

from global_resources import *

# Configuração do banco de dados SQLite
db = create_engine("sqlite:///db_database_vendas.db")
Session = sessionmaker(bind=db)
session = Session()

# Criando base declarativa
Base = declarative_base()

class Produto(Base):
    __tablename__ = "produtos"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nome_produto = Column(String, nullable=False)
    cod_produto = Column(Integer, unique=True, nullable=False)
    preco_venda = Column(Float, nullable=False)
    preco_compra = Column(Float, nullable=False)
    lucro = Column(Float, nullable=False)

    def __init__(self, nome_produto, cod_produto, preco_venda, preco_compra):
        self.nome_produto = nome_produto
        self.cod_produto = cod_produto
        self.preco_venda = preco_venda
        self.preco_compra = preco_compra
        self.lucro = preco_venda - preco_compra

class CupomVenda(Base):  
    __tablename__ = "cupons"

    id = Column(Integer, primary_key=True, autoincrement=True)
    content_cupom = Column(Text, nullable=False)  # Armazena os cupons

Base.metadata.create_all(bind=db)

# CRUD - Exemplo de uso

# Criar um produto
#produto = Produto(nome_produto="pão hotdog", cod_produto=7891, preco_venda=0.60, preco_compra=0.35)
#session.add(produto)
#session.commit()

# Ler produtos do banco
#lista_produtos = session.query(Produto).all()
#produto_especifico = session.query(Produto).filter_by(nome_produto="Pão de Hambúrguer").first()
#print(produto_especifico.nome_produto, produto_especifico.lucro) 

# Atualizar um produto
#produto_especifico.preco_venda = 14.00 
#produto_especifico.lucro = produto_especifico.preco_venda - produto_especifico.preco_compra
#session.add(produto_especifico)
#session.commit()

# Deletar um produto
#session.delete(produto_especifico)
#session.commit()
