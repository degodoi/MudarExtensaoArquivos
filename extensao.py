import tkinter as tk
from tkinter import filedialog
import os
import time
import shutil

def selecionar_pasta_origem():
    caminho_origem = filedialog.askdirectory()
    if caminho_origem:
        entry_origem.delete(0, tk.END)
        entry_origem.insert(0, caminho_origem)

def selecionar_arquivos_origem():
    caminhos_arquivos = filedialog.askopenfilenames()
    if caminhos_arquivos:
        entry_origem.delete(0, tk.END)
        entry_origem.insert(0, '; '.join(caminhos_arquivos))

def selecionar_pasta_destino():
    caminho_destino = filedialog.askdirectory()
    if caminho_destino:
        entry_destino.delete(0, tk.END)
        entry_destino.insert(0, caminho_destino)

def alterar_extensao():
    caminho_origem = entry_origem.get()
    caminho_destino = entry_destino.get()
    nova_extensao = entry_extensao.get()

    if not caminho_origem or not caminho_destino or not nova_extensao:
        label_status.config(text='Preencha todos os campos!')
        return

    if not os.path.exists(caminho_origem):
        label_status.config(text=f'O diretório de origem "{caminho_origem}" não existe.')
        return

    if not os.path.exists(caminho_destino):
        os.makedirs(caminho_destino)

    if caminho_origem == caminho_destino:
        label_status.config(text='Os diretórios de origem e destino devem ser diferentes.')
        return

    inicio = time.time()

    qtd_alterados = 0
    if os.path.isdir(caminho_origem):
        for arquivo in os.listdir(caminho_origem):
            caminho_arquivo_origem = os.path.join(caminho_origem, arquivo)

            if os.path.isfile(caminho_arquivo_origem):
                nome_arquivo, extensao_antiga = os.path.splitext(arquivo)

                if extensao_antiga.lower() == nova_extensao.lower():
                    label_status.config(text=f'O arquivo "{arquivo}" já possui a extensão "{nova_extensao}".')
                    continue

                novo_nome_arquivo = nome_arquivo + '.' + nova_extensao
                caminho_arquivo_destino = os.path.join(caminho_destino, novo_nome_arquivo)

                shutil.copy(caminho_arquivo_origem, caminho_arquivo_destino)
                qtd_alterados += 1
    else:
        for caminho_arquivo_origem in caminho_origem.split('; '):
            if os.path.isfile(caminho_arquivo_origem):
                nome_arquivo, extensao_antiga = os.path.splitext(os.path.basename(caminho_arquivo_origem))

                if extensao_antiga.lower() == nova_extensao.lower():
                    label_status.config(text=f'O arquivo "{os.path.basename(caminho_arquivo_origem)}" já possui a extensão "{nova_extensao}".')
                    continue

                novo_nome_arquivo = nome_arquivo + '.' + nova_extensao
                caminho_arquivo_destino = os.path.join(caminho_destino, novo_nome_arquivo)

                shutil.copy(caminho_arquivo_origem, caminho_arquivo_destino)
                qtd_alterados += 1

    fim = time.time()
    tempo_total = fim - inicio

    label_status.config(text=f'Alteração concluída. Tempo total: {tempo_total:.2f} segundos. Arquivos alterados: {qtd_alterados}.')

# Criar a janela principal
root = tk.Tk()
root.title('Alterar Extensão de Arquivos')

# Criar os widgets
label_origem = tk.Label(root, text='Selecione a pasta de origem ou os arquivos:', font=('Arial', 12))
label_origem.grid(row=0, column=0, padx=10, pady=5, sticky=tk.W)

entry_origem = tk.Entry(root, width=50)
entry_origem.grid(row=0, column=1, padx=10, pady=5)

button_selecionar_origem = tk.Button(root, text='Selecionar Pasta', command=selecionar_pasta_origem)
button_selecionar_origem.grid(row=0, column=2, padx=10, pady=5)

button_selecionar_arquivos = tk.Button(root, text='Selecionar Arquivos', command=selecionar_arquivos_origem)
button_selecionar_arquivos.grid(row=0, column=3, padx=10, pady=5)

label_destino = tk.Label(root, text='Selecione a pasta de destino:', font=('Arial', 12))
label_destino.grid(row=1, column=0, padx=10, pady=5, sticky=tk.W)

entry_destino = tk.Entry(root, width=50)
entry_destino.grid(row=1, column=1, padx=10, pady=5)

button_selecionar_destino = tk.Button(root, text='Selecionar', command=selecionar_pasta_destino)
button_selecionar_destino.grid(row=1, column=2, padx=10, pady=5)

label_extensao = tk.Label(root, text='Nova Extensão:', font=('Arial', 12))
label_extensao.grid(row=2, column=0, padx=10, pady=5, sticky=tk.W)

entry_extensao = tk.Entry(root, width=10)
entry_extensao.grid(row=2, column=1, padx=10, pady=5)

button_executar = tk.Button(root, text='Executar', command=alterar_extensao, bg='green', fg='white', font=('Arial', 12))
button_executar.grid(row=3, column=0, columnspan=4, pady=10)

label_status = tk.Label(root, text='', font=('Arial', 12), fg='blue')
label_status.grid(row=4, column=0, columnspan=4)

# Iniciar o loop principal da janela
root.mainloop()
