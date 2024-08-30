import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.metrics import silhouette_score
from sklearn.preprocessing import RobustScaler
from config import columns_info
from filters import FiltersManager
from millify import millify

def score(df):
    m = 2
    pc_list = [f"PC{i}" for i in range(1, m + 1)]

    X = df.fillna(0)
    pca = PCA(n_components=m)
    pca_dados = pca.fit_transform(X)
    df_result = pd.DataFrame(data=pca_dados, columns=pc_list)

    return df_result


def grafico_dispersao(df):
    st.subheader("Gráfico de Dispersão")

    scores = score(df)

    fig, ax = plt.subplots()
    plt.xlabel("PC1")
    plt.ylabel("PC2")
    plt.title("Scores PC1 x PC2")
    plt.plot(scores["PC1"], scores["PC2"], "o")

    st.pyplot(fig)


def coeficiente_silhueta(df):
    kmeans_kwargs = {"init": "k-means++", "n_init": 20, "max_iter": 300, "random_state": 42}
    X = df

    silhouette_coefficients = []
    for k in range(2, min(len(df), 11)):
        kmeans = KMeans(n_clusters=k, **kmeans_kwargs).fit(X)
        score_kmeans = silhouette_score(X, kmeans.labels_)
        silhouette_coefficients.append(score_kmeans)

    return silhouette_coefficients


def grafico_agrupamento(df):
    def color_mapper(value):
        palette = ['#FF0000', '#FF7F00', '#FFFF00', '#7FFF00', '#00FF00',
                   '#00FF7F', '#00FFFF', '#007FFF', '#0000FF', '#7F00FF']

        if 0 <= value <= 9:
            return palette[value]
        else:
            return '#FFFFFF'

    def highlight_papel(row):
        color = color_mapper(row['Grupo'])
        return [f'background-color: {color}' if col.lower() == 'papel' else '' for col in row.index]

    # Verificação de número mínimo de registros
    if len(df) < 2:
        st.text("Não é possível realizar o agrupamento com menos de 2 registros.")
        return

    df_group = df.select_dtypes(include=['number']).copy()

    # Normalizando os dados, pois existem dados com valores muito altos como o valor de mercado
    scaler = RobustScaler()
    df_group = pd.DataFrame(scaler.fit_transform(df_group), columns=df_group.columns)

    silhuetas = coeficiente_silhueta(df_group)
    if len(silhuetas) == 0:
        melhor_agrupamento = 1
    else:
        melhor_agrupamento = silhuetas.index(max(silhuetas)) + 2
        st.text(f'O melhor agrupamento a ser feito é o de "{melhor_agrupamento}" grupos (Coeficiente de Silhueta = {max(silhuetas):.4f})')
    st.text("")

    # Limitar o número de clusters ao número de registros no dataframe
    max_k = min(len(df_group), 10)
    k = st.number_input("Insira o número de agrupamentos que deseja realizar:", step=1, min_value=1, max_value=max_k, value=min(max_k, melhor_agrupamento))
    groups = [0] * len(df_group)

    if k > 1:
        kmeans_kwargs = {"init": "k-means++", "n_init": 20, "max_iter": 300, "random_state": 42}
        kmeans = KMeans(n_clusters=k, **kmeans_kwargs).fit(df_group)
        groups = kmeans.labels_

    try:
        if len(df_group.columns) > 2:
            X = score(df_group)
            x = X['PC1']
            y = X['PC2']
            silhouette_kmeans = silhouette_score(X, groups)
        else:
            if len(df_group.columns) == 1:
                x = df_group.iloc[:, 0].tolist()
                y = [0] * len(df_group)
            else:
                x = df_group.iloc[:, 0].tolist()
                y = df_group.iloc[:, 1].tolist()
            silhouette_kmeans = silhouette_score(df_group, groups)

        colors = [color_mapper(val) for val in groups]
        fig = go.Figure(data=go.Scatter(x=x,
                                        y=y,
                                        mode='markers',
                                        marker=dict(
                                            color=colors,  # Cores dos clusters
                                            size=10,       # Tamanho dos marcadores
                                            symbol='circle'
                                        ),
                                        text=df['papel']))

        fig.update_xaxes(showticklabels=False)
        fig.update_yaxes(showticklabels=False)
        st.plotly_chart(fig)

        st.text(f"Coeficiente Silhueta: {round(silhouette_kmeans, 4)}")

    except ValueError as e:
        st.text(f"Não é possível calcular o coeficiente de silhueta com o número atual de clusters. Ajuste o número de agrupamentos entre 2 e {max_k}")

    # Aplica o estilo ao DataFrame
    styled_df  = df.copy()
    nova_ordem = ['papel', 'empresa', 'setor'] + [col for col in styled_df.columns if col not in ['papel', 'empresa', 'setor']]
    styled_df  = styled_df[nova_ordem]

    # 1. Criando um dicionário de mapeamento entre indicadores e seus nomes completos
    columns_nome_completo = {col: info['full_name'] for col, info in columns_info.items()}
    columns_nome_completo['papel']   = 'Papel'
    columns_nome_completo['empresa'] = 'Empresa'
    columns_nome_completo['setor']   = 'Setor'

    styled_df = styled_df.rename(columns=columns_nome_completo)

    styled_df['Grupo'] = groups
    styled_df          = styled_df.sort_values(by=['Grupo','Papel'])

    styled_df.reset_index(drop=True, inplace=True)
    styled_df.index = styled_df.index + 1

    styled_df = styled_df.style.apply(highlight_papel, axis=1)

    # Aplica formatação numérica a todas as colunas, exceto 'Papel', 'Empresa' e 'Setor'
    styled_df = styled_df.format(precision=2,
                                 subset=[col for col in styled_df.data.columns if styled_df.data[col].dtype != 'O'])

    st.dataframe(styled_df, use_container_width=True)
    st.text(f"Registros totais: {df.shape[0]}")


