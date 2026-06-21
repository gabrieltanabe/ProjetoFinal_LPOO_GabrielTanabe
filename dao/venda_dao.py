from dao.generic_dao import GenericDAO
from dao.db_config import DatabaseConfig
from dao.ingresso_dao import IngressoDAO
from model.venda import Venda

class VendaDAO(GenericDAO):
    def __init__(self):
        self.ingresso_dao = IngressoDAO()

    def salvar(self, venda: Venda):
        conexao = DatabaseConfig.get_connection()
        if not conexao: return False, "Falha na conexão."
        cursor = None
        try:
            cursor = conexao.cursor()
            query = """INSERT INTO tb_vendas (id_ingresso, metodo_pagamento, valor_total, data_venda) 
                       VALUES (%s, %s, %s, %s) RETURNING id_venda"""
            cursor.execute(query, (venda.ingresso.id_ingresso, venda.metodo_pagamento, venda.valor_total, venda.data_venda))
            venda.id_venda = cursor.fetchone()[0]
            conexao.commit()
            return True, "Venda registrada com sucesso."
        except Exception as e:
            conexao.rollback()
            return False, f"Erro ao registrar venda: {e}"
        finally:
            if cursor: cursor.close()
            if conexao: conexao.close()

    def atualizar(self, venda: Venda):
        pass

    def remover(self, id_venda: int):
        pass

    def listar(self):
        conexao = DatabaseConfig.get_connection()
        if not conexao: return []
        cursor = None
        vendas = []
        try:
            cursor = conexao.cursor()
            cursor.execute("SELECT id_venda, id_ingresso, metodo_pagamento, valor_total, data_venda FROM tb_vendas ORDER BY id_venda")
            for linha in cursor.fetchall():
                ingresso = self.ingresso_dao.buscar_por_id(linha[1])
                vendas.append(Venda(id_venda=linha[0], ingresso=ingresso, metodo_pagamento=linha[2], 
                                    valor_total=linha[3], data_venda=linha[4]))
            return vendas
        except Exception as e:
            print(f"Erro ao listar vendas: {e}")
            return []
        finally:
            if cursor: cursor.close()
            if conexao: conexao.close()

    def buscar_por_id(self, id_venda: int):
        conexao = DatabaseConfig.get_connection()
        if not conexao: return None
        cursor = None
        try:
            cursor = conexao.cursor()
            cursor.execute("SELECT id_venda, id_ingresso, metodo_pagamento, valor_total, data_venda FROM tb_vendas WHERE id_venda = %s", (id_venda,))
            linha = cursor.fetchone()
            if linha:
                ingresso = self.ingresso_dao.buscar_por_id(linha[1])
                return Venda(id_venda=linha[0], ingresso=ingresso, metodo_pagamento=linha[2], 
                             valor_total=linha[3], data_venda=linha[4])
            return None
        except Exception as e:
            print(f"Erro ao buscar venda: {e}")
            return None
        finally:
            if cursor: cursor.close()
            if conexao: conexao.close()