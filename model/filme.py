from model.enums import StatusFilme, ClassificacaoIndicativa

class Filme:
    def __init__(self, titulo: str, duracao: int, classificacao: ClassificacaoIndicativa, status: StatusFilme, id_filme: int = None):
        self._id_filme = id_filme
        self.titulo = titulo
        self.duracao = duracao
        self.classificacao = classificacao
        self.status = status

    @property
    def id_filme(self) -> int:
        return self._id_filme

    @id_filme.setter
    def id_filme(self, valor: int):
        self._id_filme = valor

    @property
    def titulo(self) -> str:
        return self._titulo

    @titulo.setter
    def titulo(self, valor: str):
        if not valor or not valor.strip():
            raise ValueError("O título do filme não pode ser vazio.")
        self._titulo = valor.strip()

    @property
    def duracao(self) -> int:
        return self._duracao

    @duracao.setter
    def duracao(self, valor: int):
        if valor <= 0:
            raise ValueError("A duração do filme deve ser maior que zero.")
        self._duracao = valor

    @property
    def classificacao(self) -> ClassificacaoIndicativa:
        return self._classificacao

    @classificacao.setter
    def classificacao(self, valor: ClassificacaoIndicativa):
        if not isinstance(valor, ClassificacaoIndicativa):
            raise TypeError("Classificação inválida.")
        self._classificacao = valor

    @property
    def status(self) -> StatusFilme:
        return self._status

    @status.setter
    def status(self, valor: StatusFilme):
        if not isinstance(valor, StatusFilme):
            raise TypeError("Status inválido.")
        self._status = valor