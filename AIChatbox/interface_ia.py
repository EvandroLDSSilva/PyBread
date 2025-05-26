import customtkinter as ctk
from global_resources import *
from AIChatbox.nucleos_ia import resposta_bot  # Importando a IA

def open_intfc_ia():
    tela_ia = ctk.CTk()
    tela_ia.geometry("500x600")
    tela_ia.title("Chatbox IA - BaguetteBot")

    # Agora usa CTkScrollableFrame para permitir rolagem
    frame_chat = ctk.CTkScrollableFrame(tela_ia)
    frame_chat.pack(fill="both", expand=True, padx=10, pady=10)

    frame_input = ctk.CTkFrame(tela_ia)
    frame_input.pack(fill="x", padx=10, pady=5)

    entry_msg = ctk.CTkEntry(frame_input, width=300, placeholder_text="Digite sua mensagem...")
    entry_msg.pack(side="left", fill="x", expand=True)

    def enviar_mensagem():
        """Envia a mensagem do usuário e exibe a resposta da IA na interface."""
        mensagem = entry_msg.get()
        if mensagem:
            label_msg_user = ctk.CTkLabel(frame_chat, text=f"Você: {mensagem}", wraplength=350, justify="left")
            label_msg_user.pack(anchor="w", padx=10, pady=4)

            entry_msg.delete(0, "end")  # Limpa o campo de entrada
            
            resposta = resposta_bot(mensagem)  # Obtém resposta da IA
            label_msg_bot = ctk.CTkLabel(frame_chat, text=f"BaguetteBot: {resposta}", wraplength=350, justify="left")
            label_msg_bot.pack(anchor="w", padx=10, pady=4)

            # **Move automaticamente para a última mensagem**
            frame_chat._parent_canvas.yview_moveto(1)

    btn_send = ctk.CTkButton(frame_input, text="Enviar", width=80, command=enviar_mensagem)
    btn_send.pack(side="right", padx=5)

    tela_ia.protocol("WM_DELETE_WINDOW", lambda: safe_destroy(tela_ia))

    tela_ia.mainloop()
