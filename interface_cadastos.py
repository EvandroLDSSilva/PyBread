import customtkinter as ctk
from global_resources import resolucao_tela_monitor, cor_principal, cor_secundaria
from sqlalchemy.orm import sessionmaker
from database_vendas import Produto, cliente, db
import tkinter.messagebox as messagebox

# Cria a sessão com o banco de dados (usando "db_database_vendas.db")
Session = sessionmaker(bind=db)
session = Session()

# ======================== FUNÇÕES DE PRODUTOS ========================

def salvar_produto(cod_entry, nome_entry, preco_venda_entry, preco_compra_entry, status_label):
    """
    Insere um novo produto ou atualiza um existente com base no código informado.
    Se o código já existir, atualiza os dados; senão, insere um novo.
    """
    try:
        cod = int(cod_entry.get().strip())
    except ValueError:
        status_label.configure(text="Código inválido!", text_color="red")
        return
    nome = nome_entry.get().strip()
    try:
        preco_venda = float(preco_venda_entry.get().strip().replace(',', '.'))
        preco_compra = float(preco_compra_entry.get().strip().replace(',', '.'))
    except ValueError:
        status_label.configure(text="Preços inválidos!", text_color="red")
        return

    if not nome:
        status_label.configure(text="Informe o nome do produto!", text_color="red")
        return

    produto_existente = session.query(Produto).filter_by(cod_produto=cod).first()
    if produto_existente:
        produto_existente.nome_produto = nome
        produto_existente.preco_venda = preco_venda
        produto_existente.preco_compra = preco_compra
        produto_existente.lucro = preco_venda - preco_compra
        session.commit()
        status_label.configure(text="Produto atualizado com sucesso!", text_color="green")
    else:
        novo_produto = Produto(nome_produto=nome, cod_produto=cod,
                               preco_venda=preco_venda, preco_compra=preco_compra)
        session.add(novo_produto)
        session.commit()
        status_label.configure(text="Produto cadastrado com sucesso!", text_color="green")

def buscar_produto(cod_entry, nome_entry, preco_venda_entry, preco_compra_entry, status_label):
    """
    Pesquisa um produto pelo código informado; se encontrado, preenche os campos com os dados;
    senão, limpa os campos para novo cadastro.
    """
    try:
        cod = int(cod_entry.get().strip())
    except ValueError:
        status_label.configure(text="Código inválido!", text_color="red")
        return
    produto_existente = session.query(Produto).filter_by(cod_produto=cod).first()
    if produto_existente:
        nome_entry.delete(0, "end")
        nome_entry.insert(0, produto_existente.nome_produto)
        preco_venda_entry.delete(0, "end")
        preco_venda_entry.insert(0, f"{produto_existente.preco_venda:.2f}")
        preco_compra_entry.delete(0, "end")
        preco_compra_entry.insert(0, f"{produto_existente.preco_compra:.2f}")
        status_label.configure(text="Produto encontrado. Edite se necessário.", text_color="blue")
    else:
        nome_entry.delete(0, "end")
        preco_venda_entry.delete(0, "end")
        preco_compra_entry.delete(0, "end")
        status_label.configure(text="Produto não encontrado.", text_color="orange")

def deletar_produto(cod_entry, nome_entry, preco_venda_entry, preco_compra_entry, status_label):
    """
    Exibe uma confirmação para exclusão; se confirmado, deleta o produto com o código informado e limpa os campos.
    """
    try:
        cod = int(cod_entry.get().strip())
    except ValueError:
        status_label.configure(text="Código inválido!", text_color="red")
        return
    produto_existente = session.query(Produto).filter_by(cod_produto=cod).first()
    if produto_existente:
        confirm = messagebox.askyesno("Confirmar Exclusão", "Tem certeza que deseja deletar este produto?")
        if confirm:
            session.delete(produto_existente)
            session.commit()
            status_label.configure(text="Produto deletado!", text_color="green")
            cod_entry.delete(0, "end")
            nome_entry.delete(0, "end")
            preco_venda_entry.delete(0, "end")
            preco_compra_entry.delete(0, "end")
        else:
            status_label.configure(text="Exclusão cancelada.", text_color="blue")
    else:
        status_label.configure(text="Produto não encontrado!", text_color="red")

# ======================== FUNÇÕES DE CLIENTES ========================

def salvar_cliente(nome_entry, cod_entry, status_label):
    """
    Insere ou atualiza um cliente. Se o código informado já existir, atualiza o nome;
    senão, insere um novo cliente com total_conta_cliente iniciado em 0.0.
    """
    nome = nome_entry.get().strip()
    try:
        cod = int(cod_entry.get().strip())
    except ValueError:
        status_label.configure(text="Código do cliente inválido!", text_color="red")
        return

    if not nome:
        status_label.configure(text="Informe o nome do cliente!", text_color="red")
        return

    cliente_existente = session.query(cliente).filter_by(cod_cliente=cod).first()
    if cliente_existente:
        cliente_existente.nome_cliente = nome
        session.commit()
        status_label.configure(text="Cliente atualizado com sucesso!", text_color="green")
    else:
        novo_cliente = cliente(nome_cliente=nome, cod_cliente=cod, total_conta_cliente=0.0)
        session.add(novo_cliente)
        session.commit()
        status_label.configure(text="Cliente cadastrado com sucesso!", text_color="green")

