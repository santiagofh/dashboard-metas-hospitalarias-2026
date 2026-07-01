@echo off
echo Ejecutando actualizacion de visor de metas hospitalarias...
cd /d "C:\Users\fariass\OneDrive - SUBSECRETARIA DE SALUD PUBLICA\Escritorio\Salud Publica\MS_HOSP_2026"
python "Calculo MS-HOSP_2026.py"
python "Calculo_fecha_corte_REM.py"
echo Proceso completado.
pause
