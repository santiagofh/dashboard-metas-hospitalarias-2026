from pathlib import Path
import streamlit as st
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent

st.set_page_config(
    page_title="Dashboard Metas Hospitalarias 2026",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(
    """
    <style>
    :root {
        --gob-red: #FE6565;
        --gob-blue: #006FB3;
        --gob-blue-soft: #EAF4FA;
    }

    .stApp h1, .stApp h2, .stApp h3 {
        color: var(--gob-blue);
        font-weight: 700;
    }

    .stApp [data-testid="stMetric"] {
        background: linear-gradient(180deg, #ffffff 0%, var(--gob-blue-soft) 100%);
        border: 1px solid #cfe6f4;
        border-radius: 12px;
        padding: 0.5rem 0.75rem;
    }

    .stApp button[kind="primary"] {
        background-color: var(--gob-red);
        border-color: var(--gob-red);
    }

    .stApp button[kind="secondary"] {
        border-color: var(--gob-blue);
        color: var(--gob-blue);
    }

    section[data-testid="stSidebar"] {
        border-right: 1px solid #cfe6f4;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.logo(
    str(BASE_DIR / "assets" / "seremi_sidebar_logo.svg"),
    size="large",
    icon_image=str(BASE_DIR / "assets" / "seremi_sidebar_icon.svg"),
)


def home():
    st.warning("Datos Provisorios")

    st.title("Bienvenidos al Dashboard de Metas Hospitalarias 2026")
    st.subheader("Ley 18.834 - Estatuto Administrativo")

    st.write("""
    Este dashboard esta disenado para el seguimiento y control de las **14 metas sanitarias
    hospitalarias** (Ley 18.834) definidas por el Ministerio de Salud para el ano 2026.

    **Grupos de metas:**
    - **Metas 1-8:** Establecimientos de Alta, Mediana y Baja Complejidad
    - **Metas 9-11:** Servicio de Atencion Medica de Urgencia (SAMU)
    - **Metas 12-14:** Capacitacion del personal de salud
    """)

    st.info("""
    **Alcance del calculo automatico:** Solo las **metas 1 a 5** se calculan desde REM.
    Las **metas 6 a 14** usan sistemas externos (SIGGES, GRD-ALCOR, ACD, SIRH)
    y se presentan como paginas informativas con la definicion del indicador.
    """)

    st.write("## Datos para las Metas Hospitalarias")

    st.write("Fecha de corte de datos REM:")
    try:
        fecha_corte = pd.read_csv("Fecha_corte_REM.csv")
        st.write(fecha_corte[['REM', 'Fecha_corte']].rename(columns={'Fecha_corte': 'Fecha Corte'}))
    except FileNotFoundError:
        st.warning("Archivo Fecha_corte_REM.csv no encontrado.")


pages = {
    "Menu principal": [
        st.Page(home, default=True, title="Pagina de inicio", icon=":material/home:")
    ],
    "Metas Establecimientos (1-8)": [
        st.Page("MSH_I.py", title="Meta 1: Lactancia Materna Exclusiva al 6to mes", icon=":material/local_hospital:"),
        st.Page("MSH_II.py", title="Meta 2: Deteccion precoz Cancer Cervicouterino", icon=":material/local_hospital:"),
        st.Page("MSH_III.py", title="Meta 3: Personas con DM2 Compensadas", icon=":material/local_hospital:"),
        st.Page("MSH_IV.py", title="Meta 4: Personas con HTA Compensadas", icon=":material/local_hospital:"),
        st.Page("MSH_V.py", title="Meta 5: UEH - Pacientes con indicacion de hospitalizacion que acceden a cama < 12 horas", icon=":material/local_hospital:"),
        st.Page("MSH_VI.py", title="Meta 6: Cumplimiento GES en la Red", icon=":material/local_hospital:"),
        st.Page("MSH_VII.py", title="Meta 7: Disminucion exceso dias estancia (outliers)", icon=":material/local_hospital:"),
        st.Page("MSH_VIII.py", title="Meta 8: Ejecucion del Plan Anual de Mantenimiento Preventivo", icon=":material/local_hospital:"),
    ],
    "Metas SAMU (9-11)": [
        st.Page("MSH_IX.py", title="Meta 9: Llamadas 131 contestadas < 10 seg", icon=":material/phone_in_talk:"),
        st.Page("MSH_X.py", title="Meta 10: RCP telefonico en PCR", icon=":material/phone_in_talk:"),
        st.Page("MSH_XI.py", title="Meta 11: Disponibilidad Call Takers SAMU", icon=":material/phone_in_talk:"),
    ],
    "Metas Capacitacion (12-14)": [
        st.Page("MSH_XII.py", title="Meta 12: Capacitacion en tematicas transversales", icon=":material/school:"),
        st.Page("MSH_XIII.py", title="Meta 13: Capacitacion actualizada en RCP", icon=":material/school:"),
        st.Page("MSH_XIV.py", title="Meta 14: Prevencion y control de IAAS", icon=":material/school:"),
    ],
}

pg = st.navigation(pages)
pg.run()
