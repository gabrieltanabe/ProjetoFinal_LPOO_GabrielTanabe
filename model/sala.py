class Sala:
    def __init__(self, numero: int, capacidade: int, id_sala: int = None):
        self._id_sala = id_sala
        self.numero = numero
        self.capacidade = capacidade

    @property
    def id_sala(self) -> int:
        return self._id_sala

    @id_sala.setter
    def id_sala(self, valor: int):
        self._id_sala = valor

    @property
    def numero(self) -> int:
        return self._numero

    @numero.setter
    def numero(self, valor: int):
        if valor <= 0:
            raise ValueError("O número da sala deve ser maior que zero.")
        self._numero = valor

    @property
    def capacidade(self) -> int:
        return self._capacidade

    @capacidade.setter
    def capacidade(self, valor: int):
        if valor <= 0:
            raise ValueError("A capacidade da sala deve ser maior que zero.")
        self._capacidade = valor