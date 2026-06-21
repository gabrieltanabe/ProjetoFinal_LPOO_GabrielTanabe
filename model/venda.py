from datetime import datetime
from model.ingresso import Ingresso

class Venda:
    def __init__(self, ingresso: Ingresso, metodo_pagamento: str, valor_total: float, data_venda: datetime = None, id_venda: int = None):
        self._id_venda = id_venda
        self.ingresso = ingresso
        self.metodo_pagamento = metodo_pagamento
        self.valor_total = valor_total
        self.data_venda = data_venda if data_venda else datetime.now()

    @property
    def id_venda(self) -> int:
        return self._id_venda

    @id_venda.setter
    def id_venda(self, valor: int):
        self._id_venda = valor

    @property
    def ingresso(self) -> Ingresso:
        return self._ingresso

    @ingresso.setter
    def ingresso(self, valor: Ingresso):
        if not isinstance(valor, Ingresso):
            raise TypeError("O objeto deve ser do tipo Ingresso.")
        self._ingresso = valor

    @property
    def metodo_pagamento(self) -> str:
        return self._metodo_pagamento

    @metodo_pagamento.setter
    def metodo_pagamento(self, valor: str):
        if not valor or not valor.strip():
            raise ValueError("O método de pagamento não pode ser vazio.")
        self._metodo_pagamento = valor.strip()

    @property
    def valor_total(self) -> float:
        return self._valor_total

    @valor_total.setter
    def valor_total(self, valor: float):
        if valor < 0:
            raise ValueError("O valor total não pode ser negativo.")
        self._valor_total = valor

    @property
    def data_venda(self) -> datetime:
        return self._data_venda

    @data_venda.setter
    def data_venda(self, valor: datetime):
        if not isinstance(valor, datetime):
            raise TypeError("A data de venda deve ser um objeto datetime.")
        self._data_venda = valor