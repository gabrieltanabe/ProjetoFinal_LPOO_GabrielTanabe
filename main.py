import tkinter as tk
from tkinter import messagebox
from view.cliente_view import ClienteView
from view.filme_view import FilmeView
from view.sala_view import SalaView
from view.sessao_view import SessaoView
from view.venda_view import VendaView

class JanelaPrincipal(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Sistema de Bilhetagem de Cinema - LPOO")
        self.geometry("800x600")
        self.configure(bg="#2c3e50")

        self._criar_menu()
        self._criar_tela_boas_vindas()

    def _criar_menu(self):
        barra_menu = tk.Menu(self)
        self.config(menu=barra_menu)

        menu_cliente = tk.Menu(barra_menu, tearoff=0)
        menu_cliente.add_command(label="Comprar Ingresso", command=self.abrir_cliente)
        barra_menu.add_cascade(label="Cliente", menu=menu_cliente)

        menu_admin = tk.Menu(barra_menu, tearoff=0)
        menu_admin.add_command(label="Gerenciar Filmes", command=self.abrir_filmes)
        menu_admin.add_command(label="Gerenciar Salas", command=self.abrir_salas)
        menu_admin.add_command(label="Gerenciar Sessões", command=self.abrir_sessoes)
        menu_admin.add_separator()
        menu_admin.add_command(label="Consultar Vendas", command=self.abrir_vendas)
        barra_menu.add_cascade(label="Administração", menu=menu_admin)

        menu_ajuda = tk.Menu(barra_menu, tearoff=0)
        menu_ajuda.add_command(label="Sobre", command=self.abrir_sobre)
        barra_menu.add_cascade(label="Ajuda", menu=menu_ajuda)

        menu_sistema = tk.Menu(barra_menu, tearoff=0)
        menu_sistema.add_command(label="Sair", command=self.quit)
        barra_menu.add_cascade(label="Sistema", menu=menu_sistema)

    def _criar_tela_boas_vindas(self):
        frame_centro = tk.Frame(self, bg="#2c3e50")
        frame_centro.place(relx=0.5, rely=0.5, anchor="center")

        tk.Label(frame_centro, text="CineLPOO", font=("Helvetica", 36, "bold"), bg="#2c3e50", fg="white").pack(pady=10)
        tk.Label(frame_centro, text="Sistema de Bilhetagem", font=("Helvetica", 16), bg="#2c3e50", fg="#ecf0f1").pack(pady=5)
        tk.Label(frame_centro, text="Utilize o menu superior para navegar.", font=("Helvetica", 12, "italic"), bg="#2c3e50", fg="#bdc3c7").pack(pady=20)

    def abrir_cliente(self):
        ClienteView(self)

    def abrir_filmes(self):
        FilmeView(self)

    def abrir_salas(self):
        SalaView(self)

    def abrir_sessoes(self):
        SessaoView(self)

    def abrir_vendas(self):
        VendaView(self)

    def abrir_sobre(self):
        info = (
            "Sistema de Bilhetagem de Cinema\n\n"
            "Desenvolvido como Projeto Final da disciplina de LPOO.\n\n"
            "Arquitetura e Padrões:\n"
            "   Arquitetura MVC (Model-View-Controller)\n"
            "   Padrão de Persistência DAO\n"
            "   Design Pattern Factory Method (Ingressos)\n"
            "   Design Pattern Strategy (Pagamentos)\n"
            "   Interface Gráfica Tkinter\n"
            "   Banco de Dados PostgreSQL\n\n"
        )
        messagebox.showinfo("Sobre o Sistema", info)

if __name__ == "__main__":
    app = JanelaPrincipal()
    app.mainloop()