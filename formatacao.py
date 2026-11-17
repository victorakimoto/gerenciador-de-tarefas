#formatacao.py
from tarefas import STATUS_PENDENTE, STATUS_CONCLUIDA


def linha(tam=42):
    return "-" * tam


def traduzir_status(status):
    traducoes = {
        STATUS_PENDENTE: "Pendente",
        STATUS_CONCLUIDA: "Concluída",
    }

    return traducoes.get(status, status.capitalize())


def exibir_tarefa(tarefa):
    print(linha())
    print(f"ID: {tarefa['id']}")
    print(f"Título: {tarefa['titulo']}")
    print(f"Descrição: {tarefa['descricao'] or 'Não informada'}")
    print(f"Prioridade: {tarefa['prioridade'].capitalize()}")
    print(f"Status: {traduzir_status(tarefa['status'])}")
    print(f"Data de criação: {tarefa['data_criacao']}")
    print(linha())
