import customtkinter as ctk
from global_resources import *
import ctypes
from decimal import Decimal, ROUND_UP

ctypes.windll.user32.SetProcessDPIAware()

def open_interface_vendas():
    tela_vendas = ctk.CTk()
    tela_vendas.title('Tela de Vendas')
    tela_vendas.geometry(resolucao_tela_monitor())
    tela_vendas.configure(fg_color="#FFD700")

    total_valor = Decimal("0.00")

    total_label = ctk.CTkLabel(
        tela_vendas,
        text="Total: R$ 0,00",
        text_color="black",
        font=ctk.CTkFont(size=20, family="Arial Bold")
    )
    total_label.place(relx=0.35, rely=0.65)

    campo_codebar = ctk.CTkEntry(
        tela_vendas, 
        placeholder_text='Digite o código de barras', 
        width=300, 
        height=40,
        font=ctk.CTkFont(size=16, family="Arial Bold"),
        fg_color="#FFA500",
        text_color="white"
    )
    campo_codebar.place(relx=0.6, rely=0.75)

    campo_quant = ctk.CTkEntry(
        tela_vendas, 
        placeholder_text='Digite a quantidade', 
        width=300, 
        height=40,
        font=ctk.CTkFont(size=16, family="Arial Bold"),
        fg_color="#FFA500",
        text_color="white"
    )
    campo_quant.place(relx=0.6, rely=0.85)

    box_texto = ctk.CTkTextbox(
        tela_vendas, 
        width=350, 
        height=350, 
        fg_color="#FFA500",
        text_color="black"
    )
    box_texto.place(relx=0.35, rely=0.70)

    def show_info(event=None):
        nonlocal total_valor
        codigo = campo_codebar.get()
        quant = campo_quant.get()
        box_texto.configure(state="normal")
        if codigo in cod_produtos:
            info = cod_produtos[codigo]
            try:
                quant_formatado = quant.replace(',', '.')
                quant_float = float(quant_formatado)
            except ValueError:
                quant_float = 1

            preco_str = str(info['preco']).replace(',', '.')
            preco_decimal = Decimal(preco_str)
            total = preco_decimal * Decimal(quant_float)
            total = total.quantize(Decimal('0.01'), rounding=ROUND_UP)
            total_str = format(total, '.2f').replace('.', ',')

            total_valor += total
            total_label.configure(text=f"Total: R$ {format(total_valor, '.2f').replace('.', ',')}")

            box_texto.insert("end", f"Nome: {info['nome']}\n")
            box_texto.insert("end", f"Código: {codigo}\n")
            box_texto.insert("end", f"Preço: R$ {preco_decimal:.2f}     Quantidade: {quant_float}\n")
            box_texto.insert("end", f"Preço X quantidade: R$ {total_str}\n")
            box_texto.insert("end", "-" * 20 + "\n")
        else:
            box_texto.insert("end", f"Código {codigo} não encontrado.\n")
            box_texto.insert("end", "-" * 20 + "\n")
        box_texto.configure(state="disabled")
        campo_codebar.delete(0, "end")
        campo_quant.delete(0, "end")

    campo_codebar.bind("<Return>", show_info)
    campo_quant.bind("<Return>", show_info)
    tela_vendas.protocol("WM_DELETE_WINDOW", lambda: safe_destroy(tela_vendas))
    tela_vendas.bind("<q>", lambda event: safe_destroy(tela_vendas))
    tela_vendas.mainloop()
