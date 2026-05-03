import pandas as pd
from tkinter import ttk
import tkinter as tk
from tkinter import *
from tkinter import messagebox
import random

"""
AVISO IMPORTANTE: Quando selecionar uma quantidade de alunos na segunda tela (ex: 100 alunos), confirme para ver o resultado,
e em seguida, se quiser testar uma outra quantidade (1000 ou 10), volte para a Janela Principal, e refaça o processo. Se não fizer isso, o código vai dar um
erro chamado "Traceback: self.quantidade_alunos don't have a method called "get()"."

Até o momento, é o único bug existente.
"""

class JanelaQuantidadeAlunos(Toplevel):
    def __init__(self, master=None):
        super().__init__(master)

        self.title("Quantidade de Alunos")
        self.geometry("720x480")
        self.resizable(True, True)
        self.configure(bg='lightgray', bd=5, pady=20)

        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

        frame_quantidade = tk.Frame(self, bg='lightgray', bd=5, pady=20)
        frame_quantidade.grid(row=0, column=0)
        frame_quantidade.columnconfigure(0, weight=1)

        ttk.Label(
            frame_quantidade,
            text="Escolha a quantidade de alunos (Deve ser 10, 100 ou 1000):",
            font=("Segoe UI", 12), background='lightgray',
        ).grid(column=0, row=0, pady=0)

        self.quantidade_alunos = ttk.Combobox(frame_quantidade, values=["10", "100", "1000"]) #Lista de opções.
        self.quantidade_alunos.grid(column=0, row=1, pady=20)
        self.quantidade_alunos.current(0)

        ttk.Button(
            frame_quantidade,
            text="Confirmar",
            command=self.confirmar_quantidade
        ).grid(column=0, row=2, pady=10)

    def confirmar_quantidade(self):
        quantidade_str = self.quantidade_alunos.get().strip()

        if not quantidade_str:
            messagebox.showwarning("Alerta", "Esse campo não pode ficar vazio.")
            return

        self.quantidade_alunos = int(quantidade_str)

        # Se o usuário escolher 10 alunos, abre entrada manual; senão gera os dados aleatoriamente.
        if self.quantidade_alunos == 10:
            JanelaEntradaDados(self.quantidade_alunos, self)
        else:
            df_gerado = self.gerar_dados(self.quantidade_alunos)
            organizacao = OrganizacaoNotas(df_gerado)
            df_original, df_ordenado = organizacao.ordenar()
            JanelaResultado(df_original, df_ordenado, self)

    #O método é estático por não ter necessidade de ter uma instância da classe.
    @staticmethod
    def gerar_dados(quantidade):
        dados = {
            'Nome': [f'Aluno {i + 1}' for i in range(quantidade)],
            'Nota': [round(random.uniform(0, 10), 1) for _ in range(quantidade)]
        }
        return pd.DataFrame(dados)


class JanelaEntradaDados(Toplevel):
    def __init__(self, quantidade_alunos, master=None):
        super().__init__(master)

        self.quantidade_alunos = quantidade_alunos
        self.df = pd.DataFrame(columns=['Nome', 'Nota'])

        self.title("Entrada de Dados")
        self.geometry("720x480")
        self.resizable(True, True)
        self.configure(bg='lightgray', bd=5, pady=40)

        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        self.rowconfigure(2, weight=1)
        self.columnconfigure(0, weight=1)

        frame_entrada_nome = tk.Frame(self, bg='lightgray', bd=5, pady=20)
        frame_entrada_nome.grid(row=0, column=0, sticky="nsew")
        frame_entrada_nome.columnconfigure(0, weight=1)

        ttk.Label(
            frame_entrada_nome,
            text="Digite o nome do aluno:",
            font=("Segoe UI", 12),
            background='lightgray'
        ).grid(column=0, row=0, pady=5)

        self.entrada_nome = ttk.Entry(frame_entrada_nome, width=30)
        self.entrada_nome.grid(column=0, row=1, pady=5)

        frame_entrada_nota = tk.Frame(self, bg='lightgray', bd=5, pady=20)
        frame_entrada_nota.grid(row=1, column=0, sticky="nsew")
        frame_entrada_nota.columnconfigure(0, weight=1)

        ttk.Label(
            frame_entrada_nota,
            text="Digite a nota do aluno:",
            font=("Segoe UI", 12),
            background='lightgray'
        ).grid(column=0, row=0, pady=0)

        self.entrada_nota = ttk.Entry(frame_entrada_nota, width=30)
        self.entrada_nota.grid(column=0, row=1, pady=5)

        frame_botoes = tk.Frame(self, bg='lightgray', bd=5, pady=10)
        frame_botoes.grid(row=2, column=0, sticky="nsew")
        frame_botoes.columnconfigure(0, weight=1)
        frame_botoes.columnconfigure(1, weight=1)

        ttk.Button(
            frame_botoes,
            text="Adicionar Aluno",
            command=self.adicionar
        ).grid(column=0, row=0, pady=10, padx=5)

        ttk.Button(
            frame_botoes,
            text="Finalizar",
            command=self.finalizar
        ).grid(column=1, row=0, pady=10, padx=5)

    def adicionar(self):
        nome = self.entrada_nome.get().strip()
        nota_texto = self.entrada_nota.get().strip()

        if not nome:
            messagebox.showwarning("Aviso", "O nome do aluno não pode ficar vazio.")
            return
        try:
            nota = float(nota_texto.replace(",", "."))
        except ValueError:
            messagebox.showwarning("Aviso", "A nota deve ser um número.")
            return

        nova_linha = {'Nome': nome, 'Nota': nota}
        self.df = pd.concat([self.df, pd.DataFrame([nova_linha])], ignore_index=True)

        self.entrada_nome.delete(0, END)
        self.entrada_nota.delete(0, END)
        self.entrada_nome.focus_set()

    def finalizar(self):
        if self.df.empty:
            messagebox.showwarning("Aviso", "Nenhum aluno cadastrado.")
            return

        organizacao = OrganizacaoNotas(self.df)
        df_original, df_ordenado = organizacao.ordenar()
        resultado = JanelaResultado(df_original, df_ordenado, self)
        self.wait_window(resultado)


