#menu.py
from tarefas import (
    adicionar_tarefa,
    obter_tarefas,
    normalizar_prioridade,
    PRIORIDADES,
    STATUS_PENDENTE,
    STATUS_CONCLUIDA,
    busca_por_id,
    editar_tarefa,
    alterar_status_tarefa,
    excluir_tarefa
)

from formatacao import linha, exibir_tarefa


TITULO_PROGRAMA = "GERENCIADOR DE TAREFAS"


def cabecalho():
    print(linha())
    print(TITULO_PROGRAMA)
    print(linha())


def menu():
    print("1 - Ver Tarefas pendentes")
    print("2 - Ver Tarefas concluídas")
    print("3 - Gerenciar Tarefas")
    print("4 - Listar todas as tarefas (pendentes/concluídas)")
    print("0 - Sair")


def gerenciar_tarefas():
    print("1 - Criar Tarefas")
    print("2 - Editar Tarefas")
    print("3 - Concluir Tarefas")
    print("4 - Excluir Tarefas")
    print("5 - Reabrir Tarefa")
    print("0 - Retornar ao Menu")


def ler_opcao(mensagem):
    while True:
        try:
            return int(input(mensagem))
        except ValueError:
            print("Digite um número inteiro válido, por favor.")


def ler_texto(mensagem):
    while True:
        texto = input(mensagem).strip()

        if texto:
            return texto

        print("Este campo é obrigatório. Tente novamente.")


def ler_prioridade():
    prioridades_texto = ", ".join(PRIORIDADES)

    while True:
        prioridade = input(
            f"Digite a prioridade ({prioridades_texto}): "
        )

        prioridade = normalizar_prioridade(prioridade)

        if prioridade is not None:
            return prioridade

        print("Prioridade inválida.")
        print(f"Escolha entre: {prioridades_texto}.")


def ler_texto_opcional(mensagem):
    texto = input(mensagem).strip()
    return texto if texto else None


def ler_prioridade_opcional(prioridade_atual):
    prioridades_texto = ", ".join(PRIORIDADES)

    while True:
        entrada = input(
            f"Prioridade atual: {prioridade_atual.capitalize()}. "
            f"Nova prioridade ({prioridades_texto}; "
            "Enter para manter): "
        ).strip()

        if not entrada:
            return None

        prioridade = normalizar_prioridade(entrada)

        if prioridade is not None:
            return prioridade

        print("Prioridade inválida.")
        print(f"Escolha entre: {prioridades_texto}.")


def ler_descricao():
    return input("Digite a descrição (opcional): ").strip()


def criar_tarefa_menu():
    print("\n--- Criar Tarefa ---")

    titulo = ler_texto("Digite o título: ")
    descricao = ler_descricao()
    prioridade = ler_prioridade()

    tarefa = adicionar_tarefa(
        titulo,
        descricao,
        prioridade
    )

    print("\nTarefa criada com sucesso!")
    exibir_tarefa(tarefa)


def ver_tarefas(titulo, status=None):
    print()
    print(linha())
    print(titulo)
    print(linha())

    tarefas = obter_tarefas(status)

    if not tarefas:
        print("Nenhuma tarefa encontrada.")
        return

    for tarefa in tarefas:
        exibir_tarefa(tarefa)


def ver_todas():
    ver_tarefas("Todas as Tarefas")


def ver_pendentes():
    ver_tarefas("Tarefas Pendentes", STATUS_PENDENTE)


def ver_concluidas():
    ver_tarefas("Tarefas Concluídas", STATUS_CONCLUIDA)


def selecionar_tarefa_menu(
    titulo,
    mensagem_vazia,
    mensagem_id,
    status=None
):
    tarefas = obter_tarefas(status)

    if not tarefas:
        print(mensagem_vazia)
        return None

    ver_tarefas(titulo, status)

    id_tarefa = ler_opcao(mensagem_id)

    tarefa = busca_por_id(id_tarefa)

    if tarefa is None:
        print("Não há tarefa com esse ID.")
        return None

    if status is not None and tarefa["status"] != status:
        print("Essa tarefa não pertence a essa categoria.")
        return None

    return tarefa


