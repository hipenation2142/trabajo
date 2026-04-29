# TFG - Predicción horaria de ozono troposférico (O3) en el distrito del Eixample de Barcelona

Este es el repositorio del Trabajo de Fin de Grado de Francisco Manuel González Pérez, supervisado por la Dra. María Moreno de Castro, sobre la predicción horaria de ozono troposférico (O3) en la estación del Eixample de Barcelona.

## Objetivo del proyecto

El objetivo principal del trabajo es predecir la concentración horaria de O3 y evaluar hasta qué horizonte temporal las predicciones siguen siendo útiles.

El proyecto no se limita a comparar el error puntual de los modelos; también evalúa la calidad de sus intervalos de predicción y la explicabilidad de sus resultados.

## Planteamiento general

La comparación principal entre modelos se realizará en los siguientes horizontes de predicción:

- 1 hora
- 4 horas
- 12 horas
- 24 horas

Tras seleccionarse un modelo ganador, se ampliará el análisis al rango completo de horizontes entre 1 y 24 horas.

La partición cronológica prevista, pues, será:

- Entrenamiento: 2020-2022
- Calibración: 2023
- Validación/selección: 2024
- Prueba: 2025

## Modelos candidatos

Se considerarán cuatro familias principales:

1. Modelo base ingenuo estacional (seasonal naive).
2. Regresión cuantílica.
3. LightGBM cuantílico.
4. CatBoost cuantílico.

## Intervalos de predicción

La metodología principal de cuantificación de la incertidumbre será:

- Seasonal Naive + Split Conformal.
- Regresión cuantílica + CQR.
- LightGBM cuantílico + CQR.
- CatBoost cuantílico + CQR.

## Métricas

Se calcularán métricas puntuales y métricas de intervalos.

Métricas puntuales:

- MAE.
- RMSE.

Métricas de intervalos:

- Cobertura empírica.
- Anchura media.
- Interval score.

## Explicabilidad

La explicabilidad formará parte del criterio de selección del modelo ganador, mediante la explicación de las siguientes técnicas:

- Seasonal Naive: la explicación se efectuará mediante la regla de persistencia estacional.
- Regresión cuantílica: se interpretarán sus coeficientes.
- LightGBM: se aplicará la técnica SHAP.
- CatBoost: se aplicará la técnica SHAP.

## Estructura del repositorio

```text
data/
  raw/              Datos brutos locales.
  processed/        Datos procesados locales.

models/
  catboost/         Datos de CatBoost
  cqr/              Datos sobre la aplicación de la técnica CQR
  cqr_mapie/        Datos sobre la aplicación de la técnica CQR mediante MAPIE
  enbpi/            Datos sobre la aplicación de EnbPI
  lightgbm/         Datos de LightGBM
  linear_regression/Datos de la regresión lineal

notebooks/          Notebooks de análisis exploratorio y desarrollo de prototipos.

reports/
  figures/          Figuras generadas para la memoria.
  intervals/        Datos de los intervalos calculados.
  predictions/      Datos de las predicciones puntuales efectuadas.
  tables/           Tablas generadas por los notebooks.

scripts/            Scripts ejecutables del pipeline.