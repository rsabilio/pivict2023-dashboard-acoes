import streamlit as st

class FiltersManager:
    def __init__(self, df, columns_info):
        """
        Inicializa o gerenciador de sliders.

        Parâmetros:
        - df (DataFrame): DataFrame com os dados.
        - columns_info (dict): Dicionário contendo informações das colunas.
        """
        self.df = df
        self.columns_info = columns_info
        self.slider_values = {}

        self.create_analysis_type()
        self.create_sliders()

    def create_analysis_type(self):
        # Adiciona a seleção do tipo de análise à barra lateral
        if "analysis_type" not in st.session_state:
            st.session_state["analysis_type"] = "Simplificada"  # Padrão é Simplificada

        st.sidebar.radio(
            "Tipo de Análise",
            ["Simplificada", "Completa"],
            key="analysis_type",
            index=0 if st.session_state["analysis_type"] == "Simplificada" else 1
        )


    def create_sliders(self):
        """
        Cria sliders no Streamlit para todas as colunas numéricas do DataFrame, agrupando-os por seção.
        """
        # Dicionário para manter os expanders criados
        expanders = {}

        with st.sidebar:
            for column_name, column_info in self.columns_info.items():
                if column_name in self.df.columns:
                    min_val = self.df[column_name].min()
                    max_val = self.df[column_name].max()
                    if f"slider_{column_name}" not in st.session_state:
                        min_val_default = max(0.0, min_val)
                        st.session_state[f"slider_{column_name}"] = (min_val_default, max_val)

                    section = column_info.get("section", "Sem Seção")

                    # Cria o expander se ainda não estiver criado para a seção
                    if section not in expanders:
                        expanders[section] = st.expander(section, expanded=True)

                    is_basic = st.session_state["analysis_type"] == "Simplificada" and column_info.get("basic", False)

                    # Adiciona o slider ao expander apropriado
                    with expanders[section]:
                        if is_basic:
                            self.slider_values[column_name] = st.slider(
                                column_info["full_name"],
                                min_value=min_val,
                                max_value=max_val,
                                step=0.01,
                                key=f"slider_{column_name}",
                                help=column_info["help"]
                            )
                        elif st.session_state["analysis_type"] == "Completa":
                            self.slider_values[column_name] = st.slider(
                                column_info["full_name"],
                                min_value=min_val,
                                max_value=max_val,
                                step=0.01,
                                key=f"slider_{column_name}",
                                help=column_info["help"]
                            )

    def get_slider_values(self):
        """
        Retorna:
        - dict: Dicionário com os valores dos sliders.
        """
        return self.slider_values

    def reset_sliders(self):
        """
        Reseta os filtros
        """
        #st.session_state['analysis_type'] = "Simplificada"

        for column_name in self.df.select_dtypes(include=['number']).columns:
            min_val = max(0, self.df[column_name].min())
            max_val = self.df[column_name].max()
            slider_key = f"slider_{column_name}"

            st.session_state[slider_key] = (min_val, max_val)