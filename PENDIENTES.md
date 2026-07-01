# Pendientes - Dashboard Metas Hospitalarias 2026

> Nota de trabajo para retomar el proyecto. Última actualización: julio 2026.

---

## 1. Datos REM (lo más urgente)

- **`D:\DATA\REM\REM_2026\Datos\SerieP2026.csv` está vacía** (373 bytes, solo cabecera).
  - A **fin de julio 2026** debería estar disponible la Serie P 2026.
  - Al cargarla, las **metas MSH2 (CCU), MSH3 (DM2) y MSH4 (HTA)** se calculan automáticamente al re-ejecutar `Actualizar_visor_metas.bat`.
  - Establecimientos que aparecerán entonces: Hospital de Til Til, Hospital de Curacaví, Hospital Hanga Roa, CESFAM Andes (y las Direcciones si reportan).

- **`data/poblacion_adscrita_ccu.csv`** es solo un placeholder (filas con `#`).
  - Hay que completarlo con la **población adscrita mujeres/personas transmasculinos 25-64 años** por establecimiento, informada por cada Servicio de Salud.
  - Es el **denominador de MSH2 (CCU)**. Sin esto, MSH2 no tendrá denominador aunque llegue la Serie P.

- **Serie A 2026 ya tiene datos** (MSH1 y MSH5 funcionan).

---

## 2. DIRECCIONES del Servicio de Salud (decisión pendiente)

El listado oficial (`MMSS Hospitales 2026.xlsx`) incluye filas "DIRECCIÓN" (códigos administrativos `109010, 110010, 111010, 112010, 114010`) como entidades responsables de varias metas. **Estas direcciones no reportan prestaciones REM bajo su propio código** (los datos van bajo los hospitales/CESFAM reales).

- MSH1: Dirección Sur Oriente (114010) — sin datos REM.
- MSH2: 4 direcciones de 6 establecimientos.
- MSH3: 3 direcciones de 4.
- MSH4: 2 direcciones de 5.
- MSH5: 2 direcciones (Oriente 112010, Occidente 110010) de 13 — no tienen UEH.

**Decisión pendiente:** ¿dejar como está (no aparecen), agregar por Servicio de Salud, o mostrarlas como filas 0/0? Por ahora: **dejar como está**.

---

## 3. Mapeos a confirmar cuando llegue la Serie P

- **"DIRECCIÓN APS" y "SSMC"** (Meta 2 y 3, SS Central): ambos mapeados a `111010`. Confirmar si son códigos distintos cuando haya datos P.
- **Códigos REM por meta** (verificar contra diccionario MINSAL si hay dudas):
  - MSH1: A0200002 (num, Col06) / A0200001 (den, Col06) — REM A03 H61/H67.
  - MSH2: P1206010–P1206080 (num, Col01+Col02) — REM P12.
  - MSH3: P4180300+P4200200 (num) / P4150602 (den) — REM P04.
  - MSH4: P4180200+P4200100 (num) / P4150601 (den) — REM P04.
  - MSH5: 08222640 (num) / 08222640+08222650+08222660+08222680 (den) — REM A08.

---

## 4. Alcance del dashboard

- **Se calculan desde REM solo las metas 1 a 5.**
- **Metas 6 a 14** son páginas informativas (fuentes externas: SIGGES, GRD-ALCOR, ACD, SIRH, SAMU). No se calculan desde REM.
- **Sin "Meta Nacional"** numérica: la Ley 18.834 no fija un % nacional; se evalúa por brecha y línea base del establecimiento.
- **Universo de establecimientos:** definido por `data/establecimientos_metas_2026.csv` (derivado de `MMSS Hospitales 2026.xlsx`). Editar ese CSV para ajustar el listado.
- **Hospital Hanga Roa (112107):** está en región 5 pero pertenece al SS Metropolitano Oriente. El cálculo ya lo incluye correctamente porque filtra por lista de establecimientos (no por región).

---

## 5. Cómo ejecutar

```
# Refrescar datos (tras actualizar REM en D:\DATA\REM\REM_2026):
Actualizar_visor_metas.bat

# Lanzar dashboard:
streamlit run Dashboard_Metas_Hospitalarias_2026.py
```

Dependencias: `pip install -r requirements.txt` (plotly, pandas, openpyxl, xlsxwriter) + streamlit.

---

## 6. Archivos clave

| Archivo | Rol |
|---------|-----|
| `Dashboard_Metas_Hospitalarias_2026.py` | Home + navegación |
| `MSH_I.py` … `MSH_V.py` | Páginas de metas 1-5 (con datos REM) |
| `MSH_VI.py` … `MSH_XIV.py` | Páginas informativas (metas 6-14) |
| `Calculo MS-HOSP_2026.py` | Genera `MS_HOSP_2026.csv` desde REM |
| `Calculo_fecha_corte_REM.py` | Genera `Fecha_corte_REM.csv` |
| `data/establecimientos_metas_2026.csv` | Listado oficial meta→establecimiento |
| `data/establecimientos_deis_actual.xlsx` | Maestro de establecimientos DEIS |
| `data/poblacion_adscrita_ccu.csv` | Denominador MSH2 (¡a completar!) |
| `MMSS Hospitales 2026.xlsx` | Matriz oficial de establecimientos por meta |
