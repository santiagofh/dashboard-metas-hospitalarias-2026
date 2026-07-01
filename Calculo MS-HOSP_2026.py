import os
import pandas as pd

# =============================================================================
# CONFIGURACION DE DIRECTORIOS REM
# =============================================================================
directory_2026 = r"D:\DATA\REM\REM_2026"

# =============================================================================
# MAPEO OFICIAL DE ESTABLECIMIENTOS POR META
# Fuente: MMSS Hospitales 2026.xlsx (matriz oficial de establecimientos por meta)
# Solo se calculan las metas 1-5 (fuente REM). Las metas 6-14 usan sistemas
# externos y se presentan como paginas informativas en el dashboard.
# =============================================================================
mmss_path = "data/establecimientos_metas_2026.csv"
df_mmss = pd.read_csv(mmss_path, dtype={'IdEstablecimiento': str})
MMSS_ESTABLECIMIENTOS = {
    meta: set(grp['IdEstablecimiento'].astype(str))
    for meta, grp in df_mmss.groupby('MetaSanitaria')
}

# =============================================================================
# CODIGOS REM PARA METAS HOSPITALARIAS (Ley 18.834)
# =============================================================================

# Meta 1: LME al 6to mes
MSH1_NUM_CODES = ["A0200002"]
MSH1_NUM_COLS = ["Col06"]
MSH1_DEN_CODES = ["A0200001"]
MSH1_DEN_COLS = ["Col06"]

# Meta 2: CCU (PAP/VPH vigente)
# REM P12, Seccion A.1, B12-B19 (8 celdas = 8 grupos etarios 25-64).
# COL01 = Mujeres con Tamizaje vigente, COL02 = Trans Masculino con Tamizaje vigente.
# PDF dice "mujeres y personas TRANS masculinos" -> se suman ambas columnas.
# Verificado contra DICCIONARIO CODIGOS SP_25_V1.2.xlsm, hoja P12.
MSH2_NUM_CODES = [
    "P1206010", "P1206020", "P1206030", "P1206040",
    "P1206050", "P1206060", "P1206070", "P1206080"
]
MSH2_NUM_COLS = ["Col01", "Col02"]
# Denominador: Poblacion adscrita (informada por SS, no FONASA inscritos)

# Meta 3: DM2 Compensadas
# REM P04 Secc B C30+C31 (compensadas), Secc A C17 (bajo control).
# Verificado contra DICCIONARIO CODIGOS SP_25_V1.2.xlsm, hoja P4:
#   P4180300 = HbA1C<7% (15-79), P4200200 = HbA1C<8% (80+)
#   P4150602 = Diabetes Mellitus tipo 2 (bajo control)
MSH3_NUM_CODES = ["P4180300", "P4200200"]
MSH3_NUM_COLS = ["Col01"]
MSH3_DEN_CODES = ["P4150602"]
MSH3_DEN_COLS = ["Col01"]

# Meta 4: HTA Compensadas
# REM P04 Secc B C28+C29 (compensadas), Secc A C16 (bajo control).
# Verificado contra DICCIONARIO CODIGOS SP_25_V1.2.xlsm, hoja P4:
#   P4180200 = PA<140/90 (15-79), P4200100 = PA<150/90 (80+)
#   P4150601 = Hipertension Arterial (bajo control)
MSH4_NUM_CODES = ["P4180200", "P4200100"]
MSH4_NUM_COLS = ["Col01"]
MSH4_DEN_CODES = ["P4150601"]
MSH4_DEN_COLS = ["Col01"]

# Meta 5: UEH cama <12 horas
# REM A08, Seccion D. Verificado contra DICCIONARIO CODIGOS SA_25_V1.5.xlsm, hoja A08.
# Numerador (C107): 08222640 = Pacientes que ingresan a cama hospitalaria, Menos de 12 Horas
# Denominador = C107+C108+C109+C112:
#   08222640 = Menos de 12 Horas  (C107)
#   08222650 = 12 - 24 Horas       (C108)
#   08222660 = Mayor a 24 Horas    (C109)
#   08222680 = Permanecen en UEH   (C112)
# Excluidos correctamente: 08221600 (rechazan hosp), 08222670 (derivados),
#   08230500A (ingreso directo a quirofano -> tambien en exclusiones del PDF).
MSH5_NUM_CODES = ["08222640"]
MSH5_NUM_COLS = ["Col01"]
MSH5_DEN_CODES = ["08222640", "08222650", "08222660", "08222680"]
MSH5_DEN_COLS = ["Col01"]

