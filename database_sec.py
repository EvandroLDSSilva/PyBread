from sqlalchemy import *
from sqlalchemy.orm import *
from global_resources import *



db = create_engine("sqlite:///db_database_users.db")
Session = sessionmaker(bind=db)
session = Session()

Base = declarative_base()

class User(Base):
    __tablename__ = "usuários"

    id = Column("id", Integer, primary_key=True, autoincrement=True)
    nome_user = Column("nome_user", String, unique=True, nullable=False)
    senha = Column("senha", Integer, nullable=False)


    def __init__(self, nome_user, senha):
        self.nome_user = nome_user
        self.senha = senha

Base.metadata.create_all(bind=db)

# CRUD

# C - Create
#user = User(nome_user="adm", senha=2335)
#session.add(user)
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