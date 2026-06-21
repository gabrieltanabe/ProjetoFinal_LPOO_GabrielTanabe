from dao.generic_dao import GenericDAO
from dao.db_config import DatabaseConfig
from model.sala import Sala

class SalaDAO(GenericDAO):
    def salvar(self, sala: Sala):
        conexao = DatabaseConfig.get_connection()
        if not conexao: return False, "Falha na conexão."
        cursor = None
        try:
            cursor = conexao.cursor()
            query = "INSERT INTO tb_salas (numero, capacidade) VALUES (%s, %s) RETURNING id_sala"
            cursor.execute(query, (sala.numero, sala.capacidade))
            sala.id_sala = cursor.fetchone()[0]
            conexao.commit()
            return True, "Sala salva com sucesso."
        except Exception as e:
            conexao.rollback()
            return False, f"Erro ao salvar sala: {e}"
        finally:
            if cursor: cursor.close()
            if conexao: conexao.close()

    def atualizar(self, sala: Sala):
        conexao = DatabaseConfig.get_connection()
        if not conexao: return False, "Falha na conexão."
        cursor = None
        try:
            cursor = conexao.cursor()
            query = "UPDATE tb_salas SET numero = %s, capacidade = %s WHERE id_sala = %s"
            cursor.execute(query, (sala.numero, sala.capacidade, sala.id_sala))
            conexao.commit()
            return True, "Sala atualizada com sucesso."
        except Exception as e:
            conexao.rollback()
            return False, f"Erro ao atualizar sala: {e}"
        finally:
            if cursor: cursor.close()
            if conexao: conexao.close()

    def remover(self, id_sala: int):
        conexao = DatabaseConfig.get_connection()
        if not conexao: return False, "Falha na conexão."
        cursor = None
        try:
            cursor = conexao.cursor()
            cursor.execute("DELETE FROM tb_salas WHERE id_sala = %s", (id_sala,))
            conexao.commit()
            return True, "Sala removida com sucesso."
        except Exception as e:
            conexao.rollback()
            return False, f"Erro ao remover sala: {e}"
        finally:
            if cursor: cursor.close()
            if conexao: conexao.close()

    def listar(self):
        conexao = DatabaseConfig.get_connection()
        if not conexao: return []
        cursor = None
        salas = []
        try:
            cursor = conexao.cursor()
            cursor.execute("SELECT id_sala, numero, capacidade FROM tb_salas ORDER BY id_sala")
            for linha in cursor.fetchall():
                salas.append(Sala(id_sala=linha[0], numero=linha[1], capacidade=linha[2]))
            return salas
        except Exception as e:
            print(f"Erro ao listar salas: {e}")
            return []
        finally:
            if cursor: cursor.close()
            if conexao: conexao.close()

    def buscar_por_id(self, id_sala: int):
        conexao = DatabaseConfig.get_connection()
        if not conexao: return None
        cursor = None
        try:
            cursor = conexao.cursor()
            cursor.execute("SELECT id_sala, numero, capacidade FROM tb_salas WHERE id_sala = %s", (id_sala,))
            linha = cursor.fetchone()
            if linha:
                return Sala(id_sala=linha[0], numero=linha[1], capacidade=linha[2])
            return None
        except Exception as e:
            print(f"Erro ao buscar sala: {e}")
            return None
        finally:
            if cursor: cursor.close()
            if conexao: conexao.close()