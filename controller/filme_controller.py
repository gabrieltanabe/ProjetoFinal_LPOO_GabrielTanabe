from model.filme import Filme
from model.enums import StatusFilme, ClassificacaoIndicativa
from dao.filme_dao import FilmeDAO

class FilmeController:
    def __init__(self):
        self.dao = FilmeDAO()

    def salvar(self, titulo: str, duracao_str: str, classificacao_str: str, status_str: str):
        try:
            duracao = int(duracao_str)
            if not titulo.strip():
                return False, "O título não pode ser vazio."
            
            classificacao = next(c for c in ClassificacaoIndicativa if c.value == classificacao_str)
            status = next(s for s in StatusFilme if s.value == status_str)
            
            filme = Filme(titulo=titulo, duracao=duracao, classificacao=classificacao, status=status)
            return self.dao.salvar(filme)
        except ValueError:
            return False, "Duração deve ser um número inteiro válido."
        except StopIteration:
            return False, "Classificação ou Status inválido."
        except Exception as e:
            return False, f"Erro inesperado: {e}"

    def atualizar(self, id_filme: int, titulo: str, duracao_str: str, classificacao_str: str, status_str: str):
        try:
            duracao = int(duracao_str)
            if not titulo.strip():
                return False, "O título não pode ser vazio."
            
            classificacao = next(c for c in ClassificacaoIndicativa if c.value == classificacao_str)
            status = next(s for s in StatusFilme if s.value == status_str)
            
            filme = Filme(id_filme=id_filme, titulo=titulo, duracao=duracao, classificacao=classificacao, status=status)
            return self.dao.atualizar(filme)
        except ValueError:
            return False, "Duração deve ser um número inteiro válido."
        except StopIteration:
            return False, "Classificação ou Status inválido."
        except Exception as e:
            return False, f"Erro inesperado: {e}"

    def remover(self, id_filme: int):
        return self.dao.remover(id_filme)

    def listar(self):
        return self.dao.listar()

    def buscar_por_id(self, id_filme: int):
        return self.dao.buscar_por_id(id_filme)