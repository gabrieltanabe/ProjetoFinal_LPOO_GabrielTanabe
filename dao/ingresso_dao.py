from dao.generic_dao import GenericDAO
from dao.db_config import DatabaseConfig
from dao.sessao_dao import SessaoDAO
from model.ingresso import IngressoFactory

class IngressoDAO(GenericDAO):
    def __init__(self):
        self.sessao_dao = SessaoDAO()

    def salvar(self, ingresso):
        conexao = DatabaseConfig.get_connection()
        if not conexao: return False, "Falha na conexão."
        cursor = None
        try:
            cursor = conexao.cursor()
            query = """INSERT INTO tb_ingressos (id_sessao, assento, tipo) 
                       VALUES (%s, %s, %s) RETURNING id_ingresso"""
            cursor.execute(query, (ingresso.sessao.id_sessao, ingresso.assento, ingresso.get_tipo()))
            ingresso.id_ingresso = cursor.fetchone()[0]
            conexao.commit()
            return True, "Ingresso salvo com sucesso."
        except Exception as e:
            conexao.rollback()
            return False, f"Erro ao salvar ingresso: {e}"
        finally:
            if cursor: cursor.close()
            if conexao: conexao.close()

    def atualizar(self, ingresso):
        pass

    def remover(self, id_ingresso: int):
        conexao = DatabaseConfig.get_connection()
        if not conexao: return False, "Falha na conexão."
        cursor = None
        try:
            cursor = conexao.cursor()
            cursor.execute("DELETE FROM tb_ingressos WHERE id_ingresso = %s", (id_ingresso,))
            conexao.commit()
            return True, "Ingresso removido com sucesso."
        except Exception as e:
            conexao.rollback()
            return False, f"Erro ao remover ingresso: {e}"
        finally:
            if cursor: cursor.close()
            if conexao: conexao.close()

    def listar(self):
        conexao = DatabaseConfig.get_connection()
        if not conexao: return []
        cursor = None
        ingressos = []
        try:
            cursor = conexao.cursor()
            cursor.execute("SELECT id_ingresso, id_sessao, assento, tipo FROM tb_ingressos")
            for linha in cursor.fetchall():
                sessao = self.sessao_dao.buscar_por_id(linha[1])
                ingresso = IngressoFactory.criar_ingresso(linha[3], sessao, linha[2])
                ingresso.id_ingresso = linha[0]
                ingressos.append(ingresso)
            return ingressos
        except Exception as e:
            print(f"Erro ao listar ingressos: {e}")
            return []
        finally:
            if cursor: cursor.close()
            if conexao: conexao.close()

    def buscar_por_id(self, id_ingresso: int):
        conexao = DatabaseConfig.get_connection()
        if not conexao: return None
        cursor = None
        try:
            cursor = conexao.cursor()
            cursor.execute("SELECT id_ingresso, id_sessao, assento, tipo FROM tb_ingressos WHERE id_ingresso = %s", (id_ingresso,))
            linha = cursor.fetchone()
            if linha:
                sessao = self.sessao_dao.buscar_por_id(linha[1])
                ingresso = IngressoFactory.criar_ingresso(linha[3], sessao, linha[2])
                ingresso.id_ingresso = linha[0]
                return ingresso
            return None
        except Exception as e:
            print(f"Erro ao buscar ingresso: {e}")
            return None
        finally:
            if cursor: cursor.close()
            if conexao: conexao.close()