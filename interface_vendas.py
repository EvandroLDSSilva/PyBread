import customtkinter as ctk
import ctypes
from decimal import Decimal, ROUND_UP
from sqlalchemy.orm import sessionmaker
from database import Produto, db  # Importa a classe Produto e conexão com o banco

ctypes.windll.user32.SetProcessDPIAware()

# Conectar ao banco de dados
Session = sessionmaker(bind=db)
session = Session()

def open_interface_vendas():
    tela_vendas = ctk.CTk()
    tela_vendas.title('Tela de Vendas')
    tela_vendas.geometry("800x600")
    tela_vendas.configure(fg_color="#DDDDDD")

    total_valor = Decimal("0.00")

    total_label = ctk.CTkLabel(
        tela_vendas,
        text="Total: R$ 0,00",
        text_color="black",
        font=ctk.CTkFont(size=20, family="Arial Bold")
    )
    total_label.place(relx=0.35, rely=0.65)

    campo_codebar = ctk.CTkEntry(
        tela_vendas,
        placeholder_text='Digite o código de barras: ',
        width=300,
        height=40,
        font=ctk.CTkFont(size=16, family="Arial Bold"),
        text_color="black"
    )
    campo_codebar.place(relx=0.6, rely=0.75)

    campo_quant = ctk.CTkEntry(
        tela_vendas,
        placeholder_text='Digite a quantidade',
        width=300,
        height=40,
        font=ctk.CTkFont(size=16, family="Arial Bold"),
        text_color="black"
    )
    campo_quant.place(relx=0.6, rely=0.85)

    box_texto = ctk.CTkTextbox(
        tela_vendas,
        width=350,
        height=350,
        fg_color="#CCCCCC",
        text_color="black"
    )
    box_texto.place(relx=0.35, rely=0.70)

    def show_info(event=None):
        nonlocal total_valor
        codigo = campo_codebar.get()
        quant = campo_quant.get()
        box_texto.configure(state="normal")

        # 🔎 Buscar produto pelo código no banco de dados
        produto = session.query(Produto).filter_by(cod_produto=int(codigo)).first()

        if produto:
            try:
                quant_formatado = quant.replace(',', '.')
                quant_float = float(quant_formatado)
            except ValueError:
                quant_float = 1

            total = Decimal(produto.preco_venda) * Decimal(quant_float)
            total = total.quantize(Decimal('0.01'), rounding=ROUND_UP)

            total_valor += total
            total_label.configure(text=f"Total: R$ {format(total_valor, '.2f').replace('.', ',')}")

            # 🛒 Exibir informações do produto
            box_texto.insert("end", f"Nome: {produto.nome_produto}\n")
            box_texto.insert("end", f"Código: {produto.cod_produto}\n")
            box_texto.insert("end", f"Preço: R$ {produto.preco_venda:.2f}     Quantidade: {quant_float}\n")
            box_texto.insert("end", f"Total: R$ {total}\n")
            box_texto.insert("end", f"Lucro estimado: R$ {produto.lucro:.2f}\n")  # Exibe lucro armazenado no banco
            box_texto.insert("end", "-" * 20 + "\n")
        else:
            box_texto.insert("end", f"Código {codigo} não encontrado no banco.\n")
            box_texto.insert("end", "-" * 20 + "\n")

        box_texto.configure(state="disabled")
        campo_codebar.delete(0, "end")
        campo_quant.delete(0, "end")

    campo_codebar.bind("<Return>", show_info)
    campo_quant.bind("<Return>", show_info)

    tela_vendas.protocol("WM_DELETE_WINDOW", tela_vendas.destroy)
    tela_vendas.mainloop()