class OrganizacaoNotas:
    def __init__(self, df):
        self.df = df.copy()

    """ Parte principal do código -> a ordenação das notas por meio de Insertion Sort"""
    """Retorna DataFrame original e DataFrame ordenado por Insertion Sort"""
    def ordenar(self):

        df_original = self.df.copy()
        lista = self.df.values.tolist()  # Converte para lista de listas

        for i in range(1, len(lista)):
            chave = lista[i]
            chave_nota = chave[1]
            j = i - 1

            while j >= 0 and lista[j][1] > chave_nota:
                lista[j + 1] = lista[j]
                j -= 1

            lista[j + 1] = chave

        df_ordenado = pd.DataFrame(lista, columns=['Nome', 'Nota'])
        df_ordenado.reset_index(drop=True, inplace=True)

        return df_original, df_ordenado


class JanelaResultado(Toplevel):
    def __init__(self, df_original, df_ordenado, master=None):
        super().__init__(master)
        self.title("Resultado - Notas Originais vs Ordenadas (Insertion Sort)")
        self.geometry("1080x720")
        self.resizable(True, True)
        self.configure(bg='lightgray', bd=5, pady=20)

        self.rowconfigure(0, weight=0)
        self.rowconfigure(1, weight=1)
        self.rowconfigure(2, weight=0)
        self.rowconfigure(3, weight=1)
        self.columnconfigure(0, weight=1)

        ttk.Label(
            self,
            text="Notas na Ordem Original",
            font=("Segoe UI", 12, "bold"),
            background='lightgray'
        ).grid(row=0, column=0, pady=10, sticky="w", padx=10)

        colunas = ("Posição", "Nome", "Nota")
        tabela_original = ttk.Treeview(self, columns=colunas, show="headings")
        for col in colunas:
            tabela_original.heading(col, text=col.title())
            tabela_original.column(col, width=150)

        for posicao, (nome, nota) in enumerate(zip(df_original['Nome'], df_original['Nota'])):
            tabela_original.insert("", "end", values=(posicao + 1, nome, nota))

        tabela_original.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)

        ttk.Label(
            self,
            text="Notas Ordenadas (Insertion Sort)",
            font=("Segoe UI", 12, "bold"),
            background='lightgray'
        ).grid(row=2, column=0, pady=10, sticky="w", padx=10)

        tabela_ordenada = ttk.Treeview(self, columns=colunas, show="headings")
        for col in colunas:
            tabela_ordenada.heading(col, text=col.title())
            tabela_ordenada.column(col, width=150)

        for posicao, (nome, nota) in enumerate(zip(df_ordenado['Nome'], df_ordenado['Nota'])):
            tabela_ordenada.insert("", "end", values=(posicao + 1, nome, nota))

        tabela_ordenada.grid(row=3, column=0, padx=10, pady=10, sticky="nsew")


# Janela principal
janela_principal = Tk()
janela_principal.title("Organização de notas de alunos - Insertion Sort")
janela_principal.geometry("720x480")
janela_principal.resizable(True, True)
janela_principal.configure(bg='lightgray', bd=5, pady=40)

janela_principal.rowconfigure(0, weight=1)
janela_principal.columnconfigure(0, weight=1)

frame_principal = tk.Frame(
    janela_principal,
    bg='lightgray',
    bd=5,
    pady=40,
)
frame_principal.grid(row=0, column=0)

frame_principal.rowconfigure(0, weight=1)
frame_principal.columnconfigure(0, weight=1)

ttk.Label(
    frame_principal,
    text="Seja bem-vindo ao sistema de ordenação de notas de alunos por Insertion Sort!",
    font=("Segoe UI", 12),
    background='lightgray'
).grid(column=0, row=0, pady=10)

btn_iniciar = ttk.Button(
    frame_principal,
    text="Iniciar",
    command=lambda: JanelaQuantidadeAlunos(janela_principal)
)
btn_iniciar.grid(column=0, row=1, pady=10, padx=10)

janela_principal.mainloop()