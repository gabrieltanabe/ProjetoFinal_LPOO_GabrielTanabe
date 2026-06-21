import tkinter as tk
from tkinter import ttk
from controller.venda_controller import VendaController

class VendaView(tk.Toplevel):
    def __init__(self, master=None):
        super().__init__(master)
        self.title("Consulta de Vendas Realizadas")
        self.geometry("900x400")
        self.transient(master)
        self.grab_set()
        self.focus_force()
        self.controller = VendaController()

        tk.Label(self, text="Histórico de Vendas", font=("Helvetica", 16, "bold")).pack(pady=10)

        frame_tabela = tk.Frame(self)
        frame_tabela.pack(pady=10, padx=10, expand=True, fill="both")

        colunas = ("ID Venda", "ID Sessão", "Filme", "Assento", "Tipo Ingresso", "Pagamento", "Valor", "Data")
        self.tree = ttk.Treeview(frame_tabela, columns=colunas, show="headings")
        
        for col in colunas:
            self.tree.heading(col, text=col)
            self.tree.column(col, anchor="center")

        self.tree.column("ID Venda", width=60)
        self.tree.column("ID Sessão", width=60)
        self.tree.column("Assento", width=60)
        self.tree.column("Valor", width=80)

        self.tree.pack(expand=True, fill="both", side="left")

        scrollbar = ttk.Scrollbar(frame_tabela, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side="right", fill="y")

        self._carregar_dados()

    def _carregar_dados(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        vendas = self.controller.listar()
        for v in vendas:
            dt_formatada = v.data_venda.strftime("%d/%m/%Y %H:%M")
            self.tree.insert("", "end", values=(
                v.id_venda,
                v.ingresso.sessao.id_sessao,
                v.ingresso.sessao.filme.titulo,
                v.ingresso.assento,
                v.ingresso.get_tipo(),
                v.metodo_pagamento,
                f"R$ {v.valor_total:.2f}",
                dt_formatada
            ))