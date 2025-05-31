from sqlalchemy import create_engine, Column, Integer, String, Float, Text, DateTime
from sqlalchemy.orm import sessionmaker, declarative_base
from datetime import datetime

# Conexão com o banco de dados SQLite
db = create_engine("sqlite:///db_database_vendas.db", echo=True)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=db)
session = SessionLocal()

Base = declarative_base()

# Definição das tabelas
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
    content_cupom = Column(Text, nullable=False)
    total_cupom = Column(Float, nullable=False)
    lucro_cupom = Column(Float, nullable=False)
    data_venda = Column(DateTime, default=datetime.now, nullable=False)

class Cliente(Base):
    __tablename__ = "clientes"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nome_cliente = Column(String, nullable=False)
    cod_cliente = Column(Integer, unique=True, nullable=False)
    total_conta_cliente = Column(Float, nullable=False, default=0.0)

Base.metadata.create_all(bind=db)

# Funções para buscar dados no banco
def buscar_todos_clientes():
    return session.query(Cliente).all()

def buscar_cliente_por_nome(nome):
    return session.query(Cliente).filter(Cliente.nome_cliente.ilike(f"%{nome}%")).first()

def buscar_todos_produtos():
    return session.query(Produto).all()

def buscar_produto_por_nome(nome):
    return session.query(Produto).filter(Produto.nome_produto.ilike(f"%{nome}%")).first()

def buscar_historico_vendas():
    return session.query(CupomVenda).order_by(CupomVenda.data_venda.desc()).limit(10).all()
