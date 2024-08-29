import streamlit as st

class SliderManager:
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

                    # Adiciona o slider ao expander apropriado
                    with expanders[section]:
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
        Reseta os sliders no Streamlit com base nos valores do DataFrame.

        Parâmetros:
        - df (DataFrame): DataFrame com os dados.
        """
        for column_name in self.df.select_dtypes(include=['number']).columns:
            min_val = max(0, self.df[column_name].min())
            max_val = self.df[column_name].max()
            slider_key = f"slider_{column_name}"

            # Atualiza o valor do slider se já estiver no session_state
           # if slider_key not in st.session_state:
            st.session_state[slider_key] = (min_val, max_val)