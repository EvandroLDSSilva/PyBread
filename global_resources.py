import customtkinter as ctk
import ctypes
from ctypes import wintypes

ctypes.windll.user32.SetProcessDPIAware()

def cor_principal():
    return "#ffffff"  #Branco puro

def cor_secundaria():
    return "#4169E1"  # Cor Azul

def cor_terciaria():
    return "#87CEFA"  # Cor Azul claro

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

def valid_login(campo_usuario, campo_senha, result_login, security, open_interface_principal):
    usuario = campo_usuario.get()
    senha = campo_senha.get()

    if (usuario == 'jorge' and senha == '123456') or (usuario == 'adm' and senha == '2335') or (usuario == '' and senha == ''):
        result_login.configure(text='Login Concluido \n Bem Vindo :D', text_color='green')
        security.after(300, lambda: safe_destroy(security), open_interface_principal())
    else:
        result_login.configure(text='Login Inválido', text_color='red')
