from datetime import datetime
from model.filme import Filme
from model.sala import Sala
from model.enums import StatusSessao

class Sessao:
    def __init__(self, filme: Filme, sala: Sala, data_hora: datetime, preco_base: float, status: StatusSessao = StatusSessao.DISPONIVEL, id_sessao: int = None):
        self._id_sessao = id_sessao
        self.filme = filme
        self.sala = sala
        self.data_hora = data_hora
        self.preco_base = preco_base
        self.status = status

    @property
    def id_sessao(self) -> int:
        return self._id_sessao

    @id_sessao.setter
    def id_sessao(self, valor: int):
        self._id_sessao = valor

    @property
    def filme(self) -> Filme:
        return self._filme

    @filme.setter
    def filme(self, valor: Filme):
        if not isinstance(valor, Filme):
            raise TypeError("O objeto deve ser do tipo Filme.")
        self._filme = valor

    @property
    def sala(self) -> Sala:
        return self._sala

    @sala.setter
    def sala(self, valor: Sala):
        if not isinstance(valor, Sala):
            raise TypeError("O objeto deve ser do tipo Sala.")
        self._sala = valor

    @property
    def data_hora(self) -> datetime:
        return self._data_hora

    @data_hora.setter
    def data_hora(self, valor: datetime):
        if not isinstance(valor, datetime):
            raise TypeError("A data e hora devem ser do tipo datetime.")
        self._data_hora = valor

    @property
    def preco_base(self) -> float:
        return self._preco_base

    @preco_base.setter
    def preco_base(self, valor: float):
        if valor < 0:
            raise ValueError("O preço base não pode ser negativo.")
        self._preco_base = valor

    @property
    def status(self) -> StatusSessao:
        return self._status

    @status.setter
    def status(self, valor: StatusSessao):
        if not isinstance(valor, StatusSessao):
            raise TypeError("Status da sessão inválido.")
        self._status = valor