from datetime import datetime
from model.sessao import Sessao
from model.enums import StatusSessao
from dao.sessao_dao import SessaoDAO
from dao.filme_dao import FilmeDAO
from dao.sala_dao import SalaDAO

class SessaoController:
    def __init__(self):
        self.dao = SessaoDAO()
        self.filme_dao = FilmeDAO()
        self.sala_dao = SalaDAO()

    def salvar(self, id_filme: int, id_sala: int, data_hora_str: str, preco_base_str: str, status_str: str):
        try:
            filme = self.filme_dao.buscar_por_id(id_filme)
            sala = self.sala_dao.buscar_por_id(id_sala)
            
            if not filme: return False, "Filme não encontrado."
            if not sala: return False, "Sala não encontrada."
            
            data_hora = datetime.strptime(data_hora_str, "%d/%m/%Y %H:%M")
            preco_base = float(preco_base_str.replace(',', '.'))
            status = next(s for s in StatusSessao if s.value == status_str)
            
            sessao = Sessao(filme=filme, sala=sala, data_hora=data_hora, preco_base=preco_base, status=status)
            return self.dao.salvar(sessao)
        except ValueError:
            return False, "Data/Hora (DD/MM/AAAA HH:MM) ou Preço inválidos."
        except StopIteration:
            return False, "Status inválido."
        except Exception as e:
            return False, str(e)

    def atualizar(self, id_sessao: int, id_filme: int, id_sala: int, data_hora_str: str, preco_base_str: str, status_str: str):
        try:
            filme = self.filme_dao.buscar_por_id(id_filme)
            sala = self.sala_dao.buscar_por_id(id_sala)
            
            if not filme: return False, "Filme não encontrado."
            if not sala: return False, "Sala não encontrada."
            
            data_hora = datetime.strptime(data_hora_str, "%d/%m/%Y %H:%M")
            preco_base = float(preco_base_str.replace(',', '.'))
            status = next(s for s in StatusSessao if s.value == status_str)
            
            sessao = Sessao(id_sessao=id_sessao, filme=filme, sala=sala, data_hora=data_hora, preco_base=preco_base, status=status)
            return self.dao.atualizar(sessao)
        except ValueError:
            return False, "Data/Hora (DD/MM/AAAA HH:MM) ou Preço inválidos."
        except StopIteration:
            return False, "Status inválido."
        except Exception as e:
            return False, str(e)

    def remover(self, id_sessao: int):
        return self.dao.remover(id_sessao)

    def listar(self):
        return self.dao.listar()

    def buscar_por_id(self, id_sessao: int):
        return self.dao.buscar_por_id(id_sessao)