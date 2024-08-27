import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.metrics import silhouette_score


def score(df):
    X = df.drop(columns=["papel", "setor", "empresa", "dt_ultima_cot"]).fillna(0)

    m = 2
    pca = PCA(n_components=m)
    pca_dados = pca.fit_transform(X)
    pc_list = [f"PC{i}" for i in list(range(1, m+1))]

    return pd.DataFrame(data=pca_dados, columns=pc_list)


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
    X = score(df)
    kmeans_kwargs = {"init": "k-means++", "n_init": 20, "max_iter": 300, "random_state": 42}

    silhouette_coefficients = []
    if len(df) >= 10:
        for idx, k in enumerate(range(2, 11)):
            kmeans = KMeans(n_clusters=k, **kmeans_kwargs).fit(X)
            score_kmeans = silhouette_score(X, kmeans.labels_)
            silhouette_coefficients.append(score_kmeans)
    else:
        for idx, k in enumerate(range(2, len(df))):
            kmeans = KMeans(n_clusters=k, **kmeans_kwargs).fit(X)
            score_kmeans = silhouette_score(X, kmeans.labels_)
            silhouette_coefficients.append(score_kmeans)

    return silhouette_coefficients


def grafico_agrupamento(df):
    st.subheader("Agrupamento")
    if len(df) >= 10:
        k = st.number_input("Insira o número de agrupamentos que deseja realizar:", step=0, min_value=1, max_value=10)
    else:
        k = st.number_input("Insira o número de agrupamentos que deseja realizar:", step=0, min_value=1, max_value=len(df))
    
    X = score(df)

    if k == 1:
        fig = px.scatter(X, x="PC1", y="PC2", labels={"PC1":"", "PC2":""})

        fig.update_xaxes(showticklabels=False)
        fig.update_yaxes(showticklabels=False)

        st.plotly_chart(fig)
    else:
        kmeans_kwargs = {"init": "k-means++", "n_init": 20, "max_iter": 300, "random_state": 42}
        kmeans = KMeans(n_clusters=k, **kmeans_kwargs).fit(X)

        df_labels = df.copy()[["papel", "setor", "empresa"]]
        df_labels["cor"] = kmeans.labels_
        df_labels["score"] = X["PC2"]

        match k-1:
            case 1: df_labels["cor"] = df_labels["cor"].map({0: "roxo", 1: "vermelho"})
            case 2: df_labels["cor"] = df_labels["cor"].map({0: "roxo", 1: "verde_lima", 2: "vermelho"})
            case 3: df_labels["cor"] = df_labels["cor"].map({0: "roxo", 1: "ciano", 2: "ocre", 3: "vermelho"})
            case 4: df_labels["cor"] = df_labels["cor"].map({0: "roxo", 1: "azul", 2: "verde_lima", 3: "ocre", 4: "vermelho"})
            case 5: df_labels["cor"] = df_labels["cor"].map({0: "roxo", 1: "azul", 2: "verde_lima", 3: "amarelo", 4: "laranja", 5: "vermelho"})
            case 6: df_labels["cor"] = df_labels["cor"].map({0: "roxo", 1: "azul", 2: "ciano", 3: "verde_lima", 4: "ocre", 5: "laranja", 6: "vermelho"})
            case 7: df_labels["cor"] = df_labels["cor"].map({0: "roxo", 1: "azul", 2: "azul_claro", 3: "verde_lima", 4: "amarelo", 5: "ocre", 6: "laranja", 7: "vermelho"})
            case 8: df_labels["cor"] = df_labels["cor"].map({0: "roxo", 1: "azul", 2: "azul_claro", 3: "ciano", 4: "verde_lima", 5: "amarelo", 6: "ocre", 7: "laranja", 8: "vermelho"})
            case 9: df_labels["cor"] = df_labels["cor"].map({0: "roxo", 1: "azul", 2: "azul_claro", 3: "ciano", 4: "verde_lima", 5: "amarelo", 6: "ocre", 7: "laranja", 8: "laranja_escuro", 9: "vermelho"})

        fig = px.scatter(X, x="PC1", y="PC2", color=kmeans.labels_, labels={"PC1":"", "PC2":""}, color_continuous_scale=px.colors.sequential.Turbo)
        fig.update_xaxes(showticklabels=False)
        fig.update_yaxes(showticklabels=False)
        
        st.plotly_chart(fig)

        if len(df) != k:
            silhouette_kmeans = silhouette_score(X, kmeans.labels_)
            st.text(f"Coeficiente silhueta: {round(silhouette_kmeans, 4)}")
        else:
            st.text("Não é possível calcular o coeficiente silhueta de um DataFrame com o mesmo número de registros e agrupamentos.")

        silhuetas = coeficiente_silhueta(df)
        melhor_agrupamento = silhuetas.index(max(silhuetas))

        st.text(f'De acordo com o coeficiente silhueta, o melhor agrupamento a ser feito é o de "{melhor_agrupamento+2}" grupos')
        st.text("")

        st.dataframe(df_labels, use_container_width=True)


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

    maior_setor = df_plot["Quantidade de Empresas"].idxmax()
    maior_setor_nome = df_plot.iloc[[maior_setor]]["Setor"].values[0]
    maior_setor_val = df_plot.iloc[[maior_setor]]["Quantidade de Empresas"].values[0]

    title = f'"{maior_setor_nome}" é o maior setor, com {maior_setor_val} empresas.'
    fig = px.bar(df_plot, x="Quantidade de Empresas", y="Setor", title=title)
    fig.update_layout(barmode="stack", yaxis={"categoryorder": "total ascending"})

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
    df_plot = df_plot.groupby(["ticker_prefix", "empresa","setor"], as_index=False).agg({"valor_de_mercado": "max"}).reset_index()
    df_plot = df_plot.reset_index(drop=True)

    empresas = df_plot.sort_values(by=["valor_de_mercado"], ascending=False).head(3)
    empresas = ", ".join(empresas["ticker_prefix"])

    title = f"As empresas com maior valor de mercado (Marketcap) são: {empresas}"
    path = [px.Constant("B3"), "setor", "ticker_prefix"]

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


