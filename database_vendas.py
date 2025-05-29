from sqlalchemy import create_engine, Column, Integer, String, Float, Text, DateTime
from sqlalchemy.orm import sessionmaker, declarative_base
from datetime import datetime
from global_resources import *  # Certifique-se de que esse módulo está configurado corretamente

# Configuração do banco de dados usando o arquivo "db_database_vendas.db"
db = create_engine("sqlite:///db_database_vendas.db")
Session = sessionmaker(bind=db)
session = Session()

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
    content_cupom = Column(Text, nullable=False)
    total_cupom = Column(Float, nullable=False)
    lucro_cupom = Column(Float, nullable=False)
    # Aqui é onde a data/hora da venda será salva automaticamente
    data_venda = Column(DateTime, default=datetime.now, nullable=False)

class cliente(Base):
    __tablename__ = "clientes"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nome_cliente = Column(String, nullable=False)
    cod_cliente = Column(Integer, unique=True, nullable=False)
    total_conta_cliente = Column(Float, nullable=False, default=0.0)

# Cria as tabelas se elas ainda não existirem
Base.metadata.create_all(bind=db)

# --------------------------------------------------
# Exemplos de operações CRUD (comentados):
#
# Para salvar um novo cupom, por exemplo:
#
#   novo_cupom = CupomVenda(
#       content_cupom="Conteúdo da nota de venda...",
#       total_cupom=150.00,
#       lucro_cupom=30.00
#   )
#   session.add(novo_cupom)
#   session.commit()
#
# Nesse caso, o campo data_venda será preenchido automaticamente com datetime.now().
#
# Outros exemplos:
#
#   produtos = session.query(Produto).all()
#   cliente_existente = session.query(cliente).filter_by(nome_cliente="João").first()
#
#   # Para atualizar
#   cliente_existente.total_conta_cliente += 150.00
#   session.commit()
#
#   # Para deletar
#   session.delete(cliente_existente)
#   session.commit()
