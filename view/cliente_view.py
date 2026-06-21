import datetime
import tkinter as tk
from tkinter import ttk, messagebox
from controller.sessao_controller import SessaoController
from controller.ingresso_controller import IngressoController
from controller.venda_controller import VendaController
from model.enums import StatusSessao, StatusFilme

class ClienteView(tk.Toplevel):
    def __init__(self, master=None):
        super().__init__(master)
        self.title("Área do Cliente - Compra de Ingressos")
        self.geometry("900x600")
        self.transient(master)
        self.grab_set()
        self.focus_force()

        self.sessao_controller = SessaoController()
        self.ingresso_controller = IngressoController()
        self.venda_controller = VendaController()

        self.var_id_sessao = tk.StringVar()
        self.var_info_sessao = tk.StringVar(value="Nenhuma sessão selecionada")
        self.var_assento = tk.StringVar()
        self.var_tipo_ingresso = tk.StringVar()
        self.var_metodo_pagamento = tk.StringVar()

        self._criar_interface()
        self._carregar_sessoes()

    def _criar_interface(self):
        tk.Label(self, text="Bem-vindo! Escolha sua Sessão", font=("Helvetica", 16, "bold")).pack(pady=10)

        frame_sessoes = tk.LabelFrame(self, text=" 1. Sessões Disponíveis ", padx=10, pady=10)
        frame_sessoes.pack(fill="both", expand=True, padx=15, pady=5)

        colunas = ("ID", "Filme", "Data/Hora", "Sala", "Preço Base (R$)")
        self.tree = ttk.Treeview(frame_sessoes, columns=colunas, show="headings", selectmode="browse")
        for col in colunas:
            self.tree.heading(col, text=col)
            self.tree.column(col, anchor="center")
        
        self.tree.column("ID", width=40)
        self.tree.column("Filme", width=250)
        self.tree.bind("<ButtonRelease-1>", self.selecionar_sessao)
        self.tree.pack(side="left", fill="both", expand=True)

        scrollbar = ttk.Scrollbar(frame_sessoes, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side="right", fill="y")

        frame_compra = tk.LabelFrame(self, text=" 2. Configurar Ingresso e Pagamento ", padx=10, pady=10)
        frame_compra.pack(fill="x", padx=15, pady=10)

        tk.Label(frame_compra, textvariable=self.var_info_sessao, fg="blue", font=("Helvetica", 10, "bold")).grid(row=0, column=0, columnspan=4, pady=(0, 10), sticky="w")

        tk.Label(frame_compra, text="Número do Assento:").grid(row=1, column=0, sticky="e", padx=5, pady=5)
        tk.Entry(frame_compra, textvariable=self.var_assento, width=10).grid(row=1, column=1, sticky="w", padx=5, pady=5)

        tk.Label(frame_compra, text="Tipo de Ingresso:").grid(row=1, column=2, sticky="e", padx=5, pady=5)
        cb_ingresso = ttk.Combobox(frame_compra, textvariable=self.var_tipo_ingresso, state="readonly", width=15)
        cb_ingresso['values'] = ["Comum", "Meia", "VIP"]
        cb_ingresso.grid(row=1, column=3, sticky="w", padx=5, pady=5)

        tk.Label(frame_compra, text="Método de Pagamento:").grid(row=2, column=0, sticky="e", padx=5, pady=5)
        cb_pagamento = ttk.Combobox(frame_compra, textvariable=self.var_metodo_pagamento, state="readonly", width=15)
        cb_pagamento['values'] = ["PIX", "Cartão", "Dinheiro"]
        cb_pagamento.grid(row=2, column=1, sticky="w", padx=5, pady=5)

        btn_comprar = tk.Button(frame_compra, text="Confirmar Compra", command=self.processar_compra, bg="green", fg="white", font=("Helvetica", 10, "bold"), width=20)
        btn_comprar.grid(row=2, column=2, columnspan=2, padx=15, pady=5)

    def _carregar_sessoes(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
            
        sessoes = self.sessao_controller.listar()
        
        for s in sessoes:
            try:
                if s.status == StatusSessao.DISPONIVEL and s.filme.status != StatusFilme.FORA_DE_CARTAZ: 
                    if isinstance(s.data_hora, str):
                        dt_formatada = s.data_hora
                    else:
                        dt_formatada = s.data_hora.strftime("%d/%m/%Y %H:%M")
                        
                    self.tree.insert("", "end", values=(
                        s.id_sessao, 
                        s.filme.titulo, 
                        dt_formatada, 
                        f"Sala {s.sala.numero} (Cap: {s.sala.capacidade})", 
                        f"{s.preco_base:.2f}"
                    ))
            except Exception as e:
                print(f"Sessão ignorada devido a erro de formatação: {e}")

    def selecionar_sessao(self, event):
        selecao = self.tree.selection()
        if selecao:
            item = self.tree.item(selecao[0], "values")
            self.var_id_sessao.set(item[0])
            self.var_info_sessao.set(f"Sessão Selecionada: {item[1]} | {item[2]} | {item[3]}")

    def limpar_campos(self):
        self.var_id_sessao.set("")
        self.var_info_sessao.set("Nenhuma sessão selecionada")
        self.var_assento.set("")
        self.var_tipo_ingresso.set("")
        self.var_metodo_pagamento.set("")
        self.tree.selection_remove(self.tree.selection())

    def processar_compra(self):
        id_sessao = self.var_id_sessao.get()
        assento = self.var_assento.get()
        tipo_ingresso = self.var_tipo_ingresso.get()
        metodo_pagamento = self.var_metodo_pagamento.get()

        if not id_sessao:
            messagebox.showwarning("Atenção", "Selecione uma sessão na lista acima.")
            return
        if not assento or not assento.isdigit():
            messagebox.showwarning("Atenção", "Informe um número de assento válido.")
            return
        if not tipo_ingresso:
            messagebox.showwarning("Atenção", "Selecione o tipo de ingresso.")
            return
        if not metodo_pagamento:
            messagebox.showwarning("Atenção", "Selecione o método de pagamento.")
            return

        sucesso_ing, retorno_ing = self.ingresso_controller.gerar_ingresso(tipo_ingresso, int(id_sessao), assento)
        
        if not sucesso_ing:
            messagebox.showerror("Erro na emissão", retorno_ing)
            return

        ingresso = retorno_ing

        sucesso_venda, msg_venda = self.venda_controller.processar_venda(ingresso, metodo_pagamento)

        if sucesso_venda:
            resumo = (
                f"{msg_venda}\n\n"
                f"--- RESUMO DA COMPRA ---\n"
                f"Filme: {ingresso.sessao.filme.titulo}\n"
                f"Assento: {ingresso.assento}\n"
                f"Tipo: {ingresso.get_tipo()}\n"
                f"Total Pago: R$ {ingresso.calcular_preco():.2f}\n"
                f"------------------------\n"
                f"Bom filme!"
            )
            messagebox.showinfo("Compra Confirmada", resumo)
            self.limpar_campos()
        else:
            self.ingresso_controller.dao.remover(ingresso.id_ingresso)
            messagebox.showerror("Erro no Pagamento", msg_venda)