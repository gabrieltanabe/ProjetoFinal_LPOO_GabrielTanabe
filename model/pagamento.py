from abc import ABC, abstractmethod

class MetodoPagamento(ABC):
    @abstractmethod
    def processar_pagamento(self, valor: float) -> bool:
        pass

    @abstractmethod
    def get_nome(self) -> str:
        pass

class PagamentoPix(MetodoPagamento):
    def processar_pagamento(self, valor: float) -> bool:
        if valor > 0:
            return True
        return False

    def get_nome(self) -> str:
        return "PIX"

class PagamentoCartao(MetodoPagamento):
    def processar_pagamento(self, valor: float) -> bool:
        if valor > 0:
            return True
        return False

    def get_nome(self) -> str:
        return "Cartão"

class PagamentoDinheiro(MetodoPagamento):
    def processar_pagamento(self, valor: float) -> bool:
        if valor >= 0:
            return True
        return False

    def get_nome(self) -> str:
        return "Dinheiro"