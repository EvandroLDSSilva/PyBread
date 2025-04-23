import customtkinter as ctk

# Função para inserir informações no bloco de texto
def inserir_informacoes(event=None):  # Adicione "event=None" para que funcione com o bind
    codigo = entrada.get()
    if codigo in produtos:
        info = produtos[codigo]
        texto.configure(state="normal")
        texto.insert("end", f"Nome: {info['nome']}\n")
        texto.insert("end", f"Preço: {info['preco']}\n")
        texto.insert("end", f"Código: {codigo}\n")
        texto.insert("end", "-" * 20 + "\n")
        texto.configure(state="disabled")
    else:
        texto.configure(state="normal")
        texto.insert("end", f"Código {codigo} não encontrado.\n")
        texto.insert("end", "-" * 20 + "\n")
        texto.configure(state="disabled")

# Dicionário de produtos
produtos = {
    "12345": {"nome": "Produto X", "preco": 45.99},
    "67890": {"nome": "Produto Y", "preco": 25.50},
    "11121": {"nome": "Produto Z", "preco": 75.00},
}

# Inicializar janela
janela = ctk.CTk()
janela.title("Gestão de Produtos")

# Criar campo de entrada
entrada = ctk.CTkEntry(janela, placeholder_text="Digite o código do produto")
entrada.pack(pady=10)
entrada.bind("<Return>", inserir_informacoes)  # Associa a tecla Enter à função

# Criar botão para enviar o código
botao = ctk.CTkButton(janela, text="Pesquisar", command=inserir_informacoes)
botao.pack(pady=10)

# Criar bloco de texto (não editável)
texto = ctk.CTkTextbox(janela, height=200, width=300)
texto.configure(state="disabled")  # Torná-lo não editável
texto.pack(pady=10)

# Executar a aplicação
janela.mainloop()
