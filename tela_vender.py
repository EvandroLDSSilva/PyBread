import customtkinter as ctk
import ctypes
from global_resources import *
from database_vendas import *
from interface_vendas import *
from decimal import Decimal, ROUND_UP

ctypes.windll.user32.SetProcessDPIAware()

Session = sessionmaker(bind=db)
session = Session()

total_valor = Decimal('0.00')

def open_tela_vender():
    global total_valor
    
    registros = session.query(Produto).all()

    total_soma = sum(Decimal(str(registro.preco_venda)) for registro in registros)

    total_valor += total_soma

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

    campo_rcb_dinheiro= ctk.CTkEntry(
        tela_vndr,
        placeholder_text='Dinheiro recebido',
        width=300, height=40,
        font=ctk.CTkFont(size=16, 
        family="Arial Bold"), 
        fg_color=cor_secundaria(), 
        text_color="white"
    )
    campo_rcb_dinheiro.place(relx=0.75, rely=0.50)

    #campo_usuario = ctk.CTkEntry(
    #security,
    #placeholder_text='Digite o Usuário',
    #font=ctk.CTkFont(size=14, family="Roboto Bold"),
    #fg_color="#23272A",
    #text_color="white"
#)
#campo_usuario.pack(pady=15)

    tela_vndr.protocol("WM_DELETE_WINDOW", lambda: safe_destroy(tela_vndr))
    tela_vndr.bind("<q>", lambda event: safe_destroy(tela_vndr))

    tela_vndr.mainloop()