def grafico_media_indicadores(df):
    df_indicadores_altos = df.copy().drop(["papel", "setor", "empresa", "dt_ultima_cot"], axis=1)[["valor_de_mercado", "patrliq", "liq2m"]]
    df_indicadores_baicos = df.copy().drop(["papel", "setor", "empresa", "dt_ultima_cot", "valor_de_mercado", "patrliq", "liq2m"], axis=1)
    
    media_indicadores_altos = df_indicadores_altos.mean()
    media_indicadores_baixos = df_indicadores_baicos.mean()

    fig = px.bar(media_indicadores_baixos, x=media_indicadores_baixos.index, y=media_indicadores_baixos.values, labels={"index":"", "y":""}, title="Média indicadores (baixo valor)")
    st.plotly_chart(fig)

    fig = px.bar(media_indicadores_altos, x=media_indicadores_altos.index, y=media_indicadores_altos.values, labels={"index":"", "y":""}, title="Média indicadores (alto valor)")
    st.plotly_chart(fig)
    

def grafico_calor(df):
    # Verificação de presença de colunas numéricas no DataFrame:
    numeric_cols = df.select_dtypes(include=["number"]).columns
    if numeric_cols.empty:
        st.error("O DataFrame não contém colunas numéricas para calcular a correlação.")
        return None

    # Calculo da matriz de correlação
    corr_matrix = df[numeric_cols].corr()
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
        title="Correlação entre dados das empresas",
        width=1500, # Largura do gráfico
        height=1000, # Altura do gráfico
    )

    ticktexts = ["Cotação", "P/L", "P/VP", "Price Sales Ratio", "Dividend Yield", "P/Ativos", "P/Cap. Giro", "P/EBIT", "P/Atv. Circ. Liq.", "EV/EBIT", "EV/EBITDA", "Margem EBIT", "Margem Liq.", "ROIC", "ROE", "Liquidez Corrente", "Liquidez últimos 2 meses","Patrimônio Liq.", "Dívida/Patr. Liq.", "Cresc. Receita Últimos 5 Anos", "Valor de Mercado"]

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