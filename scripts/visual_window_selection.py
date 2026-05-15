"""Utilidades comunes para seleccionar tramos visuales reproducibles.

Este módulo se usa en los notebooks de comparación puntual e intervalos para que
las figuras compartan la misma lógica de selección y, si procede, el mismo tramo
maestro.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd


def find_candidate_continuous_windows(
    timestamps_df: pd.DataFrame | pd.Series | pd.Index | None = None,
    n_hours: int | None = None,
    timestamp_col: str = "target_timestamp",
    prefer_daily_starts: bool = True,
    timestamps: pd.Series | pd.Index | None = None,
) -> list[dict[str, Any]]:
    """Encuentra todos los tramos horarios continuos de longitud ``n_hours``.

    La función acepta tanto una Serie/Índice de timestamps como un DataFrame con
    una columna temporal. Esto permite reutilizarla en los notebooks 05 y 07 sin
    cambiar sus llamadas principales.
    """
    if n_hours is None or n_hours <= 0:
        raise ValueError("n_hours debe ser un entero positivo.")

    if timestamps is None:
        if timestamps_df is None:
            raise ValueError("Debe proporcionarse timestamps o timestamps_df.")

        if isinstance(timestamps_df, pd.DataFrame):
            if timestamp_col not in timestamps_df.columns:
                raise KeyError(
                    f"No se encuentra la columna temporal '{timestamp_col}' "
                    "en timestamps_df."
                )
            timestamps = timestamps_df[timestamp_col]
        else:
            timestamps = timestamps_df

    timestamps = (
        pd.to_datetime(pd.Series(timestamps))
        .dropna()
        .drop_duplicates()
        .sort_values()
        .reset_index(drop=True)
    )

    available_timestamps = set(pd.DatetimeIndex(timestamps))
    candidate_starts = timestamps.copy()

    if prefer_daily_starts:
        daily_starts = candidate_starts.loc[candidate_starts.dt.hour == 0]
        if not daily_starts.empty:
            candidate_starts = daily_starts

    candidate_windows: list[dict[str, Any]] = []

    for candidate_start in candidate_starts:
        expected_range = pd.date_range(
            start=candidate_start,
            periods=n_hours,
            freq="h",
        )

        if all(ts in available_timestamps for ts in expected_range):
            candidate_windows.append(
                {
                    "start": candidate_start,
                    "end": expected_range[-1],
                    "target_timestamps": expected_range,
                }
            )

    return candidate_windows


def save_visual_master_window(
    path: str | Path,
    selected_window: pd.Series | dict[str, Any],
    start: pd.Timestamp,
    end: pd.Timestamp,
    n_hours: int,
    source_notebook: str,
    selection_rule: str,
    figure_horizons: list[int] | None = None,
    selection_horizons: list[int] | None = None,
    extra_metadata: dict[str, Any] | None = None,
) -> Path:
    """Guarda el tramo visual maestro en CSV para notebooks posteriores."""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)

    record: dict[str, Any] = {
        "start": pd.Timestamp(start),
        "end": pd.Timestamp(end),
        "n_hours": int(n_hours),
        "source_notebook": source_notebook,
        "selection_rule": selection_rule,
    }

    if figure_horizons is not None:
        record["figure_horizons"] = ",".join(map(str, figure_horizons))

    if selection_horizons is not None:
        record["selection_horizons"] = ",".join(map(str, selection_horizons))

    selected_series = pd.Series(selected_window)
    for col, value in selected_series.items():
        if col in record:
            continue
        if isinstance(value, (pd.Timestamp, np.datetime64)):
            record[col] = pd.Timestamp(value)
        elif isinstance(value, (np.generic,)):
            record[col] = value.item()
        else:
            record[col] = value

    if extra_metadata:
        for key, value in extra_metadata.items():
            record[key] = value

    pd.DataFrame([record]).to_csv(path, index=False)
    return path


def load_visual_master_window(path: str | Path) -> pd.Series:
    """Carga el tramo visual maestro guardado por un notebook anterior."""
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(f"No se encontró el tramo visual maestro en {path}.")

    df = pd.read_csv(path)
    if df.empty:
        raise ValueError(f"El archivo de tramo visual maestro está vacío: {path}")

    row = df.iloc[0].copy()
    row["start"] = pd.Timestamp(row["start"])
    row["end"] = pd.Timestamp(row["end"])
    return row


def match_window_by_start_end(
    candidate_windows_df: pd.DataFrame,
    start: pd.Timestamp,
    end: pd.Timestamp,
) -> pd.DataFrame:
    """Devuelve los tramos candidatos que coinciden exactamente en inicio y fin."""
    return candidate_windows_df.loc[
        (pd.to_datetime(candidate_windows_df["start"]) == pd.Timestamp(start))
        & (pd.to_datetime(candidate_windows_df["end"]) == pd.Timestamp(end))
    ].copy()