# Todos los codigos usados
all_codes = (
    MSH1_NUM_CODES + MSH1_DEN_CODES +
    MSH2_NUM_CODES +
    MSH3_NUM_CODES + MSH3_DEN_CODES +
    MSH4_NUM_CODES + MSH4_DEN_CODES +
    MSH5_NUM_CODES + MSH5_DEN_CODES
)

# =============================================================================
# NOTA: Metas nacionales NO estan definidas en el PDF de Ley 18.834.
# El PDF hospitalario define metas por establecimiento segun brecha y
# linea base, no un % nacional fijo. Por eso el dashboard no muestra
# un "Meta Nacional" numerico.
# =============================================================================

# =============================================================================
# ALCANCE: Este script calcula solo las metas 1-5 con fuente REM.
# Las metas 6-14 usan sistemas externos (SIGGES, GRD-ALCOR, ACD, SIRH)
# y se documentan en paginas informativas del dashboard.
# =============================================================================


# =============================================================================
# FUNCIONES AUXILIARES
# =============================================================================

def leer_y_filtrar_archivos(directorio, all_codes, sep=";", chunksize=1000):
    """Lee archivos REM y filtra por codigos de prestacion."""
    datos_filtrados = []
    datos_dir = os.path.join(directorio, "Datos")

    if not os.path.isdir(datos_dir):
        print(f"Advertencia: No se encuentra la carpeta Datos en {directorio}")
        return pd.DataFrame()

    for filename in os.listdir(datos_dir):
        if filename.endswith(".csv") or filename.endswith(".txt"):
            filepath = os.path.join(datos_dir, filename)
            try:
                for chunk in pd.read_csv(filepath, sep=sep, chunksize=chunksize):
                    filtered_chunk = chunk[chunk['CodigoPrestacion'].isin(all_codes)]
                    datos_filtrados.append(filtered_chunk)
            except Exception as e:
                print(f"Error leyendo {filename}: {e}")

    if datos_filtrados:
        return pd.concat(datos_filtrados, ignore_index=True)
    else:
        return pd.DataFrame()


def sumar_columnas_por_establecimiento(df, codigos, columnas_sumar, id_establecimientos):
    """Suma columnas especificas agrupando por establecimiento, ano y mes.
    Filtra por la lista oficial de establecimientos asignados a la meta (MMSS).
    """
    cols_grup = ['IdEstablecimiento', 'Ano', 'Mes']
    df_filt = df.loc[
        (df['CodigoPrestacion'].isin(codigos)) &
        (df['IdEstablecimiento'].astype(str).isin(id_establecimientos))
    ].copy()

    for col in columnas_sumar:
        if col not in df_filt.columns:
            df_filt[col] = 0

    df_filt[columnas_sumar] = df_filt[columnas_sumar].fillna(0)

    df_grouped = df_filt.groupby(cols_grup)[columnas_sumar].sum().reset_index()
    df_grouped['suma'] = df_grouped[columnas_sumar].sum(axis=1)

    return df_grouped[cols_grup + ['suma']]


# =============================================================================
# FUNCIONES DE CALCULO POR META HOSPITALARIA
# =============================================================================

def calcular_MSH1_LME(df_rem):
    """Meta 1: Lactancia Materna Exclusiva al 6to mes.
    REM A03, Seccion A.5: Num=H61, Den=H67
    """
    estabs = MMSS_ESTABLECIMIENTOS.get('MSH1', set())
    df_num = sumar_columnas_por_establecimiento(
        df=df_rem, codigos=MSH1_NUM_CODES,
        columnas_sumar=MSH1_NUM_COLS, id_establecimientos=estabs
    )
    df_num = df_num.rename(columns={'suma': 'Numerador_MSH1'})

    df_den = sumar_columnas_por_establecimiento(
        df=df_rem, codigos=MSH1_DEN_CODES,
        columnas_sumar=MSH1_DEN_COLS, id_establecimientos=estabs
    )
    df_den = df_den.rename(columns={'suma': 'Denominador_MSH1'})

    df_merge = pd.merge(df_num, df_den,
                        on=['IdEstablecimiento', 'Ano', 'Mes'],
                        how='outer')
    return df_merge


