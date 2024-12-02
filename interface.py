from tkinter import Tk, Label, Entry, StringVar, messagebox, filedialog, Button, PhotoImage
import tkinter as tk
from tkcalendar import DateEntry
import locale
from tkinter import ttk  # Biblioteca ttk para usar o tema
import os
from PIL import Image, ImageTk

# Define a localidade para português
# Define a localidade para português
locale.setlocale(locale.LC_TIME, 'pt_BR.UTF-8')

def abrir_interface(callback):
    # Janela principal
    root = tk.Tk()
    root.title("Gerador de Relatório Técnico")
    
  
    
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    
    # Definir dimensões da janela (metade da tela)
    width = screen_width // 3
    height = screen_height // 2
    
    # Centralizar a janela
    x = (screen_width - width) // 2
    y = (screen_height - height) // 2
    
    # Configurar geometria
    root.geometry(f"{width}x{height}+{x}+{y}")

    # Configurar tema
    root.tk.call("source", os.path.join("Azure-ttk-theme-main", "azure.tcl"))
    root.tk.call("set_theme", "dark")

    # Canvas para rolagem
    canvas = tk.Canvas(root)
    scrollbar = ttk.Scrollbar(root, orient="vertical", command=canvas.yview)
    canvas.configure(yscrollcommand=scrollbar.set)

    # Frame principal dentro do canvas
    big_frame = ttk.Frame(canvas)
    canvas.create_window((0, 0), window=big_frame, anchor="nw")

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    # Ajuste automático do tamanho do canvas
    def ajustar_scroll(event):
        canvas.configure(scrollregion=canvas.bbox("all"))
    big_frame.bind("<Configure>", ajustar_scroll)

    # Variáveis para armazenar valores
    concessionaria_var = StringVar(root)
    concessionaria_var.set("Selecionar concessionária")
    assinaturas = []
    estacao_var = StringVar(root)
    data_var = StringVar(root)
    horario_var = StringVar(root)
    tipo_local_var = StringVar(root)
    imagens = []
    legendas = []
 

    # Função para atualizar o tipo de local e a visibilidade do campo Estação/Terminal
    def update_tipo_local(*args):
        concessionaria = concessionaria_var.get()
        if concessionaria in ["SuperVia", "MetrôRio", "Selecionar concessionária"]:
            tipo_local_var.set("Estação")
            estacao_label.config(text="Estação(ões):")  # Altera o rótulo para "Estação"
            estacao_label.grid(row=1, column=0)
            estacao_entry.grid(row=1, column=1)
        elif concessionaria == "CCR Barcas":
            tipo_local_var.set("Terminal")
            estacao_label.config(text="Terminal(ais):")  # Altera o rótulo para "Terminal"
            estacao_label.grid(row=1, column=0)
            estacao_entry.grid(row=1, column=1)
        elif concessionaria in ["CCR Via Lagos", "Rota 116"]:
            tipo_local_var.set("Rodovia")
            estacao_label.grid_remove()  # Oculta o rótulo
            estacao_entry.grid_remove()  # Oculta o campo de entrada

    # Função para selecionar imagens
    def selecionar_imagens():
        arquivos = filedialog.askopenfilenames(title="Selecionar Imagens", filetypes=[("Imagens", "*.png;*.jpg;*.jpeg")])
        if arquivos:
            imagens.extend(arquivos)
            legendas.extend([""] * len(arquivos))
            atualizar_grid_imagens()  

    # Função para remover uma imagem
    def remover_imagem(index):
        if index < len(imagens):
            imagens.pop(index)
            legendas.pop(index)  # Remove a imagem pelo índice
            atualizar_grid_imagens()  # Atualiza o grid após a remoção

    assinaturas_frame = ttk.Frame(big_frame)
    assinaturas_frame.grid(row=5, column=1, columnspan=2, sticky="w")

    
    def adicionar_assinatura():
        # Verifica o número de assinaturas existentes
        num_assinaturas = len(assinaturas)

        # Cria um novo frame para o próximo grupo de assinaturas a cada 4 entradas
        if num_assinaturas % 4 == 0:
            novo_frame = ttk.Frame(assinaturas_frame)
            novo_frame.pack(anchor="w", pady=10)  # Adiciona o novo frame ao container de assinaturas
        else:
            # Usa o último frame existente
            novo_frame = assinaturas[-1]["frame"] if assinaturas else assinaturas_frame

        # Variáveis para o nome e cargo
        nome_var = StringVar()
        cargo_var = StringVar()

        # Frame individual para cada assinatura
        assinatura_individual = ttk.Frame(novo_frame)
        assinatura_individual.pack(side="left", padx=10)

        # Entradas para o nome e cargo
        ttk.Label(assinatura_individual, text="Nome:").pack(anchor="w")
        nome_entry = ttk.Entry(assinatura_individual, textvariable=nome_var, width=20)
        nome_entry.pack(anchor="w")

        ttk.Label(assinatura_individual, text="Cargo:").pack(anchor="w")
        cargo_entry = ttk.Entry(assinatura_individual, textvariable=cargo_var, width=20)
        cargo_entry.pack(anchor="w")

        # Botão para remover a assinatura
        remover_button = ttk.Button(assinatura_individual, text="Remover", command=lambda: remover_assinatura(assinatura_individual, novo_frame))
        remover_button.pack(anchor="w", pady=5)

        # Armazena o frame e as variáveis na lista
        assinaturas.append({"frame": novo_frame, "nome_var": nome_var, "cargo_var": cargo_var, "container": assinatura_individual})

    def remover_assinatura(assinatura_individual, frame_parent):
        # Remove visualmente e da lista
        for assinatura in assinaturas:
            if assinatura["container"] == assinatura_individual:
                assinaturas.remove(assinatura)
                break

        assinatura_individual.destroy()

        # Remove o frame do grupo se estiver vazio
        if not any(a["frame"] == frame_parent for a in assinaturas):
            frame_parent.destroy()
      

    # Frame para pré-visualização das imagens com abas
    notebook = ttk.Notebook(big_frame)
    notebook.grid(row=7, column=1, padx=5, pady=5)

   
    def atualizar_grid_imagens():
        # Remove todas as abas antigas
        for tab in notebook.tabs():
            notebook.forget(tab)

        # Divide as imagens 
        paginas = [imagens[i:i+3] for i in range(0, len(imagens), 3)]
        legendas_pagina = [legendas[i:i+3] for i in range(0, len(legendas), 3)]

        for i, (pagina, legenda_pagina) in enumerate(zip(paginas, legendas_pagina)):
            frame = ttk.Frame(notebook)
            notebook.add(frame, text=f"Página {i+1}")

            for j, (imagem, legenda) in enumerate(zip(pagina, legenda_pagina)):
                img = Image.open(imagem)
                img.thumbnail((100, 100))  # Redimensiona a imagem para caber na visualização
                img = ImageTk.PhotoImage(img)

                # Label com a imagem
                label = Label(frame, image=img)
                label.image = img  # Mantém uma referência para a imagem
                label.grid(row=j*2, column=0, padx=5, pady=5)  # Posiciona a imagem no grid

                # Entrada de texto para legenda abaixo da imagem
                legenda_entry = Entry(frame, width=30)
                legenda_entry.insert(0, legenda or "Escreva a legenda da imagem...")  # Inserir a legenda ou hint text
                legenda_entry.bind("<FocusIn>", lambda event, entry=legenda_entry: entry.delete(0, 'end') if entry.get() == "Escreva a legenda da imagem..." else None)
                legenda_entry.grid(row=j*2+1, column=0, padx=5, pady=2)  # Campo de legenda diretamente abaixo da imagem

                # Botão para apagar a imagem, ao lado da imagem
                apagar_btn = Button(frame, text="APAGAR", command=lambda index=i*3+j: remover_imagem(index))
                apagar_btn.grid(row=j*2, column=1, rowspan=2, padx=5, pady=5)
                legenda_entry.bind("<FocusOut>", lambda event, index=i*3+j, entry=legenda_entry: legendas.__setitem__(index, entry.get()))

    # Concessionária
    ttk.Label(big_frame, text="Concessionária:").grid(row=0, column=0, padx=5, pady=5)
    ttk.OptionMenu(big_frame, concessionaria_var, "Selecionar concessionária", "SuperVia", "MetrôRio", "CCR Barcas", "Rota 116", "CCR Via Lagos", command=update_tipo_local).grid(row=0, column=1, padx=5, pady=5)

    # Estação/Terminal (inicialmente Estação)
    estacao_label = Label(big_frame, text="Estação:")
    estacao_entry = Entry(big_frame, width=30, textvariable=estacao_var)

    # Data da Vistoria
    ttk.Label(big_frame, text="Data da Vistoria:").grid(row=2, column=0, padx=5, pady=5)
    data_entry = DateEntry(big_frame, textvariable=data_var, date_pattern='dd/MM/yyyy', width=30)
    data_entry.grid(row=2, column=1, padx=5, pady=5)

    # Horário da Vistoria
    ttk.Label(big_frame, text="Horário da Vistoria (XhYmin):").grid(row=3, column=0, padx=5, pady=5)
    horario_entry = Entry(big_frame, width=30, textvariable=horario_var)
    horario_entry.grid(row=3, column=1, padx=5, pady=5)

    # Botão para adicionar mais assinaturas
    ttk.Button(big_frame, text="Adicionar Assinatura", command=adicionar_assinatura).grid(row=4, column=1, pady=10)


    # Botão para selecionar imagens
    ttk.Button(big_frame, text="Selecionar Imagens", command=selecionar_imagens).grid(row=6, column=1, pady=10)

    def on_generate():
        concessionaria = concessionaria_var.get()
        estacao = estacao_var.get() if tipo_local_var.get() in ["Estação", "Terminal"] else ""
        data = data_entry.get_date()
        data_formatada = data.strftime('%d de %B de %Y')
        horario = horario_var.get()
        tipo_local = tipo_local_var.get()

        # Captura os dados de assinaturas
        lista_assinaturas = [
        (assinatura["nome_var"].get(), assinatura["cargo_var"].get())
        for assinatura in assinaturas
        if assinatura["nome_var"].get() and assinatura["cargo_var"].get()
    ]

        if (concessionaria == "Selecionar concessionária" or not estacao or not data_formatada or not horario or not lista_assinaturas):
            messagebox.showwarning("Aviso", "Preencha todos os campos antes de continuar.")
            return

        # Executa a função de callback com os valores fornecidos
        callback(concessionaria, estacao, tipo_local, data_formatada, horario, imagens, legendas, lista_assinaturas)
        root.destroy()

    # Botão para gerar o relatório
    ttk.Button(big_frame, text="Gerar Relatório", command=on_generate).grid(row=8, column=1, pady=20, padx=5)

    # Atualiza o tipo de local inicialmente
    update_tipo_local()

    root.mainloop()
