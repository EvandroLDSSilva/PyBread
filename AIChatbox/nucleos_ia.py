import os
from langchain_groq import ChatGroq
from langchain.prompts import ChatPromptTemplate
#API KEY
api_key = "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"


os.environ["GROQ_API_KEY"] = api_key


chat = ChatGroq(model ='llama-3.3-70b-versatile')

primeira_interacao = chat.invoke('qual o melhor sistema de vendas do mundo?')
print (primeira_interacao.content)