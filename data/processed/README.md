# Datos procesados

Esta carpeta contiene archivos generados a partir del dataset bruto de O3.

## Archivo principal generado localmente

`o3_hourly.parquet`

Este archivo se obtiene ejecutando:

`notebooks/00_data_preparation_o3.ipynb`

## Descripción

El archivo `o3_hourly.parquet` contiene la serie horaria de O3 transformada desde el formato diario ancho `h01`-`h24` del CSV bruto.

La variable objetivo se conserva en la columna `o3`, expresada en las unidades originales del archivo fuente.

## Decisiones de depuración

- El CSV bruto no se modifica.
- La serie se transforma a frecuencia horaria regular.
- Se comprueba continuidad temporal y duplicados.
- Los valores no convertibles a número se consideran ausentes.
- Los valores negativos de O3, si aparecieran, se marcarían como ausentes.
- No se eliminan valores altos automáticamente, ya que pueden corresponder a episodios reales.
- No se imputa la variable objetivo para construir el dataset procesado.

## Reproducibilidad

El archivo procesado no se versiona porque puede regenerarse a partir de:

- `data/raw/Eixample_O3_2020_2025.csv`
- `notebooks/00_data_preparation_o3.ipynb`

Hash SHA256 del archivo bruto usado en esta ejecución:

`2C80695EB869DB2360F6C44FA81C1F2ABC9F83A217688FBAC9B498EA3059F276`
