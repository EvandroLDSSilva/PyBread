import customtkinter as ctk

def open_intfc_ia():

    tela_ia = ctk.CTk()
    tela_ia.geometry("400x500")
    tela_ia.title("Chatbox IA")

    
    frame_chat = ctk.CTkFrame(tela_ia, width=380, height=350)
    frame_chat.pack(pady=10, padx=10, fill="both", expand=True)

    
    entry_msg = ctk.CTkEntry(tela_ia, width=300, placeholder_text="Digite sua mensagem...")
    entry_msg.pack(pady=5, padx=10, side="left")

    
    btn_send = ctk.CTkButton(tela_ia, text="Enviar", width=80, command=lambda: enviar_mensagem())
    btn_send.pack(pady=5, padx=10, side="right")

    def enviar_mensagem():
        mensagem = entry_msg.get()
        if mensagem:
            label_msg = ctk.CTkLabel(frame_chat, text=mensagem, wraplength=350)
            label_msg.pack(anchor="w", padx=10, pady=4)
            entry_msg.delete(0, "end")

    tela_ia.mainloop()