def calcular_MSH2_CCU(df_rem):
    """Meta 2: Cobertura deteccion precoz cancer cervicouterino.
    REM P12, Seccion A1: Num=B12-B19
    Den = Poblacion adscrita mujeres 25-64 (informada por SS)
    """
    estabs = MMSS_ESTABLECIMIENTOS.get('MSH2', set())
    df_num = sumar_columnas_por_establecimiento(
        df=df_rem, codigos=MSH2_NUM_CODES,
        columnas_sumar=MSH2_NUM_COLS, id_establecimientos=estabs
    )
    df_num = df_num.rename(columns={'suma': 'Numerador_MSH2'})

    df_den_path = "data/poblacion_adscrita_ccu.csv"
    if os.path.exists(df_den_path):
        df_den = pd.read_csv(df_den_path)
        df_den['IdEstablecimiento'] = df_den['IdEstablecimiento'].astype(str)
        df_den = df_den[df_den['IdEstablecimiento'].isin(estabs)]
    else:
        print(f"Advertencia: {df_den_path} no encontrado. Creando denominador vacio.")
        df_den = pd.DataFrame(columns=['IdEstablecimiento', 'Denominador_MSH2'])

    df_merge = pd.merge(df_num, df_den, on='IdEstablecimiento', how='outer')
    return df_merge


def calcular_MSH3_DM2(df_rem):
    """Meta 3: Personas con DM2 compensadas.
    REM P04 Secc B (C30+C31): Num=compensadas, Secc A (C17): Den=bajo control
    """
    estabs = MMSS_ESTABLECIMIENTOS.get('MSH3', set())
    df_num = sumar_columnas_por_establecimiento(
        df=df_rem, codigos=MSH3_NUM_CODES,
        columnas_sumar=MSH3_NUM_COLS, id_establecimientos=estabs
    )
    df_num = df_num.rename(columns={'suma': 'Numerador_MSH3'})

    df_den = sumar_columnas_por_establecimiento(
        df=df_rem, codigos=MSH3_DEN_CODES,
        columnas_sumar=MSH3_DEN_COLS, id_establecimientos=estabs
    )
    df_den = df_den.rename(columns={'suma': 'Denominador_MSH3'})

    df_merge = pd.merge(df_num, df_den,
                        on=['IdEstablecimiento', 'Ano', 'Mes'],
                        how='outer')
    return df_merge


def calcular_MSH4_HTA(df_rem):
    """Meta 4: Personas con HTA compensadas.
    REM P04 Secc B (C28+C29): Num=compensadas, Secc A (C16): Den=bajo control
    """
    estabs = MMSS_ESTABLECIMIENTOS.get('MSH4', set())
    df_num = sumar_columnas_por_establecimiento(
        df=df_rem, codigos=MSH4_NUM_CODES,
        columnas_sumar=MSH4_NUM_COLS, id_establecimientos=estabs
    )
    df_num = df_num.rename(columns={'suma': 'Numerador_MSH4'})

    df_den = sumar_columnas_por_establecimiento(
        df=df_rem, codigos=MSH4_DEN_CODES,
        columnas_sumar=MSH4_DEN_COLS, id_establecimientos=estabs
    )
    df_den = df_den.rename(columns={'suma': 'Denominador_MSH4'})

    df_merge = pd.merge(df_num, df_den,
                        on=['IdEstablecimiento', 'Ano', 'Mes'],
                        how='outer')
    return df_merge


def calcular_MSH5_UEH(df_rem):
    """Meta 5: Pacientes UEH que acceden a cama en <12 horas.
    REM A08, Seccion D:
      Num = C107 (espera <12h)
      Den = C107+C108+C109+C112 (total indicacion hospitalizacion)
    """
    estabs = MMSS_ESTABLECIMIENTOS.get('MSH5', set())
    df_num = sumar_columnas_por_establecimiento(
        df=df_rem, codigos=MSH5_NUM_CODES,
        columnas_sumar=MSH5_NUM_COLS, id_establecimientos=estabs
    )
    df_num = df_num.rename(columns={'suma': 'Numerador_MSH5'})

    df_den = sumar_columnas_por_establecimiento(
        df=df_rem, codigos=MSH5_DEN_CODES,
        columnas_sumar=MSH5_DEN_COLS, id_establecimientos=estabs
    )
    df_den = df_den.rename(columns={'suma': 'Denominador_MSH5'})

    df_merge = pd.merge(df_num, df_den,
                        on=['IdEstablecimiento', 'Ano', 'Mes'],
                        how='outer')
    return df_merge


# =============================================================================
# EJECUCION PRINCIPAL
# =============================================================================

leer = True
if leer:
    print("Leyendo datos REM 2026...")
    df_rem_2026 = leer_y_filtrar_archivos(directory_2026, all_codes)
    print(f"  Registros 2026: {len(df_rem_2026)}")
