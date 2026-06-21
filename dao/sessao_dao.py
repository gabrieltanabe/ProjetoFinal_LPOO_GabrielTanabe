from dao.generic_dao import GenericDAO
from dao.db_config import DatabaseConfig
from model.sessao import Sessao
from model.enums import StatusSessao
from dao.filme_dao import FilmeDAO
from dao.sala_dao import SalaDAO

class SessaoDAO(GenericDAO):
    def __init__(self):
        self.filme_dao = FilmeDAO()
        self.sala_dao = SalaDAO()

    def salvar(self, sessao: Sessao):
        conexao = DatabaseConfig.get_connection()
        if not conexao: return False, "Falha na conexão."
        cursor = None
        try:
            cursor = conexao.cursor()
            query = """INSERT INTO tb_sessoes (id_filme, id_sala, data_hora, preco_base, status) 
                       VALUES (%s, %s, %s, %s, %s) RETURNING id_sessao"""
            cursor.execute(query, (sessao.filme.id_filme, sessao.sala.id_sala, sessao.data_hora, sessao.preco_base, sessao.status.value))
            sessao.id_sessao = cursor.fetchone()[0]
            conexao.commit()
            return True, "Sessão salva com sucesso."
        except Exception as e:
            conexao.rollback()
            return False, f"Erro ao salvar sessão: {e}"
        finally:
            if cursor: cursor.close()
            if conexao: conexao.close()

    def atualizar(self, sessao: Sessao):
        conexao = DatabaseConfig.get_connection()
        if not conexao: return False, "Falha na conexão."
        cursor = None
        try:
            cursor = conexao.cursor()
            query = """UPDATE tb_sessoes SET id_filme = %s, id_sala = %s, data_hora = %s, preco_base = %s, status = %s 
                       WHERE id_sessao = %s"""
            cursor.execute(query, (sessao.filme.id_filme, sessao.sala.id_sala, sessao.data_hora, sessao.preco_base, sessao.status.value, sessao.id_sessao))
            conexao.commit()
            return True, "Sessão atualizada com sucesso."
        except Exception as e:
            conexao.rollback()
            return False, f"Erro ao atualizar sessão: {e}"
        finally:
            if cursor: cursor.close()
            if conexao: conexao.close()

    def remover(self, id_sessao: int):
        conexao = DatabaseConfig.get_connection()
        if not conexao: return False, "Falha na conexão."
        cursor = None
        try:
            cursor = conexao.cursor()
            cursor.execute("DELETE FROM tb_sessoes WHERE id_sessao = %s", (id_sessao,))
            conexao.commit()
            return True, "Sessão removida com sucesso."
        except Exception as e:
            conexao.rollback()
            return False, f"Erro ao remover sessão: {e}"
        finally:
            if cursor: cursor.close()
            if conexao: conexao.close()

    def listar(self):
        conexao = DatabaseConfig.get_connection()
        if not conexao: return []
        cursor = None
        sessoes = []
        try:
            cursor = conexao.cursor()
            cursor.execute("SELECT id_sessao, id_filme, id_sala, data_hora, preco_base, status FROM tb_sessoes ORDER BY id_sessao")
            for linha in cursor.fetchall():
                filme = self.filme_dao.buscar_por_id(linha[1])
                sala = self.sala_dao.buscar_por_id(linha[2])
                sessoes.append(Sessao(id_sessao=linha[0], filme=filme, sala=sala, data_hora=linha[3], 
                                      preco_base=linha[4], status=StatusSessao(linha[5])))
            return sessoes
        except Exception as e:
            print(f"Erro ao listar sessões: {e}")
            return []
        finally:
            if cursor: cursor.close()
            if conexao: conexao.close()

    def buscar_por_id(self, id_sessao: int):
        conexao = DatabaseConfig.get_connection()
        if not conexao: return None
        cursor = None
        try:
            cursor = conexao.cursor()
            cursor.execute("SELECT id_sessao, id_filme, id_sala, data_hora, preco_base, status FROM tb_sessoes WHERE id_sessao = %s", (id_sessao,))
            linha = cursor.fetchone()
            if linha:
                filme = self.filme_dao.buscar_por_id(linha[1])
                sala = self.sala_dao.buscar_por_id(linha[2])
                return Sessao(id_sessao=linha[0], filme=filme, sala=sala, data_hora=linha[3], 
                              preco_base=linha[4], status=StatusSessao(linha[5]))
            return None
        except Exception as e:
            print(f"Erro ao buscar sessão: {e}")
            return None
        finally:
            if cursor: cursor.close()
            if conexao: conexao.close()