
import streamlit as st

st.set_page_config(page_title="Simulador ROI - ITA Frotas", layout="wide")

st.image("logo_ita.png", width=160)
st.title("Simulador de ROI - Frota Corporativa")
st.caption("Versão institucional • Desenvolvido para ITA Frotas")
st.markdown("---")

def calcular_roi(valor_fipe, desconto, receita_mensal, juros_mensal, prazo, desvalorizacao,
                 custo_op, custo_adm, custo_buro, qtd):
    tributos = 0.34  # premissa fixa
    valor_pago = valor_fipe * (1 - desconto)
    total_aquisicao = valor_pago * qtd

    mensal_op = custo_op * valor_pago
    mensal_adm = custo_adm * valor_pago
    total_buro = custo_buro * valor_pago
    mensal_buro = total_buro / prazo

    custo_total_mensal = (mensal_op + mensal_adm + mensal_buro) * qtd

    desval_total = desvalorizacao * (prazo / 12)
    valor_residual = valor_fipe * (1 - desval_total) * qtd

    parcela_mensal = total_aquisicao * (
        juros_mensal * (1 + juros_mensal)**prazo
    ) / ((1 + juros_mensal)**prazo - 1)

    total_pago = parcela_mensal * prazo
    receita_total = receita_mensal * qtd * prazo
    receita_gerada = receita_total + valor_residual

    lucro_bruto = receita_gerada - total_pago
    lucro_antes_ir = lucro_bruto - (custo_total_mensal * prazo)
    lucro_liquido = lucro_antes_ir * (1 - tributos)

    roi = lucro_liquido / total_aquisicao
    return round(lucro_liquido, 2), round(roi * 100, 2)

# Sidebar de entrada
valor_fipe = st.sidebar.number_input("Valor FIPE (R$)", value=125000)
desconto = st.sidebar.number_input("Desconto na compra (%)", value=20.0) / 100
prazo = st.sidebar.selectbox("Prazo (meses)", [12, 24, 36])
desvalorizacao = st.sidebar.number_input("Desvalorização anual (%)", value=10.0) / 100
juros = st.sidebar.number_input("Juros mensal (%)", value=1.2) / 100
qtd = st.sidebar.number_input("Qtd. de veículos", value=10)

st.markdown("### Premissas de custo (% sobre valor do veículo pago)")
custo_op = st.number_input("Custos operacionais mensais (%)", value=1.00) / 100
st.caption("Padrão: 1,00%")

custo_adm = st.number_input("Despesas administrativas mensais (%)", value=0.55) / 100
st.caption("Padrão: 0,55%")

custo_buro = st.number_input("Custos burocráticos totais (%)", value=5.00) / 100
st.caption("Padrão: 5,00%")

receita = st.number_input("Receita mensal por veículo (R$)", value=3000)

st.markdown("**Premissa:** carga tributária fixa de 34% sobre o lucro.")

if st.button("Calcular ROI"):
    lucro, roi = calcular_roi(valor_fipe, desconto, receita, juros, prazo, desvalorizacao,
                              custo_op, custo_adm, custo_buro, qtd)
    st.subheader("Resultado")
    st.success(f"Lucro líquido: R$ {lucro:,.2f}")
    st.success(f"ROI líquido: {roi:.2f}%")

    custo_total_percent_fipe = 0.35 * (1 - desconto)
    st.info(f"Total de custos estimado equivale a aproximadamente **{custo_total_percent_fipe:.2%}** do valor FIPE.")
