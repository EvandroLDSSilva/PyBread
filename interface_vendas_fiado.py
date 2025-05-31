import customtkinter as ctk
from global_resources import cor_principal
from database_vendas import cliente, db
from sqlalchemy.orm import sessionmaker
from interface_lista_clientes import open_lista_clientes

Session = sessionmaker(bind=db)
session = Session()

def open_interface_vendas_fiado():
    app = ctk.CTk()
    app.title("Venda Fiado")
    app.geometry("600x400")
    app.configure(fg_color=cor_principal())
    
    frame = ctk.CTkFrame(app, fg_color=cor_principal())
    frame.pack(padx=20, pady=20, fill="both", expand=True)
    
    label_title = ctk.CTkLabel(frame, text="Venda Fiado", font=ctk.CTkFont(size=20, family="Arial Bold"), text_color="black")
    label_title.pack(pady=10)
    
    label_cod = ctk.CTkLabel(frame, text="Código do Cliente:", text_color="black")
    label_cod.pack(pady=2)
    entry_cod = ctk.CTkEntry(frame, width=250, placeholder_text="Digite o código")
    entry_cod.pack(pady=2)
    
    label_valor = ctk.CTkLabel(frame, text="Valor da Venda:", text_color="black")
    label_valor.pack(pady=2)
    entry_valor = ctk.CTkEntry(frame, width=250, placeholder_text="Digite o valor")
    entry_valor.pack(pady=2)
    
    btn_vender = ctk.CTkButton(frame, text="Finalizar Venda Fiado", width=180, height=40, font=ctk.CTkFont(size=16))
    btn_vender.pack(pady=10)
    
    btn_lista = ctk.CTkButton(frame, text="Lista", width=80, height=30, font=ctk.CTkFont(size=14), fg_color=cor_principal(), text_color="black", command=open_lista_clientes)
    btn_lista.pack(pady=10)
    
    app.mainloop()

if __name__ == "__main__":
    open_interface_vendas_fiado()
