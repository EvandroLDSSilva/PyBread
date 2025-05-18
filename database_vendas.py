from sqlalchemy import *
from sqlalchemy.orm import *

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
    lucro = Column("lucro", Float)

    def __init__(self, nome_produto, cod_produto, preco_venda, preco_compra):
        self.nome_produto = nome_produto
        self.cod_produto = cod_produto
        self.preco_venda = preco_venda
        self.preco_compra = preco_compra
        self.lucro = preco_venda - preco_compra

    
Base.metadata.create_all(bind=db)

# CRUD

# C - Create
#produto = Produto(nome_produto="testeproduto2", cod_produto=2, preco_venda=8.88, preco_compra=8.88)
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
