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


def get_asia_range_highs(ohlc_dict=ohlc_by_timeframe):
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

    def session_high_liq(session_date, name):
        cs = sessions[session_date]
        if not cs:
            return None
        best = max(cs, key=lambda c: c.high)
        return Liquidity(
            timeframe="15m",
            name=name,
            price=best.high,
            time_label=best.time,
            group="intraday",
        )

    return {
        "ARH": session_high_liq(d_current, "ARH"),
        "PDARH": session_high_liq(d_prior, "PDARH"),
        "PPDARH": session_high_liq(d_prior_prior, "PPDARH"),
    }
