import customtkinter as ctk
import ctypes
from decimal import Decimal, ROUND_UP
from sqlalchemy.orm import *
from database_vendas import *
from global_resources import *
from tela_vender import *

ctypes.windll.user32.SetProcessDPIAware()

Session = sessionmaker(bind=db)
session = Session()

def open_interface_vendas():
    intfc_vendas = ctk.CTk()
    intfc_vendas.title('Tela de Vendas')
    intfc_vendas.geometry(resolucao_tela_monitor())
    intfc_vendas.configure(fg_color=cor_principal())

    total_valor = Decimal("0.00")
    total_label = ctk.CTkLabel(intfc_vendas, text="Total: R$ 0,00", text_color="black", font=ctk.CTkFont(size=20, family="Arial Bold"))
    total_label.place(relx=0.35, rely=0.65)

    campo_codebar = ctk.CTkEntry(intfc_vendas, placeholder_text='Digite o código de barras: ', width=300, height=40, font=ctk.CTkFont(size=16, family="Arial Bold"), fg_color=cor_secundaria(), text_color="white")
    campo_codebar.place(relx=0.6, rely=0.75)

    campo_quant = ctk.CTkEntry(intfc_vendas, placeholder_text='Digite a quantidade', width=300, height=40, font=ctk.CTkFont(size=16, family="Arial Bold"), fg_color=cor_secundaria(), text_color="white")
    campo_quant.place(relx=0.6, rely=0.85)

    btm_vender = ctk.CTkButton(intfc_vendas, text='receber \ná vista', command=open_tela_vender, width=250, height=50, font=ctk.CTkFont(size=16, family="Arial Bold"), fg_color=cor_secundaria(), text_color="white")
    btm_vender.place(relx=0.6, rely=0.30)

    box_texto = ctk.CTkTextbox(intfc_vendas, width=350, height=350, fg_color=cor_terciaria(), text_color="black")
    box_texto.place(relx=0.35, rely=0.70)

    #def total_tudo():
        


    def show_info(event=None):
        nonlocal total_valor
        codigo = campo_codebar.get()
        quant = campo_quant.get()
        box_texto.configure(state="normal")

        try:
            produto = session.query(Produto).filter_by(cod_produto=int(codigo)).first()
        except ValueError:
            produto = None

        if produto:
            try:
                quant_float = float(quant.replace(',', '.')) if quant else 1
            except ValueError:
                quant_float = 1

            total = Decimal(produto.preco_venda) * Decimal(quant_float)
            total = total.quantize(Decimal('0.01'), rounding=ROUND_UP)
            total_valor += total
            total_label.configure(text=f"Total: R$ {format(total_valor, '.2f').replace('.', ',')}")
            
            box_texto.configure(state="normal")
            box_texto.insert("end", f"Nome: {produto.nome_produto}\n")
            box_texto.insert("end", f"Código: {produto.cod_produto}\n")
            box_texto.insert("end", f"Preço: R$ {produto.preco_venda:.2f}     Quantidade: {quant_float}\n")
            box_texto.insert("end", f"Total: R$ {total}\n")
            box_texto.insert("end", f"Lucro armazenado: R$ {produto.lucro:.2f}\n")
            box_texto.insert("end", "-" * 20 + "\n")
        else:
            box_texto.insert("end", f"Código {codigo} não encontrado no banco.\n")
            box_texto.insert("end", "-" * 20 + "\n")

        box_texto.configure(state="disabled")
        campo_codebar.delete(0, "end")
        campo_quant.delete(0, "end")

    campo_codebar.bind("<Return>", show_info)
    campo_quant.bind("<Return>", show_info)
    intfc_vendas.protocol("WM_DELETE_WINDOW", lambda: safe_destroy(intfc_vendas))
    intfc_vendas.bind("<q>", lambda event: safe_destroy(intfc_vendas))
    intfc_vendas.mainloop()
