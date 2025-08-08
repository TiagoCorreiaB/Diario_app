import streamlit as st
from random import randint

st.set_page_config(page_title="Tarefas APP")
page_icon = "📝"

def funcao_deletar_por_valor(lista, valor):
    if valor in lista:
        lista.remove(valor)

def marcar_concluida(tarefa_concluida):
    st.session_state.tarefas_concluidas.append(tarefa_concluida)
    funcao_deletar_por_valor(st.session_state.tarefas, tarefa_concluida)
    st.rerun()

def marcar_nao_concluida(tarefa_nao_concluida):
    st.session_state.tarefas.append(tarefa_nao_concluida)
    funcao_deletar_por_valor(st.session_state.tarefas_concluidas, tarefa_nao_concluida)
    st.rerun()

st.title("APP DE TAREFAS")

# Inicia as listas de tarefa e botão
if "tarefas" not in st.session_state:
    st.session_state.tarefas = []

if "tarefas_concluidas" not in st.session_state:
    st.session_state.tarefas_concluidas = []

if "sorteio" not in st.session_state:
    st.session_state.sorteio = None

# Entrada de Tarefas
nova_tarefa = st.text_input("Digite uma nova tarefa")
if st.button("Adicionar"):
    if nova_tarefa:
        st.session_state.tarefas.append(nova_tarefa)
        st.success(f"Tarefa '{nova_tarefa}' adicionada")
    else:
        st.warning("Adicione uma nova tarefa, por favor")

# Tarefas Concluídas

if st.session_state.tarefas_concluidas:
    st.divider()
    for i, tarefa in enumerate(st.session_state.tarefas_concluidas.copy()):
        col1, col2, col3 = st.columns([0.6, 0.2, 0.2])
        with col1:
            st.success(f"✔. {tarefa}")
        with col2:
            if st.button("Não concluída", key=f"nao_concluir_{i}_{tarefa}"):
                marcar_nao_concluida(tarefa)
        with col3:
            if st.button("Excluir", key=f"excluir_concluida_{i}_{tarefa}"):
                funcao_deletar_por_valor(st.session_state.tarefas_concluidas, tarefa)
                st.rerun()

# Tarefas Pendentes

st.divider()
st.subheader("Tarefas Pendentes:")

if st.session_state.tarefas:

    st.write("Está com duvida em qual tarefa fazer primeiro?")
    if st.button("Random 🎰"):
        st.session_state.sorteio = randint(0, len(st.session_state.tarefas)-1)
        st.rerun()
    st.divider()

    for i, tarefa in enumerate(st.session_state.tarefas.copy()):
        col1, col2, col3 = st.columns([0.6, 0.2, 0.2])

        with col1:
            prioridade = st.checkbox(f"Tarefa {i + 1}", key=f"prioridade_tarefa_{i}_{tarefa}")
            if not prioridade and st.session_state.sorteio == i:
                st.warning(tarefa)
            elif prioridade:
                st.error(tarefa)
            else:
                st.write(tarefa)

        with col2:
            if st.button("Concluir", key=f"concluir_{i}_{tarefa}"):
                if "sorteio" in st.session_state and st.session_state.sorteio == i:
                    del st.session_state.sorteio
                marcar_concluida(tarefa)

        with col3:
            if st.button("Excluir", key=f"excluir_pendente_{i}_{tarefa}"):
                funcao_deletar_por_valor(st.session_state.tarefas, tarefa)
                st.rerun()