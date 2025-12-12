from datetime import timedelta

from data.ohlc import ohlc_by_timeframe
from array_definitions.liquidity import Liquidity


def _build_asia_sessions(candles):
    sessions = {}
    for c in candles:
        t = c.time
        if 19 <= t.hour <= 23:
            session_date = (t + timedelta(days=1)).date()
            if session_date not in sessions:
                sessions[session_date] = []
            sessions[session_date].append(c)
    return sessions


def get_asia_range_lows(ohlc_dict=ohlc_by_timeframe):
    candles = ohlc_dict["15m"].candles
    sessions = _build_asia_sessions(candles)
    if not sessions:
        return {}

    dates = sorted(sessions.keys())
    if len(dates) < 3:
        return {}

    d_current = dates[-1]
    d_prior = dates[-2]
    d_prior_prior = dates[-3]

    def session_low_liq(session_date, name):
        cs = sessions[session_date]
        if not cs:
            return None
        best = min(cs, key=lambda c: c.low)
        return Liquidity(
            timeframe="15m",
            name=name,
            price=best.low,
            time_label=best.time,
            group="intraday",
        )

    return {
        "ARL": session_low_liq(d_current, "ARL"),
        "PDARL": session_low_liq(d_prior, "PDARL"),
        "PPDARL": session_low_liq(d_prior_prior, "PPDARL"),
    }
