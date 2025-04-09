
import streamlit as st

st.set_page_config(page_title="Simulador de Leasing", layout="centered")

def calcular_operacao(
    valor_leasing, valor_aquisicao, custos_operacionais,
    prazo_meses, parcela_cliente, residual_cliente,
    taxa_juros_anual, capital_fidc
):
    taxa_mensal = (1 + taxa_juros_anual / 100) ** (1/12) - 1
    pmt_fidc = capital_fidc * (taxa_mensal / (1 - (1 + taxa_mensal) ** -prazo_meses))
    total_fidc = pmt_fidc * prazo_meses

    desembolso_mensal = custos_operacionais / prazo_meses
    fator_acumulacao = ((1 + taxa_mensal) ** prazo_meses - 1) / taxa_mensal
    custo_capital_proprio = desembolso_mensal * fator_acumulacao

    receita_cliente = parcela_cliente * prazo_meses + residual_cliente
    lucro = receita_cliente - total_fidc - custo_capital_proprio
    roe_nominal = (lucro / custos_operacionais) * 100 if custos_operacionais > 0 else 0
    roe_anualizado = ((1 + lucro / custos_operacionais) ** (1 / (prazo_meses / 12)) - 1) * 100 if custos_operacionais > 0 else 0

    return {
        "PMT FIDC (R$)": round(pmt_fidc, 2),
        "Total Pago ao FIDC (R$)": round(total_fidc, 2),
        "Custo Capital Próprio (R$)": round(custo_capital_proprio, 2),
        "Receita Cliente (R$)": round(receita_cliente, 2),
        "Lucro Líquido (R$)": round(lucro, 2),
        "ROE Nominal (%)": round(roe_nominal, 2),
        "ROE Anualizado (%)": round(roe_anualizado, 2)
    }

st.title("📊 Simulador de Leasing ITA")
st.caption("Todos os valores estão em reais (R$)")

# Inputs diretamente em R$
valor_leasing = st.number_input("Valor de referência do veículo (R$)", value=125000.0)
valor_aquisicao = st.number_input("Valor real de aquisição do veículo (R$)", value=100000.0)
custos_operacionais = st.number_input("Custos operacionais totais (R$)", value=35000.0)
prazo_meses = st.slider("Prazo do contrato (meses)", 12, 60, 36)
parcela_cliente = st.number_input("Parcela mensal do cliente (R$)", value=3200.0)
residual_cliente = st.number_input("Residual pago no final (bullet) (R$)", value=63320.0)
taxa_juros_anual = st.number_input("Taxa de juros anual do FIDC (%)", value=20.0)
capital_fidc = st.number_input("Valor captado via FIDC (R$)", value=100000.0)

def format_brl(valor):
    inteiro, decimal = f"{valor:.2f}".split(".")
    partes = []
    while inteiro:
        partes.insert(0, inteiro[-3:])
        inteiro = inteiro[:-3]
    return f"R$ {'.'.join(partes)},{decimal}"

if st.button("Calcular"):
    resultado = calcular_operacao(
        valor_leasing, valor_aquisicao, custos_operacionais,
        prazo_meses, parcela_cliente, residual_cliente,
        taxa_juros_anual, capital_fidc
    )
    
    st.subheader("📈 Resultado")
    for chave, valor in resultado.items():
        if "R$" in chave:
            st.write(f"**{chave}:** {format_brl(valor)}")
        else:
            st.write(f"**{chave}:** {valor:.2f}%")
