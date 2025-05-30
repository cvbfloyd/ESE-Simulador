import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(page_title="Simulador Cells for Cells", layout="wide")

st.title("Simulador de Escenarios de Inversión - Cells for Cells")

# Parámetros globales
st.sidebar.header("Parámetros Globales")
discount_rate = st.sidebar.slider("Tasa de Descuento (%)", 5, 20, 12) / 100
available_funding = st.sidebar.number_input("Capital Disponible (MM USD)", value=6.0, min_value=0.0)

# Datos base de terapias
therapies = {
    'CELLISTEM®OA': {'fase': 'Lab completed', 'patente': 1.0, 'tto_m': 11, 'estrategico': 5, 'max_needed': 12},
    'CELLISTEM®OA 2.0': {'fase': 'Lab completed', 'patente': 0.8, 'tto_m': 11, 'estrategico': 5, 'max_needed': 12},
    'Veintis': {'fase': 'Pre-lab', 'patente': 1.0, 'tto_m': 10, 'estrategico': 5, 'max_needed': 10},
    'Exosoma Cancer': {'fase': 'Lab completed', 'patente': 1.0, 'tto_m': 7, 'estrategico': 2, 'max_needed': 24},
    'CELLISTEM-ER': {'fase': 'Phase II', 'patente': 1.0, 'tto_m': 3.5, 'estrategico': 1, 'max_needed': 2},
    'Exosoma OA': {'fase': 'Lab completed', 'patente': 0.3, 'tto_m': 11, 'estrategico': 4, 'max_needed': 12}
}

st.write("### Asignación de Capital por Terapia")
allocations = {}
for therapy in therapies:
    alloc = st.number_input(
        f"Inversión en {therapy} (MM USD, máx {therapies[therapy]['max_needed']})",
        min_value=0.0,
        max_value=float(therapies[therapy]['max_needed']),
        value=0.0,
        key=therapy
    )
    allocations[therapy] = alloc

# Verificar presupuesto
total_allocated = sum(allocations.values())
if total_allocated > available_funding:
    st.error(f"¡Te pasaste del presupuesto! Asignaste {total_allocated:.2f} MM USD (máx {available_funding:.2f})")
else:
    st.success(f"Presupuesto asignado: {total_allocated:.2f} MM USD de {available_funding:.2f} MM USD")

# Cálculo de resultados
results = []
for therapy, data in therapies.items():
    investment = allocations[therapy]
    progress = min(investment / data['max_needed'], 1.0)
    base_value = data['estrategico'] * 100  # valor base estratégico ficticio
    npv = base_value * progress / ((1 + discount_rate) ** data['tto_m']) * data['patente']
    roi = (npv / investment) if investment > 0 else 0
    risk = np.random.uniform(0.6, 0.9)  # simplificado
    results.append({'Terapia': therapy, 'Inversión (MM USD)': investment,
                    'Progreso (%)': f"{progress * 100:.0f}%", 'NPV (MM USD)': npv,
                    'ROI': roi, 'Riesgo': f"{risk * 100:.0f}%"
                   })

df = pd.DataFrame(results)

st.write("### Resultados del Portfolio")
st.dataframe(df)

# Gráfico de NPV
st.write("### Gráfico de NPV por Terapia")
fig, ax = plt.subplots()
df.plot(x='Terapia', y='NPV (MM USD)', kind='bar', ax=ax)
plt.ylabel('NPV (MM USD)')
plt.xticks(rotation=45)
st.pyplot(fig)

# Exportar
st.write("### Exportar Resultados")
csv = df.to_csv(index=False).encode('utf-8')
st.download_button("Descargar CSV", csv, "resultados_portfolio.csv", "text/csv")

st.info("Simulador listo para Streamlit Cloud. Súbelo y ejecútalo online 🚀")
