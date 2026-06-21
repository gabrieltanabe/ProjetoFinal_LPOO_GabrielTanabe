from datetime import datetime
from model.ingresso import IngressoFactory
from dao.ingresso_dao import IngressoDAO
from dao.sessao_dao import SessaoDAO

class IngressoController:
    def __init__(self):
        self.dao = IngressoDAO()
        self.sessao_dao = SessaoDAO()

    def gerar_ingresso(self, tipo: str, id_sessao: int, assento_str: str):
        try:
            sessao = self.sessao_dao.buscar_por_id(id_sessao)
            if not sessao:
                return False, "Sessão não encontrada."
            
            if sessao.data_hora <= datetime.now():
                return False, "Não é possível comprar ingressos para sessões que já iniciaram ou ocorreram no passado."

            assento = int(assento_str)
            if assento <= 0 or assento > sessao.sala.capacidade:
                return False, f"Assento inválido. A sala suporta até {sessao.sala.capacidade} assentos."

            ingressos_vendidos = self.dao.listar()
            for ing in ingressos_vendidos:
                if ing.sessao.id_sessao == id_sessao and ing.assento == assento:
                    return False, "Assento já ocupado nesta sessão."

            ingresso = IngressoFactory.criar_ingresso(tipo, sessao, assento)
            
            sucesso, msg = self.dao.salvar(ingresso)
            if sucesso:
                return True, ingresso
            return False, msg
            
        except ValueError as e:
            return False, str(e)
        except Exception as e:
            return False, f"Erro inesperado: {e}"

    def listar(self):
        return self.dao.listar()