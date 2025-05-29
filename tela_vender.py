import customtkinter as ctk
from decimal import Decimal, ROUND_UP
from global_resources import *    
from database_vendas import *           
from sqlalchemy.orm import sessionmaker
import tkinter.messagebox as messagebox        

Session = sessionmaker(bind=db)
session = Session()

def open_tela_vender(total_valor, total_lucro, box_texto, campo_codebar, campo_quant, total_label):

    tela_vndr = ctk.CTk()
    tela_vndr.title('Tela de Vendas')
    tela_vndr.geometry("500x600")
    tela_vndr.configure(fg_color=cor_principal())

    label_total_vender = ctk.CTkLabel(
        tela_vndr,
        text=f"Total: R$ {total_valor:.2f}".replace('.', ','),
        text_color='black',
        font=ctk.CTkFont(size=22, family="Arial Bold")
    )
    label_total_vender.place(relx=0.5, rely=0.30, anchor="center")

    campo_rcb_dinheiro = ctk.CTkEntry(
        tela_vndr,
        placeholder_text='Dinheiro recebido',
        width=300,
        height=40,
        font=ctk.CTkFont(size=16, family="Arial Bold"),
        fg_color=cor_secundaria(),
        text_color="white"
    )
    campo_rcb_dinheiro.place(relx=0.5, rely=0.40, anchor="center")

    label_troco_vender = ctk.CTkLabel(
        tela_vndr,
        text="Troco: R$ 0,00",
        text_color='black',
        font=ctk.CTkFont(size=22, family="Arial Bold")
    )
    label_troco_vender.place(relx=0.5, rely=0.50, anchor="center")

    label_erro = ctk.CTkLabel(
        tela_vndr,
        text="",
        text_color="red",
        font=ctk.CTkFont(size=16)
    )
    label_erro.place(relx=0.5, rely=0.57, anchor="center")
    
    btm_finalizar_venda = ctk.CTkButton(
        tela_vndr,
        text='Finalizar Venda',
        command=lambda: finalizar_venda(),
        width=250,
        height=50,
        font=ctk.CTkFont(size=16, family="Arial Bold"),
        fg_color=cor_secundaria(),
        text_color="white"
    )
    btm_finalizar_venda.place_forget()

    def atualizar_troco(event=None):
        """Calcula e atualiza o troco e decide se exibe o botão de finalizar."""
        try:
            dinheiro_recebido = Decimal(campo_rcb_dinheiro.get().replace(',', '.') or '0')
            troco = dinheiro_recebido - total_valor
            label_troco_vender.configure(text=f"Troco: R$ {troco:.2f}".replace('.', ','))
            if dinheiro_recebido >= total_valor:
                label_erro.configure(text="")
                btm_finalizar_venda.place(relx=0.5, rely=0.70, anchor="center")
            else:
                label_erro.configure(text="Valor recebido insuficiente!")
                btm_finalizar_venda.place_forget()
        except Exception as e:
            label_troco_vender.configure(text="Valor inválido")
            label_erro.configure(text="Valor inválido")
            btm_finalizar_venda.place_forget()

    campo_rcb_dinheiro.bind("<Return>", atualizar_troco)

    def finalizar_venda():
        """Verifica novamente o valor recebido e finaliza a venda se for suficiente."""
        try:
            dinheiro_recebido = Decimal(campo_rcb_dinheiro.get().replace(',', '.') or '0')
        except Exception:
            label_erro.configure(text="Valor inválido no campo!")
            return

        if dinheiro_recebido < total_valor:
            label_erro.configure(text="Valor recebido insuficiente!")
            return

        print("Finalizando Venda!")
        from interface_vendas_mod import save_cupom_db
        save_cupom_db(box_texto, total_label, campo_codebar, campo_quant, total_valor, total_lucro)
        tela_vndr.destroy()

    tela_vndr.mainloop()
