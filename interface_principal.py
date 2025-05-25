import customtkinter as ctk
from global_resources import *
from interface_vendas import open_interface_vendas
from interface_cPlanilhas import open_interface_cPlanilhas
import ctypes
from datetime import datetime

ctypes.windll.user32.SetProcessDPIAware()

def carregar_data():
    """Retorna a data e hora atual formatada."""
    agora = datetime.now()
    return agora.strftime("%d/%m/%Y %H:%M:%S")

def open_interface_principal():
    tela_principal = ctk.CTk()
    tela_principal.title('Bem-vindo!')
    tela_principal.geometry(resolucao_tela_monitor())
    tela_principal.configure(fg_color=cor_principal()) 

    label_boas_vindas = ctk.CTkLabel(
        tela_principal,
        text='Bem-vindo à tela principal!',
        text_color='white',
        font=ctk.CTkFont(size=22, family="Arial Bold")
    )
    label_boas_vindas.pack(padx=50, pady=20)

    btm_f_area_vendas = ctk.CTkButton(
        tela_principal,
        text='Área\nVendas',
        command=open_interface_vendas,
        width=100,
        height=100,
        font=ctk.CTkFont(size=18, family="Arial Bold"),
        fg_color=cor_secundaria(),
        text_color="white"
    )
    btm_f_area_vendas.place(relx=0.40, rely=0.30)

    btm_f_cPlanilha = ctk.CTkButton(
        tela_principal,
        text='Criação\nPlanilhas',
        command=open_interface_cPlanilhas,
        width=100,
        height=100,
        font=ctk.CTkFont(size=18, family="Arial Bold"),
        fg_color=cor_secundaria(),
        text_color="white"
    )
    btm_f_cPlanilha.place(relx=0.55, rely=0.30)

    btm_f_area_vendas = ctk.CTkButton(
        tela_principal,
        text='IA\nBaggeteBot',
        command=open_,
        width=100,
        height=100,
        font=ctk.CTkFont(size=18, family="Arial Bold"),
        fg_color=cor_secundaria(),
        text_color="white"
    )
    btm_f_area_vendas.place(relx=0.40, rely=0.30)

    label_datahora_intf_principal = ctk.CTkLabel(
        tela_principal,
        text=carregar_data(),
        text_color='black',
        font=ctk.CTkFont(size=15, family="Arial Bold"))
    label_datahora_intf_principal.place(relx=0.10, rely=0.90)

    def atualizar_data():
        label_datahora_intf_principal.configure(text=carregar_data())
        tela_principal.after(1000, atualizar_data)

    # Inicia a atualização automática da data e hora
    atualizar_data()

    btm_exit_tela_principal = ctk.CTkButton(
        tela_principal,
        text='EXIT',
        command=lambda: safe_destroy(tela_principal),
        width=80,
        height=40,
        font=ctk.CTkFont(size=16, family="Arial Bold"),
        fg_color="red",
        text_color="white"
    )
    btm_exit_tela_principal.place(relx=0.90, rely=0.90)

    tela_principal.protocol("WM_DELETE_WINDOW", lambda: safe_destroy(tela_principal))
    tela_principal.bind("<q>", lambda event: safe_destroy(tela_principal))

    tela_principal.mainloop()
