import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title="Dashboard de Rendimiento Académico", layout="wide")
st.title("🎓 Dashboard Interactivo: Rendimiento Académico de Estudiantes")
st.markdown("Este panel web interactivo permite explorar los datos procesados del rendimiento estudiantil.")

@st.cache_data
def cargar_datos():
    return pd.read_csv("rendimiento_estudiantes_procesado.csv")

df = cargar_datos()

st.sidebar.header("Filtros del Dashboard")
niveles = df['nivel_socioeconomico'].unique().tolist()
nivel_seleccionado = st.sidebar.multiselect("Nivel Socioeconómico:", niveles, default=niveles)

estados = df['estado_aprobacion'].unique().tolist()
estado_seleccionado = st.sidebar.multiselect("Estado de Aprobación:", estados, default=estados)

df_filtrado = df[
    (df['nivel_socioeconomico'].isin(nivel_seleccionado)) & 
    (df['estado_aprobacion'].isin(estado_seleccionado))
]

st.subheader("📊 Indicadores Clave de Rendimiento (KPIs)")
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Estudiantes Mostrados", len(df_filtrado))
with col2:
    promedio = df_filtrado['calificacion_final'].mean() if len(df_filtrado) > 0 else 0
    st.metric("Calificación Final Promedio", f"{promedio:.2f}")
with col3:
    tasa = (len(df_filtrado[df_filtrado['estado_aprobacion'] == 'Aprobado']) / len(df_filtrado) * 100) if len(df_filtrado) > 0 else 0
    st.metric("Tasa de Aprobación", f"{tasa:.1f}%")

st.subheader("📋 Registro de Estudiantes (Datos Filtrados)")
st.dataframe(df_filtrado, use_container_width=True)

st.subheader("📈 Gráficos Analíticos")
col_g1, col_g2 = st.columns(2)
with col_g1:
    st.markdown("**Distribución de Calificaciones Finales**")
    fig, ax = plt.subplots(figsize=(6, 4))
    sns.histplot(df_filtrado['calificacion_final'], kde=True, color='purple', ax=ax)
    st.pyplot(fig)
with col_g2:
    st.markdown("**Horas de Estudio vs Calificación Final**")
    fig, ax = plt.subplots(figsize=(6, 4))
    sns.scatterplot(data=df_filtrado, x='horas_estudio_semana', y='calificacion_final', hue='estado_aprobacion', palette='viridis', ax=ax)
    st.pyplot(fig)

st.markdown("**Asistencia según Estado de Aprobación**")
fig, ax = plt.subplots(figsize=(8, 4))
sns.boxplot(data=df_filtrado, x='estado_aprobacion', y='asistencia_clases', palette='Set2', ax=ax)
st.pyplot(fig)
