import streamlit as st

st.title("Meta 9: Llamadas al 131 contestadas en menos de 10 segundos")
st.caption("SAMU | Fuente: Distribuidor Automatico de Llamadas (ACD) | Responsable: DIGERA")

st.warning("Los datos provienen del sistema ACD del Centro Regulador SAMU.")

st.header("Descripcion del Indicador")
st.write("""
Mide el porcentaje de llamadas al 131 contestadas en menos de 10 segundos.
Evalua la capacidad de respuesta del Centro Regulador ante emergencias.

**Formula:**
- **Numerador:** Numero de llamadas al 131 contestadas en menos de 10 segundos
- **Denominador:** Total llamadas entrantes al 131 - llamadas abandonadas antes de 3 segundos (Ghost)

**Exclusiones:**
- Llamadas abandonadas antes de 3 segundos (Ghost)
- Llamadas de prueba, administrativas o internas
- Eventos de falla tecnica documentada del ACD
""")

st.header("Fuente de Datos")
st.write("""
- **Sistema:** Distribuidor Automatico de Llamadas (ACD) del Centro Regulador SAMU
- **Medio de Verificacion:** Reporte extraido del ACD
""")

st.info("Para consultar los datos, contactar al Departamento de Gestion Hospitalaria y Red de Urgencias - DIGERA.")
