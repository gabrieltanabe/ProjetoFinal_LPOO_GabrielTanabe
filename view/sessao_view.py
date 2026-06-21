import tkinter as tk
from tkinter import ttk, messagebox
from controller.sessao_controller import SessaoController
from controller.filme_controller import FilmeController
from controller.sala_controller import SalaController
from model.enums import StatusSessao

class SessaoView(tk.Toplevel):
    def __init__(self, master=None):
        super().__init__(master)
        self.title("Gerenciamento de Sessões")
        self.geometry("900x550")
        self.transient(master)
        self.grab_set()
        self.focus_force()
        self.controller = SessaoController()
        self.filme_ctrl = FilmeController()
        self.sala_ctrl = SalaController()

        self.id_selecionado = tk.StringVar()
        self.var_filme = tk.StringVar()
        self.var_sala = tk.StringVar()
        self.var_datahora = tk.StringVar()
        self.var_preco = tk.StringVar()
        self.var_status = tk.StringVar()

        self._criar_formulario()
        self._criar_botoes()
        self._criar_tabela()
        self._carregar_dados()

    def _carregar_comboboxes(self):
        filmes = self.filme_ctrl.listar()
        salas = self.sala_ctrl.listar()
        self.lista_filmes = [f"{f.id_filme} - {f.titulo}" for f in filmes]
        self.lista_salas = [f"{s.id_sala} - Sala {s.numero}" for s in salas]
        self.cb_filme['values'] = self.lista_filmes
        self.cb_sala['values'] = self.lista_salas

    def _criar_formulario(self):
        frame_form = tk.Frame(self)
        frame_form.pack(pady=10, padx=10, fill="x")

        tk.Label(frame_form, text="Filme:").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.cb_filme = ttk.Combobox(frame_form, textvariable=self.var_filme, state="readonly", width=40)
        self.cb_filme.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(frame_form, text="Sala:").grid(row=0, column=2, sticky="w", padx=5, pady=5)
        self.cb_sala = ttk.Combobox(frame_form, textvariable=self.var_sala, state="readonly", width=20)
        self.cb_sala.grid(row=0, column=3, padx=5, pady=5)

        tk.Label(frame_form, text="Data/Hora (DD/MM/AAAA HH:MM):").grid(row=1, column=0, sticky="w", padx=5, pady=5)
        tk.Entry(frame_form, textvariable=self.var_datahora, width=43).grid(row=1, column=1, padx=5, pady=5)

        tk.Label(frame_form, text="Preço Base (R$):").grid(row=1, column=2, sticky="w", padx=5, pady=5)
        tk.Entry(frame_form, textvariable=self.var_preco, width=23).grid(row=1, column=3, padx=5, pady=5)

        tk.Label(frame_form, text="Status:").grid(row=2, column=0, sticky="w", padx=5, pady=5)
        cb_status = ttk.Combobox(frame_form, textvariable=self.var_status, state="readonly", width=40)
        cb_status['values'] = [s.value for s in StatusSessao]
        cb_status.grid(row=2, column=1, padx=5, pady=5)
        
        self._carregar_comboboxes()

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
        colunas = ("ID", "Filme", "Sala", "Data/Hora", "Preço", "Status")
        self.tree = ttk.Treeview(frame_tabela, columns=colunas, show="headings")
        for col in colunas:
            self.tree.heading(col, text=col)
            self.tree.column(col, anchor="center")
        self.tree.column("ID", width=40)
        self.tree.bind("<ButtonRelease-1>", self.selecionar_linha)
        self.tree.pack(expand=True, fill="both")

    def limpar_campos(self):
        self.id_selecionado.set("")
        self.var_filme.set("")
        self.var_sala.set("")
        self.var_datahora.set("")
        self.var_preco.set("")
        self.var_status.set("")
        self._carregar_comboboxes()

    def _carregar_dados(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        sessoes = self.controller.listar()
        for s in sessoes:
            dt_formatada = s.data_hora.strftime("%d/%m/%Y %H:%M")
            self.tree.insert("", "end", values=(
                s.id_sessao, f"{s.filme.id_filme} - {s.filme.titulo}", 
                f"{s.sala.id_sala} - Sala {s.sala.numero}", 
                dt_formatada, f"{s.preco_base:.2f}", s.status.value
            ))

    def extrair_id(self, texto):
        if not texto: return None
        return int(texto.split(" - ")[0])

    def selecionar_linha(self, event):
        selecao = self.tree.selection()
        if selecao:
            item = self.tree.item(selecao[0], "values")
            self.id_selecionado.set(item[0])
            self.var_filme.set(item[1])
            self.var_sala.set(item[2])
            self.var_datahora.set(item[3])
            self.var_preco.set(item[4])
            self.var_status.set(item[5])

    def salvar(self):
        id_f = self.extrair_id(self.var_filme.get())
        id_s = self.extrair_id(self.var_sala.get())
        sucesso, msg = self.controller.salvar(id_f, id_s, self.var_datahora.get(), self.var_preco.get(), self.var_status.get())
        if sucesso:
            messagebox.showinfo("Sucesso", msg)
            self.limpar_campos()
            self._carregar_dados()
        else:
            messagebox.showerror("Erro", msg)

    def atualizar(self):
        if not self.id_selecionado.get(): return
        id_f = self.extrair_id(self.var_filme.get())
        id_s = self.extrair_id(self.var_sala.get())
        sucesso, msg = self.controller.atualizar(int(self.id_selecionado.get()), id_f, id_s, self.var_datahora.get(), self.var_preco.get(), self.var_status.get())
        if sucesso:
            self.limpar_campos()
            self._carregar_dados()
        else:
            messagebox.showerror("Erro", msg)

    def excluir(self):
        if not self.id_selecionado.get(): return
        if messagebox.askyesno("Confirmar", "Excluir sessão?"):
            sucesso, msg = self.controller.remover(int(self.id_selecionado.get()))
            if sucesso:
                self.limpar_campos()
                self._carregar_dados()
            else:
                messagebox.showerror("Erro", msg)