from abc import ABC, abstractmethod

class GenericDAO(ABC):
    @abstractmethod
    def salvar(self, objeto):
        pass

    @abstractmethod
    def atualizar(self, objeto):
        pass

    @abstractmethod
    def remover(self, id_objeto: int):
        pass

    @abstractmethod
    def listar(self):
        pass

    @abstractmethod
    def buscar_por_id(self, id_objeto: int):
        pass