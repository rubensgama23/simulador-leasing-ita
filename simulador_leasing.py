
"""
Simulador de Leasing com FIDC e Capital Próprio
Autor: ChatGPT
Descrição: Este script calcula o lucro e o ROE de uma operação de leasing estruturada.
"""

def calcular_operacao(
    valor_leasing=125,
    valor_aquisicao=100,
    custos_operacionais=35,
    prazo_meses=36,
    parcela_cliente=3.20,
    residual_cliente=63.32,
    taxa_juros_anual=20,
    capital_fidc=100
):
    taxa_mensal = (1 + taxa_juros_anual / 100) ** (1/12) - 1
    pmt_fidc = capital_fidc * (taxa_mensal / (1 - (1 + taxa_mensal) ** -prazo_meses))
    total_fidc = pmt_fidc * prazo_meses

    # Capital próprio é utilizado ao longo dos meses, calcular custo futuro equivalente
    desembolso_mensal = custos_operacionais / prazo_meses
    fator_acumulacao = ((1 + taxa_mensal) ** prazo_meses - 1) / taxa_mensal
    custo_capital_proprio = desembolso_mensal * fator_acumulacao

    receita_cliente = parcela_cliente * prazo_meses + residual_cliente
    lucro = receita_cliente - total_fidc - custo_capital_proprio
    roe_nominal = (lucro / custos_operacionais) * 100 if custos_operacionais > 0 else 0
    roe_anualizado = ((1 + lucro / custos_operacionais) ** (1 / (prazo_meses / 12)) - 1) * 100 if custos_operacionais > 0 else 0

    return {
        "PMT_FIDC": round(pmt_fidc, 2),
        "Total_Pago_FIDC": round(total_fidc, 2),
        "Custo_Capital_Proprio": round(custo_capital_proprio, 2),
        "Receita_Cliente": round(receita_cliente, 2),
        "Lucro_Liquido": round(lucro, 2),
        "ROE_Nominal (%)": round(roe_nominal, 2),
        "ROE_Anualizado (%)": round(roe_anualizado, 2)
    }

# Exemplo de uso
if __name__ == "__main__":
    resultado = calcular_operacao()
    for k, v in resultado.items():
        print(f"{k}: {v}")
