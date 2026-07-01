import streamlit as st

st.title("Meta 12: Funcionarios/as capacitados/as en tematicas transversales relevantes")
st.caption("Capacitacion | Fuente: SIRH | Responsable: DIGEDEP - Depto. Formacion, Capacitacion y Educacion Continua")

st.warning("Los datos provienen del modulo de capacitacion de SIRH.")

st.header("Descripcion del Indicador")
st.write("""
Mide el porcentaje de la dotacion de personal de salud capacitado/a en al menos un tema transversal relevante.

**Tematicas transversales:**
- Trato usuario
- Humanizacion en la atencion
- Derechos humanos
- Integridad y prevencion en corrupcion y violencia en espacios de trabajo (probidad, transparencia)

**Formula:**
- **Numerador:** Funcionarios/as capacitados/as en tematicas transversales en el ano t (nota >= 4.0, estado "Aprobado")
- **Denominador:** Total funcionarios/as de la dotacion al 31 de marzo de 2026 (Ley 18.834: titular, contrata, suplente)

**Requisitos:**
- Duracion minima: 20 horas pedagogicas
- Modalidad: presencial, e-learning o b-learning
- Cada funcionario se contabiliza una sola vez
""")

st.header("Exclusiones")
st.write("Personal en calidad de honorarios, codigo del trabajo y contrato transitorio (reemplazo).")

st.header("Fechas Clave")
st.write("""
- **31 marzo 2026:** Corte de dotacion
- **17 abril 2026:** Fecha limite para informar dotacion y actividades programadas
- **31 diciembre 2026:** Corte de personal capacitado
""")
