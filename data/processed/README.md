# Datos procesados

## Serie horaria temporal base

`o3_hourly.parquet`

Este archivo se obtiene ejecutando:

`notebooks/00_data_preparation_o3.ipynb`

## Descripción

El archivo `o3_hourly.parquet` contiene la serie horaria base de O3 transformada desde el formato diario ancho `h01`-`h24` del conjunto de datos bruto.

La variable objetivo se conserva en la columna `o3`, expresada en las unidades originales del archivo fuente.

## Decisiones de depuración

- El conjunto de datos bruto no se ha modificado.
- La serie se transformó a frecuencia horaria regular.
- Se comprobó la continuidad temporal de la serie y la ausencia de duplicados.
- Los valores no convertibles a un número se registraron como `NaN`.
- Los valores negativos de O3, en caso de existir, se marcaron como `NaN`.
- Los valores ausentes de O3, a su vez, se registraron como `NaN`.
- No se eliminaron los valores extremos, ya que podrían corresponderse con episodios meteorológicos reales.
- Se decidió no imputar los huecos detectados en la serie inicialmente, a fin de no introducir sesgos en los posteriores entrenamientos de modelos.

## Salida de esta fase

El archivo `o3_hourly.parquet` se considera el dataset horario base definitivo para la EDA y la posterior ingeniería de características.

## Reproducibilidad

El archivo procesado puede regenerarse a partir de:

- `data/raw/Eixample_O3_2020_2025.csv`
- `notebooks/00_data_preparation_o3.ipynb`

Hash SHA256 del archivo bruto usado en esta ejecución:

`2C80695EB869DB2360F6C44FA81C1F2ABC9F83A217688FBAC9B498EA3059F276`