else:
    df_rem_2026 = pd.DataFrame()
    print("Modo lectura deshabilitado.")

# --- DEIS ---
path_deis = "data/establecimientos_deis_actual.xlsx"
if os.path.exists(path_deis):
    df_deis = pd.read_excel(path_deis, sheet_name='establecimientos')
    df_deis = df_deis.rename(columns={
        'EstablecimientoCodigo': 'IdEstablecimiento',
        'DependenciaAdministrativa': 'Dependencia Administrativa',
        'NivelComplejidadEstabGlosa': 'Nivel de Atencion'
    })
else:
    print(f"Advertencia: {path_deis} no encontrado.")
    df_deis = pd.DataFrame()

# --- CALCULAR METAS ---
print("\nCalculando metas hospitalarias...")

print("  MSH1: LME...")
df_MSH1 = calcular_MSH1_LME(df_rem_2026)

print("  MSH2: CCU...")
df_MSH2 = calcular_MSH2_CCU(df_rem_2026)

print("  MSH3: DM2 Compensadas...")
df_MSH3 = calcular_MSH3_DM2(df_rem_2026)

print("  MSH4: HTA Compensadas...")
df_MSH4 = calcular_MSH4_HTA(df_rem_2026)

print("  MSH5: UEH cama <12h...")
df_MSH5 = calcular_MSH5_UEH(df_rem_2026)


# =============================================================================
# CONSOLIDAR Y EXPORTAR
# =============================================================================

def preparar_df_final(df_in, meta_name, num_col, den_col):
    """Formatea un dataframe de meta para el formato final unificado."""
    df_out = df_in.copy()
    df_out['MetaSanitaria'] = meta_name
    df_out = df_out.rename(columns={
        num_col: 'Numerador',
        den_col: 'Denominador'
    })
    for c in ['Ano', 'Mes', 'IdEstablecimiento']:
        if c not in df_out.columns:
            df_out[c] = None
    df_out = df_out[['IdEstablecimiento', 'Ano', 'Mes', 'Numerador', 'Denominador', 'MetaSanitaria']]
    return df_out


dfs_finales = []
dfs_finales.append(preparar_df_final(df_MSH1, 'MSH1', 'Numerador_MSH1', 'Denominador_MSH1'))
dfs_finales.append(preparar_df_final(df_MSH2, 'MSH2', 'Numerador_MSH2', 'Denominador_MSH2'))
dfs_finales.append(preparar_df_final(df_MSH3, 'MSH3', 'Numerador_MSH3', 'Denominador_MSH3'))
dfs_finales.append(preparar_df_final(df_MSH4, 'MSH4', 'Numerador_MSH4', 'Denominador_MSH4'))
dfs_finales.append(preparar_df_final(df_MSH5, 'MSH5', 'Numerador_MSH5', 'Denominador_MSH5'))

df_final = pd.concat(dfs_finales, ignore_index=True)

# --- Merge con DEIS ---
if not df_deis.empty:
    cols_merge = ['IdEstablecimiento']
    if 'Dependencia Administrativa' in df_deis.columns:
        cols_merge.append('Dependencia Administrativa')
    elif 'DependenciaAdm' in df_deis.columns:
        cols_merge.append('DependenciaAdm')
    if 'Nivel de Atencion' in df_deis.columns:
        cols_merge.append('Nivel de Atencion')
    elif 'NivelAtencion' in df_deis.columns:
        cols_merge.append('NivelAtencion')

    df_deis_merge = df_deis.drop_duplicates(subset=['IdEstablecimiento'])
    df_deis_merge['IdEstablecimiento'] = df_deis_merge['IdEstablecimiento'].astype(str)
    df_final['IdEstablecimiento'] = df_final['IdEstablecimiento'].astype(str)

    df_final = pd.merge(df_final, df_deis_merge[cols_merge],
                        on='IdEstablecimiento', how='left')

# =============================================================================
# NOTA: No se aplica filtro por tipo/complexion. El universo de establecimientos
# se define exclusivamente desde el listado oficial (data/establecimientos_metas_2026.csv),
# derivado de MMSS Hospitales 2026.xlsx.
# =============================================================================

# Guardar
output_path = 'MS_HOSP_2026.csv'
df_final.to_csv(output_path, index=False, encoding='utf-8')
print(f"\nArchivo guardado: '{output_path}'")
print(f"Total registros: {len(df_final)}")
print("Metas incluidas:", df_final['MetaSanitaria'].unique().tolist())
