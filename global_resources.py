import customtkinter as ctk
import ctypes
from datetime import datetime
from sqlalchemy import *
from sqlalchemy.orm import *

#ctypes.windll.user32.SetProcessDPIAware()

def cor_principal():
    return "#ffffff"

def cor_secundaria():
    return "#4169E1"

def cor_terciaria():
    return "#87CEFA"

def resolucao_tela_monitor():
    tela_monitor = ctk.CTk()
    largura_monitor = tela_monitor.winfo_screenwidth()
    altura_monitor = tela_monitor.winfo_screenheight()
    tela_monitor.destroy()
    return f"{largura_monitor - 100}x{altura_monitor - 300}+10+30"

def safe_destroy(widget):
    try:
        after_info = widget.tk.call('after', 'info')
        if after_info:
            ids = after_info.split()
            for id in ids:
                try:
                    widget.after_cancel(id)
                except Exception:
                    pass
    except Exception:
        pass

    try:
        widget.destroy()
    except Exception as e:
        print(f"Erro ao destruir o widget: {e}")

usuarios_validos = {
    'jorge': '123456',
    'adm': '2335',
    '': ''  
}

def valid_login(usuario, senha):
    """Verifica credenciais e retorna True se o login for válido."""
    return usuario in usuarios_validos and senha == usuarios_validos[usuario]

def carregar_data():
    agora = datetime.now()
    return agora.strftime("%d/%m/%Y %H:%M:%S")

def atualizar_data(label, tela):
    nova_data = carregar_data()
    label.configure(text=nova_data)
    tela.after(1000, lambda: atualizar_data(label, tela))
