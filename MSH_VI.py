import streamlit as st

st.title("Meta 6: Porcentaje de Cumplimiento de Garantias Explicitas de Salud (GES) en la Red")
st.caption("Fuente: SIGGES | Responsable: DIGERA - Departamento GES y Redes Complejas")

st.warning("Los datos de esta meta provienen directamente de la plataforma SIGGES. No se calculan desde REM.")

st.header("Descripcion del Indicador")
st.write("""
Velar por el adecuado acceso y gestion para la entrega oportuna de las Garantias Explicitas en Salud (GES).

**Formula:**
- **Numerador:** (Garantias cumplidas + garantias exceptuadas + garantias incumplidas atendidas) en el ano t
- **Denominador:** (Garantias cumplidas + garantias exceptuadas + garantias incumplidas atendidas + garantias incumplidas no atendidas) en el ano t + garantias retrasadas acumuladas

**Universo:** Garantias acumuladas de enero a diciembre. Las garantias retrasadas incluyen el acumulado total de anos anteriores.

**Exclusiones:** Establecimientos no afectos al instrumento de evaluacion de Metas Sanitarias.
""")

st.header("Fuente de Datos")
st.write("""
- **Sistema:** SIGGES (Sistema de Informacion para la Gestion de Garantias Explicitas en Salud)
- **Monitoreo:** Directo desde plataforma SIGGES con reporteria actualizada diaria
- **Medio de Verificacion:** Reporte con datos provistos por DIGERA
""")

st.info("Para consultar los datos actualizados, acceder a la plataforma SIGGES o contactar al Departamento GES y Redes Complejas - DIGERA.")
