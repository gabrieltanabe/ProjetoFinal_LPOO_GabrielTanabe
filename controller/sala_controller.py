from model.sala import Sala
from dao.sala_dao import SalaDAO

class SalaController:
    def __init__(self):
        self.dao = SalaDAO()

    def salvar(self, numero_str: str, capacidade_str: str):
        try:
            numero = int(numero_str)
            capacidade = int(capacidade_str)
            
            sala = Sala(numero=numero, capacidade=capacidade)
            return self.dao.salvar(sala)
        except ValueError:
            return False, "Número e capacidade devem ser números inteiros."
        except Exception as e:
            return False, str(e)

    def atualizar(self, id_sala: int, numero_str: str, capacidade_str: str):
        try:
            numero = int(numero_str)
            capacidade = int(capacidade_str)
            
            sala = Sala(id_sala=id_sala, numero=numero, capacidade=capacidade)
            return self.dao.atualizar(sala)
        except ValueError:
            return False, "Número e capacidade devem ser números inteiros."
        except Exception as e:
            return False, str(e)

    def remover(self, id_sala: int):
        return self.dao.remover(id_sala)

    def listar(self):
        return self.dao.listar()

    def buscar_por_id(self, id_sala: int):
        return self.dao.buscar_por_id(id_sala)