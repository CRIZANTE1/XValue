import streamlit as st
from end.dfc_model import DCFModel

def pageconfig():
    st.set_page_config(
        page_title="Valor Justo da Ação - FCD",
        page_icon="💵",
        layout="centered"
    )
    st.title("Cálculo do Valor Justo de uma Ação")

def pageone():
    st.markdown("""
    Este aplicativo ajuda você a descobrir quanto **deveria pagar por uma ação hoje**, 
    com base na geração de caixa da empresa e nas suas projeções.
    
    Basta preencher os dados abaixo, que geralmente estão no **relatório trimestral da empresa (ex: ITR ou Release de Resultados)**.
    """)

    st.markdown("## Passo 1: Informações extraídas do relatório")

    fcl_base = st.number_input(
        "1️⃣ Fluxo de Caixa Livre mais recente (em milhões de R$)",
        value=900.0,
        help="Você encontra esse valor na seção de 'Fluxo de Caixa Operacional' ou 'Atividades Operacionais'."
    )

    num_acoes = st.number_input(
        "2️⃣ Número total de ações em circulação (em milhões)",
        value=1119.0,
        help="Você encontra na seção 'Mercado de Capitais' ou 'Capital Social'."
    )

    preco_mercado = st.number_input(
        "3️⃣ Preço atual da ação (em R$)",
        value=19.10,
        help="Cotação da ação no dia atual, ou informada no relatório (última página ou quadro de ações)."
    )

    st.markdown("## Passo 2: Suas estimativas para o futuro")

    anos = st.slider(
        "4️⃣ Por quantos anos você quer projetar os lucros futuros?",
        min_value=3, max_value=10, value=5,
        help="Normalmente usa-se entre 5 e 10 anos."
    )

    crescimento_anual = st.number_input(
        "5️⃣ Estimativa de crescimento anual do fluxo de caixa (%)",
        value=5.0,
        help="Se a empresa está crescendo, coloque uma taxa como 5%. Se estiver estável, use 0%."
    ) / 100

    discount_rate = st.number_input(
        "6️⃣ Taxa de desconto (WACC ou Ke) (%)",
        value=10.0,
        help="Reflete o risco do investimento. Se não souber, use 10%."
    ) / 100

    g_rate = st.number_input(
        "7️⃣ Crescimento perpétuo após os anos projetados (%)",
        value=3.0,
        help="Taxa de crescimento da empresa após o último ano projetado. Use algo entre 2% e 5%."
    ) / 100

    st.markdown("---")

    if st.button("📊 Calcular Valor Justo da Ação"):
        # Projeção dos fluxos futuros com crescimento
        cash_flows = [fcl_base * ((1 + crescimento_anual) ** i) for i in range(anos)]

        # Cálculo do valor presente
        dcf = DCFModel(cash_flows, discount_rate, g_rate)
        valor_intrinseco_total = dcf.calculate_intrinsic_value()
        valor_justo_acao = valor_intrinseco_total / num_acoes

        st.markdown("## ✅ Resultado")

        st.subheader(f"💰 Valor Justo da Ação: **R$ {valor_justo_acao:,.2f}**")

        if valor_justo_acao > preco_mercado:
            st.success("🔽 A ação está **descontada** (subavaliada).")
            st.markdown(f"""
            ### Explicação:
            - O valor justo por ação é **R$ {valor_justo_acao:,.2f}**.
            - O preço atual de mercado é **R$ {preco_mercado:,.2f}**.
            - Isso indica que **a ação vale mais do que custa hoje**, segundo suas projeções.
            - Pode ser uma **oportunidade de compra**, se suas premissas forem razoáveis.
            """)
        elif valor_justo_acao < preco_mercado:
            st.error("🔼 A ação está **cara** (supervalorizada).")
            st.markdown(f"""
            ### Explicação:
            - O valor justo por ação é **R$ {valor_justo_acao:,.2f}**.
            - O preço atual de mercado é **R$ {preco_mercado:,.2f}**.
            - Isso sugere que **o mercado está esperando mais crescimento** do que você projetou, ou **ignorando riscos**.
            """)
        else:
            st.info("⚖️ A ação está com preço justo.")
            st.markdown(f"""
            ### Explicação:
            - O valor justo e o preço atual estão praticamente iguais (**R$ {valor_justo_acao:,.2f}**).
            - A ação parece estar corretamente precificada segundo os dados e premissas inseridos.
            """)

    st.markdown("## ℹ️ Dica:")
    with st.expander("📘 Onde encontrar esses dados no relatório?"):
        st.markdown("""
        - **Fluxo de Caixa Livre**: seção de "Demonstração dos Fluxos de Caixa" → linha "Caixa gerado nas atividades operacionais".
        - **Número de ações**: seção "Mercado de Capitais" ou "Capital Social".
        - **Preço da ação**: cotação do dia ou média no período.
        """)

