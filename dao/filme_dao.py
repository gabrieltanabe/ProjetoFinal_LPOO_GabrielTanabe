from dao.generic_dao import GenericDAO
from dao.db_config import DatabaseConfig
from model.filme import Filme
from model.enums import StatusFilme, ClassificacaoIndicativa

class FilmeDAO(GenericDAO):
    def salvar(self, filme: Filme):
        conexao = DatabaseConfig.get_connection()
        if not conexao: return False, "Falha na conexão com o banco de dados."
        cursor = None
        try:
            cursor = conexao.cursor()
            query = """INSERT INTO tb_filmes (titulo, duracao, classificacao, status) 
                       VALUES (%s, %s, %s, %s) RETURNING id_filme"""
            cursor.execute(query, (filme.titulo, filme.duracao, filme.classificacao.value, filme.status.value))
            filme.id_filme = cursor.fetchone()[0]
            conexao.commit()
            return True, "Filme salvo com sucesso."
        except Exception as e:
            conexao.rollback()
            return False, f"Erro ao salvar filme: {e}"
        finally:
            if cursor: cursor.close()
            if conexao: conexao.close()

    def atualizar(self, filme: Filme):
        conexao = DatabaseConfig.get_connection()
        if not conexao: return False, "Falha na conexão."
        cursor = None
        try:
            cursor = conexao.cursor()
            query = """UPDATE tb_filmes SET titulo = %s, duracao = %s, classificacao = %s, status = %s 
                       WHERE id_filme = %s"""
            cursor.execute(query, (filme.titulo, filme.duracao, filme.classificacao.value, filme.status.value, filme.id_filme))
            conexao.commit()
            return True, "Filme atualizado com sucesso."
        except Exception as e:
            conexao.rollback()
            return False, f"Erro ao atualizar filme: {e}"
        finally:
            if cursor: cursor.close()
            if conexao: conexao.close()

    def remover(self, id_filme: int):
        conexao = DatabaseConfig.get_connection()
        if not conexao: return False, "Falha na conexão."
        cursor = None
        try:
            cursor = conexao.cursor()
            cursor.execute("DELETE FROM tb_filmes WHERE id_filme = %s", (id_filme,))
            conexao.commit()
            return True, "Filme removido com sucesso."
        except Exception as e:
            conexao.rollback()
            return False, f"Erro ao remover filme: {e}"
        finally:
            if cursor: cursor.close()
            if conexao: conexao.close()

    def listar(self):
        conexao = DatabaseConfig.get_connection()
        if not conexao: return []
        cursor = None
        filmes = []
        try:
            cursor = conexao.cursor()
            cursor.execute("SELECT id_filme, titulo, duracao, classificacao, status FROM tb_filmes ORDER BY id_filme")
            for linha in cursor.fetchall():
                filmes.append(Filme(id_filme=linha[0], titulo=linha[1], duracao=linha[2], 
                                    classificacao=ClassificacaoIndicativa(linha[3]), status=StatusFilme(linha[4])))
            return filmes
        except Exception as e:
            print(f"Erro ao listar filmes: {e}")
            return []
        finally:
            if cursor: cursor.close()
            if conexao: conexao.close()

    def buscar_por_id(self, id_filme: int):
        conexao = DatabaseConfig.get_connection()
        if not conexao: return None
        cursor = None
        try:
            cursor = conexao.cursor()
            cursor.execute("SELECT id_filme, titulo, duracao, classificacao, status FROM tb_filmes WHERE id_filme = %s", (id_filme,))
            linha = cursor.fetchone()
            if linha:
                return Filme(id_filme=linha[0], titulo=linha[1], duracao=linha[2], 
                             classificacao=ClassificacaoIndicativa(linha[3]), status=StatusFilme(linha[4]))
            return None
        except Exception as e:
            print(f"Erro ao buscar filme: {e}")
            return None
        finally:
            if cursor: cursor.close()
            if conexao: conexao.close()