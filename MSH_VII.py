import streamlit as st

st.title("Meta 7: Disminucion del exceso de dias de estancias asociados a egresos con estancias prolongadas (outliers superiores)")
st.caption("Fuente: GRD-ALCOR | Responsable: DIGERA - Departamento de Gestion Hospitalaria y Red de Urgencia")

st.warning("Los datos de esta meta provienen del sistema GRD-ALCOR. Requiere >= 95% de egresos con codificacion GRD.")

st.header("Descripcion del Indicador")
st.write("""
Evidencia el numero de dias de estada consumidos en exceso, sobre el punto de corte establecido,
en aquellos egresos que tuvieron una estadia superior a la establecida en la norma de estancias.

**Formula:**
- **Numerador:** Exceso de estancias outliers superiores periodo t - exceso de estancias outliers superiores periodo t-1
- **Denominador:** Exceso de estancias outliers superiores periodo t-1

**Condicion para evaluacion:** Establecimientos con >= 95% egresos hospitalarios con codificacion GRD.

**Linea Base 2026:** Se disponibilizara en carpeta compartida del Departamento cuando sea entregada por DIGERA.

**Exclusiones:**
- Pacientes con especialidad medica psiquiatria
- Judicializados CIE10 Z65.3
- Problemas relacionados con otras circunstancias legales
""")

st.header("Fuente de Datos")
st.write("""
- **Sistema:** GRD-ALCOR
- **Medio de Verificacion:** Descarga GRD-ALCOR + Planilla emitida por unidad GRD - MINSAL
""")

st.info("Para consultar los datos actualizados, contactar al Departamento de Analisis e Informacion para la Gestion - DIGERA.")
