import pandas as pd

from data.ohlc import ohlc_by_timeframe
from array_definitions.liquidity import Liquidity
from array_definitions.swing_hl import detect_swing_highs, detect_swing_lows


def _normalize_ohlc(df: pd.DataFrame) -> pd.DataFrame:
    if isinstance(df.columns, pd.MultiIndex):
        cols = [str(col[0]) for col in df.columns]
        df = df.copy()
        df.columns = cols
    else:
        df = df.copy()
        df.columns = [str(c) for c in df.columns]
    return df


def _get_daily_df(ohlc_dict=ohlc_by_timeframe) -> pd.DataFrame:
    df_1d = ohlc_dict["1d"].data

    if df_1d.empty:
        return pd.DataFrame()

    df = _normalize_ohlc(df_1d)

    if "High" not in df.columns or "Low" not in df.columns:
        raise KeyError(f"Expected 'High' and 'Low' columns, got {list(df.columns)}")

    if not isinstance(df.index, pd.DatetimeIndex):
        df.index = pd.to_datetime(df.index)

    return df


def get_daily_liquidity(ohlc_dict=ohlc_by_timeframe):
    df = _get_daily_df(ohlc_dict)

    if df.empty or len(df) < 4:
        return {}

    tail = df.tail(4)

    idx_ppp = tail.index[-4]
    idx_pp = tail.index[-3]
    idx_p = tail.index[-2]

    row_ppp = tail.loc[idx_ppp]
    row_pp = tail.loc[idx_pp]
    row_p = tail.loc[idx_p]

    date_ppp = idx_ppp.date()
    date_pp = idx_pp.date()
    date_p = idx_p.date()

    PDH = Liquidity("1d", "PDH", row_p["High"], date_p, "daily")
    PPDH = Liquidity("1d", "PPDH", row_pp["High"], date_pp, "daily")
    PPPDH = Liquidity("1d", "PPPDH", row_ppp["High"], date_ppp, "daily")

    PDL = Liquidity("1d", "PDL", row_p["Low"], date_p, "daily")
    PPDL = Liquidity("1d", "PPDL", row_pp["Low"], date_pp, "daily")
    PPPDL = Liquidity("1d", "PPPDL", row_ppp["Low"], date_ppp, "daily")

    return {
        "PDH": PDH,
        "PPDH": PPDH,
        "PPPDH": PPPDH,
        "PDL": PDL,
        "PPDL": PPDL,
        "PPPDL": PPPDL,
    }


def detect_daily_swing_highs(ohlc_dict=ohlc_by_timeframe):
    all_highs = detect_swing_highs(ohlc_dict)
    return all_highs.get("1d", [])


def detect_daily_swing_lows(ohlc_dict=ohlc_by_timeframe):
    all_lows = detect_swing_lows(ohlc_dict)
    return all_lows.get("1d", [])
