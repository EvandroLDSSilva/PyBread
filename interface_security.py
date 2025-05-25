import customtkinter as ctk
from interface_principal import open_interface_principal
from global_resources import *
from sqlalchemy import *
from sqlalchemy.orm import *
import ctypes

ctypes.windll.user32.SetProcessDPIAware()

security = ctk.CTk()
security.title('Sistema de Login')
security.geometry('300x400+0+0')
security.configure(fg_color="#2C2F33")  

label_usuario = ctk.CTkLabel(
    security,
    text='Usuário',
    text_color='white',
    font=ctk.CTkFont(size=16, family="Roboto Bold"),
)
label_usuario.pack(pady=10)

campo_usuario = ctk.CTkEntry(
    security,
    placeholder_text='Digite o Usuário',
    font=ctk.CTkFont(size=14, family="Roboto Bold"),
    fg_color="#23272A",
    text_color="white"
)
campo_usuario.pack(pady=15)

label_senha = ctk.CTkLabel(
    security,
    text='Senha',
    text_color='white',
    font=ctk.CTkFont(size=16, family="Roboto Bold")
)
label_senha.pack(pady=10)

campo_senha = ctk.CTkEntry(
    security,
    placeholder_text='Digite a senha',
    show='*',
    font=ctk.CTkFont(size=14, family="Roboto Bold"),
    fg_color="#23272A",
    text_color="white"
)
campo_senha.pack(pady=15)

result_login = ctk.CTkLabel( 
    security,
    text='',
    text_color='white',
    font=ctk.CTkFont(size=14, family="Roboto Bold")
)
result_login.pack(pady=10)

button_login = ctk.CTkButton(
    security,
    text='Login',
    command=lambda: valid_login(campo_usuario, campo_senha, result_login, security, open_interface_principal),
    font=ctk.CTkFont(size=16, family="Roboto Bold"),
    fg_color="#7289DA",
    text_color="white"
)
button_login.pack(pady=10)

label_guia_fecha_security = ctk.CTkLabel(
    security,
    text='Aperte "Q" para sair',
    text_color='white',
    font=ctk.CTkFont(size=14, family="Roboto Bold")
)
label_guia_fecha_security.pack(pady=10)

security.bind("<q>", lambda event: safe_destroy(security)) 
security.protocol("WM_DELETE_WINDOW", lambda: safe_destroy(security))

security.mainloop()