def editar_tarefa_menu():
    print("\n--- Editar Tarefa ---")

    tarefa = selecionar_tarefa_menu(
        "Todas as tarefas",
        "Não há tarefas cadastradas para editar.",
        "Digite o ID da tarefa que deseja editar: "
    )

    if tarefa is None:
        return

    print("\nDeixe o campo vazio para manter o valor atual.")

    titulo = ler_texto_opcional(
        f"Título atual: {tarefa['titulo']}. Novo título: "
    )

    descricao = ler_texto_opcional(
        f"Descrição atual: {tarefa['descricao'] or 'Não informada'}. "
        "Nova descrição: "
    )

    prioridade = ler_prioridade_opcional(
        tarefa["prioridade"]
    )

    if (
        titulo is None
        and descricao is None
        and prioridade is None
    ):
        print("Nenhuma alteração foi realizada.")
        return

    try:
        tarefa_editada = editar_tarefa(
            tarefa["id"],
            titulo=titulo,
            descricao=descricao,
            prioridade=prioridade
        )

    except ValueError as erro:
        print(f"\nErro ao editar tarefa: {erro}")
        return

    if tarefa_editada is None:
        print("Não foi possível editar essa tarefa.")
        return

    print("\nTarefa editada com sucesso!")
    exibir_tarefa(tarefa_editada)


def concluir_tarefa_menu():
    print("\n--- Concluir Tarefa ---")

    tarefa = selecionar_tarefa_menu(
        "Tarefas pendentes",
        "Não há tarefas pendentes.",
        "Digite o ID da tarefa que deseja concluir: ",
        STATUS_PENDENTE
    )

    if tarefa is None:
        return

    tarefa = alterar_status_tarefa(
        tarefa["id"],
        STATUS_CONCLUIDA
    )

    if tarefa is None:
        print("Não foi possível concluir essa tarefa.")
        return

    print("\nTarefa concluída com sucesso!")
    exibir_tarefa(tarefa)


def reabrir_tarefa_menu():
    print("\n--- Reabrir Tarefa ---")

    tarefa = selecionar_tarefa_menu(
        "Tarefas concluídas",
        "Não há tarefas concluídas para reabrir.",
        "Digite o ID da tarefa que deseja reabrir: ",
        STATUS_CONCLUIDA
    )

    if tarefa is None:
        return

    tarefa = alterar_status_tarefa(
        tarefa["id"],
        STATUS_PENDENTE
    )

    if tarefa is None:
        print("Não foi possível reabrir essa tarefa.")
        return

    print("\nTarefa reaberta com sucesso.")
    exibir_tarefa(tarefa)


def ler_confirmacao(mensagem):
    while True:
        resposta = input(
            f"{mensagem} (s/n): "
        ).strip().lower()

        if resposta in ("s", "sim"):
            return True

        if resposta in ("n", "nao", "não"):
            return False

        print(
            "Resposta inválida. Digite 's' para 'sim' "
            "ou 'n' para 'não'."
        )


def excluir_tarefa_menu():
    print("\n--- Excluir Tarefa ---")

    tarefa = selecionar_tarefa_menu(
        "Todas as tarefas",
        "Não há tarefas cadastradas para excluir.",
        "Digite o ID da tarefa que deseja excluir: "
    )

    if tarefa is None:
        return

    id_tarefa = tarefa["id"]

    exibir_tarefa(tarefa)

    confirmar = ler_confirmacao(
        "Tem certeza que deseja excluir essa tarefa?"
    )

    if not confirmar:
        print("Exclusão cancelada.")
        return

    sucesso = excluir_tarefa(id_tarefa)

    if sucesso:
        print("Tarefa excluída com sucesso.")
    else:
        print("Não foi possível excluir essa tarefa.")


def executar_submenu_tarefas():
    while True:
        gerenciar_tarefas()

        escolha = ler_opcao(
            "Escolha uma opção de gerenciamento: "
        )

        if escolha == 1:
            criar_tarefa_menu()

        elif escolha == 2:
            editar_tarefa_menu()

        elif escolha == 3:
            concluir_tarefa_menu()

        elif escolha == 4:
            excluir_tarefa_menu()

        elif escolha == 5:
            reabrir_tarefa_menu()

        elif escolha == 0:
            return

        else:
            print("Opção inválida. Escolha de 0 a 5.")


def executar_menu():
    while True:
        cabecalho()
        menu()

        opcao = ler_opcao("Escolha uma opção: ")

        if opcao == 1:
            ver_pendentes()

        elif opcao == 2:
            ver_concluidas()

        elif opcao == 3:
            executar_submenu_tarefas()

        elif opcao == 4:
            ver_todas()

        elif opcao == 0:
            print("Saindo...")
            break

        else:
            print("Opção inválida. Escolha de 0 a 4.")