def grafico_empresas_setor(df):
    df_plot = df.copy()
    df_plot = df_plot.reset_index()
    df_plot = df_plot[["papel", "setor"]]

    # Criação de uma coluna com os 4 primeiros caracteres do ticker
    df_plot["ticker_prefix"] = df_plot["papel"].str[:4]
    df_plot = df_plot.drop_duplicates(subset=["ticker_prefix"])

    df_plot = df_plot[["ticker_prefix", "setor"]].groupby(by=["setor"]).count()
    df_plot = df_plot.reset_index()

    df_plot.columns = ["Setor", "Quantidade de Empresas"]

    maior_setor      = df_plot["Quantidade de Empresas"].idxmax()
    maior_setor_nome = df_plot.iloc[[maior_setor]]["Setor"].values[0]
    maior_setor_val  = df_plot.iloc[[maior_setor]]["Quantidade de Empresas"].values[0]

    title = f'"{maior_setor_nome}" é o maior setor, com {maior_setor_val} empresas.'
    fig = px.bar(df_plot, x="Quantidade de Empresas", y="Setor", title=title)
    fig.update_layout(
        barmode="stack",
        yaxis={"categoryorder": "total ascending"},
        height=800  # Ajuste o valor conforme necessário para aumentar a altura
    )

    st.plotly_chart(fig)


def grafico_mapa_arvores(df):
    df_plot = df.drop_duplicates(subset=["empresa"]).copy()
    df_plot = df_plot.reset_index()
    df_plot = df_plot[["papel", "empresa", "setor", "valor_de_mercado"]]

    # Criação de uma coluna com os 4 primeiros caracteres do ticker
    df_plot["ticker_prefix"] = df_plot["papel"].str[:4]

    # Consolidação do nome da empresa
    # Assumindo que o nome da empresa deve ser consolidado se os prefixos e setores forem iguais
    df_plot["empresa"] = df_plot.groupby(["ticker_prefix", "setor"])["empresa"].transform("first")

    # Agrupamento pelo prefixo do ticker e obtenção do valor máximo
    df_plot = df_plot.groupby(["ticker_prefix", "empresa", "setor"], as_index=False).agg({"valor_de_mercado": "max"}).reset_index()
    df_plot = df_plot.reset_index(drop=True)

    empresas = df_plot.sort_values(by=["valor_de_mercado"], ascending=False).head(3)
    empresas = ", ".join(empresas["ticker_prefix"])

    title = f"As empresas com maior valor de mercado (Marketcap) são: {empresas}"
    path  = [px.Constant("B3"), "setor", "ticker_prefix"]

    fig = px.treemap(
        df_plot,
        path=path,
        color="valor_de_mercado",
        values="valor_de_mercado",
        hover_data={"empresa": True, "valor_de_mercado": True},
        title=title,
        color_continuous_scale="RdBu"
    )

    fig.update_traces(
        root_color="lightgrey",
        hovertemplate="Empresa: %{customdata[0]}<br>Valor de Mercado: R$%{value:,.2f}<extra></extra>",
        customdata=df_plot[["empresa", "valor_de_mercado"]].values,
        textfont_size=14
    )

    # Atualização do título da legenda
    fig.update_coloraxes(colorbar_title="Valor de Mercado")
    fig.update_layout(margin=dict(t=50, l=25, r=25, b=25))

    st.plotly_chart(fig)


