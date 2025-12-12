from datetime import timedelta

from data.ohlc import ohlc_by_timeframe
from array_definitions.liquidity import Liquidity
from array_definitions.swing_hl import detect_swing_highs, detect_swing_lows


def get_weekly_liquidity(ohlc_dict=ohlc_by_timeframe):
    ohlc = ohlc_dict["1wk"]
    candles = getattr(ohlc, "candles", [])

    if len(candles) < 4:
        return {}

    tail = candles[-4:]

    c_ppp = tail[0]
    c_pp = tail[1]
    c_p = tail[2]

    def next_monday_label(candle):
        t = candle.time
        return t + timedelta(days=7)

    PWH = Liquidity("1wk", "PWH", c_p.high, next_monday_label(c_p), "weekly")
    PPWH = Liquidity("1wk", "PPWH", c_pp.high, next_monday_label(c_pp), "weekly")
    PPPWH = Liquidity("1wk", "PPPWH", c_ppp.high, next_monday_label(c_ppp), "weekly")

    PWL = Liquidity("1wk", "PWL", c_p.low, next_monday_label(c_p), "weekly")
    PPWL = Liquidity("1wk", "PPWL", c_pp.low, next_monday_label(c_pp), "weekly")
    PPPWL = Liquidity("1wk", "PPPWL", c_ppp.low, next_monday_label(c_ppp), "weekly")

    return {
        "PWH": PWH,
        "PPWH": PPWH,
        "PPPWH": PPPWH,
        "PWL": PWL,
        "PPWL": PPWL,
        "PPPWL": PPPWL,
    }


def detect_weekly_swing_highs(ohlc_dict=ohlc_by_timeframe):
    all_highs = detect_swing_highs(ohlc_dict)
    return all_highs.get("1wk", [])


def detect_weekly_swing_lows(ohlc_dict=ohlc_by_timeframe):
    all_lows = detect_swing_lows(ohlc_dict)
    return all_lows.get("1wk", [])
