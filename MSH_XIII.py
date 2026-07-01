import streamlit as st

st.title("Meta 13: Funcionarios/as con capacitacion actualizada en Reanimacion Cardiopulmonar (RCP)")
st.caption("Capacitacion | Fuente: SIRH | Responsable: DIGEDEP")

st.warning("Los datos provienen del modulo de capacitacion de SIRH.")

st.header("Descripcion del Indicador")
st.write("""
Mide la cobertura de funcionarios/as capacitados/as en reanimacion cardiopulmonar (RCP).

**Formula:**
- **Numerador:** Funcionarios/as con capacitacion actualizada en RCP (aprobada, antiguedad <= 5 anos: 2022-2026)
- **Denominador:** Total funcionarios/as de la dotacion al 31 de marzo de 2026 (Ley 18.834: titular, contrata, suplente)

**Requisitos:**
- Actividades especificas de RCP o con modulo de RCP
- Modalidad presencial o b-learning (con modulo presencial obligatorio)
- Cada funcionario se contabiliza una sola vez
""")

st.header("Exclusiones")
st.write("Personal en calidad de honorarios, codigo del trabajo y contrato transitorio (reemplazo).")

st.header("Fechas Clave")
st.write("""
- **31 marzo 2026:** Corte de dotacion
- **17 abril 2026:** Fecha limite para informar dotacion
- **31 diciembre 2026:** Corte de personal capacitado (incluye capacitaciones desde 1 enero 2022)
""")
