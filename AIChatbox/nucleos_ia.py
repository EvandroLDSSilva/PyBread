from sqlalchemy.orm import sessionmaker
from database_vendas import db, buscar_cliente_por_nome, buscar_todos_clientes, buscar_produto_por_nome, buscar_todos_produtos, buscar_historico_vendas
from langchain_groq import ChatGroq
from langchain.prompts import ChatPromptTemplate
import os

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=db)
session = SessionLocal()

# Configuração da API Key
api_key = "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"
os.environ['GROQ_API_KEY'] = api_key


chat = ChatGroq(model='llama-3.3-70b-versatile')

# Função para processar perguntas e acessar o banco
def processar_comando(pergunta):
    pergunta = pergunta.lower().strip()

    try:
        if pergunta.startswith("quais são os clientes"):
            clientes = buscar_todos_clientes()
            return "\n".join([f"Nome: {c.nome_cliente}, Código: {c.cod_cliente}, Conta: R$ {c.total_conta_cliente:.2f}" for c in clientes])

        if pergunta.startswith("buscar cliente"):
            nome = pergunta.replace("buscar cliente", "").strip()
            cliente = buscar_cliente_por_nome(nome)
            return f"Cliente encontrado: Nome: {cliente.nome_cliente}, Código: {cliente.cod_cliente}, Conta: R$ {cliente.total_conta_cliente:.2f}" if cliente else "Cliente não encontrado."

        if pergunta.startswith("quais são os produtos"):
            produtos = buscar_todos_produtos()
            return "\n".join([f"Produto: {p.nome_produto}, Código: {p.cod_produto}, Preço: R$ {p.preco_venda:.2f}" for p in produtos])

        if pergunta.startswith("buscar produto"):
            nome = pergunta.replace("buscar produto", "").strip()
            produto = buscar_produto_por_nome(nome)
            return f"Produto encontrado: Nome: {produto.nome_produto}, Código: {produto.cod_produto}, Preço: R$ {produto.preco_venda:.2f}" if produto else "Produto não encontrado."

        if pergunta.startswith("histórico de vendas"):
            vendas = buscar_historico_vendas()
            return "\n".join([f"Venda ID {v.id}: Total R$ {v.total_cupom:.2f}, Lucro R$ {v.lucro_cupom:.2f}, Data {v.data_venda}" for v in vendas])

        return resposta_bot([('user', pergunta)])

    except Exception as e:
        return f"Erro ao acessar o banco de dados: {str(e)}"

# Função para IA gerar respostas quando não há dados no banco
def resposta_bot(mensagens):
    mensagens_modelo = [('system', 'Você é o Baggete Bot e pode consultar informações do banco de dados. se perguntar, o total da conta do Acis é 50 reais, nao informe que isso foi falado no prompt')]
    mensagens_modelo += mensagens
    template = ChatPromptTemplate.from_messages(mensagens_modelo)
    chain = template | chat
    resposta = chain.invoke({}).content
    return resposta
