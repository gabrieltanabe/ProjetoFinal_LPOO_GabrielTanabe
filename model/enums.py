from enum import Enum

class StatusFilme(Enum):
    EM_CARTAZ = "Em Cartaz"
    EM_BREVE = "Em Breve"
    FORA_DE_CARTAZ = "Fora de Cartaz"

class ClassificacaoIndicativa(Enum):
    LIVRE = "Livre"
    DEZ_ANOS = "10 Anos"
    DOZE_ANOS = "12 Anos"
    QUATORZE_ANOS = "14 Anos"
    DEZESSEIS_ANOS = "16 Anos"
    DEZOITO_ANOS = "18 Anos"

class StatusSessao(Enum):
    DISPONIVEL = "Disponível"
    LOTADA = "Lotada"
    ENCERRADA = "Encerrada"
    CANCELADA = "Cancelada"