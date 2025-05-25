import customtkinter as ctk

# Configuração da janela principa
root = ctk.CTk()
root.geometry("400x500")
root.title("Chatbox IA")

# Criando um frame para exibir as mensagens
frame_chat = ctk.CTkFrame(root, width=380, height=350)
frame_chat.pack(pady=10, padx=10, fill="both", expand=True)

# Criando um campo de entrada para digitar mensagens
entry_msg = ctk.CTkEntry(root, width=300, placeholder_text="Digite sua mensagem...")
entry_msg.pack(pady=5, padx=10, side="left")

# Botão para enviar a mensagem
btn_send = ctk.CTkButton(root, text="Enviar", width=80, command=lambda: enviar_mensagem())
btn_send.pack(pady=5, padx=10, side="right")

def enviar_mensagem():
    mensagem = entry_msg.get()
    if mensagem:
        label_msg = ctk.CTkLabel(frame_chat, text=mensagem, wraplength=350)
        label_msg.pack(anchor="w", padx=10, pady=4)
        entry_msg.delete(0, "end")

root.mainloop()