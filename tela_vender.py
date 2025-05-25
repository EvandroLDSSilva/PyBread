import customtkinter as ctk
import ctypes
from global_resources import *
from database_vendas import *
from decimal import Decimal, ROUND_UP

ctypes.windll.user32.SetProcessDPIAware()

Session = sessionmaker(bind=db)
session = Session()

def open_tela_vender(total_valor):
    
    tela_vndr = ctk.CTk()
    tela_vndr.title('Tela de Vendas')
    tela_vndr.geometry(resolucao_tela_monitor())
    tela_vndr.configure(fg_color=cor_principal())

    label_total_vender = ctk.CTkLabel(
        tela_vndr,
        text=f"Total: R$ {total_valor:.2f}".replace('.', ','),
        text_color='black',
        font=ctk.CTkFont(size=22, family="Arial Bold")
    )
    label_total_vender.place(relx=0.75, rely=0.40)

    def atualizar_total():
        label_total_vender.configure(text=f"Total: R$ {total_valor:.2f}".replace('.', ','))
        tela_vndr.after(500, atualizar_total)

    atualizar_total()

    campo_rcb_dinheiro = ctk.CTkEntry(
        tela_vndr,
        placeholder_text='Dinheiro recebido',
        width=300, height=40,
        font=ctk.CTkFont(size=16, family="Arial Bold"), 
        fg_color=cor_secundaria(), 
        text_color="white"
    )
    campo_rcb_dinheiro.place(relx=0.75, rely=0.50)

    label_troco_vender = ctk.CTkLabel(
        tela_vndr,
        text="Troco: R$ 0,00",
        text_color='black',
        font=ctk.CTkFont(size=22, family="Arial Bold")
    )
    label_troco_vender.place(relx=0.75, rely=0.60)

    def atualizar_troco(event=None):
        try:
            dinheiro_recebido = Decimal(campo_rcb_dinheiro.get().replace(',', '.') or '0')
            troco = dinheiro_recebido - total_valor
            label_troco_vender.configure(text=f"Troco: R$ {troco:.2f}".replace('.', ','))
        except ValueError:
            label_troco_vender.configure(text="Valor inválido")

    campo_rcb_dinheiro.bind("<Return>", atualizar_troco)

    tela_vndr.protocol("WM_DELETE_WINDOW", lambda: safe_destroy(tela_vndr))
    tela_vndr.bind("<q>", lambda event: safe_destroy(tela_vndr))

    tela_vndr.mainloop()
