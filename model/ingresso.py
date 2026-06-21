from abc import ABC, abstractmethod
from model.sessao import Sessao

class Ingresso(ABC):
    def __init__(self, sessao: Sessao, assento: int, id_ingresso: int = None):
        self._id_ingresso = id_ingresso
        self.sessao = sessao
        self.assento = assento

    @property
    def id_ingresso(self) -> int:
        return self._id_ingresso

    @id_ingresso.setter
    def id_ingresso(self, valor: int):
        self._id_ingresso = valor

    @property
    def sessao(self) -> Sessao:
        return self._sessao

    @sessao.setter
    def sessao(self, valor: Sessao):
        if not isinstance(valor, Sessao):
            raise TypeError("O objeto deve ser do tipo Sessao.")
        self._sessao = valor

    @property
    def assento(self) -> int:
        return self._assento

    @assento.setter
    def assento(self, valor: int):
        if valor <= 0:
            raise ValueError("O assento deve ser um número positivo.")
        self._assento = valor

    @abstractmethod
    def calcular_preco(self) -> float:
        pass

    @abstractmethod
    def get_tipo(self) -> str:
        pass


class IngressoComum(Ingresso):
    def calcular_preco(self) -> float:
        return float(self.sessao.preco_base)

    def get_tipo(self) -> str:
        return "Comum"


class IngressoMeia(Ingresso):
    def calcular_preco(self) -> float:
        return float(self.sessao.preco_base) * 0.5

    def get_tipo(self) -> str:
        return "Meia Entrada"


class IngressoVip(Ingresso):
    def calcular_preco(self) -> float:
        return float(self.sessao.preco_base) * 1.5

    def get_tipo(self) -> str:
        return "VIP"


class IngressoFactory:
    @staticmethod
    def criar_ingresso(tipo: str, sessao: Sessao, assento: int) -> Ingresso:
        tipo_formatado = tipo.upper().strip()
        
        if tipo_formatado == "COMUM":
            return IngressoComum(sessao, assento)
            
        elif tipo_formatado in ["MEIA", "MEIA ENTRADA", "MEIA-ENTRADA"]:
            return IngressoMeia(sessao, assento)
            
        elif tipo_formatado == "VIP":
            return IngressoVip(sessao, assento)
            
        else:
            raise ValueError(f"Tipo de ingresso inválido: '{tipo}'")