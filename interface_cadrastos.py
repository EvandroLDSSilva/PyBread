import customtkinter as ctk
from global_resources import *
import ctypes

#ctypes.windll.user32.SetProcessDPIAware()

def open_interface_cadastros():
    tela_cadastros = ctk.CTk()
    tela_cadastros.title('CRUD - Cadrastos')
    tela_cadastros.geometry(resolucao_tela_monitor())
    tela_cadastros.configure(fg_color= cor_principal()) 

    label_bvnd_cadrastos = ctk.CTkLabel(
        tela_cadastros,
        text='Bem-vindo à Criação de Planilhas! 😃',
        text_color='black',
        font=ctk.CTkFont(size=22, family="Arial Bold")
    )
    label_bvnd_cadrastos.pack(relx= 0.5, rely= 0.05)

    tela_cadastros.protocol("WM_DELETE_WINDOW", lambda: safe_destroy(tela_cadastros))
    tela_cadastros.bind("<q>", lambda event: safe_destroy(tela_cadastros))

    tela_cadastros.mainloop()
