import streamlit as st
import pandas as pd
import graficos


st.set_page_config(layout="wide", page_title="Dashboard B3")


@st.cache_data
def carregar_dados():
    dados = pd.read_csv("dados/dados.csv")

    # Removendo as linhas onde a coluna "setor" é NaN (empresas sem setor)
    dados.dropna(subset=["setor"], inplace=True)

    # Removendo ativos que não tiveram cotação em 2024
    dados = dados[dados["dt_ultima_cot"] > "2024-01-01"]

    return dados


st.title("Dashboard B3")
st.header("Conhecendo as ações negociadas na Bolsa de Valores Brasileira - B3")
st.divider()

with st.spinner("Carregando dados, por favor aguarde..."):
    dados = carregar_dados()

st.sidebar.header("Filtros")

tickers = sorted(dados["papel"].unique())
filtro_ticker = st.sidebar.selectbox("Análise Individual", ["Não analisar individualmente"]+tickers)


if filtro_ticker == "Não analisar individualmente":
    setores = sorted(dados["setor"].unique())
    filtro_setor = st.sidebar.selectbox("Setor", ["Todos"]+setores)

    # Definindo mínimo e máximo de cada indicador
    min_cotacao = dados["cotacao"].min()
    max_cotacao = dados["cotacao"].max()

    min_pl = dados["pl"].min()
    max_pl = dados["pl"].max()

    min_pvp = dados["pvp"].min()
    max_pvp = dados["pvp"].max()
    
    min_psr = dados["psr"].min()
    max_psr = dados["psr"].max()

    min_dy = dados["dy"].min()
    max_dy = dados["dy"].max()

    min_pa = dados["pa"].min()
    max_pa = dados["pa"].max()

    min_pcg = dados["pcg"].min()
    max_pcg = dados["pcg"].max()

    min_pebit = dados["pebit"].min()
    max_pebit = dados["pebit"].max()
    
    min_pacl = dados["pacl"].min()
    max_pacl = dados["pacl"].max()
    
    min_evebit = dados["evebit"].min()
    max_evebit = dados["evebit"].max()
    
    min_evebitda = dados["evebitda"].min()
    max_evebitda = dados["evebitda"].max()
    
    min_mrgebit = dados["mrgebit"].min()
    max_mrgebit = dados["mrgebit"].max()
    
    min_mrgliq = dados["mrgliq"].min()
    max_mrgliq = dados["mrgliq"].max()
    
    min_roic = dados["roic"].min()
    max_roic = dados["roic"].max()

    min_roe = dados["roe"].min()
    max_roe = dados["roe"].max()
    
    min_liqc = dados["liqc"].min()
    max_liqc = dados["liqc"].max()
    
    min_liq2m = dados["liq2m"].min()
    max_liq2m = dados["liq2m"].max()
    
    min_patrliq = dados["patrliq"].min()
    max_patrliq = dados["patrliq"].max()
    
    min_divbpatr = dados["divbpatr"].min()
    max_divbpatr = dados["divbpatr"].max()
    
    min_c5y = dados["c5y"].min()
    max_c5y = dados["c5y"].max()
    
    min_valor_mercado = dados["valor_de_mercado"].min()
    max_valor_mercado = dados["valor_de_mercado"].max()

    min_valor = 0.00

    # Definindo intervalo de cada slider dos indicadores com 'session_state'
    if "slider_cotacao" not in st.session_state:
        st.session_state.slider_cotacao = (min_valor, max_cotacao)

    if "slider_pl" not in st.session_state:
        st.session_state.slider_pl = (min_valor, max_pl)

    if "slider_pvp" not in st.session_state:
        st.session_state.slider_pvp = (min_valor, max_pvp)

    if "slider_psr" not in st.session_state:
        st.session_state.slider_psr = (min_valor, max_psr)

    if "slider_dy" not in st.session_state:
        st.session_state.slider_dy = (min_valor, max_dy)

    if "slider_pa" not in st.session_state:
        st.session_state.slider_pa = (min_valor, max_pa)

    if "slider_pcg" not in st.session_state:
        st.session_state.slider_pcg = (min_valor, max_pcg)

    if "slider_pebit" not in st.session_state:
        st.session_state.slider_pebit = (min_valor, max_pebit)

    if "slider_pacl" not in st.session_state:
        st.session_state.slider_pacl = (min_valor, max_pacl)

    if "slider_evebit" not in st.session_state:
        st.session_state.slider_evebit = (min_valor, max_evebit)

    if "slider_evebitda" not in st.session_state:
        st.session_state.slider_evebitda = (min_valor, max_evebitda)

    if "slider_mrgebit" not in st.session_state:
        st.session_state.slider_mrgebit = (min_valor, max_mrgebit)

    if "slider_mrgliq" not in st.session_state:
        st.session_state.slider_mrgliq = (min_valor, max_mrgliq)

    if "slider_roic" not in st.session_state:
        st.session_state.slider_roic = (min_valor, max_roic)

    if "slider_roe" not in st.session_state:
        st.session_state.slider_roe = (min_valor, max_roe)

    if "slider_liqc" not in st.session_state:
        st.session_state.slider_liqc = (min_valor, max_liqc)

    if "slider_liq2m" not in st.session_state:
        st.session_state.slider_liq2m = (min_valor, max_liq2m)

    if "slider_patrliq" not in st.session_state:
        st.session_state.slider_patrliq = (min_valor, max_patrliq)

    if "slider_divbpatr" not in st.session_state:
        st.session_state.slider_divbpatr = (min_valor, max_divbpatr)

    if "slider_c5y" not in st.session_state:
        st.session_state.slider_c5y = (min_valor, max_c5y)

    if "slider_valor_mercado" not in st.session_state:
        st.session_state.slider_valor_mercado = (min_valor, max_valor_mercado)

    # Definindo funções para limpar cada slider
    def reset_slider_cotacao():
        st.session_state.slider_cotacao = (min_valor, max_cotacao)

    def reset_slider_pl():
        st.session_state.slider_pl = (min_valor, max_pl)

    def reset_slider_pvp():
        st.session_state.slider_pvp = (min_valor, max_pvp)

    def reset_slider_psr():
        st.session_state.slider_psr = (min_valor, max_psr)

    def reset_slider_dy():
        st.session_state.slider_dy = (min_valor, max_dy)

    def reset_slider_pa():
        st.session_state.slider_pa = (min_valor, max_pa)

    def reset_slider_pcg():
        st.session_state.slider_pcg = (min_valor, max_pcg)

    def reset_slider_pebit():
        st.session_state.slider_pebit = (min_valor, max_pebit)

    def reset_slider_pacl():
        st.session_state.slider_pacl = (min_valor, max_pacl)

    def reset_slider_evebit():
        st.session_state.slider_evebit = (min_valor, max_evebit)

    def reset_slider_evebitda():
        st.session_state.slider_evebitda = (min_valor, max_evebitda)

    def reset_slider_mrgebit():
        st.session_state.slider_mrgebit = (min_valor, max_mrgebit)

    def reset_slider_mrgliq():
        st.session_state.slider_mrgliq = (min_valor, max_mrgliq)

    def reset_slider_roic():
        st.session_state.slider_roic = (min_valor, max_roic)

    def reset_slider_roe():
        st.session_state.slider_roe = (min_valor, max_roe)

    def reset_slider_liqc():
        st.session_state.slider_liqc = (min_valor, max_liqc)

    def reset_slider_liq2m():
        st.session_state.slider_liq2m = (min_valor, max_liq2m)

    def reset_slider_patrliq():
        st.session_state.slider_patrliq = (min_valor, max_patrliq)

    def reset_slider_divbpatr():
        st.session_state.slider_divbpatr = (min_valor, max_divbpatr)

    def reset_slider_c5y():
        st.session_state.slider_c5y = (min_valor, max_c5y)

    def reset_slider_valor_mercado():
        st.session_state.slider_valor_mercado = (min_valor, max_valor_mercado)

    def reset_sliders():
        reset_slider_cotacao()
        reset_slider_pl()
        reset_slider_pvp()
        reset_slider_psr()
        reset_slider_dy()
        reset_slider_pa()
        reset_slider_pcg()
        reset_slider_pebit()
        reset_slider_pacl()
        reset_slider_evebit()
        reset_slider_evebitda()
        reset_slider_mrgebit()
        reset_slider_mrgliq()
        reset_slider_roic()
        reset_slider_roe()
        reset_slider_liqc()
        reset_slider_liq2m()
        reset_slider_patrliq()
        reset_slider_divbpatr()
        reset_slider_c5y()
        reset_slider_valor_mercado()

    # Botão para limpar sliders
    if st.sidebar.button("Limpar Filtros", use_container_width=True):
        reset_sliders()

    # Programando botão de análise básica com 'session state' (o botão aparecerá abaixo dos sliders)
    if "button" not in st.session_state:
        st.session_state.button = False

    def click_button():
        reset_sliders()
        st.session_state.button = not st.session_state.button


    # Definindo sliders
    cotacao_range = st.sidebar.slider("Cotação", min_value=min_cotacao, max_value=max_cotacao, step=0.01, key="slider_cotacao", value=st.session_state.slider_cotacao, help="Refere-se ao valor pelo qual a ação é negociada em determinado momento na Bolsa de Valores.")

    pl_range = st.sidebar.slider("Preço/Lucro (P/L)", min_value=min_pl, max_value=max_pl, step=0.01, key="slider_pl", value=st.session_state.slider_pl, help="É o número de anos necessários para reaver o capital aplicado na compra da ação através do recebimento do lucro gerado pela empresa, considerando que esses lucros permaneçam constantes.")
    
    pvp_range = st.sidebar.slider("Preço/Valor Patrimonial (P/VP)", disabled=st.session_state.button, min_value=min_pvp, max_value=max_pvp, step=0.01, key="slider_pvp", value=st.session_state.slider_pvp, help="Informa quanto o mercado está disposto a pagar sobre o patrimônio líquido da empresa.")
    
    psr_range = st.sidebar.slider("Preço/Sales Ratio (P/SR)", disabled=st.session_state.button, min_value=min_psr, max_value=max_psr, step=0.01, key="slider_psr", value=st.session_state.slider_psr, help="Indica o quanto os investidores pagam em relação às vendas da empresa.")
    
    dy_range = st.sidebar.slider("Dividend Yield (DY)", min_value=min_dy, max_value=max_dy, step=0.01, key="slider_dy", value=st.session_state.slider_dy, help="É o rendimento gerado para o dono da ação pelo pagamento de dividendos.")
    
    pa_range = st.sidebar.slider("Preço/Ativo (P/A)", disabled=st.session_state.button, min_value=min_pa, max_value=max_pa, step=0.01, key="slider_pa", value=st.session_state.slider_pa, help="Permite identificar se uma ação está subvalorizada ou sobrevalorizada em relação aos seus ativos.")
    
    pcg_range = st.sidebar.slider("Preço/Capital de Giro (P/CG)", disabled=st.session_state.button, min_value=min_pcg, max_value=max_pcg, step=0.01, key="slider_pcg", value=st.session_state.slider_pcg, help="Ajuda a avaliar o quanto os investidores estão dispostos a pagar pelo capital de giro da empresa.")

    pebit_range = st.sidebar.slider("Preço/EBIT (P/EBIT)", disabled=st.session_state.button, min_value=min_pebit, max_value=max_pebit, step=0.01, key="slider_pebit", value=st.session_state.slider_pebit, help="É utilizado para ponderar se a ação está cara ou barata em relação ao seu desempenho operacional.")
    
    pacl_range = st.sidebar.slider("Preço/Ativo Circulante Líquido (P/ACL)", disabled=st.session_state.button, min_value=min_pacl, max_value=max_pacl, step=0.01, key="slider_pacl", value=st.session_state.slider_pacl, help="Representa a solidez de uma instituição diante de suas obrigações e quanto o mercado paga por isso.")
    
    evebit_range = st.sidebar.slider("EV/EBIT", disabled=st.session_state.button, min_value=min_evebit, max_value=max_evebit, step=0.01, key="slider_evebit", value=st.session_state.slider_evebit, help="Auxilia na avaliação do valor da empresa em relação ao seu desempenho operacional, descontando os efeitos de juros e impostos.")
    
    evebitda_range = st.sidebar.slider("EV/EBITDA", disabled=st.session_state.button, min_value=min_evebitda, max_value=max_evebitda, step=0.01, key="slider_evebitda", value=st.session_state.slider_evebitda, help="Relaciona o valor da empresa com sua geração de caixa.")
    
    mrgebit_range = st.sidebar.slider("Margem EBIT", min_value=min_mrgebit, max_value=max_mrgebit, step=0.01, key="slider_mrgebit", value=st.session_state.slider_mrgebit, help="Indica a porcentagem de cada R$ 01,00 adquirido em vendas que sobrou após o pagamento das despesas decorrentes.")
    
    mrgliq_range = st.sidebar.slider("Margem Líquida", min_value=min_mrgliq, max_value=max_mrgliq, step=0.01, key="slider_mrgliq", value=st.session_state.slider_mrgliq, help="Revela a porcentagem de lucro em relação às receitas que a empresa apresentou no seu demonstrativo de resultados.")
    
    roic_range = st.sidebar.slider("Retorno sobre Capital Investido (ROIC)", min_value=min_roic, max_value=max_roic, step=0.01, key="slider_roic", value=st.session_state.slider_roic, help="Informa quanto de dinheiro a empresa consegue gerar em razão de todo o capital investido.")
    
    roe_range = st.sidebar.slider("Retorno sobre Patrimônio Líquido (ROE)", min_value=min_roe, max_value=max_roe, step=0.01, key="slider_roe", value=st.session_state.slider_roe, help="Refere-se à capacidade da empresa em agregar valor a ela mesma utilizando os seus próprios recursos.")
    
    liqc_range = st.sidebar.slider("Liquidez Corrente", min_value=min_liqc, max_value=max_liqc, step=0.01, key="slider_liqc", value=st.session_state.slider_liqc, help="Mede a capacidade da companhia de pagar todas as suas dívidas em um curto horizonte de tempo.")
    
    liq2m_range = st.sidebar.slider("Liquidez 2 Meses", disabled=st.session_state.button, min_value=min_liq2m, max_value=max_liq2m, step=0.01, key="slider_liq2m", value=st.session_state.slider_liq2m, help="Avalia a capacidade da empresa de atender suas obrigações de curto prazo (2 meses).")
    
    patrliq_range = st.sidebar.slider("Patrimônio Líquido", disabled=st.session_state.button, min_value=min_patrliq, max_value=max_patrliq, step=0.01, key="slider_patrliq", value=st.session_state.slider_patrliq, help="É tudo aquilo que a empresa possui e que pode ser transformado em dinheiro, seja a curto, médio ou longo prazo.")
    
    divbpatr_range = st.sidebar.slider("Dívida Bruta/Patrimônio Líquido", min_value=min_divbpatr, max_value=max_divbpatr, step=0.01, key="slider_divbpatr", value=st.session_state.slider_divbpatr, help="Faz um comparativo sobre as questões que envolvem a área de endividamento e alavancagem da empresa, isto é, a diferença entre os passivos e ativos que o negócio possui.")
    
    c5y_range = st.sidebar.slider("Crescimento 5 Anos", min_value=min_c5y, max_value=max_c5y, step=0.01, key="slider_c5y", value=st.session_state.slider_c5y, help="Crescimento da receita líquida nos últimos 5 anos")
    
    valor_mercado_range = st.sidebar.slider("Valor de Mercado", min_value=min_valor_mercado, max_value=max_valor_mercado, step=0.01, key="slider_valor_mercado", value=st.session_state.slider_valor_mercado, help="É o montante total que representa o valor da empresa no mercado de ações.")


    # Botão para simplificar a análise
    st.sidebar.button("Análise Simplificada", on_click=click_button, use_container_width=True)


    dados_filtrados = dados.copy()
    if filtro_setor != "Todos":
        dados_filtrados = dados[dados["setor"] == filtro_setor].reset_index(drop=True)

    dados_filtrados = dados_filtrados[(dados_filtrados["cotacao"] >= cotacao_range[0]) & (dados_filtrados["cotacao"] <= cotacao_range[1])].reset_index(drop=True)
    dados_filtrados = dados_filtrados[(dados_filtrados["pl"] >= pl_range[0]) & (dados_filtrados["pl"] <= pl_range[1])].reset_index(drop=True)
    dados_filtrados = dados_filtrados[(dados_filtrados["pvp"] >= pvp_range[0]) & (dados_filtrados["pvp"] <= pvp_range[1])].reset_index(drop=True)
    dados_filtrados = dados_filtrados[(dados_filtrados["psr"] >= psr_range[0]) & (dados_filtrados["psr"] <= psr_range[1])].reset_index(drop=True)
    dados_filtrados = dados_filtrados[(dados_filtrados["dy"] >= dy_range[0]) & (dados_filtrados["dy"] <= dy_range[1])].reset_index(drop=True)
    dados_filtrados = dados_filtrados[(dados_filtrados["pa"] >= pa_range[0]) & (dados_filtrados["pa"] <= pa_range[1])].reset_index(drop=True)
    dados_filtrados = dados_filtrados[(dados_filtrados["pcg"] >= pcg_range[0]) & (dados_filtrados["pcg"] <= pcg_range[1])].reset_index(drop=True)
    dados_filtrados = dados_filtrados[(dados_filtrados["pebit"] >= pebit_range[0]) & (dados_filtrados["pebit"] <= pebit_range[1])].reset_index(drop=True)
    dados_filtrados = dados_filtrados[(dados_filtrados["pacl"] >= pacl_range[0]) & (dados_filtrados["pacl"] <= pacl_range[1])].reset_index(drop=True)
    dados_filtrados = dados_filtrados[(dados_filtrados["evebit"] >= evebit_range[0]) & (dados_filtrados["evebit"] <= evebit_range[1])].reset_index(drop=True)
    dados_filtrados = dados_filtrados[(dados_filtrados["evebitda"] >= evebitda_range[0]) & (dados_filtrados["evebitda"] <= evebitda_range[1])].reset_index(drop=True)
    dados_filtrados = dados_filtrados[(dados_filtrados["mrgebit"] >= mrgebit_range[0]) & (dados_filtrados["mrgebit"] <= mrgebit_range[1])].reset_index(drop=True)
    dados_filtrados = dados_filtrados[(dados_filtrados["mrgliq"] >= mrgliq_range[0]) & (dados_filtrados["mrgliq"] <= mrgliq_range[1])].reset_index(drop=True)
    dados_filtrados = dados_filtrados[(dados_filtrados["roic"] >= roic_range[0]) & (dados_filtrados["roic"] <= roic_range[1])].reset_index(drop=True)
    dados_filtrados = dados_filtrados[(dados_filtrados["roe"] >= roe_range[0]) & (dados_filtrados["roe"] <= roe_range[1])].reset_index(drop=True)
    dados_filtrados = dados_filtrados[(dados_filtrados["liqc"] >= liqc_range[0]) & (dados_filtrados["liqc"] <= liqc_range[1])].reset_index(drop=True)
    dados_filtrados = dados_filtrados[(dados_filtrados["liq2m"] >= liq2m_range[0]) & (dados_filtrados["liq2m"] <= liq2m_range[1])].reset_index(drop=True)
    dados_filtrados = dados_filtrados[(dados_filtrados["patrliq"] >= patrliq_range[0]) & (dados_filtrados["patrliq"] <= patrliq_range[1])].reset_index(drop=True)
    dados_filtrados = dados_filtrados[(dados_filtrados["divbpatr"] >= divbpatr_range[0]) & (dados_filtrados["divbpatr"] <= divbpatr_range[1])].reset_index(drop=True)
    dados_filtrados = dados_filtrados[(dados_filtrados["c5y"] >= c5y_range[0]) & (dados_filtrados["c5y"] <= c5y_range[1])].reset_index(drop=True)
    dados_filtrados = dados_filtrados[(dados_filtrados["valor_de_mercado"] >= valor_mercado_range[0]) & (dados_filtrados["valor_de_mercado"] <= valor_mercado_range[1])].reset_index(drop=True)
else:
    dados_filtrados = dados[dados["papel"] == filtro_ticker].reset_index(drop=True)


tab1, tab2 = st.tabs(["Visão Geral do Mercado", "Análise de Grupos"])

with tab1:
    st.dataframe(dados_filtrados, use_container_width=True)
    st.text(f"Registros totais: {dados_filtrados.shape[0]}")
    if dados_filtrados.empty:
        st.warning("Nenhum registro encontrado. Tente alterar os filtros.")
    elif dados_filtrados.shape[0] > 1:
        st.divider()

        if filtro_setor == "Todos": graficos.grafico_empresas_setor(dados_filtrados)
        graficos.grafico_mapa_arvores(dados_filtrados)
        graficos.grafico_media_indicadores(dados_filtrados)
        graficos.grafico_calor(dados_filtrados)


with tab2:
    if dados_filtrados.empty:
        st.warning("Nenhum registro encontrado. Tente alterar os filtros.")
    else:
        graficos.grafico_agrupamento(dados_filtrados)