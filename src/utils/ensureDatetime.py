import pandas as pd
import numpy as np

def ensure_datetime(
    df: pd.DataFrame,
    time_col: str | None = "data",       # se None, tenta detectar: coluna "data" > índice
    out_col: str = "data",               # coluna de saída padronizada
    set_index: bool = True,              # True: define DatetimeIndex
    tz: str | None = None                # ex.: "America/Sao_Paulo"
) -> pd.DataFrame:
    """
    Robustifica parsing de datetime a partir de uma coluna ou do índice.
    - Testa formatos comuns e escolhe o com maior taxa de acerto.
    - Tenta ISO8601, dayfirst, epoch (s/ms) e, por fim, dateutil.
    - Padroniza saída em string '%Y-%m-%d %H:%M:%S' (e opcionalmente DatetimeIndex).
    """

    df = df.copy()

    # 1) Escolher a fonte do tempo
    if time_col is None:
        if "data" in df.columns:
            s = df["data"]
        elif not isinstance(df.index, pd.RangeIndex):
            # usa o índice se não for RangeIndex
            s = pd.Series(df.index, index=df.index, name="data")
        else:
            # último recurso: primeira coluna
            s = df.iloc[:, 0]
            s.name = out_col
    else:
        if time_col in df.columns:
            s = df[time_col]
        elif time_col == "index":
            s = pd.Series(df.index, index=df.index, name=out_col)
        else:
            raise KeyError(f"Fonte de tempo '{time_col}' não encontrada (coluna ou índice).")

    # 2) Se já for datetime, só normaliza TZ/saída
    if pd.api.types.is_datetime64_any_dtype(s):
        dt = s
    else:
        # Se numérico: pode ser epoch
        if pd.api.types.is_numeric_dtype(s):
            v = pd.to_numeric(s, errors="coerce")
            med = np.nanmedian(v)
            # heurística simples: ms ~ 1e12, s ~ 1e9
            unit = "ms" if med > 1e11 else "s"
            dt = pd.to_datetime(v, unit=unit, utc=True, errors="coerce")
        else:
            # 3) Tenta formatos explícitos (rápidos)
            candidates = [
                "%Y-%m-%d %H:%M:%S",
                "%Y-%m-%d %H:%M",
                "%Y/%m/%d %H:%M:%S",
                "%d/%m/%Y %H:%M:%S",
                "%d/%m/%Y %H:%M",
                "%m/%d/%Y %H:%M:%S",
                "%Y-%m-%dT%H:%M:%S",
                "%Y-%m-%d",            # só data
                "%d/%m/%Y",            # só data BR
            ]
            best_dt = None
            best_rate = -1.0

            for fmt in candidates:
                tmp = pd.to_datetime(s, format=fmt, errors="coerce")
                rate = tmp.notna().mean()
                if rate > best_rate:
                    best_rate = rate
                    best_dt = tmp
                    if rate >= 0.98:  # bom o suficiente, já aceita
                        break

            dt = best_dt

            # 4) Fallbacks: ISO+dateutil, dayfirst, e por fim parse “livre”
            if dt is None or dt.notna().mean() < 0.7:
                # ISO/geral
                tmp = pd.to_datetime(s, errors="coerce", utc=True)
                if tmp.notna().mean() > dt.notna().mean():
                    dt = tmp

            if dt.notna().mean() < 0.7:
                # tenta BR dayfirst
                tmp = pd.to_datetime(s, errors="coerce", dayfirst=True, utc=True)
                if tmp.notna().mean() > dt.notna().mean():
                    dt = tmp

            if dt.notna().mean() < 0.7:
                # último recurso: sem UTC (dateutil puro)
                tmp = pd.to_datetime(s, errors="coerce")
                if tmp.notna().mean() > dt.notna().mean():
                    dt = tmp

    # 5) Timezone handling
    if tz:
        if dt.dt.tz is None:
            # se for naive, localiza
            dt = dt.dt.tz_localize(tz, nonexistent="shift_forward", ambiguous="NaT")
        else:
            # se tiver TZ (ex.: UTC), converte
            dt = dt.dt.tz_convert(tz)

    # 6) Saída: coluna formatada e (opcional) índice
    df[out_col] = dt.dt.strftime("%Y-%m-%d %H:%M:%S")
    if set_index:
        df = df.set_index(pd.DatetimeIndex(dt, name=out_col))

    return df
