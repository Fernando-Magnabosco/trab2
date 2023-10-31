import json
import re

# Scripts para impressão
from print_out import print_transactions, print_json, print_update


def find_transations_after_checkpoint(file):
    transactions = []

    # Retona pra início do arquivo
    file.seek(0)

    # Percorre arquivo de baixo pra cima
    for line in reversed(list(file)):
        # Só vai percorrer até encontrar um checkpoint
        if "END CKPT" in line:
            break

        matches = re.search("<start (.+?)>", line)
        # Se encontra commit, adiciona transição na lista
        if matches:
            transactions.append(matches.group(1))

    # Retorna transações em ordem de commit
    return transactions[::-1]


def find_changes_after_checkpoint(file):
    transactions = []

    file.seek(0)

    for line in reversed(list(file)):
        if "END CKPT" in line:
            break

        matches = re.search("<(.+?),(.+?), (.+?),(.+?)>", line)
        if matches:
            transactions.append(matches.groups())

    return transactions[::-1]


def undo_changes(file, cursor, changes_after_first_checkpoint):
    for change in changes_after_first_checkpoint:
        cursor.execute(
            "UPDATE data SET "
            + change[2]
            + " = "
            + change[3]
            + " WHERE id = "
            + change[1]
        )
        print_update(change[1], change[2], change[3])


with open("metadados.json", "r") as metadados_file:
    metadados = json.load(metadados_file)


def log_undo(cursor):
    # Abre arquivo da entradaLog apenas para leitura
    file = open("log.txt", "r")

    try:
        transactions_after_checkpoint = find_transations_after_checkpoint(file)
        changes_after_checkpoint = find_changes_after_checkpoint(file)

        print_transactions(transactions_after_checkpoint)
        undo_changes(file, cursor, changes_after_checkpoint)

        print_json(cursor)

    finally:
        # Fecha arquivo
        file.close()
