from data.ohlc import ohlc_by_timeframe
from array_definitions.liquidity import Liquidity


def _detect_swing_highs_in_candles(timeframe, candles):
    swings = []
    for i in range(1, len(candles) - 1):
        c1 = candles[i - 1]
        c2 = candles[i]
        c3 = candles[i + 1]

        if c2.high > c1.high and c2.high > c3.high:
            swings.append(
                Liquidity(
                    timeframe=timeframe,
                    name="SH",
                    price=c2.high,
                    time_label=c2.time,
                    group="swing_high",
                )
            )
    return swings


def _detect_swing_lows_in_candles(timeframe, candles):
    swings = []
    for i in range(1, len(candles) - 1):
        c1 = candles[i - 1]
        c2 = candles[i]
        c3 = candles[i + 1]

        if c2.low < c1.low and c2.low < c3.low:
            swings.append(
                Liquidity(
                    timeframe=timeframe,
                    name="SL",
                    price=c2.low,
                    time_label=c2.time,
                    group="swing_low",
                )
            )
    return swings


def detect_swing_highs(ohlc_dict=ohlc_by_timeframe):
    swing_highs_by_tf = {}
    for timeframe, ohlc in ohlc_dict.items():
        candles = getattr(ohlc, "candles", [])
        swing_highs_by_tf[timeframe] = _detect_swing_highs_in_candles(
            timeframe, candles
        )
    return swing_highs_by_tf


def detect_swing_lows(ohlc_dict=ohlc_by_timeframe):
    swing_lows_by_tf = {}
    for timeframe, ohlc in ohlc_dict.items():
        candles = getattr(ohlc, "candles", [])
        swing_lows_by_tf[timeframe] = _detect_swing_lows_in_candles(
            timeframe, candles
        )
    return swing_lows_by_tf
