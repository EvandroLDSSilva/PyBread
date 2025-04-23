import customtkinter as ctk
from global_resources import *
import ctypes

ctypes.windll.user32.SetProcessDPIAware()

def open_interface_cPlanilhas():
    tela_cPlanilhas = ctk.CTk()
    tela_cPlanilhas.title('Criador de Planilhas')
    tela_cPlanilhas.geometry(resolucao_tela_monitor())
    tela_cPlanilhas.configure(fg_color="#FFD700") 

    label_test = ctk.CTkLabel(
        tela_cPlanilhas,
        text='Bem-vindo à Criação de Planilhas! 😃',
        text_color='black',
        font=ctk.CTkFont(size=22, family="Arial Bold")
    )
    label_test.pack(pady=50)

    tela_cPlanilhas.protocol("WM_DELETE_WINDOW", lambda: safe_destroy(tela_cPlanilhas))
    tela_cPlanilhas.bind("<q>", lambda event: safe_destroy(tela_cPlanilhas))

    tela_cPlanilhas.mainloop()
