#tarefas.py
from datetime import datetime
import unicodedata


STATUS_PENDENTE = "pendente"
STATUS_CONCLUIDA = "concluida"

PRIORIDADES = ["baixa", "média", "alta"]


def remover_acentos(valor):
    valor = unicodedata.normalize("NFD", valor.strip().lower())

    return "".join(
        caractere
        for caractere in valor
        if unicodedata.category(caractere) != "Mn"
    )


def normalizar_prioridade(valor):
    if not isinstance(valor, str):
        return None

    valor_normalizado = remover_acentos(valor)

    for prioridade in PRIORIDADES:
        if remover_acentos(prioridade) == valor_normalizado:
            return prioridade

    return None


def validar_prioridade(valor):
    prioridade = (
        normalizar_prioridade(valor)
        if isinstance(valor, str)
        else None
    )

    if prioridade is None:
        raise ValueError(
            "Prioridade inválida. "
            f"Escolha entre: {', '.join(PRIORIDADES)}."
        )

    return prioridade


def validar_titulo(titulo):
    if not isinstance(titulo, str) or not titulo.strip():
        raise ValueError("O título não pode ser vazio.")

    return titulo.strip()


lista_tarefas = []

proximo_id = 1


def adicionar_tarefa(titulo, descricao, prioridade):
    global proximo_id

    titulo = validar_titulo(titulo)
    prioridade = validar_prioridade(prioridade)

    tarefa = {
        "id": proximo_id,
        "titulo": titulo,
        "descricao": descricao,
        "prioridade": prioridade,
        "status": STATUS_PENDENTE,
        "data_criacao": datetime.now().strftime("%d/%m/%Y"),
    }

    lista_tarefas.append(tarefa)
    proximo_id += 1

    return tarefa


def obter_tarefas(status=None):
    if status is None:
        return lista_tarefas.copy()

    return [
        tarefa
        for tarefa in lista_tarefas
        if tarefa["status"] == status
    ]


def busca_por_id(id_tarefa):
    for tarefa in lista_tarefas:
        if tarefa["id"] == id_tarefa:
            return tarefa

    return None


def editar_tarefa(
    id_tarefa,
    titulo=None,
    descricao=None,
    prioridade=None
):
    tarefa = busca_por_id(id_tarefa)

    if tarefa is None:
        return None

    # Valida os dados antes de modificar a tarefa
    if titulo is not None:
        titulo = validar_titulo(titulo)

    if prioridade is not None:
        prioridade = validar_prioridade(prioridade)

    # Aplica as alterações após as validações
    if titulo is not None:
        tarefa["titulo"] = titulo

    if descricao is not None:
        tarefa["descricao"] = descricao

    if prioridade is not None:
        tarefa["prioridade"] = prioridade

    return tarefa


def alterar_status_tarefa(id_tarefa, novo_status):
    tarefa = busca_por_id(id_tarefa)

    if tarefa is None:
        return None

    if novo_status not in (STATUS_PENDENTE, STATUS_CONCLUIDA):
        return None

    tarefa["status"] = novo_status

    return tarefa


def excluir_tarefa(id_tarefa):
    tarefa = busca_por_id(id_tarefa)

    if tarefa is None:
        return False

    lista_tarefas.remove(tarefa)

    return True


if __name__ == "__main__":

    # LIMPA A LISTA E REINICIA O CONTADOR

    lista_tarefas.clear()
    proximo_id = 1

    # CRIA UMA TAREFA PARA OS TESTES

    tarefa = adicionar_tarefa(
        "Tarefa de teste",
        "Descrição original",
        "alta"
    )

    id_teste = tarefa["id"]

    print("Tarefa de teste criada!")

    # TESTES DE BUSCA POR ID

    tarefa_encontrada = busca_por_id(id_teste)

    assert tarefa_encontrada is not None
    assert tarefa_encontrada["id"] == id_teste
    assert busca_por_id(99) is None

    print("Testes de busca por ID passaram!")

    # TESTES DE EDIÇÃO

    tarefa_editada = editar_tarefa(
        id_teste,
        titulo="Título editado",
        descricao="Descrição editada",
        prioridade="baixa"
    )

    assert tarefa_editada is not None
    assert tarefa_editada["titulo"] == "Título editado"
    assert tarefa_editada["descricao"] == "Descrição editada"
    assert tarefa_editada["prioridade"] == "baixa"

    # ID inexistente

    assert editar_tarefa(99, titulo="Teste") is None

    # Prioridade inválida

    try:
        editar_tarefa(id_teste, prioridade="urgente")
        assert False, "Deveria gerar ValueError."
    except ValueError:
        pass

    # Título vazio

    try:
        editar_tarefa(id_teste, titulo="   ")
        assert False, "Deveria gerar ValueError."
    except ValueError:
        pass

    # Confirma que não houve alteração parcial

    assert tarefa["titulo"] == "Título editado"
    assert tarefa["prioridade"] == "baixa"

    print("Testes de edição passaram!")

    # TESTES DE ALTERAÇÃO DE STATUS

    tarefa_alterada = alterar_status_tarefa(
        id_teste,
        STATUS_CONCLUIDA
    )

    assert tarefa_alterada is not None
    assert tarefa_alterada["status"] == STATUS_CONCLUIDA

    # ID inexistente

    assert alterar_status_tarefa(
        99,
        STATUS_CONCLUIDA
    ) is None

    # Status inválido

    assert alterar_status_tarefa(
        id_teste,
        "invalido"
    ) is None

    # Confirma que o status continua concluído

    assert tarefa["status"] == STATUS_CONCLUIDA

    # Reabre a tarefa

    alterar_status_tarefa(
        id_teste,
        STATUS_PENDENTE
    )

    assert tarefa["status"] == STATUS_PENDENTE

    print("Testes de alteração de status passaram!")

    # TESTES DE EXCLUSÃO

    tarefa_exclusao = adicionar_tarefa(
        "Tarefa para exclusão",
        "Teste de exclusão",
        "média"
    )

    id_exclusao = tarefa_exclusao["id"]

    assert busca_por_id(id_exclusao) is not None

    # Exclui a tarefa

    resultado = excluir_tarefa(id_exclusao)

    assert resultado is True
    assert busca_por_id(id_exclusao) is None

    # Tenta excluir novamente

    resultado = excluir_tarefa(id_exclusao)

    assert resultado is False

    print("Testes de exclusão passaram!")

    # TESTES DE VALIDAÇÃO DE PRIORIDADE

    try:
        adicionar_tarefa(
            "Tarefa inválida",
            "Teste",
            "urgente"
        )

        assert False, "Deveria gerar ValueError."

    except ValueError:
        pass

    print("Testes de prioridade passaram!")

    # TESTES DE VALIDAÇÃO DE TÍTULO

    try:
        adicionar_tarefa(
            "   ",
            "Teste",
            "alta"
        )

        assert False, "Deveria gerar ValueError."

    except ValueError:
        pass

    print("Testes de título passaram!")

    print("\nTodos os testes passaram com sucesso!")
