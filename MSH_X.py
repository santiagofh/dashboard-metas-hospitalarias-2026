import streamlit as st

st.title("Meta 10: Llamados 131 por PCR con entrega de instrucciones de Soporte Vital Basico (RCP Telefonico)")
st.caption("SAMU | Fuente: Sistema de informacion del Centro Regulador | Responsable: DIGERA")

st.warning("Los datos provienen del sistema de registro del Centro Regulador SAMU.")

st.header("Descripcion del Indicador")
st.write("""
Mide el porcentaje de llamados al 131 por Paro Cardiorrespiratorio (PCR) en los cuales
se entregan instrucciones de Soporte Vital Basico (SVB) telefonico a los testigos.

**Formula:**
- **Numerador:** Llamados telefonicos con instrucciones de SVB entregadas a testigos en caso de PCR
- **Denominador:** Total de llamados telefonicos de atencion de pacientes por PCR

**Exclusiones:**
- Signos de muerte evidente o imposibilidad de RCP guiada
- Llamadas duplicadas por la misma solicitud
- Eventos con interrupcion de comunicacion no restablecida
""")

st.header("Requisitos")
st.write("""
- Personal capacitado en protocolos de atencion del paro y RCP telefonica
- Protocolo de RCP telefonica implementado en el Centro Regulador
- Sistema de registro de entrega de instrucciones
- Supervision clinica continua de registros y grabaciones
""")
