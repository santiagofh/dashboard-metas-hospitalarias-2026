import streamlit as st

st.title("Meta 14: Cobertura de personal de salud con atencion clinica directa capacitados en prevencion y control de IAAS")
st.caption("Capacitacion | Fuente: SIRH | Responsable: DIGERA - Depto. Seguridad y Calidad en la Atencion")

st.warning("Los datos provienen del modulo de capacitacion de SIRH y del Programa de Control de IAAS de cada hospital.")

st.header("Descripcion del Indicador")
st.write("""
Mide el porcentaje de integrantes del equipo de salud con atencion clinica directa que cuentan
con capacitacion en precauciones estandares aprobada durante los ultimos 5 anos.

**Formula:**
- **Numerador:** Personal de salud con atencion clinica directa con curso de prevencion y control de IAAS aprobado con antiguedad < 5 anos
- **Denominador:** Total personal de salud con atencion clinica directa (unidades definidas en "Clasificador Unidades DIGEDEP")

**Contenidos minimos:**
- Higiene de manos
- Uso de equipo de proteccion personal
- Prevencion de lesiones cortopunzantes
- Inyecciones seguras
- Limpieza y desinfeccion de superficies
- Desinfeccion de alto nivel y esterilizacion de dispositivos medicos
- Tecnica aseptica
""")

st.header("Requisitos")
st.write("""
- Duracion minima: 20 horas pedagogicas
- Modalidad: presencial, e-learning o b-learning
- Cursos certificados desde 01 enero 2022 hasta 31 diciembre 2026
- Aprobado por el Programa de Control y Prevencion de IAAS del establecimiento
""")

st.header("Exclusiones")
st.write("""
- Personal de unidades no consideradas en el "Clasificador Unidades DIGEDEP"
- Personal en calidad de honorarios, codigo del trabajo y contrato transitorio (reemplazo)
""")

st.header("Medio de Verificacion")
st.write("""
Informe elaborado por la Unidad de Capacitacion con la nomina de personal capacitado,
aprobado por la jefatura del Programa Prevencion y Control de IAAS del Hospital
y por el director(a) del Establecimiento.
""")
