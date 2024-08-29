# config.py

# Descrição das colunas do DataFrame
columns_info = {
    "cotacao": {
        "full_name": "Cotação",
        "help": "Refere-se ao valor pelo qual a ação é negociada em determinado momento na Bolsa de Valores.",
        "section": "Valores de Mercado"
    },
    "valor_de_mercado": {
        "full_name": "Valor de Mercado",
        "help": "É o montante total que representa o valor da empresa no mercado de ações.",
        "section": "Valores de Mercado"
    },
    "pl": {
        "full_name": "Preço/Lucro (P/L)",
        "help": "É o número de anos necessários para reaver o capital aplicado na compra da ação através do recebimento do lucro gerado pela empresa, considerando que esses lucros permaneçam constantes.",
        "section": "Indicadores de Valor"
    },
    "pvp": {
        "full_name": "Preço/Valor Patrimonial (P/VP)",
        "help": "Informa quanto o mercado está disposto a pagar sobre o patrimônio líquido da empresa.",
        "section": "Indicadores de Valor"
    },
    "psr": {
        "full_name": "Preço/Sales Ratio (P/SR)",
        "help": "Indica o quanto os investidores pagam em relação às vendas da empresa.",
        "section": "Indicadores de Valor"
    },
    "dy": {
        "full_name": "Dividend Yield (DY)",
        "help": "É o rendimento gerado para o dono da ação pelo pagamento de dividendos.",
        "section": "Indicadores de Valor"
    },
    "pa": {
        "full_name": "Preço/Ativo (P/A)",
        "help": "Permite identificar se uma ação está subvalorizada ou sobrevalorizada em relação aos seus ativos.",
        "section": "Indicadores de Valor"
    },
    "pcg": {
        "full_name": "Preço/Capital de Giro (P/CG)",
        "help": "Ajuda a avaliar o quanto os investidores estão dispostos a pagar pelo capital de giro da empresa.",
        "section": "Indicadores de Valor"
    },
    "pebit": {
        "full_name": "Preço/EBIT (P/EBIT)",
        "help": "É utilizado para ponderar se a ação está cara ou barata em relação ao seu desempenho operacional.",
        "section": "Indicadores de Valor"
    },
    "pacl": {
        "full_name": "Preço/Ativo Circulante Líquido (P/ACL)",
        "help": "Representa a solidez da empresa diante de suas obrigações e quanto o mercado paga por isso.",
        "section": "Indicadores de Valor"
    },
    "evebit": {
        "full_name": "EV/EBIT",
        "help": "Auxilia na avaliação do valor da empresa em relação ao seu desempenho operacional, descontando os efeitos de juros e impostos.",
        "section": "Indicadores de Valor"
    },
    "evebitda": {
        "full_name": "EV/EBITDA",
        "help": "Relaciona o valor da empresa com sua geração de caixa.",
        "section": "Indicadores de Valor"
    },
    "mrgebit": {
        "full_name": "Margem EBIT",
        "help": "Indica a porcentagem de cada R$ 1,00 adquirido em vendas que sobrou após o pagamento das despesas operacionais.",
        "section": "Indicadores de Rentabilidade"
    },
    "mrgliq": {
        "full_name": "Margem Líquida",
        "help": "Revela a porcentagem de lucro em relação às receitas totais da empresa.",
        "section": "Indicadores de Rentabilidade"
    },
    "roic": {
        "full_name": "Retorno sobre Capital Investido (ROIC)",
        "help": "Informa quanto de lucro a empresa gera com base no capital total investido.",
        "section": "Indicadores de Rentabilidade"
    },
    "roe": {
        "full_name": "Retorno sobre Patrimônio Líquido (ROE)",
        "help": "Refere-se à capacidade da empresa de gerar lucro com os recursos próprios dos acionistas.",
        "section": "Indicadores de Rentabilidade"
    },
    "liqc": {
        "full_name": "Liquidez Corrente",
        "help": "Mede a capacidade da empresa de pagar suas obrigações de curto prazo com seus ativos circulantes.",
        "section": "Indicadores de Liquidez"
    },
    "liq2m": {
        "full_name": "Liquidez 2 Meses",
        "help": "Avalia a capacidade da empresa de cumprir suas obrigações de curto prazo (2 meses).",
        "section": "Indicadores de Liquidez"
    },
    "patrliq": {
        "full_name": "Patrimônio Líquido",
        "help": "É o valor total dos ativos líquidos da empresa que pode ser convertido em dinheiro, seja a curto, médio ou longo prazo.",
        "section": "Indicadores de Liquidez"
    },
    "divbpatr": {
        "full_name": "Dívida Bruta/Patrimônio Líquido",
        "help": "Compara a dívida bruta da empresa com seu patrimônio líquido para avaliar seu nível de endividamento.",
        "section": "Indicadores de Endividamento"
    },
    "c5y": {
        "full_name": "Crescimento 5 Anos",
        "help": "Reflete o crescimento da receita líquida da empresa nos últimos 5 anos.",
        "section": "Indicadores de Crescimento"
    }
}
