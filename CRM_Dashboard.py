import pandas as pd
import streamlit as st

st.set_page_config(page_title="Dashboard CRM", layout="wide")

st.title("📊 Dashboard de CRM - Embudo de Ventas")

# Subida de archivo
archivo = st.file_uploader("📂 Sube tu archivo CRM (.xlsx)", type=["xlsx"])

@st.cache_data
def cargar_datos(excel_file):
    df = pd.read_excel(excel_file, sheet_name="Sales Funnel", skiprows=2)

    df = df.rename(columns={
        "Unnamed: 0": "Company",
        "Unnamed: 1": "Contact Name",
        "Unnamed: 2": "Email",
        "Unnamed: 3": "Stage",
        "Unnamed: 5": "Value",
        "Unnamed: 6": "Probability",
        "Unnamed: 7": "Expected Revenue",
        "Unnamed: 8": "Creation Date",
        "Unnamed: 9": "Close Date",
        "Unnamed: 10": "Team member",
        "Unnamed: 11": "Progress to Won",
        "Unnamed: 12": "Last Interaction",
        "Unnamed: 13": "Next Step"
    })

    # Limpiar y convertir tipos
    df = df.dropna(subset=["Company Name", "Stage"])
    df["Value"] = pd.to_numeric(df["Value"], errors="coerce").fillna(0)
    df["Expected Revenue"] = pd.to_numeric(df["Expected Revenue"], errors="coerce").fillna(0)

    return df

if archivo:
    try:
        df = cargar_datos(archivo)

        # Filtros
        st.sidebar.header("🔍 Filtros")
        etapas = st.sidebar.multiselect("Etapa del embudo", df["Stage"].unique(), default=list(df["Stage"].unique()))
        responsables = st.sidebar.multiselect("Responsable", df["Team member"].dropna().unique(), default=list(df["Team member"].dropna().unique()))

        df_filtrado = df[df["Stage"].isin(etapas) & df["Team member"].isin(responsables)]

        # Métricas clave
        st.subheader("📈 Métricas Generales")
        col1, col2, col3 = st.columns(3)
        col1.metric("Oportunidades", len(df_filtrado))
        col2.metric("Valor Total", f"${df_filtrado['Value'].sum():,.0f}")
        col3.metric("Ingreso Esperado", f"${df_filtrado['Expected Revenue'].sum():,.0f}")

        # Embudo de ventas
        st.subheader("🪜 Oportunidades por Etapa")
        etapas_count = df_filtrado["Stage"].value_counts().reset_index()
        etapas_count.columns = ["Etapa", "Número de Oportunidades"]
        st.bar_chart(etapas_count.set_index("Etapa"))

        # Detalle en tabla
        st.subheader("📋 Detalle de Oportunidades")
        st.dataframe(df_filtrado)

        st.caption("Actualiza el archivo Excel y vuelve a cargarlo aquí para ver los cambios.")

    except Exception as e:
        st.error(f"Ocurrió un error al leer el archivo: {e}")
else:
    st.info("Por favor, sube un archivo .xlsx para comenzar.")
