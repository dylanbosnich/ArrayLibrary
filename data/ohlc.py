import pandas as pd
from datetime import timedelta

from data.candle import Candle


FILE_MAP = {
    "15m": "data/raw/EURUSD_15m.csv",
    "1h": "data/raw/EURUSD_1h.csv",
    "4h": "data/raw/EURUSD_4h.csv",
    "1d": "data/raw/EURUSD_1d.csv",
    "1wk": "data/raw/EURUSD_1wk.csv",
}


class OHLC:
    def __init__(self, symbol, interval):
        self.symbol = symbol          # "EURUSD" (not used for loading, but kept for clarity)
        self.interval = interval      # "15m", "1h", "4h", "1d", "1wk"

        path = FILE_MAP[interval]

        # Read CSV saved by oanda_fetch.py
        df = pd.read_csv(path, parse_dates=["time"])
        df.set_index("time", inplace=True)

        # Keep raw data (index is in UTC, naive)
        self.data = df

        idx = df.index
        if not isinstance(idx, pd.DatetimeIndex):
            idx = pd.to_datetime(idx)
        if idx.tz is None:
            # OANDA timestamps are UTC
            idx = idx.tz_localize("UTC")

        # Convert to New York time
        idx_nyt = idx.tz_convert("America/New_York")

        candles = []
        for ts_nyt, (_, row) in zip(idx_nyt, df.iterrows()):
            o = row.get("Open")
            h = row.get("High")
            l = row.get("Low")
            c = row.get("Close")

            if pd.isna(o) or pd.isna(h) or pd.isna(l) or pd.isna(c):
                continue

            # Time handling per timeframe
            if self.interval in ["15m", "1h", "4h"]:
                # NY clock time, no tzinfo so we don't print "-05:00"
                time_value = ts_nyt.replace(tzinfo=None)
            elif self.interval == "1d":
                # Session day (17:00–17:00 NY) = date of the 00:00 candle
                time_value = (ts_nyt + timedelta(hours=7)).date()
            elif self.interval == "1wk":
                # Weekly: Monday of that session week
                shifted = ts_nyt + timedelta(hours=7)
                d = shifted.date()
                monday = d - timedelta(days=d.weekday())
                time_value = monday
            else:
                time_value = ts_nyt.replace(tzinfo=None)

            candles.append(
                Candle(self.interval, time_value, o, h, l, c)
            )

        self.candles = candles


TIMEFRAMES = ["15m", "1h", "4h", "1d", "1wk"]

ohlc_by_timeframe = {
    tf: OHLC("EURUSD", tf)
    for tf in TIMEFRAMES
}
