import tkinter as tk
from tkinter import messagebox
import os
import webbrowser
from main import main

# Funções de interface
def executar_algoritmos():
    try:
        main()
        messagebox.showinfo("Execução Concluída", "ACO e GA executados com sucesso!")
    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao executar os algoritmos:\n{e}")

def abrir_mapa(nome_arquivo):
    caminho = os.path.abspath(nome_arquivo)
    if os.path.exists(caminho):
        webbrowser.open(f"file:///{caminho}")
    else:
        messagebox.showerror("Erro", f"O arquivo {nome_arquivo} não foi encontrado.")

def abrir_tabela_html():
    caminho = os.path.abspath("tabela_comparativa_render.html")
    if os.path.exists(caminho):
        webbrowser.open(f"file:///{caminho}")
    else:
        messagebox.showerror("Erro", "Arquivo HTML da tabela não encontrado. Execute os algoritmos primeiro.")

# GUI
root = tk.Tk()
root.title("Otimizador Logístico - ACO e GA")
root.geometry("400x500")

fonte = ("Segoe UI", 11)

tk.Label(root, text="Otimizador Logístico - ACO e GA", font=("Segoe UI", 14, "bold")).pack(pady=20)

tk.Button(root, text="▶️ Executar ACO e GA", font=fonte, command=executar_algoritmos, width=30).pack(pady=10)

tk.Label(root, text="Abrir Mapas:", font=("Segoe UI", 12, "underline")).pack(pady=5)

tk.Button(root, text="📍 Ver Rotas ACO (top 3)", font=fonte,
          command=lambda: abrir_mapa("mapa_aco_top3.html")).pack(pady=4)

tk.Button(root, text="📍 Ver Rotas GA (top 3)", font=fonte,
          command=lambda: abrir_mapa("mapa_genetico_top3.html")).pack(pady=4)

tk.Button(root, text="🧭 Ver Mapa Comparativo", font=fonte,
          command=lambda: abrir_mapa("mapa_comparativo.html")).pack(pady=4)

tk.Button(root, text="📊 Ver Tabela Comparativa", font=fonte,
          command=abrir_tabela_html).pack(pady=20)

root.mainloop()