def deletar_cliente(nome_entry, cod_entry, status_label):
    """
    Exibe uma confirmação para exclusão e, se afirmada, deleta o cliente correspondente ao código informado e limpa os campos.
    """
    try:
        cod = int(cod_entry.get().strip())
    except ValueError:
        status_label.configure(text="Código do cliente inválido!", text_color="red")
        return
    cliente_existente = session.query(cliente).filter_by(cod_cliente=cod).first()
    if cliente_existente:
        confirm = messagebox.askyesno("Confirmar Exclusão", "Tem certeza que deseja deletar este cliente?")
        if confirm:
            session.delete(cliente_existente)
            session.commit()
            status_label.configure(text="Cliente deletado!", text_color="green")
            nome_entry.delete(0, "end")
            cod_entry.delete(0, "end")
        else:
            status_label.configure(text="Exclusão cancelada.", text_color="blue")
    else:
        status_label.configure(text="Cliente não encontrado!", text_color="red")

def buscar_cliente(nome_entry, cod_entry, status_label, entry_receber, btn_receber_pagamento):
    """
    Pesquisa o cliente com base nos campos de nome e código. Se encontrado, exibe o total da conta.
    Se o total for maior que zero, mostra os widgets para receber pagamento.
    """
    nome = nome_entry.get().strip()
    try:
        cod = int(cod_entry.get().strip())
    except ValueError:
        status_label.configure(text="Código inválido!", text_color="red")
        return
    cl = session.query(cliente).filter_by(nome_cliente=nome, cod_cliente=cod).first()
    if cl:
        status_label.configure(text=f"💰 Total da Conta: R$ {cl.total_conta_cliente:.2f}", text_color="green")
        if cl.total_conta_cliente > 0:
            entry_receber.pack(pady=5)
            btn_receber_pagamento.pack(pady=5)
            btn_receber_pagamento.configure(command=lambda: receber_pagamento_cliente(cl, status_label, entry_receber))
        else:
            entry_receber.pack_forget()
            btn_receber_pagamento.pack_forget()
    else:
        status_label.configure(text="❌ Cliente não encontrado!", text_color="red")
        entry_receber.pack_forget()
        btn_receber_pagamento.pack_forget()

def receber_pagamento_cliente(cl, status_label, entry_receber):
    """
    Recebe um valor para pagamento: se o valor recebido for maior ou igual ao total da conta,
    zera o total e mostra o troco; caso contrário, atualiza o total para total - valor recebido.
    """
    try:
        valor = float(entry_receber.get().strip().replace(',', '.'))
    except ValueError:
        status_label.configure(text="Valor inválido!", text_color="red")
        return
    if valor >= cl.total_conta_cliente:
        troco = valor - cl.total_conta_cliente
        cl.total_conta_cliente = 0.0
        session.commit()
        status_label.configure(text=f"Pagamento recebido. Troco: R$ {troco:.2f}", text_color="green")
    else:
        cl.total_conta_cliente -= valor
        session.commit()
        status_label.configure(text=f"Pagamento recebido. Novo total: R$ {cl.total_conta_cliente:.2f}", text_color="green")
    entry_receber.delete(0, "end")

# ======================== INTERFACE DE CADASTROS ========================

