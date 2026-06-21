from datetime import datetime
from model.venda import Venda
from model.pagamento import PagamentoPix, PagamentoCartao, PagamentoDinheiro
from dao.venda_dao import VendaDAO

class VendaController:
    def __init__(self):
        self.dao = VendaDAO()

    def processar_venda(self, ingresso, metodo_str: str):
        try:
            metodo_str = metodo_str.upper()
            if metodo_str == "PIX":
                estrategia_pagamento = PagamentoPix()
            elif metodo_str == "CARTÃO":
                estrategia_pagamento = PagamentoCartao()
            elif metodo_str == "DINHEIRO":
                estrategia_pagamento = PagamentoDinheiro()
            else:
                return False, "Método de pagamento inválido."

            valor_a_pagar = ingresso.calcular_preco()

            pagamento_aprovado = estrategia_pagamento.processar_pagamento(valor_a_pagar)

            if not pagamento_aprovado:
                return False, "Pagamento recusado pela operadora."

            venda = Venda(
                ingresso=ingresso,
                metodo_pagamento=estrategia_pagamento.get_nome(),
                valor_total=valor_a_pagar,
                data_venda=datetime.now()
            )

            return self.dao.salvar(venda)
        except Exception as e:
            return False, f"Erro ao processar venda: {e}"

    def listar(self):
        return self.dao.listar()