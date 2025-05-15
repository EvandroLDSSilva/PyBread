import customtkinter as ctk
import ctypes
from global_resources import *
from database_vendas import *
from interface_vendas import *
#from interface_vendas import

ctypes.windll.user32.SetProcessDPIAware()

Session = sessionmaker(bind=db)
session = Session()

total_valor = Decimal('0.00')

def open_tela_vender():
    global total_valor
    tela_vndr = ctk.CTk()
    tela_vndr.title('Tela de Vendas')
    tela_vndr.geometry(resolucao_tela_monitor())
    tela_vndr.configure(fg_color=cor_principal())

    label_boas_vindas = ctk.CTkLabel(
    tela_vndr,
    text=f"Total: R$ {total_valor:.2f}".replace('.', ','),
    text_color='black',
    font=ctk.CTkFont(size=22, family="Arial Bold")
)

    tela_vndr.protocol("WM_DELETE_WINDOW", lambda: safe_destroy(tela_vndr))
    tela_vndr.bind("<q>", lambda event: safe_destroy(tela_vndr))

    tela_vndr.mainloop()