def open_interface_cadastros():
    """
    Abre a interface de cadastros dividida em duas áreas:
      • Lado esquerdo: Cadastro de Produtos (campos para código, nome, preço de venda, preço de compra;
        botões para salvar, buscar e deletar).
      • Lado direito: Cadastro de Clientes (campos para nome, código; botões para buscar, salvar e deletar;
        se for buscado e houver dívida, exibe campo e botão para receber pagamento).
    A interface só será aberta quando esta função for chamada.
    """
    app = ctk.CTk()
    app.title("Cadastro de Produtos e Clientes")
    app.geometry("300, 500,+0+0")
    app.configure(fg_color=cor_principal())

    # Contêiner principal (usando grid com duas colunas)
    frame_main = ctk.CTkFrame(app, fg_color=cor_principal())
    frame_main.pack(padx=20, pady=20, fill="both", expand=True)

    # ----- Área de Produtos (lado esquerdo) -----
    frame_produtos = ctk.CTkFrame(frame_main, fg_color=cor_principal())
    frame_produtos.grid(row=0, column=0, padx=20, pady=20, sticky="n")

    label_produtos = ctk.CTkLabel(frame_produtos, text="Cadastro de Produtos",
                                  font=ctk.CTkFont(size=20, family="Arial Bold"),
                                  text_color="black")
    label_produtos.pack(pady=10)

    # Campos de produto:
    label_cod_prod = ctk.CTkLabel(frame_produtos, text="Código do Produto:", text_color="black")
    label_cod_prod.pack(pady=2)
    entry_cod_prod = ctk.CTkEntry(frame_produtos, width=250, placeholder_text="Digite o código")
    entry_cod_prod.pack(pady=2)

    label_nome_prod = ctk.CTkLabel(frame_produtos, text="Nome do Produto:", text_color="black")
    label_nome_prod.pack(pady=2)
    entry_nome_prod = ctk.CTkEntry(frame_produtos, width=250, placeholder_text="Digite o nome")
    entry_nome_prod.pack(pady=2)

    label_preco_venda = ctk.CTkLabel(frame_produtos, text="Preço de Venda:", text_color="black")
    label_preco_venda.pack(pady=2)
    entry_preco_venda = ctk.CTkEntry(frame_produtos, width=250, placeholder_text="Digite o preço de venda")
    entry_preco_venda.pack(pady=2)

    label_preco_compra = ctk.CTkLabel(frame_produtos, text="Preço de Compra:", text_color="black")
    label_preco_compra.pack(pady=2)
    entry_preco_compra = ctk.CTkEntry(frame_produtos, width=250, placeholder_text="Digite o preço de compra")
    entry_preco_compra.pack(pady=2)

    status_produto = ctk.CTkLabel(frame_produtos, text="", font=ctk.CTkFont(size=14), text_color="black")
    status_produto.pack(pady=5)

    # Botões para produtos:
    btn_salvar_prod = ctk.CTkButton(frame_produtos, text="Salvar Produto",
                                   command=lambda: salvar_produto(entry_cod_prod, entry_nome_prod,
                                                                  entry_preco_venda, entry_preco_compra,
                                                                  status_produto))
    btn_salvar_prod.pack(pady=5)

    btn_buscar_prod = ctk.CTkButton(frame_produtos, text="Buscar Produto",
                                    command=lambda: buscar_produto(entry_cod_prod, entry_nome_prod,
                                                                   entry_preco_venda, entry_preco_compra,
                                                                   status_produto))
    btn_buscar_prod.pack(pady=5)

    btn_deletar_prod = ctk.CTkButton(frame_produtos, text="Deletar Produto", fg_color="red", text_color="white",
                                    command=lambda: deletar_produto(entry_cod_prod, entry_nome_prod,
                                                                    entry_preco_venda, entry_preco_compra,
                                                                    status_produto))
    btn_deletar_prod.pack(pady=5)

    # ----- Área de Clientes (lado direito) -----
    frame_clientes = ctk.CTkFrame(frame_main, fg_color=cor_principal())
    frame_clientes.grid(row=0, column=1, padx=20, pady=20, sticky="n")

    label_clientes = ctk.CTkLabel(frame_clientes, text="Cadastro de Clientes",
                                  font=ctk.CTkFont(size=20, family="Arial Bold"), text_color="black")
    label_clientes.pack(pady=10)

    label_nome_cliente = ctk.CTkLabel(frame_clientes, text="Nome do Cliente:", text_color="black")
    label_nome_cliente.pack(pady=2)
    entry_nome_cliente = ctk.CTkEntry(frame_clientes, width=250, placeholder_text="Digite o nome")
    entry_nome_cliente.pack(pady=2)

    label_cod_cliente = ctk.CTkLabel(frame_clientes, text="Código do Cliente:", text_color="black")
    label_cod_cliente.pack(pady=2)
    entry_cod_cliente = ctk.CTkEntry(frame_clientes, width=250, placeholder_text="Digite o código")
    entry_cod_cliente.pack(pady=2)

    # Botão para buscar o cliente e exibir o total da conta
    btn_buscar_cliente = ctk.CTkButton(frame_clientes, text="Buscar Cliente",
                                       command=lambda: buscar_cliente(entry_nome_cliente, entry_cod_cliente,
                                                                      status_cliente, entry_valor_receber,
                                                                      btn_receber_pagamento))
    btn_buscar_cliente.pack(pady=5)

    status_cliente = ctk.CTkLabel(frame_clientes, text="", font=ctk.CTkFont(size=14), text_color="black")
    status_cliente.pack(pady=5)

    # Widgets para receber pagamento - inicialmente ocultos
    entry_valor_receber = ctk.CTkEntry(frame_clientes, width=200, placeholder_text="Valor a receber")
    entry_valor_receber.pack_forget()

    btn_receber_pagamento = ctk.CTkButton(frame_clientes, text="Receber Pagamento", fg_color="green", text_color="black")
    btn_receber_pagamento.pack_forget()

    btn_salvar_cliente = ctk.CTkButton(frame_clientes, text="Salvar Cliente",
                                       command=lambda: salvar_cliente(entry_nome_cliente, entry_cod_cliente, status_cliente))
    btn_salvar_cliente.pack(pady=5)

    btn_deletar_cliente = ctk.CTkButton(frame_clientes, text="Deletar Cliente", fg_color="red", text_color="white",
                                        command=lambda: deletar_cliente(entry_nome_cliente, entry_cod_cliente, status_cliente))
    btn_deletar_cliente.pack(pady=5)

    app.mainloop()
