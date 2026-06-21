import tkinter as tk
from tkinter import ttk, messagebox
from controller.sala_controller import SalaController

class SalaView(tk.Toplevel):
    def __init__(self, master=None):
        super().__init__(master)
        self.title("Gerenciamento de Salas")
        self.geometry("600x400")
        self.transient(master)
        self.grab_set()
        self.focus_force()
        self.controller = SalaController()

        self.id_selecionado = tk.StringVar()
        self.var_numero = tk.StringVar()
        self.var_capacidade = tk.StringVar()

        self._criar_formulario()
        self._criar_botoes()
        self._criar_tabela()
        self._carregar_dados()

    def _criar_formulario(self):
        frame_form = tk.Frame(self)
        frame_form.pack(pady=10, padx=10, fill="x")

        tk.Label(frame_form, text="Número da Sala:").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        tk.Entry(frame_form, textvariable=self.var_numero, width=15).grid(row=0, column=1, padx=5, pady=5)

        tk.Label(frame_form, text="Capacidade:").grid(row=0, column=2, sticky="w", padx=5, pady=5)
        tk.Entry(frame_form, textvariable=self.var_capacidade, width=15).grid(row=0, column=3, padx=5, pady=5)

    def _criar_botoes(self):
        frame_btn = tk.Frame(self)
        frame_btn.pack(pady=5)
        tk.Button(frame_btn, text="Salvar", command=self.salvar, width=12).grid(row=0, column=0, padx=5)
        tk.Button(frame_btn, text="Atualizar", command=self.atualizar, width=12).grid(row=0, column=1, padx=5)
        tk.Button(frame_btn, text="Excluir", command=self.excluir, width=12).grid(row=0, column=2, padx=5)
        tk.Button(frame_btn, text="Limpar", command=self.limpar_campos, width=12).grid(row=0, column=3, padx=5)

    def _criar_tabela(self):
        frame_tabela = tk.Frame(self)
        frame_tabela.pack(pady=10, padx=10, expand=True, fill="both")
        self.tree = ttk.Treeview(frame_tabela, columns=("ID", "Número", "Capacidade"), show="headings")
        for col in ("ID", "Número", "Capacidade"):
            self.tree.heading(col, text=col)
            self.tree.column(col, anchor="center")
        self.tree.bind("<ButtonRelease-1>", self.selecionar_linha)
        self.tree.pack(expand=True, fill="both")

    def limpar_campos(self):
        self.id_selecionado.set("")
        self.var_numero.set("")
        self.var_capacidade.set("")

    def _carregar_dados(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        salas = self.controller.listar()
        for s in salas:
            self.tree.insert("", "end", values=(s.id_sala, s.numero, s.capacidade))

    def selecionar_linha(self, event):
        selecao = self.tree.selection()
        if selecao:
            item = self.tree.item(selecao[0], "values")
            self.id_selecionado.set(item[0])
            self.var_numero.set(item[1])
            self.var_capacidade.set(item[2])

    def salvar(self):
        sucesso, msg = self.controller.salvar(self.var_numero.get(), self.var_capacidade.get())
        if sucesso:
            messagebox.showinfo("Sucesso", msg)
            self.limpar_campos()
            self._carregar_dados()
        else:
            messagebox.showerror("Erro", msg)

    def atualizar(self):
        if not self.id_selecionado.get():
            messagebox.showwarning("Aviso", "Selecione uma sala.")
            return
        sucesso, msg = self.controller.atualizar(int(self.id_selecionado.get()), self.var_numero.get(), self.var_capacidade.get())
        if sucesso:
            messagebox.showinfo("Sucesso", msg)
            self.limpar_campos()
            self._carregar_dados()
        else:
            messagebox.showerror("Erro", msg)

    def excluir(self):
        if not self.id_selecionado.get():
            return
        if messagebox.askyesno("Confirmar", "Excluir sala?"):
            sucesso, msg = self.controller.remover(int(self.id_selecionado.get()))
            if sucesso:
                self.limpar_campos()
                self._carregar_dados()
            else:
                messagebox.showerror("Erro", msg)