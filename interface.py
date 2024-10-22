from tkinter import Tk, Label, Entry, StringVar, messagebox, filedialog, Button, PhotoImage, Canvas, Scrollbar, Radiobutton, IntVar
from tkcalendar import DateEntry
import locale
from tkinter import ttk  # Biblioteca ttk para usar o tema
import os
from PIL import Image, ImageTk
import json
from tkinter import Tk, StringVar, messagebox, filedialog, IntVar
from tkcalendar import DateEntry
import locale

# Define a localidade para português
locale.setlocale(locale.LC_TIME, 'pt_BR.UTF-8')

def abrir_interface(callback):

    with open('estações.json', 'r',encoding='utf-8') as f:
        estacoes_por_concessionaria = json.load(f)

    # Janela principal
    root = Tk()
    root.title("Gerador de Relatório Técnico")
  
    #icon = PhotoImage(file="Logo AGETRANSP.png")
    #root.iconphoto(False, icon)
  
    big_frame = ttk.Frame(root)
    big_frame.grid(row=0, column=0, padx=20, pady=20)  # Usando grid para o frame

    # Definir o tema Azure
    root.tk.call("source", os.path.join("Azure-ttk-theme-main", "azure.tcl"))  # Carregar o tema a partir do arquivo TCL
    root.tk.call("set_theme", "dark")

    # Variáveis para armazenar os valores
    concessionaria_var = StringVar(root)
    concessionaria_var.set("Selecionar concessionária")  # valor padrão

    estacao_var = StringVar(root)
    data_var = StringVar(root)
    horario_var = StringVar(root)

    tipo_local_var = StringVar(root)

    # Lista para armazenar as imagens
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

    # Frame para pré-visualização das imagens com abas
    notebook = ttk.Notebook(big_frame)
    notebook.grid(row=5, column=1, padx=5, pady=5)

   
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

    # Botão para selecionar imagens
    ttk.Button(big_frame, text="Selecionar Imagens", command=selecionar_imagens).grid(row=4, column=1, pady=10)

    def on_generate():
        concessionaria = concessionaria_var.get()
        estacao = estacao_var.get() if tipo_local_var.get() in ["Estação", "Terminal"] else ""  # Usa estacao_var ou terminal_var
        data = data_entry.get_date()  # Obtém a data como objeto
        data_formatada = data.strftime('%d de %B de %Y')  # Formata a data
        horario = horario_var.get()
        tipo_local = tipo_local_var.get()
        

        # Verifica se todos os campos estão preenchidos
        if (concessionaria == "Selecionar concessionária" or 
            not estacao or 
            not data_formatada or 
            not horario):
            messagebox.showwarning("Aviso", "Preencha todos os campos antes de continuar.")
            return
        
        # Executa a função de callback com os valores fornecidos
        callback(concessionaria, estacao, tipo_local, data_formatada, horario, imagens, legendas)  
        root.destroy()

    # Botão para gerar o relatório
    ttk.Button(big_frame, text="Gerar Relatório", command=on_generate).grid(row=6, column=1, pady=20, padx=5)

    # Atualiza o tipo de local inicialmente
    update_tipo_local()

    root.mainloop()
