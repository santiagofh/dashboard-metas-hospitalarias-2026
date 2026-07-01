import streamlit as st

st.title("Meta 11: Disponibilidad Operativa de Call Takers SAMU")
st.caption("SAMU | Fuente: Distribuidor Automatico de Llamadas (ACD) | Responsable: DIGERA")

st.warning("Los datos provienen del sistema ACD del Centro Regulador SAMU.")

st.header("Descripcion del Indicador")
st.write("""
Mide el porcentaje de tiempo dentro del turno en que los call takers del Centro Regulador SAMU
estan efectivamente conectados y disponibles para recibir llamadas de emergencia.

**Formula:**
- **Numerador:** Minutos totales del turno - minutos en pausa, modo auxiliar o desconectado
- **Denominador:** Minutos totales del turno

**Exclusiones:**
- Periodos de caida de linea 131
""")

st.header("Consideraciones")
st.write("""
- Planificacion y cobertura de turnos adecuada
- Supervision de tiempos de conexion efectiva
- Uso correcto de estados de conexion (disponible, pausa, auxiliar)
- Protocolos de descanso con registros auditables
""")
