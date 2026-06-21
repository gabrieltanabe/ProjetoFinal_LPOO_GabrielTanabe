import psycopg2

class DatabaseConfig:
    @staticmethod
    def get_connection():
        try:
            conexao = psycopg2.connect(
                host="localhost",
                database="lpoo_projeto_gabriel_tanabe",
                user="postgres",
                password="postgres"
            )
            return conexao
        except Exception as e:
            print(f"Erro ao conectar ao banco de dados: {e}")
            return None