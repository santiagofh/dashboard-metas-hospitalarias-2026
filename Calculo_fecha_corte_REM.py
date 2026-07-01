import os
import pandas as pd
from datetime import datetime

base_dir = r"D:\DATA\REM\REM_2026\Datos"

series = {
    "REM A": "SerieA2026.csv",
    "REM BM": "SerieBM2026.csv",
    "REM BS": "SerieBS2026.csv",
    "REM P": "SerieP2026.csv",
}


def obtener_fecha_corte(ruta_archivo):
    if os.path.exists(ruta_archivo):
        timestamp = os.path.getmtime(ruta_archivo)
        fecha = datetime.fromtimestamp(timestamp)
        return fecha.strftime("%Y-%m-%d")
    return "No disponible"


fechas = []
for nombre, archivo in series.items():
    fechas.append(obtener_fecha_corte(os.path.join(base_dir, archivo)))

df_corte = pd.DataFrame({
    "REM": list(series.keys()),
    "Fecha_corte": fechas
})

df_corte.to_csv('Fecha_corte_REM.csv', index=False)
print("Fecha_corte_REM.csv generado.")
