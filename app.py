import streamlit as st
import pandas as pd
import graficos
from filters import FiltersManager
from config import columns_info

st.set_page_config(layout="wide", page_title="Dashboard B3")

## Funções
@st.cache_data
def carregar_dados():
    dados = pd.read_csv("dados/dados.csv")

    # Removendo as linhas onde a coluna "setor" é NaN (empresas sem setor)
    dados.dropna(subset=["setor"], inplace=True)

    # Removendo ativos que não tiveram cotação em 2024
    dados = dados[dados["dt_ultima_cot"] > "2024-01-01"]

    return dados

def reset_filters():
    if "filtro_setor" in st.session_state:
        st.session_state['filtro_setor'] = "Todos"

    filters_manager.reset_sliders()

####

st.title("Dashboard B3")
st.header("Conhecendo as ações negociadas na Bolsa de Valores Brasileira - B3")
st.divider()

with st.spinner("Carregando dados, por favor aguarde..."):
    dados = carregar_dados()


### Filtros

st.sidebar.header("Filtros")

setores = sorted(dados["setor"].unique())
filtro_setor = st.sidebar.selectbox("Setor", ["Todos"]+setores, key='filtro_setor')

# Cria todos os sliders
filters_manager = FiltersManager(dados, columns_info)
#slider_manager.create_sliders()


# Botão para limpar filtros
st.sidebar.button("Limpar Filtros", on_click=reset_filters, key='button_reset_filters',use_container_width=True)

####


dados_filtrados = dados.copy()
if filtro_setor != "Todos":
    dados_filtrados = dados[dados["setor"] == filtro_setor].reset_index(drop=True)

slider_values = filters_manager.get_slider_values()
for column_name, (min_val, max_val) in slider_values.items():
    dados_filtrados = dados_filtrados[
        (dados_filtrados[column_name] >= min_val) &
        (dados_filtrados[column_name] <= max_val)
        ].reset_index(drop=True)


tab1, tab2 = st.tabs(["Visão Geral do Mercado", "Análise de Grupos"])

with tab1:
    st.dataframe(dados_filtrados, use_container_width=True)
    st.text(f"Registros totais: {dados_filtrados.shape[0]}")
    if dados_filtrados.empty:
        st.warning("Nenhum registro encontrado. Tente alterar os filtros.")
    elif dados_filtrados.shape[0] > 1:
        st.divider()
        if len(dados_filtrados) > 1:
            if filtro_setor == "Todos":
                graficos.grafico_empresas_setor(dados_filtrados)

            graficos.grafico_mapa_arvores(dados_filtrados)
            graficos.grafico_media_indicadores(dados_filtrados)
            graficos.grafico_calor(dados_filtrados)


with tab2:
    if dados_filtrados.empty or len(dados_filtrados) < 2:
        msg = """
                É preciso ter mais de uma empresa para realizar a Análise de Grupos.

                Tente alterar os filtros.
              """
        st.warning(msg)

    else:
        graficos.grafico_agrupamento(dados_filtrados)
