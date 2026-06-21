import tkinter as tk
from tkinter import ttk, messagebox
from controller.filme_controller import FilmeController
from model.enums import StatusFilme, ClassificacaoIndicativa

class FilmeView(tk.Toplevel):
    def __init__(self, master=None):
        super().__init__(master)
        self.title("Gerenciamento de Filmes")
        self.geometry("800x500")
        self.transient(master)
        self.grab_set()
        self.focus_force()
        self.controller = FilmeController()
    
        self.id_selecionado = tk.StringVar()
        self.var_titulo = tk.StringVar()
        self.var_duracao = tk.StringVar()
        self.var_classificacao = tk.StringVar()
        self.var_status = tk.StringVar()

        self._criar_formulario()
        self._criar_botoes()
        self._criar_tabela()
        self._carregar_dados()

    def _criar_formulario(self):
        frame_form = tk.Frame(self)
        frame_form.pack(pady=10, padx=10, fill="x")

        tk.Label(frame_form, text="Título:").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        tk.Entry(frame_form, textvariable=self.var_titulo, width=40).grid(row=0, column=1, padx=5, pady=5)

        tk.Label(frame_form, text="Duração (min):").grid(row=0, column=2, sticky="w", padx=5, pady=5)
        tk.Entry(frame_form, textvariable=self.var_duracao, width=15).grid(row=0, column=3, padx=5, pady=5)

        tk.Label(frame_form, text="Classificação:").grid(row=1, column=0, sticky="w", padx=5, pady=5)
        cb_classificacao = ttk.Combobox(frame_form, textvariable=self.var_classificacao, state="readonly", width=37)
        cb_classificacao['values'] = [c.value for c in ClassificacaoIndicativa]
        cb_classificacao.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(frame_form, text="Status:").grid(row=1, column=2, sticky="w", padx=5, pady=5)
        cb_status = ttk.Combobox(frame_form, textvariable=self.var_status, state="readonly", width=12)
        cb_status['values'] = [s.value for s in StatusFilme]
        cb_status.grid(row=1, column=3, padx=5, pady=5)

    def _criar_botoes(self):
        frame_btn = tk.Frame(self)
        frame_btn.pack(pady=5)

        tk.Button(frame_btn, text="Salvar", command=self.salvar, width=15).grid(row=0, column=0, padx=5)
        tk.Button(frame_btn, text="Atualizar", command=self.atualizar, width=15).grid(row=0, column=1, padx=5)
        tk.Button(frame_btn, text="Excluir", command=self.excluir, width=15).grid(row=0, column=2, padx=5)
        tk.Button(frame_btn, text="Limpar", command=self.limpar_campos, width=15).grid(row=0, column=3, padx=5)

    def _criar_tabela(self):
        frame_tabela = tk.Frame(self)
        frame_tabela.pack(pady=10, padx=10, expand=True, fill="both")

        colunas = ("ID", "Título", "Duração", "Classificação", "Status")
        self.tree = ttk.Treeview(frame_tabela, columns=colunas, show="headings")
        
        for col in colunas:
            self.tree.heading(col, text=col)
            self.tree.column(col, anchor="center")

        self.tree.column("ID", width=50)
        self.tree.column("Duração", width=80)
        
        self.tree.bind("<ButtonRelease-1>", self.selecionar_linha)
        self.tree.pack(expand=True, fill="both", side="left")

        scrollbar = ttk.Scrollbar(frame_tabela, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side="right", fill="y")

    def limpar_campos(self):
        self.id_selecionado.set("")
        self.var_titulo.set("")
        self.var_duracao.set("")
        self.var_classificacao.set("")
        self.var_status.set("")

    def _carregar_dados(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        filmes = self.controller.listar()
        for f in filmes:
            self.tree.insert("", "end", values=(f.id_filme, f.titulo, f.duracao, f.classificacao.value, f.status.value))

    def selecionar_linha(self, event):
        selecao = self.tree.selection()
        if selecao:
            item = self.tree.item(selecao[0], "values")
            self.id_selecionado.set(item[0])
            self.var_titulo.set(item[1])
            self.var_duracao.set(item[2])
            self.var_classificacao.set(item[3])
            self.var_status.set(item[4])

    def salvar(self):
        sucesso, msg = self.controller.salvar(
            self.var_titulo.get(), self.var_duracao.get(), 
            self.var_classificacao.get(), self.var_status.get()
        )
        if sucesso:
            messagebox.showinfo("Sucesso", msg)
            self.limpar_campos()
            self._carregar_dados()
        else:
            messagebox.showerror("Erro", msg)

    def atualizar(self):
        if not self.id_selecionado.get():
            messagebox.showwarning("Aviso", "Selecione um filme para atualizar.")
            return
        sucesso, msg = self.controller.atualizar(
            int(self.id_selecionado.get()), self.var_titulo.get(), 
            self.var_duracao.get(), self.var_classificacao.get(), self.var_status.get()
        )
        if sucesso:
            messagebox.showinfo("Sucesso", msg)
            self.limpar_campos()
            self._carregar_dados()
        else:
            messagebox.showerror("Erro", msg)

    def excluir(self):
        if not self.id_selecionado.get():
            messagebox.showwarning("Aviso", "Selecione um filme para excluir.")
            return
        if messagebox.askyesno("Confirmar", "Deseja realmente excluir este filme?"):
            sucesso, msg = self.controller.remover(int(self.id_selecionado.get()))
            if sucesso:
                messagebox.showinfo("Sucesso", msg)
                self.limpar_campos()
                self._carregar_dados()
            else:
                messagebox.showerror("Erro", msg)