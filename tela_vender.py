import customtkinter as ctk
from decimal import Decimal, ROUND_UP
from global_resources import *                  # Ex.: carregar_data(), cor_principal(), cor_secundaria(), etc.
from database_vendas import *                   # Ex.: Produto, CupomVenda, cliente, db, etc.
from sqlalchemy.orm import sessionmaker
import tkinter.messagebox as messagebox         # Para exibir mensagens, se necessário

Session = sessionmaker(bind=db)
session = Session()

def open_tela_vender(total_valor, total_lucro, box_texto, campo_codebar, campo_quant, total_label):
    """
    Abre a janela de finalização da venda.
    - total_valor e total_lucro (do tipo Decimal) são os valores acumulados da venda.
    - box_texto, campo_codebar, campo_quant e total_label vêm da interface de vendas.
    
    O botão "Finalizar Venda" só aparece quando o usuário pressiona Enter no campo
    "Dinheiro recebido" e o valor informado é igual ou superior a total_valor.
    Em caso de valor insuficiente, um rótulo de erro é mostrado na mesma janela.
    """
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
    label_total_vender.place(relx=0.5, rely=0.30, anchor="center")

    campo_rcb_dinheiro = ctk.CTkEntry(
        tela_vndr,
        placeholder_text='Dinheiro recebido',
        width=300,
        height=40,
        font=ctk.CTkFont(size=16, family="Arial Bold"),
        fg_color=cor_secundaria(),
        text_color="white"
    )
    campo_rcb_dinheiro.place(relx=0.5, rely=0.40, anchor="center")

    label_troco_vender = ctk.CTkLabel(
        tela_vndr,
        text="Troco: R$ 0,00",
        text_color='black',
        font=ctk.CTkFont(size=22, family="Arial Bold")
    )
    label_troco_vender.place(relx=0.5, rely=0.50, anchor="center")
    
    # Label de erro para informar valor insuficiente ou inválido
    label_erro = ctk.CTkLabel(
        tela_vndr,
        text="",
        text_color="red",
        font=ctk.CTkFont(size=16)
    )
    label_erro.place(relx=0.5, rely=0.57, anchor="center")
    
    # Cria o botão de finalizar mas o oculta inicialmente
    btm_finalizar_venda = ctk.CTkButton(
        tela_vndr,
        text='Finalizar Venda',
        command=lambda: finalizar_venda(),
        width=250,
        height=50,
        font=ctk.CTkFont(size=16, family="Arial Bold"),
        fg_color=cor_secundaria(),
        text_color="white"
    )
    btm_finalizar_venda.place_forget()  # Inicialmente oculto

    def atualizar_troco(event=None):
        """Calcula e atualiza o troco e decide se exibe o botão de finalizar."""
        try:
            dinheiro_recebido = Decimal(campo_rcb_dinheiro.get().replace(',', '.') or '0')
            troco = dinheiro_recebido - total_valor
            label_troco_vender.configure(text=f"Troco: R$ {troco:.2f}".replace('.', ','))
            if dinheiro_recebido >= total_valor:
                label_erro.configure(text="")  # Remove mensagem de erro, se houver.
                btm_finalizar_venda.place(relx=0.5, rely=0.70, anchor="center")
            else:
                label_erro.configure(text="Valor recebido insuficiente!")
                btm_finalizar_venda.place_forget()
        except Exception as e:
            label_troco_vender.configure(text="Valor inválido")
            label_erro.configure(text="Valor inválido")
            btm_finalizar_venda.place_forget()

    campo_rcb_dinheiro.bind("<Return>", atualizar_troco)

    def finalizar_venda():
        """Verifica novamente o valor recebido e finaliza a venda se for suficiente."""
        try:
            dinheiro_recebido = Decimal(campo_rcb_dinheiro.get().replace(',', '.') or '0')
        except Exception:
            label_erro.configure(text="Valor inválido no campo!")
            return

        if dinheiro_recebido < total_valor:
            label_erro.configure(text="Valor recebido insuficiente!")
            return

        # Se o valor for suficiente, prossegue com a finalização da venda.
        print("Finalizando Venda!")
        from interface_vendas_mod import save_cupom_db  # Certifique-se de que essa função esteja corretamente implementada.
        save_cupom_db(box_texto, total_label, campo_codebar, campo_quant, total_valor, total_lucro)
        tela_vndr.destroy()

    tela_vndr.mainloop()
