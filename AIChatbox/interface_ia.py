import customtkinter as ctk
from AIChatbox.nucleos_ia import processar_comando

def open_interface_ia():
    root = ctk.CTk()
    root.title("Baggete Bot - Assistente Virtual")
    root.geometry("600x500")
    root.configure(fg_color="white")

    frame = ctk.CTkFrame(root, fg_color="white")
    frame.pack(padx=20, pady=20, fill="both", expand=True)

    label = ctk.CTkLabel(frame, text="Baggete Bot", font=ctk.CTkFont(size=20, family="Arial Bold"), text_color="black")
    label.pack(pady=10)

    chat_frame = ctk.CTkScrollableFrame(frame, width=550, height=300)
    chat_frame.pack(pady=5)

    chat_log = ctk.CTkTextbox(chat_frame, width=530, height=280, state="disabled")
    chat_log.pack(side="left", fill="both", expand=True)

    entry_pergunta = ctk.CTkEntry(frame, width=400, placeholder_text="Digite sua pergunta...")
    entry_pergunta.pack(pady=5)

    def enviar_mensagem():
        pergunta = entry_pergunta.get().strip()
        if pergunta:
            chat_log.configure(state="normal")
            chat_log.insert("end", f"Usuário: {pergunta}\n")
            entry_pergunta.delete(0, "end")

            resposta = processar_comando(pergunta)

            chat_log.insert("end", f"Baggete Bot: {resposta}\n")
            chat_log.see("end")
            chat_log.configure(state="disabled")

    btn_enviar = ctk.CTkButton(frame, text="Enviar", width=100, height=40, font=ctk.CTkFont(size=16), command=enviar_mensagem)
    btn_enviar.pack(pady=10)

    root.mainloop()
