import customtkinter as ctk
from global_resources import *
from interface_vendas_mod import open_interface_vendas
from interface_cadastos import open_interface_cadastros
from interface_receita import open_interface_receita
from AIChatbox.interface_ia import open_interface_ia  # Baggete Bot
import ctypes
from datetime import datetime
from PIL import Image

def carregar_data():
    agora = datetime.now()
    return agora.strftime("%d/%m/%Y %H:%M:%S")

def resolucao_tela_monitor():
    tela_monitor = ctk.CTk()
    largura_monitor = tela_monitor.winfo_screenwidth()
    altura_monitor = tela_monitor.winfo_screenheight() - 75
    tela_monitor.destroy()
    return (largura_monitor, altura_monitor)

def open_interface_principal():
    tela_principal = ctk.CTk()
    tela_principal.title('PyPão - Tela inicial')
    largura, altura = resolucao_tela_monitor()
    tela_principal.geometry(f"{largura}x{altura}+0+0")
    tela_principal.configure(fg_color=cor_principal())

    img_fundo = Image.open("C:\\PyBread\\fundo_azul_branco.jpg")
    img_fundo = img_fundo.resize((largura, altura))
    bg_image = ctk.CTkImage(light_image=img_fundo, dark_image=img_fundo, size=(largura, altura))

    label_fundo = ctk.CTkLabel(tela_principal, image=bg_image, text="")
    label_fundo.pack(fill="both", expand=True)
    label_fundo.lower()

    img_papel_cadastro = ctk.CTkImage(light_image=Image.open("C:\\PyBread\\blue_area_cadastros_paper.png"),
                                      dark_image=Image.open("C:\\PyBread\\blue_area_cadastros_paper.png"), size=(150, 150))

    img_baggete_bot_logo = ctk.CTkImage(light_image=Image.open("C:\\PyBread\\bagguete_bot_logo.png"),
                                        dark_image=Image.open("C:\\PyBread\\bagguete_bot_logo.png"), size=(200, 200))

    img_carrinho_compras = ctk.CTkImage(light_image=Image.open("C:\\PyBread\\blue_area_vendas_car.png"),
                                        dark_image=Image.open("C:\\PyBread\\blue_area_vendas_car.png"), size=(150, 150))

    img_receitas = ctk.CTkImage(light_image=Image.open("C:\\PyBread\\blue_area_receitas.png"),
                                dark_image=Image.open("C:\\PyBread\\blue_area_receitas.png"), size=(150, 150))

    img_bvnd_pypao = ctk.CTkImage(light_image=Image.open("C:\\PyBread\\bvnd_PyPao.png"),
                                  dark_image=Image.open("C:\\PyBread\\bvnd_PyPao.png"), size=(320, 180))

    label_img_bvnd_pypao = ctk.CTkLabel(tela_principal, image=img_bvnd_pypao, text='', text_color='Black',
                                        fg_color="transparent", font=ctk.CTkFont(size=22, family="Arial Bold"))
    label_img_bvnd_pypao.place(relx=0.75, rely=0.05)

    btm_f_area_vendas = ctk.CTkButton(tela_principal, image=img_carrinho_compras, text='', command=open_interface_vendas,
                                      width=200, height=200, font=ctk.CTkFont(size=18, family="Arial Bold"),
                                      fg_color="transparent", hover_color=cor_principal(), text_color="white")
    btm_f_area_vendas.place(relx=0.05, rely=0.05)

    btm_f_cadastros = ctk.CTkButton(tela_principal, image=img_papel_cadastro, text='', command=open_interface_cadastros,
                                    width=200, height=200, font=ctk.CTkFont(size=18, family="Arial Bold"),
                                    fg_color="transparent", hover_color=cor_principal(), text_color="white")
    btm_f_cadastros.place(relx=0.20, rely=0.05)

    btm_f_receita = ctk.CTkButton(tela_principal, image=img_receitas, text='Receita', command=open_interface_receita,
                                  width=200, height=200, font=ctk.CTkFont(size=18, family="Arial Bold"),
                                  fg_color="transparent", hover_color=cor_principal(), text_color="white")
    btm_f_receita.place(relx=0.35, rely=0.05)

    btm_open_ia = ctk.CTkButton(tela_principal, image=img_baggete_bot_logo, text='', command=open_interface_ia,
                                width=200, height=200, font=ctk.CTkFont(size=18, family="Arial Bold"),
                                fg_color="transparent", hover_color=cor_principal(), text_color="white")
    btm_open_ia.place(relx=0.80, rely=0.27)

    tela_principal.mainloop()