def grafico_media_indicadores(df, analysis_type):

    # Filtrando indicadores baseados no tipo de análise
    indicadores = [col for col, info in columns_info.items() if info.get('basic')]
    if analysis_type == FiltersManager.ANALYSIS_TYPE_COMPLETA:
        indicadores = list(columns_info.keys())

    # Agrupando indicadores por seção
    secoes = {}
    for col in indicadores:
        secao = columns_info.get(col, {}).get('section', 'Outras')
        if secao not in secoes:
            secoes[secao] = []
        secoes[secao].append(col)

    metrics = {}

    # Calculando métricas para cada indicador dentro de cada seção
    for secao, cols in secoes.items():
        metrics[secao] = {}
        for col in cols:
            media = df[col].mean()
            desvio = df[col].std()
            metrics[secao][col] = (media, desvio)

    # Número de colunas
    num_colunas = 3

    # Exibir as métricas usando st.metric
    for secao, indicadores in metrics.items():
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown(f"### _{secao}_")

        # Cria as colunas
        colunas = st.columns(num_colunas)

        # Divide os indicadores em linhas
        indicadores_lista = list(indicadores.items())
        num_indicadores = len(indicadores_lista)
        indicadores_por_coluna = -(-num_indicadores // num_colunas)  # Divisão para cima

        for i, col in enumerate(colunas):
            start_idx = i * indicadores_por_coluna
            end_idx = start_idx + indicadores_por_coluna
            indicadores_subset = indicadores_lista[start_idx:end_idx]

            with col:
                if indicadores_subset:
                    for indicador, (media, desvio) in indicadores_subset:
                        label = f"**{columns_info[indicador]['full_name']}**"
                        media = millify(media, precision=2)
                        desvio = millify(desvio, precision=2)
                        value = f"<div style='font-size: 2em;'>{media}</div><div style='font-size: 1em;'>± {desvio}</div>"
                        st.markdown(f"{label}<br>{value}", unsafe_allow_html=True)


def grafico_calor(df):

    # Verificação de presença de colunas numéricas no DataFrame:
    numeric_cols = df.select_dtypes(include=["number"]).columns
    if numeric_cols.empty:
        st.error("O DataFrame não contém colunas numéricas para calcular a correlação.")
        return None

    # Calculo da matriz de correlação
    corr_matrix = df.dropna()[numeric_cols].corr()
    # Criação da máscara para ocultar valores acima da diagonal principal
    mask = np.triu(np.ones_like(corr_matrix, dtype=bool), k=1)

    # Aplicação da máscara na matriz de correlação
    masked_corr_matrix = corr_matrix.copy()
    masked_corr_matrix[mask] = np.nan

    # Criação do heatmap com plotly.express
    fig = px.imshow(
        masked_corr_matrix,
        text_auto=".2f", # Exibe os valores nas células
        color_continuous_scale="RdBu", # Usa uma escala de cores nomeada
        width=1500, # Largura do gráfico
        height=1000, # Altura do gráfico
    )

    ticktexts = [columns_info[indicador]['full_name'] for indicador in df.columns.values.tolist() if indicador in columns_info]

    # Atualização do layout do gráfico
    fig.update_layout(
        xaxis_title = "",
        yaxis_title = "",
        xaxis=dict(tickmode="array", tickvals=list(range(len(corr_matrix.columns))), ticktext=ticktexts), # corr_matrix.columns
        yaxis=dict(tickmode="array", tickvals=list(range(len(corr_matrix.columns))), ticktext=ticktexts), # corr_matrix.columns
        coloraxis_colorbar_title = "Correlação"
    )

    # Atualização do hovertemplate para formatar valores com duas casas decimais
    fig.update_traces(hovertemplate="Correlação: %{z:.2f}<extra></extra>")
    
    st.plotly_chart(fig)