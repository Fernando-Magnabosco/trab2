# Pacote adaptador do banco de dados
import psycopg2

# Scrips desenvolvidos para o projeto
from db_config import db_config
from load_database import load_database
from log_undo import log_undo


def main():
    conn = None
    try:
        # conecta com banco de dados e cria cursor
        params = db_config()
        conn = psycopg2.connect(**params)
        cursor = conn.cursor()

        # carrega o banco com dados do arquivo
        load_database(cursor)

        # recuperar log UNDO
        log_undo(cursor)

        # fecha conexão com banco
        cursor.close()

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

    finally:
        if conn is not None:
            conn.close()


if __name__ == "__main__":
    main()
