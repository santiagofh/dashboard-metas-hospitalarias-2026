import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import io

meta_tag = 'MSH1'
meta_titulo = 'Meta 1: Lactancia Materna Exclusiva en ninos y ninas al sexto mes de vida'

deis_path = "data/establecimientos_deis_actual.xlsx"

# --- Carga de datos ---
df_ms = pd.read_csv('MS_HOSP_2026.csv')
col_est = ['EstablecimientoCodigo', 'EstablecimientoGlosa', 'SeremiSaludGlosa_ServicioDeSaludGlosa', 'ComunaGlosa']
col_rename = {
    'EstablecimientoCodigo': 'IdEstablecimiento',
    'EstablecimientoGlosa': 'nombre_establecimiento',
    'SeremiSaludGlosa_ServicioDeSaludGlosa': 'servicio_salud',
    'ComunaGlosa': 'comuna'
}
df_est = pd.read_excel(deis_path, sheet_name='establecimientos', usecols=col_est)
df_est = df_est.rename(columns=col_rename)

df = df_ms.loc[df_ms.MetaSanitaria == meta_tag]
df = df.merge(df_est, on='IdEstablecimiento', how='left')
df = df.dropna(subset=['Ano', 'Mes'])
df['Ano'] = df['Ano'].fillna(0).astype(int)
df['Mes'] = df['Mes'].fillna(0).astype(int)
df['Ano_Mes'] = df['Ano'] * 100 + df['Mes']
df['Numerador'] = df['Numerador'].fillna(0).astype(int)
df['Denominador'] = df['Denominador'].fillna(0).astype(int)
df['IdEstablecimiento'] = df['IdEstablecimiento'].astype(str)
df['nombre_establecimiento'] = df['nombre_establecimiento'].astype(str)
df = df.dropna(subset=["servicio_salud", "comuna"])
df["servicio_salud"] = df["servicio_salud"].fillna("No especificado").astype(str)
df['codigo_nombre'] = df['IdEstablecimiento'] + ' - ' + df['nombre_establecimiento']

df = df.groupby(['IdEstablecimiento']).agg({
    'Ano_Mes': 'max',
    'Numerador': 'sum',
    'Denominador': 'sum',
    'codigo_nombre': 'first',
    'Dependencia Administrativa': 'first',
    'Nivel de Atencion': 'first',
    'comuna': 'first',
    'servicio_salud': 'first',
}).reset_index()
df['Porcentaje'] = df['Numerador'] / df['Denominador']

st.title(meta_titulo)
st.caption("Fuente: REM A03 - Seccion A.5 | Numerador: H61 | Denominador: H67")

with st.expander("Exclusiones (segun OOTT Ley 18.834)"):
    st.write("""
    Se exceptuan de la evaluacion y se descuentan del numerador y denominador:
    - Ninos y ninas, hijos de madres con VIH+ y HTLV
    - Ninos y ninas bajo tutelaje del Estado

    **Procedimiento:** Cada Servicio de Salud debe emitir un oficio dirigido a la
    Subsecretaria de Redes Asistenciales indicando el numero total de lactantes a excluir,
    a mas tardar el decimo dia habil de enero del 2027.
    """)

st.warning("Datos Provisorios")

# --- Filtros ---
st.header("Filtros")
establecimientos = sorted(df['codigo_nombre'].dropna().unique())
seleccion = st.multiselect("Establecimiento", establecimientos)
df_filtered = df[df['codigo_nombre'].isin(seleccion)] if seleccion else df

# --- Metricas ---
num_services = df_filtered['servicio_salud'].nunique()
num_communes = df_filtered['comuna'].nunique()
num_establishments = df_filtered['codigo_nombre'].nunique()

col1, col2, col3 = st.columns(3)
with col1:
    st.metric(label='N Servicios de Salud', value=num_services)
with col2:
    st.metric(label='N de comunas', value=num_communes)
with col3:
    st.metric(label='N de establecimientos', value=num_establishments)

# --- Tabla ---
col_tabla = ['Ano_Mes', 'codigo_nombre', 'servicio_salud', 'Numerador', 'Denominador', 'Porcentaje']
rename_tabla = {
    'Ano_Mes': 'Ano y Mes',
    'codigo_nombre': 'Nombre del establecimiento',
    'servicio_salud': 'Servicio de Salud',
    'Numerador': 'Numerador',
    'Denominador': 'Denominador',
    'Porcentaje': 'Cumplimiento MSH'
}
st.write("## Tabla de establecimientos")
st.write(df_filtered[col_tabla].rename(columns=rename_tabla))

df_export = df_filtered[col_tabla].rename(columns=rename_tabla)
output = io.BytesIO()
with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
    df_export.to_excel(writer, index=False, sheet_name='Tabla_Establecimientos')
st.download_button(
    label="Descargar tabla (Excel)",
    data=output.getvalue(),
    file_name="MSH1_LME.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
)

# --- Gauge ---
total_num = df_filtered['Numerador'].sum()
total_den = df_filtered['Denominador'].sum()
total_pct = (total_num / total_den) if total_den > 0 else 0

st.write("## Cumplimiento de la Meta Hospitalaria")
col1, col2, col3 = st.columns(3)
with col1:
    st.metric(label='Numerador', value=total_num)
with col2:
    st.metric(label='Denominador', value=total_den)
with col3:
    st.metric(label='% Cumplimiento', value=f"{total_pct:.1%}")

fig = go.Figure(go.Indicator(
    mode="gauge+number",
    value=total_pct * 100,
    title={'text': 'INDICADOR LME'},
    gauge={
        'axis': {'range': [0, 100]},
        'bar': {'color': "#FE6565"},
        'bgcolor': "white",
        'borderwidth': 2,
        'bordercolor': "gray",
        'steps': [
            {'range': [0, 100], 'color': "#EAF4FA"}
        ],
        'threshold': {
            'line': {'color': "black", 'width': 4},
            'thickness': 0.75,
            'value': total_pct * 100
        },
        'shape': "angular"
    }
))
st.plotly_chart(fig)

# --- Barra por comuna ---
df_com = df_filtered.groupby('comuna').agg(
    total_numerador=('Numerador', 'sum'),
    total_denominador=('Denominador', 'sum')
).reset_index()
df_com['porcentaje_cumplimiento'] = (df_com['total_numerador'] / df_com['total_denominador']) * 100
df_com = df_com.sort_values(by='porcentaje_cumplimiento', ascending=False)

st.write("## Cumplimiento por Comuna")
st.write(df_com.rename(columns={
    'porcentaje_cumplimiento': 'Porcentaje de cumplimiento',
    'total_numerador': 'Numerador',
    'total_denominador': 'Denominador',
    'comuna': 'Comuna'
}))

fig = px.bar(
    df_com, x='comuna', y='porcentaje_cumplimiento',
    title='Porcentaje de Cumplimiento por Comuna',
    labels={'comuna': 'Comuna', 'porcentaje_cumplimiento': 'Porcentaje de Cumplimiento'},
    text='porcentaje_cumplimiento'
)
fig.update_layout(xaxis_title='Comuna', yaxis_title='Porcentaje de Cumplimiento', yaxis=dict(range=[0, 100]))
st.plotly_chart(fig)
