
import os
import platform
import tkinter as tk
from tkinter import messagebox
import threading
import time
import sys

# Função para acessar recursos mesmo quando empacotado com PyInstaller
def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS  # Diretório temporário usado pelo PyInstaller
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

if platform.system() == "Windows":
    try:
        import winshell
        from win32com.client import Dispatch

        def criar_atalho():
            desktop = winshell.desktop()
            caminho_atalho = os.path.join(desktop, "Cronômetro de Desligamento.lnk")
            caminho_exec = sys.executable
            shell = Dispatch('WScript.Shell')
            atalho = shell.CreateShortCut(caminho_atalho)
            atalho.TargetPath = caminho_exec
            atalho.WorkingDirectory = os.path.dirname(caminho_exec)
            atalho.IconLocation = caminho_exec
            atalho.save()

        criar_atalho()
    except Exception:
        pass

shutdown_thread = None
cancel_event = threading.Event()

def mostrar_aviso_temporario(mensagem, duracao=3000):
    aviso = tk.Toplevel()
    aviso.overrideredirect(True)  # Remove a borda da janela
    aviso.attributes("-topmost", True)
    aviso.configure(bg="#323232")  # Cor de fundo escura

    # Centralizar na tela
    largura = 320
    altura = 80
    x = (aviso.winfo_screenwidth() // 2) - (largura // 2)
    y = (aviso.winfo_screenheight() // 2) - (altura // 2)
    aviso.geometry(f"{largura}x{altura}+{x}+{y}")

    # Mensagem
    label = tk.Label(aviso, text=mensagem, font=("Segoe UI", 12, "bold"),
                     bg="#323232", fg="white", wraplength=300, justify="center")
    label.pack(expand=True, fill="both", padx=10, pady=10)

    # Fechar automaticamente após 'duracao' milissegundos
    aviso.after(duracao, aviso.destroy)

def shutdown_system():
    if platform.system() == "Windows":
        os.system("shutdown /s /f /t 0")
    elif platform.system() == "Linux":
        os.system("shutdown -h now")
    else:
        messagebox.showerror("Erro", "Sistema operacional não suportado.")

def countdown_timer(total_seconds):
    if total_seconds > 30:
        for _ in range(total_seconds - 30):
            if cancel_event.is_set():
                return
            time.sleep(1)
        mostrar_aviso_temporario("O computador será desligado em 30 segundos!")
        for _ in range(30):
            if cancel_event.is_set():
                return
            time.sleep(1)
    else:
        for _ in range(total_seconds):
            if cancel_event.is_set():
                return
            time.sleep(1)
    shutdown_system()

def start_timer():
    global shutdown_thread
    cancel_event.clear()
    try:
        hours = int(entry_hours.get())
        minutes = int(entry_minutes.get())
        total_seconds = hours * 3600 + minutes * 60
        if total_seconds <= 0:
            messagebox.showerror("Erro", "O tempo deve ser maior que 0.")
            return
        shutdown_thread = threading.Thread(target=countdown_timer, args=(total_seconds,), daemon=True)
        shutdown_thread.start()
        messagebox.showinfo("Iniciado", f"O PC será desligado em {hours}h {minutes}min.")
    except ValueError:
        messagebox.showerror("Erro", "Insira valores válidos para horas e minutos.")

def cancel_timer():
    cancel_event.set()
    messagebox.showinfo("Cancelado", "O desligamento foi cancelado.")

root = tk.Tk()
root.title("Cronômetro de Desligamento")
root.configure(bg="#f0f0f0")
try:
    root.iconbitmap(resource_path("icon.ico"))
except:
    pass
root.geometry("320x200")
root.resizable(False, False)

root.update_idletasks()
w = root.winfo_width()
h = root.winfo_height()
x = (root.winfo_screenwidth() // 2) - (w // 2)
y = (root.winfo_screenheight() // 2) - (h // 2)
root.geometry(f"{w}x{h}+{x}+{y}")












title = tk.Label(root, text="Configure o tempo:", font=("Segoe UI", 14, "bold"), bg="#f0f0f0")
title.pack(pady=10)

frame_inputs = tk.Frame(root, bg="#f0f0f0")
frame_inputs.pack()

tk.Label(frame_inputs, text="Horas:", font=("Segoe UI", 11), bg="#f0f0f0").grid(row=0, column=0, padx=5, pady=5)
entry_hours = tk.Entry(frame_inputs, width=5, font=("Segoe UI", 11))
entry_hours.grid(row=0, column=1)

tk.Label(frame_inputs, text="Minutos:", font=("Segoe UI", 11), bg="#f0f0f0").grid(row=1, column=0, padx=5, pady=5)
entry_minutes = tk.Entry(frame_inputs, width=5, font=("Segoe UI", 11))
entry_minutes.grid(row=1, column=1)

frame_buttons = tk.Frame(root, bg="#f0f0f0")
frame_buttons.pack(pady=15)

btn_start = tk.Button(frame_buttons, text="Iniciar", font=("Segoe UI", 10, "bold"), bg="#4CAF50", fg="white", width=10, command=start_timer)
btn_start.grid(row=0, column=0, padx=10)

btn_cancel = tk.Button(frame_buttons, text="Cancelar", font=("Segoe UI", 10, "bold"), bg="#F44336", fg="white", width=10, command=cancel_timer)
btn_cancel.grid(row=0, column=1, padx=10)

root.mainloop()
