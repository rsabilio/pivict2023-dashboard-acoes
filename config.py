# config.py

# Descrição das colunas do DataFrame
columns_info = {
    "cotacao": {
        "full_name": "Cotação",
        "help": "Refere-se ao valor pelo qual a ação é negociada em determinado momento na Bolsa de Valores.",
        "section": "Valores de Mercado",
        "basic": True
    },
    "valor_de_mercado": {
        "full_name": "Valor de Mercado",
        "help": "É o montante total que representa o valor da empresa no mercado de ações.",
        "section": "Valores de Mercado",
        "basic": True
    },
    "pl": {
        "full_name": "Preço/Lucro (P/L)",
        "help": "É o número de anos necessários para reaver o capital aplicado na compra da ação através do recebimento do lucro gerado pela empresa, considerando que esses lucros permaneçam constantes.",
        "section": "Indicadores de Valor",
        "basic": True
    },
    "pvp": {
        "full_name": "Preço/Valor Patrimonial (P/VP)",
        "help": "Informa quanto o mercado está disposto a pagar sobre o patrimônio líquido da empresa.",
        "section": "Indicadores de Valor",
        "basic": True
    },
    "psr": {
        "full_name": "Preço/Sales Ratio (P/SR)",
        "help": "Indica o quanto os investidores pagam em relação às vendas da empresa.",
        "section": "Indicadores de Valor",
        "basic": False
    },
    "dy": {
        "full_name": "Dividend Yield (DY)",
        "help": "É o rendimento gerado para o dono da ação pelo pagamento de dividendos.",
        "section": "Indicadores de Valor",
        "basic": True
    },
    "pa": {
        "full_name": "Preço/Ativo (P/A)",
        "help": "Permite identificar se uma ação está subvalorizada ou sobrevalorizada em relação aos seus ativos.",
        "section": "Indicadores de Valor",
        "basic": False
    },
    "pcg": {
        "full_name": "Preço/Capital de Giro (P/CG)",
        "help": "Ajuda a avaliar o quanto os investidores estão dispostos a pagar pelo capital de giro da empresa.",
        "section": "Indicadores de Valor",
        "basic": False
    },
    "pebit": {
        "full_name": "Preço/EBIT (P/EBIT)",
        "help": "É utilizado para ponderar se a ação está cara ou barata em relação ao seu desempenho operacional.",
        "section": "Indicadores de Valor",
        "basic": False
    },
    "pacl": {
        "full_name": "Preço/Ativo Circulante Líquido (P/ACL)",
        "help": "Representa a solidez de uma instituição diante de suas obrigações e quanto o mercado paga por isso.",
        "section": "Indicadores de Valor",
        "basic": False
    },
    "evebit": {
        "full_name": "EV/EBIT",
        "help": "Auxilia na avaliação do valor da empresa em relação ao seu desempenho operacional, descontando os efeitos de juros e impostos.",
        "section": "Indicadores de Valor",
        "basic": False
    },
    "evebitda": {
        "full_name": "EV/EBITDA",
        "help": "Relaciona o valor da empresa com sua geração de caixa.",
        "section": "Indicadores de Valor",
        "basic": False
    },
    "mrgebit": {
        "full_name": "Margem EBIT",
        "help": "Indica a porcentagem de cada R$ 01,00 adquirido em vendas que sobrou após o pagamento das despesas decorrentes.",
        "section": "Margens",
        "basic": False
    },
    "mrgliq": {
        "full_name": "Margem Líquida",
        "help": "Revela a porcentagem de lucro em relação às receitas que a empresa apresentou no seu demonstrativo de resultados.",
        "section": "Margens",
        "basic": False
    },
    "roic": {
        "full_name": "Retorno sobre Capital Investido (ROIC)",
        "help": "Informa quanto de dinheiro a empresa consegue gerar em razão de todo o capital investido.",
        "section": "Retornos",
        "basic": False
    },
    "roe": {
        "full_name": "Retorno sobre Patrimônio Líquido (ROE)",
        "help": "Refere-se à capacidade da empresa em agregar valor a ela mesma utilizando os seus próprios recursos.",
        "section": "Retornos",
        "basic": False
    },
    "liqc": {
        "full_name": "Liquidez Corrente",
        "help": "Mede a capacidade da companhia de pagar todas as suas dívidas em um curto horizonte de tempo.",
        "section": "Liquidez",
        "basic": False
    },
    "liq2m": {
        "full_name": "Liquidez 2 Meses",
        "help": "Avalia a capacidade da empresa de atender suas obrigações de curto prazo (2 meses).",
        "section": "Liquidez",
        "basic": False
    },
    "patrliq": {
        "full_name": "Patrimônio Líquido",
        "help": "É tudo aquilo que a empresa possui e que pode ser transformado em dinheiro, seja a curto, médio ou longo prazo.",
        "section": "Valores de Mercado",
        "basic": False
    },
    "divbpatr": {
        "full_name": "Dívida Bruta/Patrimônio Líquido",
        "help": "Faz um comparativo sobre endividamento e alavancagem da empresa, isto é, a diferença entre os passivos e ativos que o negócio possui.",
        "section": "Endividamento",
        "basic": False
    },
    "c5y": {
        "full_name": "Crescimento 5 Anos",
        "help": "Crescimento da receita líquida nos últimos 5 anos.",
        "section": "Crescimento",
        "basic": False
    }
}
