import customtkinter as ctk
from decimal import Decimal, ROUND_UP
from sqlalchemy.orm import sessionmaker
from database_vendas import *
from global_resources import *
from AIChatbox.nucleos_ia import *


Session = sessionmaker(bind=db)
session = Session()

def save_cupom_db(box_texto, total_label, campo_codebar, campo_quant, total_valor, total_lucro):
    """
    Salva o cupom no banco de dados, incluindo o total_cupom e o lucro_cupom,
    e reseta a interface.
    """
    box_texto.configure(state="normal")
    conteudo_cupom = box_texto.get("1.0", "end").strip()
    box_texto.configure(state="disabled")

    if conteudo_cupom:
        novo_cupom = CupomVenda(content_cupom=conteudo_cupom, 
                                total_cupom=float(total_valor),
                                lucro_cupom=float(total_lucro))
        session.add(novo_cupom)
        session.commit()
        print("Cupom salvo no banco!")
        total_valor = Decimal('0.00')
        total_label.configure(text=f"Total: R$ {total_valor:.2f}".replace('.', ','))
        box_texto.configure(state="normal")
        box_texto.delete("1.0", "end")
        box_texto.configure(state="disabled")
        campo_codebar.delete(0, "end")
        campo_quant.delete(0, "end")

def open_interface_vendas():
    intfc_vendas = ctk.CTk()
    intfc_vendas.title('Tela de Vendas')
    intfc_vendas.geometry(resolucao_tela_monitor())
    intfc_vendas.configure(fg_color=cor_principal())

    total_valor = Decimal('0.00')
    total_lucro = Decimal('0.00')

    total_label = ctk.CTkLabel(
        intfc_vendas,
        text=f"Total: R$ {total_valor:.2f}".replace('.', ','),
        text_color="black",
        font=ctk.CTkFont(size=20, family="Arial Bold")
    )
    total_label.place(relx=0.35, rely=0.55)

    campo_codebar = ctk.CTkEntry(
        intfc_vendas, 
        placeholder_text='Digite o código de barras:', 
        width=300, height=40,
        font=ctk.CTkFont(size=16, family="Arial Bold"), 
        fg_color=cor_secundaria(), text_color="white"
    )
    campo_codebar.place(relx=0.6, rely=0.75)

    campo_quant = ctk.CTkEntry(
        intfc_vendas, 
        placeholder_text='Digite a quantidade', 
        width=300, height=40,
        font=ctk.CTkFont(size=16, family="Arial Bold"),
        fg_color=cor_secundaria(), text_color="white"
    )
    campo_quant.place(relx=0.6, rely=0.85)

    box_texto = ctk.CTkTextbox(
        intfc_vendas, 
        width=350, height=350,
        fg_color=cor_terciaria(), text_color="black",
        state="disabled"
    )
    box_texto.place(relx=0.35, rely=0.65)

    label_datahora_intf_principal = ctk.CTkLabel(
        intfc_vendas,
        text=carregar_data(),
        text_color='black',
        font=ctk.CTkFont(size=15, family="Arial Bold")
    )
    label_datahora_intf_principal.place(relx=0.10, rely=0.90)

    def atualizar_data():
        label_datahora_intf_principal.configure(text=carregar_data())
        intfc_vendas.after(1000, atualizar_data)

    atualizar_data()

    def show_info(event=None):
        nonlocal total_valor, total_lucro  
        codigo = campo_codebar.get()
        quant = campo_quant.get()
        box_texto.configure(state="normal")
        try:
            produto = session.query(Produto).filter_by(cod_produto=int(codigo)).first()
        except ValueError:
            produto = None
        if produto:
            try:
                quant_float = float(quant.replace(',', '.')) if quant else 1
            except ValueError:
                quant_float = 1
            total = Decimal(produto.preco_venda) * Decimal(quant_float)
            total = total.quantize(Decimal('0.01'), rounding=ROUND_UP)
            total_valor += total                    
            total_label.configure(text=f"Total: R$ {format(total_valor, '.2f').replace('.', ',')}")
            
            lucro_item = Decimal(produto.lucro) * Decimal(quant_float)
            lucro_item = lucro_item.quantize(Decimal('0.01'), rounding=ROUND_UP)
            total_lucro += lucro_item

            box_texto.insert("end", carregar_data() + "\n")
            box_texto.configure(text_color="black", font=ctk.CTkFont(family="Arial Bold", size=15))
            box_texto.insert("end", f"Nome: {produto.nome_produto}\n")
            box_texto.insert("end", f"Código: {produto.cod_produto}\n")
            box_texto.insert("end", f"Preço: R$ {produto.preco_venda:.2f}  Quantidade: {quant_float}\n")
            box_texto.insert("end", f"Total: R$ {total}\n")
            box_texto.insert("end", "-" * 20 + "\n")
        else:
            box_texto.insert("end", f"Código {codigo} não encontrado no banco.\n")
            box_texto.insert("end", "-" * 20 + "\n")
        box_texto.configure(state="disabled")
        campo_codebar.delete(0, "end")
        campo_quant.delete(0, "end")

    campo_codebar.bind("<Return>", show_info)
    campo_quant.bind("<Return>", show_info)

    # Função para finalizar venda no fiado
    def finalizar_venda_fiado():
        janela_fiado = ctk.CTk()
        janela_fiado.title("Finalizar Venda no Fiado")
        janela_fiado.geometry("400x300")
        janela_fiado.configure(fg_color=cor_principal())
        
        label_instrucao = ctk.CTkLabel(janela_fiado,
                                      text="Digite Nome e Código do Cliente",
                                      text_color="black",
                                      font=ctk.CTkFont(size=16, family="Arial Bold"))
        label_instrucao.pack(pady=10)
        
        entry_nome = ctk.CTkEntry(janela_fiado,
                                  placeholder_text="Nome do Cliente",
                                  width=300, height=40,
                                  font=ctk.CTkFont(size=16),
                                  fg_color=cor_secundaria(), text_color="white")
        entry_nome.pack(pady=5)
        
        entry_codigo = ctk.CTkEntry(janela_fiado,
                                    placeholder_text="Código do Cliente",
                                    width=300, height=40,
                                    font=ctk.CTkFont(size=16),
                                    fg_color=cor_secundaria(), text_color="white")
        entry_codigo.pack(pady=5)
        
        label_msg = ctk.CTkLabel(janela_fiado, text="", text_color="red", font=ctk.CTkFont(size=14))
        label_msg.pack(pady=5)
        
        def confirmar_fiado():
            nome = entry_nome.get().strip()
            codigo = entry_codigo.get().strip()
            if not nome or not codigo.isdigit():
                label_msg.configure(text="Preencha nome e código corretamente!")
                return
            cliente_existente = session.query(Cliente).filter_by(nome_cliente=nome, cod_cliente=int(codigo)).first()
            if not cliente_existente:
                label_msg.configure(text="Cliente não encontrado!")
                return
            
            novo_total = cliente_existente.total_conta_cliente + float(total_valor)
            cliente_existente.total_conta_cliente = novo_total
            session.commit()

            save_cupom_db(box_texto, total_label, campo_codebar, campo_quant, total_valor, total_lucro)
            print("Venda no fiado finalizada!")
            janela_fiado.destroy()
        
        btn_confirmar = ctk.CTkButton(janela_fiado,
                                      text="Confirmar Venda no Fiado",
                                      command=confirmar_fiado,
                                      width=250, height=40,
                                      font=ctk.CTkFont(size=16),
                                      fg_color=cor_secundaria(), text_color="white")
        btn_confirmar.pack(pady=10)
        janela_fiado.mainloop()
    

    def finalizar_venda():
        from tela_vender import open_tela_vender
        open_tela_vender(total_valor, total_lucro, box_texto, campo_codebar, campo_quant, total_label)
    

    btm_vender = ctk.CTkButton(
        intfc_vendas, 
        text='Receber à vista',
        command=finalizar_venda,
        width=250, height=50,
        font=ctk.CTkFont(size=16, family="Arial Bold"),
        fg_color=cor_secundaria(), text_color="white"
    )
    btm_vender.place(relx=0.6, rely=0.30)

    btm_venda_fiado = ctk.CTkButton(
        intfc_vendas,
        text='Finalizar Venda no Fiado',
        command=finalizar_venda_fiado,
        width=250, height=50,
        font=ctk.CTkFont(size=16, family="Arial Bold"),
        fg_color=cor_secundaria(), text_color="white"
    )
    btm_venda_fiado.place(relx=0.3, rely=0.30)
    
    intfc_vendas.mainloop()

if __name__ == "__main__":
    open_interface_vendas()
