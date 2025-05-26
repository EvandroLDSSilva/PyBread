import os
from langchain_groq import ChatGroq
from langchain.prompts import ChatPromptTemplate

api_key = "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"
os.environ["GROQ_API_KEY"] = api_key

chat = ChatGroq(model="llama-3.3-70b-versatile")

mensagens = []  # Histórico de conversas

def resposta_bot(mensagem_usuario):
    
    mensagens.append(("user", mensagem_usuario))  # Adiciona ao histórico
    mensagens_modelo = [("system", "Você é um assistente amigável chamado Baguette IA.")]
    mensagens_modelo += mensagens
    template = ChatPromptTemplate.from_messages(mensagens_modelo)
    chain = template | chat

    try:
        resposta = chain.invoke({}).content
        mensagens.append(("assistant", resposta))  # Mantém histórico
        return resposta
    except Exception as e:
        return f"Erro ao gerar resposta: {e}"
