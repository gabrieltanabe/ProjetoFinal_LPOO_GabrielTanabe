from dao.venda_dao import VendaDAO
from dao.filme_dao import FilmeDAO
from dao.sessao_dao import SessaoDAO

class AdminController:
    def __init__(self):
        self.venda_dao = VendaDAO()
        self.filme_dao = FilmeDAO()
        self.sessao_dao = SessaoDAO()

    def obter_resumo_sistema(self):
        try:
            vendas = self.venda_dao.listar()
            filmes = self.filme_dao.listar()
            sessoes = self.sessao_dao.listar()
            
            receita_total = sum(v.valor_total for v in vendas)
            qtd_ingressos = len(vendas)
            
            resumo = {
                "total_filmes": len(filmes),
                "total_sessoes": len(sessoes),
                "total_ingressos_vendidos": qtd_ingressos,
                "receita_total": receita_total
            }
            return True, resumo
        except Exception as e:
            return False, f"Erro ao gerar resumo: {e}"