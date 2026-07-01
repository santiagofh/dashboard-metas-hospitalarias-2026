import streamlit as st

st.title("Meta 8: Ejecucion del Plan Anual de Mantenimiento Preventivo")
st.caption("Responsable: Division de Inversiones - Subsecretaria de Redes Asistenciales")

st.warning("Los datos de esta meta provienen de registros locales de cada establecimiento.")

st.header("Descripcion del Indicador")
st.write("""
Ejecutar el plan de mantenimiento de equipos medicos, ambulancias, equipos industriales e infraestructura
para conservar y asegurar el correcto funcionamiento y la continuidad asistencial.

**Componentes (5 trazadoras, 20% cada una):**
1. Mantencion de equipos medicos (ejecutadas / programadas)
2. Mantencion de equipos industriales (ejecutadas / programadas)
3. Mantencion de ambulancias (ejecutadas / programadas)
4. Mantencion de infraestructura (ejecutadas / programadas)
5. Ejecucion presupuestaria en SIGFE (gasto ejecutado / presupuesto asignado)

**Nota:** Si un establecimiento no cuenta con ambulancias, se evaluan solo 4 trazadoras (25% c/u).

**Actualizaciones:** El plan puede modificarse hasta el ultimo dia habil de octubre.
""")

st.header("Exclusiones")
st.write("""
Equipos que durante la ejecucion del plan de mantenimiento:
- Sean dados de baja
- Se encuentren en reparacion por un periodo de tiempo prolongado
- No se pueda ejecutar por causa tecnica (retraso en gestiones administrativas:
  licitacion, trato directo, emision de orden de compra, contratos, etc.)
- No se cuente con disponibilidad presupuestaria
""")

st.header("Fuente de Datos")
st.write("""
- **Registros:** Locales de cada establecimiento
- **Medio de Verificacion:** Plan de mantenimiento 2026, planillas de mantenimiento, resolucion que aprueba el presupuesto
- **Norma:** Decreto N 290/2017
""")

st.info("Para consultar los datos, contactar a la Division de Inversiones - SRA.")
