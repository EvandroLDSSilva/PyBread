import os
from langchain_groq import ChatGroq
from langchain.prompts import ChatPromptTemplate

api_key =  "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"
os.environ['GROQ_API_KEY'] = api_key

chat = ChatGroq(model='llama-3.3-70b-versatile')

def resposta_bot(mensagens):
  mensagens_modelo = [('system', 'Você é um assistente amigável chamado Baguette oIa')]
  mensagens_modelo += mensagens
  template = ChatPromptTemplate.from_messages(mensagens_modelo)
  chain = template | chat
  return chain.invoke({}).content

print('Bem-vindo ao Baguette Ia')

mensagens = []
while True:
  pergunta = input('Usuario: ')
  if pergunta.lower() == 'x' or pergunta.lower() == 'sair'  :
    break
  mensagens.append(('user', pergunta))
  resposta = resposta_bot(mensagens)
  mensagens.append(('assistant', resposta))
  print(f'Bot: {resposta}')

print('Muito obrigado por usar o Baguette IA')