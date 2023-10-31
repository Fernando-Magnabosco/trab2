import json
import re

# Scripts para impressão
from print_out import print_transactions, print_json, print_update


def find_checkpoint(file):
    # Encontrando o checkpoint e salvando as transações que ainda não terminaram
    matches = re.findall("<CKPT \((.+?)\)>", file.read())
    # Retorna transações do último checkpoint, se não tiver retorna array vazio
    return matches[-1].split(",") if matches else []


def find_committed_transations(file):
    transactions = []

    # Retona pra início do arquivo
    file.seek(0)

    # Percorre arquivo de baixo pra cima
    for line in reversed(list(file)):
        # Só vai percorrer até encontrar um checkpoint
        if "CKPT" in line:
            break

        matches = re.search("<commit (.+?)>", line)
        # Se encontra commit, adiciona transição na lista
        if matches:
            transactions.append(matches.group(1))

    # Retorna transações em ordem de commit
    return transactions[::-1]


with open("metadados.json", "r") as metadados_file:
    metadados = json.load(metadados_file)

tabela = metadados["table"]
coluna_id = tabela["id"]
coluna_A = tabela["A"]
coluna_B = tabela["B"]
