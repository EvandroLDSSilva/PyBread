import customtkinter as ctk
import ctypes
from global_resources import *
from database_vendas import *
from decimal import Decimal, ROUND_UP

#ctypes.windll.user32.SetProcessDPIAware()

Session = sessionmaker(bind=db)
session = Session()

def open_tela_vender(total_valor, box_texto, campo_codebar, campo_quant, total_label):
    
    tela_vndr = ctk.CTk()
    tela_vndr.title('Tela de Vendas')
    tela_vndr.geometry("500x600")
    tela_vndr.configure(fg_color=cor_principal())

    label_total_vender = ctk.CTkLabel(
        tela_vndr,
        text=f"Total: R$ {total_valor:.2f}".replace('.', ','),
        text_color='black',
        font=ctk.CTkFont(size=22, family="Arial Bold")
    )
    label_total_vender.place(relx=0.5, rely=0.35, anchor="center")

    campo_rcb_dinheiro = ctk.CTkEntry(
        tela_vndr,
        placeholder_text='Dinheiro recebido',
        width=300, height=40,
        font=ctk.CTkFont(size=16, family="Arial Bold"), 
        fg_color=cor_secundaria(), 
        text_color="white"
    )
    campo_rcb_dinheiro.place(relx=0.5, rely=0.45, anchor="center")  # Centralizado

    label_troco_vender = ctk.CTkLabel(
        tela_vndr,
        text="Troco: R$ 0,00",
        text_color='black',
        font=ctk.CTkFont(size=22, family="Arial Bold")
    )
    label_troco_vender.place(relx=0.5, rely=0.55, anchor="center")  # Centralizado

    def atualizar_troco(event=None):
        """Atualiza o troco quando o dinheiro recebido é inserido."""
        try:
            dinheiro_recebido = Decimal(campo_rcb_dinheiro.get().replace(',', '.') or '0')
            troco = dinheiro_recebido - total_valor
            label_troco_vender.configure(text=f"Troco: R$ {troco:.2f}".replace('.', ','))
        except ValueError:
            label_troco_vender.configure(text="Valor inválido")

    campo_rcb_dinheiro.bind("<Return>", atualizar_troco)

    def finalizar_venda():
        """Salva o cupom e fecha a janela corretamente."""
        print("Botão Finalizar Venda foi clicado!")

        from interface_vendas_mod import save_cupom_db  
        save_cupom_db(box_texto, total_label, campo_codebar, campo_quant)

        tela_vndr.destroy()

    btm_finalizar_venda = ctk.CTkButton(
        tela_vndr, 
        text='Finalizar Venda',
        command=finalizar_venda,  
        width=250, height=50,
        font=ctk.CTkFont(size=16, family="Arial Bold"),
        fg_color=cor_secundaria(), text_color="white"
    )
    btm_finalizar_venda.place(relx=0.5, rely=0.65, anchor="center")  # Centralizado

    tela_vndr.mainloop()
