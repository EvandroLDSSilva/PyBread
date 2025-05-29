import customtkinter as ctk
from datetime import datetime, timedelta
from sqlalchemy.orm import sessionmaker
from sqlalchemy import func
from database_vendas import CupomVenda, db
from global_resources import cor_principal


Session = sessionmaker(bind=db)
session = Session()

def open_interface_receita():

    receita_win = ctk.CTk()
    receita_win.title("Relatório de Receita")
    receita_win.geometry("500x500")
    receita_win.configure(fg_color=cor_principal())


    title_label = ctk.CTkLabel(receita_win, 
                               text="Relatório de Receita",
                               font=ctk.CTkFont(size=24, family="Arial Bold"),
                               text_color="black")
    title_label.pack(pady=20)


    frame_selecao = ctk.CTkFrame(receita_win, fg_color=cor_principal())
    frame_selecao.pack(pady=10)

    unidade_options = ["Minuto(s)", "Hora(s)", "Dia(s)", "Mês(es)", "Ano(s)"]
    unidade_var = ctk.StringVar(value=unidade_options[0])
    unidade_menu = ctk.CTkOptionMenu(frame_selecao, values=unidade_options, variable=unidade_var)
    unidade_menu.grid(row=0, column=0, padx=5, pady=5)
    
    quant_minutos = list(map(str, range(1, 61)))
    quantidade_var = ctk.StringVar(value=quant_minutos[0])
    quantidade_menu = ctk.CTkOptionMenu(frame_selecao, values=quant_minutos, variable=quantidade_var)
    quantidade_menu.grid(row=0, column=1, padx=5, pady=5)

    def update_quantidade_options(new_unidade):
        if new_unidade == "Minuto(s)":
            new_values = list(map(str, range(1, 61)))
        elif new_unidade == "Hora(s)":
            new_values = list(map(str, range(1, 25)))
        elif new_unidade == "Dia(s)":
            new_values = list(map(str, range(1, 32)))
        elif new_unidade == "Mês(es)":
            new_values = list(map(str, range(1, 13)))
        elif new_unidade == "Ano(s)":
            new_values = list(map(str, range(1, 31)))
        else:
            new_values = ["1"]
        quantidade_menu.configure(values=new_values)
        quantidade_var.set(new_values[0])

    unidade_menu.configure(command=update_quantidade_options)

    btn_gerar = ctk.CTkButton(receita_win, text="Gerar Receita",
                              font=ctk.CTkFont(size=16, family="Arial Bold"))
    btn_gerar.pack(pady=10)


    label_total = ctk.CTkLabel(receita_win, text="Total Movimentado: R$ 0,00",
                                font=ctk.CTkFont(size=16), text_color="black")
    label_total.pack(pady=5)
    label_lucro = ctk.CTkLabel(receita_win, text="Lucro: R$ 0,00",
                                font=ctk.CTkFont(size=16), text_color="black")
    label_lucro.pack(pady=5)
    label_preco_compra = ctk.CTkLabel(receita_win, text="Preço de Compra: R$ 0,00",
                                      font=ctk.CTkFont(size=16), text_color="black")
    label_preco_compra.pack(pady=5)

    def gerar_relatorio():

        unidade = unidade_var.get()
        try:
            qtd = int(quantidade_var.get())
        except ValueError:
            qtd = 1

        now = datetime.now()

        if unidade == "Minuto(s)":
            delta = timedelta(minutes=qtd)
        elif unidade == "Hora(s)":
            delta = timedelta(hours=qtd)
        elif unidade == "Dia(s)":
            delta = timedelta(days=qtd)
        elif unidade == "Mês(es)":
            delta = timedelta(days=qtd * 30)
        elif unidade == "Ano(s)":
            delta = timedelta(days=qtd * 365)
        else:
            delta = timedelta(0)
        
        cutoff = now - delta

        result = session.query(
            func.sum(CupomVenda.total_cupom),
            func.sum(CupomVenda.lucro_cupom)
        ).filter(CupomVenda.data_venda >= cutoff).one()

        total_mov = result[0] if result[0] is not None else 0.0
        total_lucro = result[1] if result[1] is not None else 0.0
        preco_compra = total_mov - total_lucro

        label_total.configure(text=f"Total Movimentado: R$ {total_mov:.2f}".replace('.', ','))
        label_lucro.configure(text=f"Lucro: R$ {total_lucro:.2f}".replace('.', ','))
        label_preco_compra.configure(text=f"Preço de Compra: R$ {preco_compra:.2f}".replace('.', ','))

    btn_gerar.configure(command=gerar_relatorio)

    receita_win.mainloop()
