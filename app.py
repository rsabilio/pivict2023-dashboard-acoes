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
    dados = dados.drop(columns='dt_ultima_cot')  # Nao estamos usando 'dt_ultima_cot'
    return dados

def reset_filters():
    if "filtro_setor" in st.session_state:
        st.session_state['filtro_setor'] = "Todos"

    filters_manager.reset_sliders()

def get_default_cols():
    return ['papel', 'empresa', 'setor']
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

# Botão para limpar filtros
st.sidebar.button("Limpar Filtros", on_click=reset_filters, key='button_reset_filters',use_container_width=True)

####


dados_filtrados = dados.copy()

if filters_manager.get_analysis_type() == FiltersManager.ANALYSIS_TYPE_SIMPLIFICADA:
    cols_basic = [col for col, info in columns_info.items() if info.get('basic') == True]
    cols_basic = get_default_cols() + cols_basic
    dados_filtrados = dados_filtrados[cols_basic]


if filtro_setor != "Todos":
    dados_filtrados = dados_filtrados[dados["setor"] == filtro_setor].reset_index(drop=True)

slider_values = filters_manager.get_slider_values()
for column_name, (min_val, max_val) in slider_values.items():
    dados_filtrados = dados_filtrados[
        (dados_filtrados[column_name] >= min_val) &
        (dados_filtrados[column_name] <= max_val)
        ].reset_index(drop=True)


tab1, tab2 = st.tabs(["Visão Geral do Mercado", "Análise de Grupos"])

with tab1:
    df_tabela  = dados_filtrados.copy()
    nova_ordem = get_default_cols() + [col for col in df_tabela.columns if col not in get_default_cols()]
    df_tabela  = df_tabela[nova_ordem]

    # 1. Criando um dicionário de mapeamento entre indicadores e seus nomes completos
    columns_nome_completo = {col: info['full_name'] for col, info in columns_info.items()}
    columns_nome_completo['papel']   = 'Papel'
    columns_nome_completo['empresa'] = 'Empresa'
    columns_nome_completo['setor']   = 'Setor'

    df_tabela = df_tabela.rename(columns=columns_nome_completo)
    st.dataframe(df_tabela, use_container_width=True)
    st.text(f"Registros totais: {dados_filtrados.shape[0]}")

    if dados_filtrados.empty:
        st.warning("Nenhum registro encontrado. Tente alterar os filtros.")
    elif dados_filtrados.shape[0] > 1:

        if len(dados_filtrados) > 1:
            if filtro_setor == "Todos":
                st.markdown("<br><br>", unsafe_allow_html=True)
                st.subheader("Quantas empresas existem por setor?", divider='gray')
                graficos.grafico_empresas_setor(dados_filtrados)

            st.markdown("<br><br>", unsafe_allow_html=True)
            st.subheader("Qual é o valor de mercado das empresas?", divider='gray')
            graficos.grafico_mapa_arvores(dados_filtrados)

            st.markdown("<br><br>", unsafe_allow_html=True)
            st.subheader("A Média e Desvio Padrão dos Indicadores são:", divider='gray')
            graficos.grafico_media_indicadores(dados_filtrados, filters_manager.get_analysis_type())

            st.markdown("<br><br>", unsafe_allow_html=True)
            st.subheader(f"A correlação entre dados das empresas é:", divider='gray')
            graficos.grafico_calor(dados_filtrados)


with tab2:
    st.subheader("Agrupamento")

    if dados_filtrados.empty or len(dados_filtrados) < 2:
        msg = """
                É preciso ter mais de uma empresa para realizar a Análise de Grupos.

                Tente alterar os filtros.
              """
        st.warning(msg)

    else:
        # 1. Criando um dicionário de mapeamento entre indicadores e seus nomes completos
        indicador_para_nome_completo = {col: info['full_name'] for col, info in columns_info.items()}

        # Lista de indicadores básicos
        indicadores = [col for col, info in columns_info.items() if info.get('basic')]

        # Filtro de seleção de indicadores baseado no tipo de análise
        if filters_manager.get_analysis_type() == FiltersManager.ANALYSIS_TYPE_COMPLETA:
            indicadores = list(columns_info.keys())

        # 2. Exibindo nomes completos no `st.multiselect`
        nomes_completos = [indicador_para_nome_completo[indicador] for indicador in indicadores]
        indicadores_selecionados = st.multiselect("Selecione os Indicadores para Agrupamento",
                                                      options=nomes_completos,
                                                      default=nomes_completos)

        if len(indicadores_selecionados) > 0:
            # 3. Convertendo os nomes completos de volta para os indicadores originais
            indicadores_selecionados = [key for key, value in indicador_para_nome_completo.items() if
                                        value in indicadores_selecionados]

            dados_agrupamento = dados_filtrados[get_default_cols() + indicadores_selecionados]

            graficos.grafico_agrupamento(dados_agrupamento)
        else:
            st.warning("Você deve selecionar pelo menos 1 indicador para realizar o agrupamento")


#### Rodapé

 # Adicionar o rodapé no final da página
rodape = """
<style>
.rodape {
    position: fixed;
    left: 0;
    bottom: 0;
    width: 100%;
    background-color: #f1f1f1;
    color: #333;
    text-align: center;
    padding: 10px;
    font-size: 14px;
}
</style>
<div class="rodape">
    Projeto desenvolvido como Iniciação Científica Voluntária por discente 
    do curso técnico de Redes de Computadores integrado ao Ensino Médio do
    Instituto Federal de São Paulo (IFSP)
</div>
"""
st.markdown(rodape, unsafe_allow_html=True)